# 四个 Skill 独立能力与可选组合：实施与验收

2026-09-08。用户批准本目录 RESULT.md 的方案，并授权五库分别 commit、push。
RESULT.md 保留为实施前的诊断快照；本文件记录实际变更与本轮证据。

## 发布内容

| 仓库 | 版本 | 提交 | 主要变化 |
|---|---|---|---|
| deepthink-skill | 0.2.0 | 38e322ff8bbbad3c8a38bc6a8c5fc15a631d2401 | 行动成果携带原要求、验收 ID、证据、授权边界与确定路径；建议不冒充已接受要求 |
| plan-with-flie-skill | 0.4.0 | 73d28bc7f70011ace9281d46a7a7f6a6d1925a92 | 显式 task/file 或原生会话绑定恢复；无选择静默；增加 activate/deactivate |
| agent-delegate-skill | 0.4.1 | 0a817535f7a464dfdf6fc7bd32e3dc25b860e0fd | 交接继承来源、纠正、现有授权与唯一状态写入者；区分等待、终态和业务验收 |
| ultra-goal-skill | 2.16.0 | 7210d3a8cb22731e0471380c5de8e0355f5cd5ed | 保留完整独立入口；组合时复用来源；准确说明异步派发观测；接受并精确保留大写验收 ID |

四个源码提交均已推送到 origin/main。Marketplace 将四端目录和新 ZIP 固定到以上 SHA；
Agent Harness 的既有 pin 与旧版 ZIP 保留。没有增加公共运行时、强制 Skill 链或目录迁移。
业务文档按明确路径、既有任务文档、仓库约定、新项目 documents 的顺序定位。

## 实际验收

本轮使用真实 Claude Code 会话和真实本地业务命令；原始会话日志留在本机临时验收目录，
仓库只保存业务夹具、产物、压缩后的运行元数据与主审检查结果，不提交完整模型推理或环境日志。
所有夹具均为本轮生成的可丢弃本地任务，不代表生产业务或生产授权。

| 场景 | 观察与主审核对 | 证据 |
|---|---|---|
| Deep 单独使用 | 独立研究会话交付 THOUGHTS/RESULT；保留 A1–A4，P1–P6 单列建议；未实施业务 | acceptance/deep-final/；native-sessions.json |
| Task 单独使用 | 原生 SessionStart 恢复正确记录；实现 CSV→JSON，保留退款、重复 ID 和前导零；无效 cancelled 行不覆盖成功输出；归档并解除绑定 | task-independent-check.json；task-solo/ |
| Send 单独使用 | 真实坏实现先失败，派发后修复；timeout=0 只结束等待，继续观察同一 ID；主审重跑原检查通过，输入与检查脚本未变 | send-independent-check.json；send-solo/ |
| Ultra 单独使用 | 无伴随 Skill，读取已准备的测试目标并实现真实 CLI；显式 verify 产生当前 green 事件；主审重跑保护检查并核对基线；已 disarm | ultra-independent-check.json；ultra-solo/ |
| Thinking→Task→新会话 | 将实际研究文件交给新 Claude 会话，通过 Send 启动；读取唯一 Task 记录，完成缺失业务步骤；7 个来源文件字节未变，A1–A4 真实检查通过 | chain-task-independent-check.json；chain-task/ |
| Thinking→Ultra | 只准备目标草案；A1–A4 正文逐字继承，covers 精确对应；7 个来源文件未变；未实现或 arm；校验仅报预期的 OWNER_CONFIRMATION_MISSING | chain-ultra-independent-check.json；chain-ultra/ |
| Task+Ultra 共同恢复 | 同一真实原生 SessionStart 运行两个候选 hook；读取指向同一 Task 的 Carry-over，准确回报结果；16 个既有文件字节未变，没有重跑业务 | combined-independent-check.json；native-sessions.json |
| 结果未知时核对效果 | **明确模拟的 unknown 收据**配合真实本地已发生效果；新会话读效果与产物后拒绝重试，效果仍只有一条 | unknown-recovery/recovery.json |
| 生成包→新原生会话 | 解压本次 Task 0.4.0 ZIP，使用其实际 Skill 与原生 SessionStart hook；恢复唯一记录并完成业务复核，36 个产物未变，正常解除会话绑定 | published-package-check.json |

