# 组合指南

`skill-task-continuity` 是长任务连续性套件的入口包，方便下游仓库用一个清晰的入口理解整套工作流，同时不打破原子技能包的边界。
它负责解释 packet、root state、subtask、gate 和 handoff 如何组合，以及如何为下游仓库引导初始化文件，而不是取代原子技能。

## 套件如何组合

- `skill-context-keeper` 负责刷新当前任务状态，并清楚区分事实、假设和决策。
- `skill-subtask-context` 负责维护边界清楚的子任务状态，避免子任务推理污染根任务。
- `skill-context-packet` 负责把下一轮真正需要的上下文压缩成最小注入对象。
- `skill-phase-gate` 负责在较大或较高风险的改动前后增加紧凑的检查点。
- `skill-handoff-summary` 负责在暂停或交接时写出面向续做的交接摘要。

这个组合包的价值在于：下游仓库可以从一个入口安装、从一个入口学习套件结构，并把启动模板复制到自己的仓库里。
如果团队希望一开始就把 4 个包都装好，也可以用一条 `skill-installer` 命令把组合包和三个原子包一起安装。

## 安装选择

- 只安装 `skill-task-continuity`，适合先从套件入口理解整体结构
- 用一条命令安装整套工具链，适合一开始就把 6 个包全部装好

这个组合包本身不会隐式自动安装另外三个原子包。
它做的是把现有的多路径 `skill-installer` 用法文档化，让用户既能一条命令装完整套件，又不会遇到隐藏副作用。

## 每个原子技能的明确调用措辞

可以直接使用下面这类提示词：

- `Use $skill-context-keeper to refresh .agent-state/root/TASK_STATE.md before more implementation work.`
- `Use $skill-subtask-context to open or refresh .agent-state/subtasks/api-migration/TASK_STATE.md for this child task.`
- `Use $skill-context-packet to compress the next turn into .agent-state/root/PACKET.md before we continue.`
- `Use $skill-phase-gate for a preflight before this risky multi-file change.`
- `Use $skill-phase-gate for a postflight gate now that the refactor is done.`
- `Use $skill-handoff-summary to write the root or subtask handoff before we pause.`

如果需求本身就是在搭建或协调整套连续性流程，则先从 `skill-task-continuity` 开始，再路由到真正拥有下一步动作的原子技能。

## 推荐的下游布局

```text
AGENTS.md
.agent-state/
  INDEX.md
  root/
    TASK_STATE.md
    PACKET.md
    HANDOFF.md
    DECISIONS.md
    RUN_LOG.md
  subtasks/
  archive/
    root/
    subtasks/
    packets/
```

beginner mode 是只使用 `INDEX.md` 和 `root/` 的子集。
当仓库真正打开 `subtasks/` 里的子任务目录时，就进入 expanded mode。

## 推荐的长任务循环

1. 先阅读 `.agent-state/INDEX.md`。
2. 默认优先加载 `.agent-state/root/PACKET.md` 或某个子任务 packet，而不是一上来就读整份状态。
3. 只有当 packet 不够时，再打开对应的 root 或 subtask task state。
4. 如果下一步改动较大或风险较高，先运行一次 `skill-phase-gate` 预检。
5. 执行实现工作。
6. 刷新对应的 root 或 subtask state，然后再把下一轮需要的内容压回 packet。
7. 只有当某些决策或证据值得长期保留时，才补充 decisions log 或 run log。
8. 如果工作要暂停，则刷新 root 或 subtask handoff。

## 可选的仓库本地包装模式

有些团队会在 `.agents/skills/` 下放一些本地辅助提示或示例。
这是一种可选模式，不是强制要求。
建议保持这些包装非常薄，例如：

- `.agents/skills/refresh-task-state.md`：提示调用 `skill-context-keeper` 来刷新 `.agent-state/root/TASK_STATE.md`
- `.agents/skills/open-subtask.md`：提示调用 `skill-subtask-context`
- `.agents/skills/compress-next-turn.md`：提示调用 `skill-context-packet`
- `.agents/skills/preflight-risky-change.md`：提示调用 `skill-phase-gate`
- `.agents/skills/write-handoff.md`：提示调用 `skill-handoff-summary`

这些本地包装的目标是帮助仓库内部采用套件，而不是分叉或替代公共技能包的行为。
