"""Offline regressions for native catalog and package contracts."""

import io
import json
from pathlib import Path
import sys
import unittest
import zipfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import catalog


class CatalogTests(unittest.TestCase):
    def test_native_catalog_and_package_contracts(self):
        source = catalog.load_sources()
        rendered = catalog.catalogs(source)
        kimi = rendered[catalog.ROOT / "marketplaces/kimi.json"]["plugins"]
        # Kimi 0.41.0 rejects "third-party" and returns an unusable catalog.
        self.assertTrue(all(p["tier"] in {"official", "curated"} for p in kimi))
        for host, variable in [("claude", "CLAUDE_PLUGIN_ROOT"), ("zcode", "ZCODE_PLUGIN_ROOT")]:
            entries = rendered[catalog.ROOT / f".{host}-plugin/marketplace.json"]["plugins"]
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
