# Excellent Skill Marketplace

[English](README.md)

这是一个供 Codex、Claude Code、zCode 和 Kimi Code 使用的插件市场，收录了五个插件。添加市场后，按需选择安装。

每个插件保留自己的源码仓库、版本和发布节奏。本仓库记录选定的提交，提供各宿主能读取的市场目录，并根据这些提交生成 Kimi 安装包。

四个工作流 Skill 可以独立使用，也可以通过既有文档按需组合。见[独立使用与组合接力约定](docs/skill-composition.md)，其中说明了 Task State 0.4.0 的显式恢复选择方式。

## 有哪些插件

| 插件 ID | 用途 | 源码与完整说明 |
| --- | --- | --- |
| `ultra-goal` | 将想法整理成可执行目标，确定证据、边界和完成条件。 | [UltraGoal](https://github.com/rocky2431/ultra-goal-skill) |
| `agent-delegation` | 把工作委派给本地其他 Agent，并检查返回结果。 | [Agent Delegation](https://github.com/rocky2431/agent-delegate-skill) |
| `task-state-with-files` | 把任务进度保存在文件里，便于新会话或上下文压缩后恢复。 | [Task State with Files](https://github.com/rocky2431/plan-with-flie-skill) |
| `agent-harness-design` | 设计和审查 Agent 的工具、权限、上下文恢复与验证机制。 | [Agent Harness Design](https://github.com/rocky2431/agent-harness-design-skill) |
| `deep-thinking` | 澄清想法、研究证据、检验不同观点，形成有依据的结论。 | [Deep Thinking](https://github.com/rocky2431/deepthink-skill) |

这些插件可以自由组合。安装其中一个，不会连带安装其余插件。

## 怎么安装

请使用支持插件市场的宿主版本。下面以 UltraGoal 为例，将 `ultra-goal` 换成表格中的其他 ID 即可安装对应插件。

### Codex

在终端执行：

```sh
codex plugin marketplace add rocky2431/Excellent-skill-Marketplace --ref main
codex plugin add ultra-goal@excellent-skill-marketplace
```

注册后，也可以在 Codex 的插件界面浏览这个市场。如果当前任务尚未加载新安装的 Skill 或 Hook，请开启一个新任务。

### Claude Code（CC）

在 Claude Code 内输入：

```text
/plugin marketplace add rocky2431/Excellent-skill-Marketplace
/plugin install ultra-goal@excellent-skill-marketplace
```

终端中的对应命令是 `claude plugin marketplace add` 和 `claude plugin install`。安装或更新后，重启 Claude Code，让插件组件重新加载。

### zCode

打开插件页，选择「添加市场」，粘贴下面的目录地址：

```text
https://raw.githubusercontent.com/rocky2431/Excellent-skill-Marketplace/main/.zcode-plugin/marketplace.json
```

进入 `excellent-skill-marketplace`，选择需要的插件安装。请使用这个 JSON 地址：zCode 当前通过仓库地址发现市场时会优先读取 Claude 目录，而两者的 Task State Hook 命令不同。

### Kimi Code

在 Kimi Code 内打开目录：

```text
/plugins marketplace https://raw.githubusercontent.com/rocky2431/Excellent-skill-Marketplace/main/marketplaces/kimi.json
```

选择插件并安装。每个条目都指向一个 ZIP，包含插件文件和 Kimi 原生清单。也可以把条目中的 ZIP 地址传给 `/plugins install`。

## 使用前需要知道

UltraGoal 和 Task State 使用 Python 脚本，请让宿主能够执行 `python3`。支持的 Python 版本、目标设置和 Hook 行为见各自仓库的说明。

Agent Delegation 还需要 `agent-delegate` 命令、ACP 依赖，以及你打算调用的 Agent。安装市场插件只会加载 Skill，不会替你配置这些运行环境。请按[原仓库的运行环境安装说明](https://github.com/rocky2431/agent-delegate-skill#安装模型)完成配置。

Task State 在 Codex、CC 和 zCode 上包含 `SessionStart` 恢复 Hook。Kimi 安装包通过 `UserPromptSubmit` 在每次用户发消息时补回有长度上限的任务状态，包括恢复会话后的消息。Kimi 0.41.0 不会把 `SessionStart` 或 `PostCompact` 的输出注入模型，因此这不保证自主压缩后立即恢复。UltraGoal 自带 Kimi Hook，其续跑限制见 UltraGoal 的 README。

当前适配及实测范围见 [2026-09-06 四宿主核查记录](docs/host-compatibility-2026-09-06.md)。

如果已经从某个插件的独立市场安装过它，在这里启用同一个插件前，请先停用或卸载原来的副本。两个副本同时启用，可能重复加载 Skill 或执行 Hook。操作前先检查宿主的已安装插件列表。

## 怎么更新

刷新市场会获取目录，更新插件才会加载新安装包。这是两步操作，不能假定四个宿主都会在刷新市场时自动升级全部已安装插件。

| 宿主 | 刷新目录 | 更新已安装插件 |
| --- | --- | --- |
| Codex | `codex plugin marketplace upgrade excellent-skill-marketplace` | 在插件界面操作。需要明确重装时，刷新后移除选定插件，再重新添加。 |
| CC | `/plugin marketplace update excellent-skill-marketplace` | `/plugin update 插件ID@excellent-skill-marketplace`，或开启该市场的自动更新。 |
| zCode | 在插件页刷新市场。 | 在同一页面更新选定插件。 |
| Kimi Code | 重新打开上面的 `/plugins marketplace` 地址。 | 从当前目录选择新安装包。保存的旧 ZIP 地址仍然指向旧包。 |

CC 的第三方市场默认不开启自动更新，具体设置见[官方说明](https://code.claude.com/docs/en/discover-plugins#configure-auto-updates)。

## 维护这个市场

[sources.json](sources.json) 记录各插件的版本和完整提交哈希。[Sync upstream plugins 工作流](.github/workflows/sync.yml) 在每小时第 17 分钟检查各源码库的 `main`，也可以在 GitHub Actions 手动运行。它更新引用、运行测试并验证制品可重复生成；只有验证通过且存在变化时，才提交并推送新目录和 ZIP。GitHub 的定时任务可能延迟；运行失败会保留当前已发布的市场。发布内容改变时应提升插件版本，因为宿主可能按版本缓存安装包。

安装 Python 3.10+ 和 Git 后运行：

```sh
# 更新一个插件，引用其远程 main 的最新提交。
python3 scripts/catalog.py refresh --plugin agent-harness-design

# 或更新全部引用。
python3 scripts/catalog.py refresh

# 离线检查生成文件。
python3 scripts/catalog.py check
python3 -m unittest discover -s tests -v
```

在本地手动刷新时，检查差异后 commit、push 本仓库；否则由下一次成功的自动同步发布上游变化。用户刷新市场，再更新自己选择安装的插件。

`python3 scripts/catalog.py build` 根据现有提交重新生成目录和 Kimi ZIP，不会推进版本。CI 会从这些上游提交重新构建，检查结果是否与仓库内的制品一致。

| 路径 | 内容 |
| --- | --- |
| `sources.json` | 原仓库、插件路径、版本和固定提交。 |
| `.agents/plugins/marketplace.json` | Codex 目录。 |
| `.claude-plugin/marketplace.json` | CC 目录及组件适配。 |
| `.zcode-plugin/marketplace.json` | zCode 目录及组件适配。 |
| `marketplaces/kimi.json` | Kimi 目录及安装包地址。 |
| `packages/kimi/` | 自动生成的 ZIP，每个包内都有 `marketplace-origin.json`。 |
| `scripts/catalog.py` | 使用 Python 标准库的目录和安装包生成器。 |

请通过生成器更新目录和 ZIP，不要手动修改。保留旧 ZIP，因为已有安装可能仍保存着它的地址。Agent Delegation 的 ZIP 包含原仓库中的运行环境安装脚本和锁文件；其他 ZIP 包含插件子目录及上游已有的许可证。zCode 也使用 Agent Harness Design 的这个 ZIP，读取包内的 Codex 原生清单，并校验目录记录的 SHA-256 摘要。

## 许可证

本市场自己的代码和文档采用 [MIT 许可证](LICENSE)。安装包中的上游文件仍适用原来的许可条款，本许可证不替代它们。
