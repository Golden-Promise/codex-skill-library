# 长任务连续性套件

## 问题陈述

长任务很少是一次性坏掉的。
它更常见的失败方式是逐步漂移：

- root state 变旧、变散、变臃肿
- child-task 细节泄漏到不该去的地方
- 下一轮加载了过多上下文
- risky edit 缺少 checkpoint
- 暂停后让下一位执行者靠猜继续

`context protocol` 的目标，就是把这些退化模式变成可路由、可验证、可维护的对象。
它不再把“连续性”当成一个模糊的摘要问题，而是明确拆成 root state、subtask state、packet compression、checkpoint 和 handoff。

## Context Protocol

当前套件围绕三层状态组织：

- **Root state：** 主任务的持久顶层图景
- **Subtask state：** 不应该污染 root summary 的局部子任务上下文
- **Packet：** 下一轮 root 或 subtask 执行真正需要的最小上下文对象

这三层默认落在一个 repo-first 的启动布局里：

- `AGENTS.md`
- `.agent-state/INDEX.md`
- `.agent-state/root/`
- `.agent-state/subtasks/`
- `.agent-state/archive/`

Beginner mode 通常只使用 `INDEX.md` 和 `.agent-state/root/`。
当任务需要拆子任务，或者需要把活跃上下文压成 packet 并移入 archive 时，才进入 expanded mode。

## 包结构图

| 包 | 职责 | 触发形态 |
| --- | --- | --- |
| `skill-context-keeper` | 刷新并压缩可信的 root-task state | root 任务还在继续，但当前图景已经过时、嘈杂或过大 |
| `skill-subtask-context` | 打开、刷新或关闭有边界的 child-task state | 某段工作需要自己的局部范围和重启状态 |
| `skill-context-packet` | 为下一轮写最小上下文 packet | 下一步只需要比完整 state 更小的注入面 |
| `skill-phase-gate` | 为 risky work 加一个可选操作检查点 | 有分量的多文件改动需要显式 preflight / postflight |
| `skill-handoff-summary` | 生成 root 或 subtask 的紧凑 handoff | 工作即将暂停、转交或跨 session |
| `skill-task-continuity` | 启动套件并路由到正确的原子包 | repo 需要 starter files、协议说明或选包帮助 |

## 兼容与迁移

如果你之前把这套东西理解成“4 个包分别负责状态、gate、handoff 和 orchestration”，现在应该看迁移说明：

- [docs/context-protocol-migration.md](context-protocol-migration.md)
- [docs/context-protocol-migration.zh-CN.md](context-protocol-migration.zh-CN.md)

短版结论是：

- root-state refresh 仍然归 `skill-context-keeper`
- `skill-phase-gate` 不再是连续性系统中心
- subtask isolation 现在有了一等所有者：`skill-subtask-context`
- 最小下一轮注入现在有了一等所有者：`skill-context-packet`

## 仓库边界规则

这个仓库是公开可安装的 skill library，所以套件说明必须保持面向读者、便于维护。

- 公开架构说明放在 `docs/`，不要写进这个 public library 自己的 live repo state 文件里。
- 把 `evals/cases.csv` 当成规范化路由矩阵，而不是内部草稿。
- 能匹配单个原子包时，就不要让 suite entry package 抢走任务。
- Beginner mode 必须对多数用户足够明显，不要求大家一开始就拆 subtasks。
- 迁移说明必须足够直接，避免旧四包用户靠猜来理解新模型。

## 成功标准

当下游 repo 可以在不重读整条线程的前提下走完这条路径时，这套东西才算成功：

1. bootstrap continuity starter files
2. refresh root state
3. split a bounded subtask
4. inject only a packet into the next execution turn
5. checkpoint a risky change when needed
6. pause with a valid handoff
7. resume from root 或 subtask artifacts without context bleed

## 种子评估矩阵

种子矩阵位于 `evals/cases.csv`。
它现在校验的是 protocol model，而不是旧的扁平布局模型。

| 用例 | 包 | 是否触发 | 提示形态 | 期望产物 | 期望事件 |
| --- | --- | --- | --- | --- | --- |
| `root_state_refresh` | `skill-context-keeper` | 是 | 从 repo 刷新 root task 图景 | `root/task_state` | `root:refresh`、`root:reconcile`、`root:compress` |
| `root_state_compress` | `skill-context-keeper` | 是 | 压缩 bloated root state，但不转成 packet-only 流程 | `root/task_state` | `root:refresh`、`root:reconcile`、`root:compress` |
| `root_state_refresh_not_needed` | `skill-context-keeper` | 否 | 没有连续性风险的一次性小问题 | `none` | `root:skip`、`route:other` |
| `subtask_split_from_root` | `skill-subtask-context` | 是 | 把有边界的 child work 从 root 线程拆出去 | `subtask/task_state` | `subtask:split`、`subtask:refresh`、`subtask:isolate` |
| `subtask_resume_from_packet` | `skill-subtask-context` | 是 | 从 packet 恢复 child task 并刷新局部状态 | `subtask/task_state` | `subtask:split`、`subtask:refresh`、`subtask:isolate` |
| `subtask_state_not_needed` | `skill-subtask-context` | 否 | 留在 root state，不打开 child task | `none` | `subtask:skip`、`route:root_or_packet` |
| `packet_root_minimal_injection` | `skill-context-packet` | 是 | 把下一轮 root turn 压成最小 packet | `root/packet` | `packet:compose`、`packet:trim`、`packet:inject` |
| `packet_not_needed_for_full_refresh` | `skill-context-packet` | 否 | 需要 full-state refresh，而不是 packet compression | `none` | `packet:skip`、`route:state_or_handoff` |
| `phase_gate_risky_checkpoint` | `skill-phase-gate` | 是 | 为 risky multi-file work 加 checkpoint | `phase/preflight`、`phase/postflight` | `phase:preflight`、`phase:checkpoint`、`phase:postflight` |
| `tiny_edit_not_gate` | `skill-phase-gate` | 否 | 只做一个 trivial local edit | `none` | `phase:skip`、`direct:edit` |
| `handoff_subtask_pause` | `skill-handoff-summary` | 是 | 暂停 child task 并留下 restart note | `subtask/handoff` | `handoff:capture`、`handoff:pause`、`handoff:resume` |
| `handoff_not_needed` | `skill-handoff-summary` | 否 | 直接给最终答案，不需要 continuation artifact | `none` | `handoff:skip`、`direct:answer` |
| `suite_bootstrap_protocol` | `skill-task-continuity` | 是 | bootstrap protocol 并在套件内路由 | `suite/agents`、`suite/index`、root/subtask templates | `suite:bootstrap`、`suite:route`、`suite:explain` |
| `suite_boundary_clean` | `skill-task-continuity` | 否 | trivial README fix 中顺带提到了 continuity 关键词 | `none` | `suite:skip`、`direct:edit` |

## 校验策略

当前静态 harness 会检查：

- 路由正负向
- 精确事件命名空间
- 严格产物映射
- required file 存在性
- workflow 文档覆盖
- 已发布文档里的边界语言

这让维护者可以在不运行 live model 的情况下，把 protocol 当成可回归校验的对象。
