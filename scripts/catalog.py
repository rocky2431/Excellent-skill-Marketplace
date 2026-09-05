#!/usr/bin/env python3
"""Build host catalogs from independently versioned upstream repositories."""

from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def json_text(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


def load_sources() -> dict:
    source = json.loads((ROOT / "sources.json").read_text(encoding="utf-8"))
    validate_sources(source)
    return source


def validate_sources(source: dict) -> None:
    names = set()
    for plugin in source["plugins"]:
        name = plugin["name"]
        if not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", name) or name in names:
            raise ValueError(f"Invalid or duplicate plugin name: {name}")
        names.add(name)
        if not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", plugin["repository"]):
            raise ValueError(f"Invalid GitHub repository: {name}")
        if not re.fullmatch(r"[0-9a-f]{40}", plugin["sha"]):
            raise ValueError(f"A full commit SHA is required: {name}")
        if not re.fullmatch(r"\d+\.\d+\.\d+(?:-[A-Za-z0-9.-]+)?", plugin["version"]):
            raise ValueError(f"Invalid version: {name}")
        path = PurePosixPath(plugin["path"])
        if path.is_absolute() or ".." in path.parts or "\\" in plugin["path"] or str(path) in ("", "."):
            raise ValueError(f"Invalid plugin subdirectory: {name}")


def upstream_files(plugin: dict) -> dict[str, bytes]:
    url = f"https://codeload.github.com/{plugin['repository']}/zip/{plugin['sha']}"
    with urllib.request.urlopen(url, timeout=60) as response:
        content = response.read()
    files = {}
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        for entry in archive.infolist():
            if entry.is_dir():
                continue
            path = PurePosixPath(entry.filename)
            if path.is_absolute() or ".." in path.parts or "\\" in entry.filename or len(path.parts) < 2:
                raise ValueError(f"Unsafe upstream archive path: {entry.filename}")
            if (entry.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError(f"Upstream symlinks require review: {entry.filename}")
            relative = str(PurePosixPath(*path.parts[1:]))
            if relative in files:
                raise ValueError(f"Duplicate upstream path: {relative}")
            files[relative] = archive.read(entry)
    manifest = json.loads(files[f"{plugin['path']}/.codex-plugin/plugin.json"])
    if manifest["name"] != plugin["name"] or manifest["version"] != plugin["version"]:
        raise ValueError(f"Pinned source name/version does not match: {plugin['name']}")
    return files


def package_path(plugin: dict) -> str:
    return f"packages/kimi/{plugin['name']}-{plugin['version']}-{plugin['sha'][:12]}.zip"


def origin(plugin: dict) -> dict:
    return {key: plugin[key] for key in ("name", "repository", "path", "sha", "version")}


def build_kimi(plugin: dict, files: dict[str, bytes]) -> bytes:
    # The delegation installer also needs its repository-level runtime lockfiles.
    prefix = "" if plugin["name"] == "agent-delegation" else plugin["path"] + "/"
    payload = {path[len(prefix):]: body for path, body in files.items() if path.startswith(prefix)}
    if "LICENSE" in files and "LICENSE" not in payload:
        payload["LICENSE"] = files["LICENSE"]
    if "kimi.plugin.json" not in payload:
        skills = f"./{plugin['path']}/skills" if not prefix else "./skills"
        payload["kimi.plugin.json"] = json_text({
            "name": plugin["name"],
            "version": plugin["version"],
            "description": plugin["description"],
            "author": {"name": "rocky2431"},
            "homepage": f"https://github.com/{plugin['repository']}",
            "skills": [skills],
        }).encode()
    payload["marketplace-origin.json"] = json_text(origin(plugin)).encode()
    output = io.BytesIO()
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_DEFLATED) as archive:
        for path, body in sorted(payload.items()):
            entry = zipfile.ZipInfo(path, (1980, 1, 1, 0, 0, 0))
            entry.compress_type = zipfile.ZIP_DEFLATED
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, body)
    return output.getvalue()


def git_source(plugin: dict, *, subtree: bool = True) -> dict:
    source = {
        "source": "git-subdir" if subtree else "url",
        "url": f"https://github.com/{plugin['repository']}.git",
        "ref": plugin["ref"],
        "sha": plugin["sha"],
    }
    if subtree:
        source["path"] = plugin["path"]
    return source


def claude_entry(plugin: dict, host: str) -> dict:
    entry = {"name": plugin["name"], "description": plugin["description"]}
    if plugin["name"] == "ultra-goal":
        entry["source"] = git_source(plugin)
        return entry
    # These upstream projects ship Codex manifests. The marketplace supplies the
    # other host's component definition without editing those source repositories.
    entry.update(source=git_source(plugin, subtree=False), strict=False,
                 version=plugin["version"], skills=[f"./{plugin['path']}/skills"])
    if plugin["name"] == "task-state-with-files":
        variable = "CLAUDE_PLUGIN_ROOT" if host == "claude" else "ZCODE_PLUGIN_ROOT"
        script = f"${{{variable}}}/{plugin['path']}/skills/task-state-with-files/scripts/lifecycle_hook.py"
        entry["hooks"] = {"SessionStart": [{
            "matcher": "^(startup|resume|clear|compact)$",
            "hooks": [{"type": "command", "command": f'python3 "{script}" --host {host}', "timeout": 10}],
        }]}
    return entry


