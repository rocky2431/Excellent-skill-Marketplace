# 四个 Skill 的组合与解耦审查

- 问题：在独立安装、任意接力、无关 hook 静默的前提下，明确 Thinking/Research、任务状态、派发和 UltraGoal 的边界与文档约定。
- 范围：deepthink-skill、plan-with-flie-skill、agent-delegate-skill、ultra-goal-skill；marketplace 仅检查分发层。Agent Harness 不在产品范围内。
- 产出：独立可读的现状及具体优化方向总结，含约两轮 Claude Code 对抗审查、最新一手实践、源码与可复核观察。
- 阶段：Deliver。状态：delivered。
- 授权：调研、只读审查、保存本次报告及临时证据。未授权改产品、迁目录、安装、提交或发布。
- 路径：沿用本仓库已有 docs 目录；本次路径不构成统一 documents 规范的实施决定。
- 已核对：五个仓库本地 HEAD 与远程 main 相同；UltraGoal 有原有未跟踪研究文件，保留。总 marketplace 的四项 pin 均低于关联源码版本。
- 当前证据：marketplace sources.json；各仓库当前源码。历史记忆仅用于定位，版本已实时复核。
- 独立审查：Claude Code，会话 four-skills-review-20260908-01a07edf；第一轮 delegation_id=5fdf54b6e5254762b1916585f4900404。
- 下一步：核对全局 hook 的无目标、错会话、多目标行为；调研公开组合方案；把第一轮意见和源码证据组成第二轮候选方案。
- 交付位置：RESULT.md。

## 第一轮后修订

- 两类 hook 无目标均静默；Task 的隐式唯一文件选择会向无关会话恢复，四适配脚本已复现。Ultra 的正确 session marker 对其他会话静默且无文件修改。最初临时 probe 使用了 session: 字面量，实际触发 legacy-binding warning；已按源码格式 session <id> 重跑，原始与修正结果均保留于 hook-probes.json。
- Ultra 派发观测识别直接 run，不识别 submit/wait/rtk 包装。此为观测覆盖缺口，不代表派发失败或独立验收被绕过。
- 自行运行当前源码的 20 项 Ultra 激活/归属测试和 39 项 Task 恢复测试，全部通过。它们不是四宿主新会话业务验收。
- Claude 第一轮成功返回，native session 2b5b827f-c1b2-4e32-ba68-791b9c1ebbd3，CLI 2.1.263，receipt 位于 agent-delegation/runs/20260908T023855Z-5fdf54b6e5254762b1916585f4900404/result.json。
- 对其意见保留异议：无代码耦合不等于零组合；旧 pin 不等于源码未发布；文件可读不是交接成功；纯提示词无需为 pytest 计数加框架；两段恢复提示不构成天然权限冲突。
- 第二轮已派发：a9789600b2fd42ecaa877a13a14613a1，同 Claude 会话，要求审查具体候选与上列异议。
- 候选方案：四模块独立，行动型交付用少量可读验收/交接字段；唯一当前工作状态；Task 显式选择恢复；业务文档遵循既有 docs/documents；保留模块控制状态和原始收据位置；真实接力验证先于通用 adapter 与大规模迁移。候选未获用户采用。
- 一手实践：Agent Skills 当前规范；Anthropic 2025-09 上下文与 2026-03 长任务复盘；Superpowers b36e082（保留文档链接，拒绝套用其全局强制启动）；OpenSpec e062b957；Spec Kit 4a7341a9；Claude hooks 与 ACP prompt-turn 当前官方文档。

## 交付核对

- 两轮 Claude Code 均返回 success/end_turn，第二轮复用同一原生会话；原始回执链接保留于 RESULT.md。
- 第二轮复测撤回“派发观测缺口导致验收绕过”，支持 Task 显式选择、单一当前工作状态、短交接约定、分层文档与版本报告。
- 主审再次复现两类 hook 接收同一事件时同时注入相反下一步（811/888 字符）。这是临时构造探针，未发生业务写操作。
- 未采纳：以 ID 集合/不同文档整体哈希证明语义一致；docs 与 documents 并存就报错；将当前准确的 run 检测文档改写成已支持 submit。
- RESULT.md 已完成现状、公开案例、优化优先级、可观察验收和证据边界；用户尚未评价或采用方案。
- 本轮所需工作已完成；待用户进一步决定是否实施，不继续产品修改或发布。
