# 长任务连续性套件

## 问题陈述

长线程通常不是一次性坏掉的，而是逐步退化：共享状态开始过时，工作流失去节奏，交接信息也变得不足以让下一位执行者放心接手。

这套文档要解决的，就是把这些退化模式说清楚。我们把长任务中的失效拆成三类：

- 状态漂移，也就是工作认知和真实进展开始脱节
- 流程漂移，也就是本来需要分阶段推进的任务变成了没有检查点的直冲
- 交接摩擦，也就是换人之后需要靠猜才能继续

目标不是增加仪式感，而是让连续性变成可观察、可验证、可维护的东西。只有这样，长任务才更容易恢复、审阅和转交。

## 状态漂移、流程漂移、与交接摩擦

这三种问题彼此相关，但并不相同。

状态漂移通常表现为摘要、上下文或任务记忆已经跟不上真实工作进度。它最大的风险是悄悄偏离：线程表面上很顺，实际上已经带着错误前提继续往前走。

流程漂移则发生在需要分阶段推进的任务被当成一次性动作处理。工作可能还在继续，但检查点、决策点和边界感都会变弱。

交接摩擦出现在暂停或转交之后，下一位执行者拿到的信息不够完整，必须重新猜测当前状态。问题不一定是错误，但一定会增加恢复成本。

这个套件就是用这三种差异来决定：哪些包应该触发，哪些包不该被卷进来。

评估矩阵里的产物和事件都使用了规范化的路径和值，这样后续执行器就能稳定校验，而不是依赖自然语言猜测。

## 包结构图

| 包 | 职责 | 触发形态 |
| --- | --- | --- |
| `skill-context-keeper` | 在长线程中保存和重建工作状态，尤其适合处理中断或过时摘要后的恢复。 | 恢复、刷新、或对齐上下文。 |
| `skill-phase-gate` | 判断任务是否需要阶段边界、检查点，或在继续执行前先停一下。 | 拆分、门控、或分阶段推进。 |
| `skill-handoff-summary` | 在任务暂停或转交时产出清晰的交接说明。 | 总结状态、阻塞点和下一步。 |
| `skill-task-continuity` | 当任务本身就是为了维持长线程连续性时，统筹前三个原子包。 | 启动套件、协调边界、保持流程连贯。 |

## 仓库边界规则

这个仓库是公开可安装的 skill 库，所以套件文档必须尽量面向读者，且便于维护。

- 套件规范放在 `docs/`，不要写进运行中的 agent 状态文件。
- 本任务不要创建根目录 `AGENTS.md`、`.agent-state/`，也不要写入 public-package 的 `.agents/skills` 内容。
- `evals/cases.csv` 是触发覆盖的事实来源，但正文也要能独立读懂。
- 先用通俗语言解释包边界，不要要求读者先去看实现文件。
- 能匹配原子包的就优先匹配原子包，组合包不应该抢走本该由原子包处理的工作。
- 把模糊情况写进矩阵，方便维护者看到“只是关键词出现”并不等于真正触发。

## 成功标准

### 结果

- 长任务可以在不中断意图的情况下恢复、暂停或转交。
- 套件能覆盖四个目标包的误触发和漏触发情况。
- 维护者不看包源码，也能理解整体架构和边界。

### 过程

- 每个原子包都要有正触发和负触发用例。
- 矩阵里要有组合包的启动用例，也要有边界保护用例。
- 每个案例都要写清楚期望产物，以及必要时对应的工作流事件或命令形态。

### 风格

- 文档要简洁、面向读者、易于扫读。
- 英文版和中文版保持相同的主要章节顺序。
- 触发说明要像维护建议，不要像内部草稿。

### 效率

- 维护者可以只看文档和 CSV 就完成验证，不需要反推包实现。
- 矩阵要足够小，方便持续扩展，而不是越写越乱。
- 模糊提示只需要定义一次，之后就能作为回归覆盖重复使用。

## 初始评估矩阵

种子矩阵存放在 `evals/cases.csv`。下面这张表展示了初始覆盖的形状，以及在什么情况下应该关注哪些产物和流程事件。

| 用例 | 包 | 是否触发 | 提示形态 | 期望产物 | 期望事件 |
| --- | --- | --- | --- | --- | --- |
| `context_resume` | `skill-context-keeper` | 是 | 恢复最后已知状态，并把未完成工作带下去。 | `state/context.snapshot`、`state/continuity.note` | `context:reload`、`context:reconstruct`、`context:summary` |
| `context_resume_not_needed` | `skill-context-keeper` | 否 | 回答一个一次性问题，没有连续性风险。 | `none` | `context:skip`、`direct:answer` |
| `phase_gate_before_multi_step` | `skill-phase-gate` | 是 | 在开始编码前先把多步骤任务拆成阶段。 | `plan/phase.plan`、`plan/checkpoints.md`、`plan/exit-criteria.md` | `phase:split`、`phase:checkpoint`、`phase:gate` |
| `tiny_edit_not_gate` | `skill-phase-gate` | 否 | 只做一个很小的本地修改，不需要分阶段。 | `none` | `phase:skip`、`direct:edit` |
| `handoff_before_pause` | `skill-handoff-summary` | 是 | 暂停工作并交给另一个执行者。 | `handoff/HANDOFF.md`、`handoff/blockers.md`、`handoff/next-steps.md` | `handoff:capture`、`handoff:pause`、`handoff:transfer` |
| `handoff_not_needed` | `skill-handoff-summary` | 否 | 直接给最终答案，不需要转交说明。 | `none` | `handoff:skip`、`direct:answer` |
| `suite_bootstrap` | `skill-task-continuity` | 是 | 协调长任务套件，让三个原子包一起工作。 | `AGENTS.md`、`.agent-state/TASK_STATE.md`、`.agent-state/HANDOFF.md` | `bootstrap:agents_md`、`bootstrap:task_state`、`bootstrap:handoff` |
| `suite_boundary_clean` | `skill-task-continuity` | 否 | 一个很小的编辑，只是碰巧提到了所有关键词。 | `none` | `bootstrap:skip`、`direct:edit` |

## 阶段计划

当前任务本身就是引导阶段：先定义套件、先种下矩阵、先把边界讲清楚。

第一阶段要先把文档稳定下来，等包实现逐步成形后，再按需补充新的用例。重点不是堆数量，而是补能提高覆盖质量的案例。

第二阶段可以扩展成更接近真实长线程的场景，尤其是那些容易让错误包误触发的情况。

第三阶段则是把这套矩阵变成后续改动的回归护栏，确保触发行为一直保持窄而明确。