def catalogs(source: dict) -> dict[Path, dict]:
    common = {"name": source["name"], "owner": {"name": "rocky2431"}}
    zcode = []
    for plugin in source["plugins"]:
        entry = claude_entry(plugin, "zcode")
        if plugin["name"] == "agent-harness-design":
            # Reuse the package and let zCode verify its digest before reading
            # the native Codex manifest it contains.
            entry = {key: entry[key] for key in ("name", "description", "version")}
            entry["source"] = {
                "source": "url", "type": "zip",
                "url": f"https://raw.githubusercontent.com/{source['repository']}/main/{package_path(plugin)}",
                "sha256": hashlib.sha256((ROOT / package_path(plugin)).read_bytes()).hexdigest(),
            }
        zcode.append(entry)
    return {
        ROOT / ".agents/plugins/marketplace.json": {
            "name": source["name"], "interface": {"displayName": "Excellent Skill Marketplace"},
            "plugins": [{"name": p["name"], "source": git_source(p),
                         "policy": {"installation": "AVAILABLE", "authentication": "ON_INSTALL"},
                         "category": p["category"]} for p in source["plugins"]],
        },
        ROOT / ".claude-plugin/marketplace.json": {
            **common, "plugins": [claude_entry(p, "claude") for p in source["plugins"]],
        },
        ROOT / ".zcode-plugin/marketplace.json": {
            **common, "plugins": zcode,
        },
        ROOT / "marketplaces/kimi.json": {
            "plugins": [{"id": p["name"], "displayName": p["name"], "type": "plugin",
                         "tier": "curated", "version": p["version"], "description": p["description"],
                         "homepage": f"https://github.com/{p['repository']}",
                         "source": f"https://raw.githubusercontent.com/{source['repository']}/main/{package_path(p)}"}
                        for p in source["plugins"]],
        },
    }


def check(source: dict) -> None:
    for path, expected in catalogs(source).items():
        if path.read_text(encoding="utf-8") != json_text(expected):
            raise ValueError(f"Stale catalog: {path.relative_to(ROOT)}; run build")
    for plugin in source["plugins"]:
        with zipfile.ZipFile(ROOT / package_path(plugin)) as archive:
            if archive.testzip() is not None:
                raise ValueError(f"Corrupt package: {plugin['name']}")
            if json.loads(archive.read("marketplace-origin.json")) != origin(plugin):
                raise ValueError(f"Incorrect package origin: {plugin['name']}")
            manifest = json.loads(archive.read("kimi.plugin.json"))
            if (manifest["name"], manifest["version"]) != (plugin["name"], plugin["version"]):
                raise ValueError(f"Incorrect Kimi manifest: {plugin['name']}")
            for skill_root in manifest["skills"]:
                prefix = skill_root.removeprefix("./").rstrip("/") + "/"
                if not any(n.startswith(prefix) and n.endswith("/SKILL.md") for n in archive.namelist()):
                    raise ValueError(f"Missing packaged skills: {plugin['name']}")
    print(f"OK: four host catalogs and {len(source['plugins'])} pinned Kimi packages")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("command", choices=("build", "check", "refresh"))
    parser.add_argument("--plugin", help="Refresh one plugin; omit to refresh all")
    args = parser.parse_args()
    source = load_sources()
    if args.plugin and args.command != "refresh":
        parser.error("--plugin is only valid with refresh")
    if args.command == "check":
        check(source)
        return
    if args.command == "refresh":
        selected = [p for p in source["plugins"] if args.plugin is None or p["name"] == args.plugin]
        if not selected:
            parser.error("Unknown plugin")
        for plugin in selected:
            result = subprocess.check_output([
                "git", "ls-remote", "--refs", f"https://github.com/{plugin['repository']}.git",
                f"refs/heads/{plugin['ref']}",
            ], text=True, timeout=60).split()
            if not result:
                raise ValueError(f"Upstream branch is unavailable: {plugin['name']}")
            plugin["sha"] = result[0]
            url = f"https://raw.githubusercontent.com/{plugin['repository']}/{plugin['sha']}/{plugin['path']}/.codex-plugin/plugin.json"
            with urllib.request.urlopen(url, timeout=30) as response:
                plugin["version"] = json.load(response)["version"]
        validate_sources(source)
    packages = [(ROOT / package_path(p), build_kimi(p, upstream_files(p))) for p in source["plugins"]]
    # Prepare all downloads before replacing any generated output.
    for path, body in packages:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(body)
    for path, value in catalogs(source).items():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json_text(value), encoding="utf-8")
    (ROOT / "sources.json").write_text(json_text(source), encoding="utf-8")
    check(source)


if __name__ == "__main__":
    main()
