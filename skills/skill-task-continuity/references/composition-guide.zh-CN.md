# 组合指南

`skill-task-continuity` 是长任务连续性套件的入口包，方便下游仓库用一个清晰的入口理解整套工作流，同时不打破原子技能包的边界。
它负责解释这些包如何组合，以及如何为下游仓库引导初始化文件，而不是取代原子技能。

## 套件如何组合

- `skill-context-keeper` 负责刷新当前任务状态，并清楚区分事实、假设和决策。
- `skill-phase-gate` 负责在较大或较高风险的改动前后增加紧凑的检查点。
- `skill-handoff-summary` 负责在暂停或交接时写出面向续做的交接摘要。

这个组合包的价值在于：下游仓库可以从一个入口安装、从一个入口学习套件结构，并把启动模板复制到自己的仓库里。
如果团队希望一开始就把 4 个包都装好，也可以用一条 `skill-installer` 命令把组合包和三个原子包一起安装。

## 安装选择

- 只安装 `skill-task-continuity`，适合先从套件入口理解整体结构
- 用一条命令安装整套工具链，适合一开始就把 4 个包全部装好

这个组合包本身不会隐式自动安装另外三个原子包。
它做的是把现有的多路径 `skill-installer` 用法文档化，让用户既能一条命令装完整套件，又不会遇到隐藏副作用。

## 每个原子技能的明确调用措辞

可以直接使用下面这类提示词：

- `Use $skill-context-keeper to refresh .agent-state/TASK_STATE.md before more implementation work.`
- `Use $skill-phase-gate for a preflight before this risky multi-file change.`
- `Use $skill-phase-gate for a postflight gate now that the refactor is done.`
- `Use $skill-handoff-summary to write .agent-state/HANDOFF.md before we pause.`

如果需求本身就是在搭建或协调整套连续性流程，则先从 `skill-task-continuity` 开始，再路由到真正拥有下一步动作的原子技能。

## 推荐的下游布局

```text
AGENTS.md
.agent-state/
  TASK_STATE.md
  HANDOFF.md
  DECISIONS.md
  RUN_LOG.md
```

这个布局刻意保持精简。
套件会提供这些文件的模板，帮助下游仓库标准化“如何恢复工作”的约定。

## 推荐的长任务循环

1. 接手任务前先阅读 `.agent-state/TASK_STATE.md` 和 `.agent-state/HANDOFF.md`。
2. 如果下一步改动较大或风险较高，先运行一次 `skill-phase-gate` 预检。
3. 执行实现工作。
4. 用 `skill-context-keeper` 刷新 `.agent-state/TASK_STATE.md`。
5. 如果本轮产生了需要长期保留的决策或验证记录，则补充 `.agent-state/DECISIONS.md` 或 `.agent-state/RUN_LOG.md`。
6. 如果工作要暂停，则用 `skill-handoff-summary` 刷新 `.agent-state/HANDOFF.md`。

## 可选的仓库本地包装模式

有些团队会在 `.agents/skills/` 下放一些本地辅助提示或示例。
这是一种可选模式，不是强制要求。
建议保持这些包装非常薄，例如：

- `.agents/skills/refresh-task-state.md`：提示调用 `skill-context-keeper` 来刷新 `.agent-state/TASK_STATE.md`
- `.agents/skills/preflight-risky-change.md`：提示调用 `skill-phase-gate`
- `.agents/skills/write-handoff.md`：提示调用 `skill-handoff-summary`

这些本地包装的目标是帮助仓库内部采用套件，而不是分叉或替代公共技能包的行为。
