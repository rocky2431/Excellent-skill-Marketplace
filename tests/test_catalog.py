"""Offline regressions for native catalog and package contracts."""

import io
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import catalog


class CatalogTests(unittest.TestCase):
    def test_build_metadata_versions(self):
        plugin = catalog.load_sources()["plugins"][0]
        for version in ("0.1.0+codex.20260906011727", "0.1.0-rc.1+build.2"):
            with self.subTest(version=version):
                catalog.validate_sources({"plugins": [{**plugin, "version": version}]})
        for version in ("0.1.0+", "0.1.0+build..1", "0.1.0+build/1"):
            with self.subTest(version=version), self.assertRaises(ValueError):
                catalog.validate_sources({"plugins": [{**plugin, "version": version}]})

    def test_published_task_state_package_executes_its_kimi_recovery_hook(self):
        plugin = next(p for p in catalog.load_sources()["plugins"] if p["name"] == "task-state-with-files")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "plugin"
            with zipfile.ZipFile(catalog.ROOT / catalog.package_path(plugin)) as archive:
                manifest = json.loads(archive.read("kimi.plugin.json"))
                self.assertIn("UserPromptSubmit", [h["event"] for h in manifest.get("hooks", [])])
                archive.extractall(package)
            workspace = root / "project"
            (workspace / "work").mkdir(parents=True)
            (workspace / "work/task-state.md").write_text("## Next action\nPACKAGED-RECOVERY-MARKER\n")
            hook = next(h for h in manifest["hooks"] if h["event"] == "UserPromptSubmit")
            result = subprocess.run(hook["command"], shell=True, cwd=package,
                                    input=json.dumps({"hook_event_name": "UserPromptSubmit", "cwd": str(workspace)}),
                                    env={**{k: v for k, v in os.environ.items() if not k.startswith("TASK_STATE_")},
                                         "TASK_STATE_FILE": "work/task-state.md"},
                                    capture_output=True, text=True, timeout=10)
            self.assertEqual(0, result.returncode, result.stderr)
            self.assertIn("PACKAGED-RECOVERY-MARKER", result.stdout)

    def test_shipped_task_selection_is_scoped_and_hooks_are_read_only(self):
        plugin = next(p for p in catalog.load_sources()["plugins"] if p["name"] == "task-state-with-files")
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            package = root / "plugin"
            with zipfile.ZipFile(catalog.ROOT / catalog.package_path(plugin)) as archive:
                archive.extractall(package)
            scripts = package / "skills/task-state-with-files/scripts"
            workspace = root / "project"
            (workspace / ".tasks").mkdir(parents=True)
            (workspace / ".tasks/selected.md").write_text("Keep refund signs. Next: verify the output.\n")
            env = {k: v for k, v in os.environ.items() if not k.startswith("TASK_STATE_")}
            env["PLUGIN_ROOT"] = str(package)

            def hook(host, session):
                command = ([str(package / "hooks/session_start.py")] if host == "codex" else
                           [str(scripts / "lifecycle_hook.py"), "--host", host])
                event = {"cwd": str(workspace), "session_id": session, "source": "resume",
                         "hook_event_name": "UserPromptSubmit" if host == "kimi" else "SessionStart"}
                result = subprocess.run([sys.executable, *command], input=json.dumps(event),
                                        env=env, text=True, capture_output=True, timeout=10)
                self.assertEqual((0, ""), (result.returncode, result.stderr))
                return result.stdout

            for host in ("codex", "claude", "zcode", "kimi"):
                self.assertEqual("", hook(host, "owner"), host)
            selected = subprocess.run([sys.executable, str(scripts / "task_state.py"),
                                       "activate", "--task", "selected", "--session", "owner",
                                       "--root", str(workspace)], env=env, text=True, capture_output=True)
            self.assertEqual(0, selected.returncode, selected.stderr)
            before = {str(p): p.read_bytes() for p in workspace.rglob("*") if p.is_file()}
            for host in ("codex", "claude", "zcode", "kimi"):
                self.assertIn("Keep refund signs", hook(host, "owner"), host)
                self.assertEqual("", hook(host, "unrelated"), host)
            self.assertEqual(before, {str(p): p.read_bytes() for p in workspace.rglob("*") if p.is_file()})

    def test_native_catalog_and_package_contracts(self):
        source = catalog.load_sources()
        rendered = catalog.catalogs(source)
        kimi = rendered[catalog.ROOT / "marketplaces/kimi.json"]["plugins"]
        # Kimi 0.41.0 rejects "third-party" and returns an unusable catalog.
        self.assertTrue(all(p["tier"] in {"official", "curated"} for p in kimi))
        for host, variable in [("claude", "CLAUDE_PLUGIN_ROOT"), ("zcode", "ZCODE_PLUGIN_ROOT")]:
            entries = rendered[catalog.ROOT / f".{host}-plugin/marketplace.json"]["plugins"]
            self.assertEqual(
                {p["name"]: p["version"] for p in source["plugins"]},
                {p["name"]: p.get("version") for p in entries},
                host,
            )
            thinking = next(p for p in entries if p["name"] == "deep-thinking")
            self.assertEqual("git-subdir", thinking["source"]["source"])
            self.assertEqual("plugins/deep-thinking", thinking["source"]["path"])
            self.assertNotIn("strict", thinking)
            self.assertNotIn("skills", thinking)
            task = next(p for p in entries if p["name"] == "task-state-with-files")
            self.assertFalse(task["strict"])
            command = task["hooks"]["SessionStart"][0]["hooks"][0]["command"]
            self.assertIn(variable, command)
            self.assertIn(f"--host {host}", command)
        harness = next(p for p in rendered[catalog.ROOT / ".zcode-plugin/marketplace.json"]["plugins"]
                       if p["name"] == "agent-harness-design")
        self.assertEqual(harness["source"]["type"], "zip")
        self.assertRegex(harness["source"]["sha256"], r"^[0-9a-f]{64}$")
        plugin = source["plugins"][0]
        native = {"name": plugin["name"], "version": plugin["version"],
                  "skills": ["./skills"], "hooks": [{"event": "Stop", "command": "python3 check.py"}]}
        files = {f"{plugin['path']}/kimi.plugin.json": json.dumps(native).encode(),
                 f"{plugin['path']}/skills/example/SKILL.md": b"example", "LICENSE": b"upstream license"}
        body = catalog.build_kimi(plugin, files)
        self.assertEqual(body, catalog.build_kimi(plugin, dict(reversed(list(files.items())))))
        with zipfile.ZipFile(io.BytesIO(body)) as archive:
            self.assertEqual(json.loads(archive.read("kimi.plugin.json")), native)
            self.assertEqual(archive.read("LICENSE"), b"upstream license")
            self.assertEqual(archive.read("skills/example/SKILL.md"), b"example")
            self.assertEqual(json.loads(archive.read("marketplace-origin.json"))["sha"], plugin["sha"])
        with self.assertRaises(ValueError):
            catalog.validate_sources({"plugins": [{**plugin, "sha": "main"}]})
        with self.assertRaises(ValueError):
            catalog.validate_sources({"plugins": [{**plugin, "path": "../outside"}]})


if __name__ == "__main__":
    unittest.main()
