# 四宿主适配核查：2026-09-06

本次核查覆盖四个独立源码仓库及市场生成的安装包。修复先发布到源码仓库，市场再更新固定提交和安装包。添加或刷新市场，与更新用户已安装的插件是两步操作。

## Kimi 的问题与修复

本机原生 Kimi Code 为 0.41.0，与当日官方更新渠道一致。旧 Python CLI 的版本号不能用来判断原生客户端是否较旧；模型 API 兼容 OpenAI 或 Anthropic，也不意味着客户端会执行同一套 Hook 协议。

当前 Kimi 支持生命周期 Hook，但事件发生、脚本执行、输出进入模型是三个不同的条件：

- `SessionStart` 会运行，但返回文本不注入模型。
- `PostCompact` 会运行，但返回文本不注入模型。
- `UserPromptSubmit` 的返回文本会加入用户消息。因此 Task State 改用这个事件，在每次用户输入时重新读取有长度上限的任务状态。
- 自主执行中没有新用户消息时，这个适配不会立即补回压缩后的状态。不把下一条用户消息时的恢复写成无人值守压缩恢复。

相关依据：[Kimi Hook 文档](https://www.kimi.com/code/docs/kimi-code-cli/customization/hooks.html)、[原生技能目录](https://www.kimi.com/code/docs/kimi-code-cli/customization/skills.html)、[环境变量](https://www.kimi.com/code/docs/kimi-code-cli/configuration/env-vars.html)、[输出消费问题 #1896](https://github.com/MoonshotAI/kimi-code/issues/1896)。官方的[会话日志恢复改进 #3423](https://github.com/MoonshotAI/kimi-code/pull/3423)属于宿主内部恢复，不能替代插件状态是否进入模型的验证。

## 四个源码仓库

| Skill | 本次修改 | 核查结果 |
| --- | --- | --- |
| UltraGoal | 修正旧用户安装器的 Kimi 路径；快捷入口支持 `KIMI_CODE_HOME`；修复 Windows 启动命令的条件分组。 | 原生 Kimi 清单已包含 6 个 Hook，保留已有 `UserPromptSubmit`、`TurnStarted` 适配。 |
| Task State | 新增原生 Kimi 清单；安装器和恢复适配改用 `UserPromptSubmit`；doctor 检查事件和命令；更新恢复说明。 | 用户安装与原生插件安装两条路径的状态文本均到达实际模型请求。 |
| Agent Delegation | 修正 Kimi 技能安装目录，保留现有 ACP 命令。 | 默认入口已是原生 Kimi 的 ACP；这个 Skill 不需要状态恢复 Hook。 |
| Agent Harness Design | 修正 Kimi 技能安装目录和安装说明。 | 只改仓库安装器，Skill 内容及 0.4.0 行为评测未改变，保留原插件版本。 |

四个安装器均使用 `$KIMI_CODE_HOME/skills`，未设置时为 `~/.kimi-code/skills`。旧 `~/.kimi/skills` 不是当前原生客户端的默认目录。

此次发布的准确提交及版本见 [sources.json](../sources.json)。Task State 原开发目录另有未提交的 0.3.0 工作，本次修复从已发布的 0.2.0 隔离完成；原有工作已保留并接入修复，没有混入本次发布。

UltraGoal 的 Windows 命令曾写成 `if not exist "script" exit 0 & ...`。原生 Windows CI 证明：即使脚本和 Python launcher 都存在，后续命令也被包含在条件范围内，脚本没有执行。修复为先用括号限定存在性检查，再启动解释器。新增回归使用真实 `cmd.exe` 执行三个清单中的全部 Windows 命令，检查单次运行、保留退出码 2、缺失脚本时放行；这取代了仅凭字符串存在就判断命令可达的结论。相关命令语义见 [Microsoft cmd 文档](https://learn.microsoft.com/en-us/windows-server/administration/windows-commands/cmd)。

## 验证范围

本次检查使用 Codex 0.153.4、Claude Code 2.1.261、Kimi Code 0.41.0、zCode 0.16.5。检查覆盖源仓库注册、安装路径和市场适配；未将四宿主的完整自主任务循环列为本次验收。

| 边界 | 实际证据 |
| --- | --- |
| Codex 插件发现 | 原生 app-server 的 `plugin/read` 解析四个源插件；UltraGoal 4 个 Skill / 3 个 Hook，Task State 1 / 1，另两个插件各 1 / 0。通用脚手架校验器不支持的现有扩展字段，以当前宿主解析结果核对。 |
| CC 目录 | 原生 `claude plugin validate` 接受 UltraGoal 和市场目录；市场保留 Task State 的 `CLAUDE_PLUGIN_ROOT` 适配。 |
| zCode 目录 | 保留独立目录及 `ZCODE_PLUGIN_ROOT`；目录回归校验 Task State 命令、Harness ZIP 类型和 SHA-256。没有冒充本次已完成 zCode 模型回合实测。 |
| Kimi 原生安装 | 在临时 `KIMI_CODE_HOME` 中通过原生插件安装 API 安装市场的四个 ZIP。发现 UltraGoal 4 / 6、Task State 1 / 1、另两个插件各 1 / 0。 |
| Kimi 模型请求 | 四插件同时启用，用户消息触发 Hook；随机任务状态标记出现在实际发往本地模型端点的请求中。 |
| 市场制品 | 测试解压真正的 Task State ZIP，从插件目录运行其 Hook，验证另一个工作目录中的状态出现在输出；缺失原生恢复 Hook 时检查失败。 |

Kimi 请求探针使用本地模型桩和临时配置，不读取用户凭证或更新用户安装。它证明宿主把状态送到了模型边界，不证明模型理解了状态，也不证明自主压缩后的连续执行。可在 Task State 源仓库运行：

```sh
python3 tests/probe_kimi_recovery.py
```

源码回归测试覆盖 UltraGoal 444 项（本机跳过 1 项 Windows 专属测试）、Task State 32 项、Agent Harness 33 项、Agent Delegation 38 项（1 项需显式启用 ACP 传输环境，跳过）。Task State 原目录保留的 0.3.0 工作另有 47 项测试通过。

[UltraGoal CI](https://github.com/rocky2431/ultra-goal-skill/actions/runs/33982589313)、[Task State CI](https://github.com/rocky2431/plan-with-flie-skill/actions/runs/33981370408)、[Agent Harness CI](https://github.com/rocky2431/agent-harness-design-skill/actions/runs/33981771409) 在 Linux、macOS、Windows 上均通过。UltraGoal 的 Windows 专属命令执行测试在 Windows CI 中实际运行。Agent Delegation 当前没有仓库 CI，本次验证为本地回归测试；市场的制品重建检查见其 [CI](https://github.com/rocky2431/Excellent-skill-Marketplace/actions)。

今后核查恢复能力，应沿着“事件触发 → 脚本运行 → 宿主消费输出 → 模型请求”验证。仅有清单、Hook 数量、脚本退出码或静态测试通过，不足以说明状态已经恢复。
