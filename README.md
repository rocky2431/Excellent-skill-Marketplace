# Excellent Skill Marketplace

[简体中文](README.zh-CN.md)

A shared catalog of five plugins for Codex, Claude Code, zCode, and Kimi Code. Add the marketplace in your agent, then install the plugins you want.

Each plugin keeps its own source repository, version, and release schedule. This repository records the selected commits and provides the catalog format each host reads. Kimi packages are generated from those commits.

The four workflow Skills can be used independently or composed through existing artifacts. See [independent skills and optional handoffs](docs/skill-composition.md), including the explicit recovery selection required by Task State 0.4.0.

## Available plugins

| Plugin ID | Use it for | Source and full instructions |
| --- | --- | --- |
| `ultra-goal` | Turn an objective into an executable goal with evidence, boundaries, and completion checks. | [UltraGoal](https://github.com/rocky2431/ultra-goal-skill) |
| `agent-delegation` | Delegate work between local agents and inspect their results. | [Agent Delegation](https://github.com/rocky2431/agent-delegate-skill) |
| `task-state-with-files` | Keep task progress in files so an agent can recover after a new session or compaction. | [Task State with Files](https://github.com/rocky2431/plan-with-flie-skill) |
| `agent-harness-design` | Design and review an agent's tools, authority, context recovery, and verification. | [Agent Harness Design](https://github.com/rocky2431/agent-harness-design-skill) |
| `deep-thinking` | Clarify ideas, research evidence, examine competing views, and form a defensible conclusion. | [Deep Thinking](https://github.com/rocky2431/deepthink-skill) |

You can install any combination. Installing one plugin does not install the others.

## Install

Use a host version that supports plugin marketplaces. The commands below install UltraGoal as an example; substitute any plugin ID from the table.

### Codex

Run in a terminal:

```sh
codex plugin marketplace add rocky2431/Excellent-skill-Marketplace --ref main
codex plugin add ultra-goal@excellent-skill-marketplace
```

The same marketplace can be browsed through the Codex plugin interface once registered. Open a new task if the current task has not loaded the newly installed Skill or hooks.

### Claude Code

Inside Claude Code:

```text
/plugin marketplace add rocky2431/Excellent-skill-Marketplace
/plugin install ultra-goal@excellent-skill-marketplace
```

Terminal equivalents are `claude plugin marketplace add` and `claude plugin install`. Restart Claude Code after installing or updating plugins to load their components.

### zCode

Open the plugin page, choose **Add marketplace**, and paste this catalog URL:

```text
https://raw.githubusercontent.com/rocky2431/Excellent-skill-Marketplace/main/.zcode-plugin/marketplace.json
```

Select `excellent-skill-marketplace` and install the plugins you need. Use this JSON URL: zCode's repository discovery currently selects the Claude catalog, which has a different Task State hook command.

### Kimi Code

Inside Kimi Code, open the catalog:

```text
/plugins marketplace https://raw.githubusercontent.com/rocky2431/Excellent-skill-Marketplace/main/marketplaces/kimi.json
```

Choose a plugin and install it. Each entry points to a ZIP containing the plugin and a native Kimi manifest. You can also pass an entry's ZIP URL to `/plugins install`.

## Before using the plugins

UltraGoal and Task State use Python scripts. Make `python3` available to the host. Read the upstream instructions for supported Python versions, goal setup, and hook behavior.

Agent Delegation also needs the `agent-delegate` CLI, its ACP dependencies, and the agents you want to use. Installing its marketplace plugin loads the Skill; it does not configure those runtimes. Follow the [upstream runtime installation instructions](https://github.com/rocky2431/agent-delegate-skill#安装模型).

Task State includes a `SessionStart` recovery hook on Codex, Claude Code, and zCode. Its Kimi package restores a bounded state excerpt through `UserPromptSubmit` whenever you send a message, including after resuming a session. Kimi 0.41.0 does not inject returned text from `SessionStart` or `PostCompact`, so this does not guarantee immediate recovery during autonomous compaction. UltraGoal includes its own Kimi hooks, whose continuation limits are described in its README.

See the [2026-09-06 host compatibility review](docs/host-compatibility-2026-09-06.md) (Chinese) for the tested paths and their limits.

If you already installed a plugin from its individual marketplace, disable or uninstall that copy before enabling the same plugin here. Two enabled copies can load duplicate Skills or run the same hooks twice. Check your host's installed-plugin list before changing anything.

## Updates

Refreshing a marketplace fetches its catalog. Updating an installed plugin loads a newer package. Hosts handle these as separate operations, and refreshing this repository does not automatically upgrade every installed plugin on every host.

| Host | Refresh the catalog | Update installed plugins |
| --- | --- | --- |
| Codex | `codex plugin marketplace upgrade excellent-skill-marketplace` | Use the plugin interface. For an explicit reinstall, remove the selected plugin and add it again after refreshing. |
| Claude Code | `/plugin marketplace update excellent-skill-marketplace` | `/plugin update PLUGIN@excellent-skill-marketplace`, or enable this marketplace's auto-update setting. |
| zCode | Refresh the marketplace in the plugin page. | Update the selected plugins in the same page. |
| Kimi Code | Reopen the `/plugins marketplace` URL above. | Select the current package from that catalog. A saved older ZIP URL continues to identify the older package. |

Claude Code's third-party marketplaces have auto-update disabled by default. See its [marketplace documentation](https://code.claude.com/docs/en/discover-plugins#configure-auto-updates).

## Maintain this marketplace

The selected versions and full commit hashes live in [sources.json](sources.json). The [Sync upstream plugins workflow](.github/workflows/sync.yml) checks the upstream `main` branches hourly, at minute 17, and can also be run manually from GitHub Actions. It refreshes the pins, runs the tests, verifies reproducible artifacts, and commits and pushes updated catalogs and ZIPs only when validation passes and changes exist. GitHub may delay scheduled runs; a failed run leaves the published marketplace unchanged. A changed release should have a new plugin version because hosts may cache packages by version.

With Python 3.10+ and Git installed:

```sh
# Select the latest published main commit of one plugin.
python3 scripts/catalog.py refresh --plugin agent-harness-design

# Or refresh all source references.
python3 scripts/catalog.py refresh

# Validate the generated files without network access.
python3 scripts/catalog.py check
python3 -m unittest discover -s tests -v
```

For a local manual refresh, review the diff, commit it, and push this repository. Otherwise, the next successful automatic sync publishes upstream changes. Users then refresh their marketplace and update the plugins they have chosen.

`python3 scripts/catalog.py build` rebuilds the catalogs and Kimi ZIPs from the existing pins. It does not advance them. CI rebuilds from the upstream commits and checks that the result matches the committed artifacts.

| Path | Purpose |
| --- | --- |
| `sources.json` | Upstream repositories, plugin paths, versions, and commit pins. |
| `.agents/plugins/marketplace.json` | Codex catalog. |
| `.claude-plugin/marketplace.json` | Claude Code catalog and component adapters. |
| `.zcode-plugin/marketplace.json` | zCode catalog and component adapters. |
| `marketplaces/kimi.json` | Kimi catalog with package URLs. |
| `packages/kimi/` | Generated ZIPs. Each includes `marketplace-origin.json`. |
| `scripts/catalog.py` | Standard-library catalog and package generator. |

Do not edit generated catalogs or ZIPs directly. Keep older ZIPs available because existing installations may retain their URLs. Agent Delegation's ZIP includes its repository-level runtime installer and lockfiles; the other ZIPs contain their plugin subtree and the available upstream license. zCode also uses the Agent Harness Design ZIP, reading its native Codex manifest and verifying the catalog's SHA-256 digest.

## License

The marketplace's own code and documentation use the [MIT license](LICENSE). Packaged upstream files retain their original licensing terms; this license does not relicense them.