真实 Send 修复 ID：`7e821b32a93e4db1b7e71464ee74faf8`，终态 success/end_turn。
实际接力 ID：`2451b7da752e49b18e69aa8ef00c098a`，终态 success/end_turn。
Ultra 验证 ID：`a3f76c5e12a5442cb17c079c63ed275b`，`verification_passed: true`。
这些传输终态之外，业务通过结论均有独立重跑或原始文件对比支撑。

保存产物的最小复核命令（在 Marketplace 根目录）：

```sh
python3 docs/research/2026-09-08-four-skill-composition/acceptance/check.py
```

此命令重跑保存的业务程序，不启动模型，也不冒充原生宿主生命周期回放。

## 源码与分发检查

- Deep：`python3 tests/check_package.py`，四份 manifest 0.2.0、64 个本地链接和包检查通过。
- Task：`python3 -m unittest discover -s tests -q`，51 项通过。
- Send：相同命令，46 项，1 skipped，其余通过。
- Ultra：相同命令，干净源码发布快照 441 项，1 skipped，其余通过。
- Marketplace：四端目录、pin、ZIP 来源/版本和 hook 检查通过；4 项包测试通过。
- Marketplace 重复 build 核对生成目录与 ZIP 字节一致；保留结果于 acceptance/catalog-determinism.json。
- 两个未参与实现的审查上下文核对组合语义与会话选择；修复后复核未发现新的具体缺陷。

Ultra 原工作区的全量包卫生测试会扫描既有 work/ultragoal-native-install 本机回执而失败。
本轮未删除这些在途材料、未削弱检查；以上全量结果来自只包含受版本控制源码与本轮改动的干净副本。
既有未跟踪 docs/research/2026-09-05-* 原样保留，没有纳入本轮提交。

## 修正过的观察与边界

- Task 无显式选择但根目录异常时仍输出诊断：独立审查复现后修复，四适配器回归覆盖静默与显式错误两条路径。
- Ultra 原 parser 拒绝 `A1`：新增回归先红后绿；现在保留大小写精确映射，没有自动重编号。
- Deep 初次受控输出曾把证据案例写成额外验收行：收窄交接指令后重跑，最终只保留 A1–A4。
  这是一次观察到的提示词改进，不是统计可靠率实验。
- 一次 Ultra 手动检查包装用了 macOS 不存在的 timeout，退出 127；直接执行同一检查后成功，未把前次失败抹去。
- Send 升版时首次全量检查发现 runtime/package*.json 仍为旧版本；统一版本后全量通过。
- Marketplace 默认 Python 缺少默认 CA 文件，首次下载失败；使用系统 `/etc/ssl/cert.pem` 重跑成功，未关闭 TLS 校验。

受控 Claude 会话使用实际 CLI 2.1.263，保留默认模型配置；init 显示 plugins=[]。
Skill 通过候选 SKILL.md 与资源路径显式提供，Task/Ultra hooks 通过临时原生 settings 加载。
因此它们证明选定包内容可以独立完成所列任务及原生 hook 可以恢复，**不等于四宿主均完成插件安装与自动发现**。
Send 使用已有 ACP 运行环境，其依赖仍然是独立使用前提；无需另外三个 Skill。

四端脚本/包适配已检查；本轮没有更新用户的全局安装、认证或配置，也没有声称
Codex、Kimi、zCode 的真实新会话、所有插件全装状态、或四端无人值守持续执行均已验收。
Ultra 独立运行使用可丢弃的已准备目标；Thinking→Ultra 覆盖未授权草案的继承路径，
没有把草案包装成一次完成的真实用户确认。未知结果恢复夹具不证明真实网络故障恢复率。
