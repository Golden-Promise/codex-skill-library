# skill-context-keeper 提示词模板

当你希望 `skill-context-keeper` 刷新或压缩可信的 root task state，而且不要偏离到 subtask local state、packet compression、流程门控或最终交接时，可直接复用下面这些模板。

## Positive Trigger Prompts

- `请使用 skill-context-keeper 在继续之前根据仓库刷新根任务状态。`
- `请把现有根任务摘要与代码库现状对齐，并重写 .agent-state/root/TASK_STATE.md。`
- `刷新根任务状态，明确区分事实、假设和决策，并给出推荐的下一步动作。`
- `把根任务里已经陈旧的细节压进 archive notes，但保留仍然活跃的事实。`

## Negative Trigger Prompts

- `先决定项目阶段，并在实现前设置阶段门。`
- `为某个子任务打开独立的局部状态。`
- `把下一轮压成一个 packet，而不是刷新完整 root 状态。`
- `为下一位代理生成最终交接说明，并结束这个线程。`
- `把规划、状态刷新和最终转交流程合并成一个整体工作流来处理。`

## 刷新当前任务状态

当你想直接表达“刷新状态”时，可以这样说：

```text
请使用 skill-context-keeper 刷新根任务状态。
检查仓库，把已验证事实与假设、决策分开，
更新 .agent-state/root/TASK_STATE.md，并在需要时补上 compression / archive notes，
最后写出推荐的下一步动作和仍需完成的验证。
不要创建 subtask state，不要压 packet，也不要加入流程门控或最终交接。
```

## 紧凑续做模板

```text
请刷新这个长编码任务的根任务状态。
假设下游状态文件路径是 .agent-state/root/TASK_STATE.md。
记录当前目标、范围、硬约束、已验证代码库事实、已完成工作、开放风险、最近决策、compression / archive notes，以及推荐的下一步动作。
保持包边界收敛：只做 root-state refresh 和 compression。
```

## 事实 / 假设 / 决策模板

```text
请重建任务状态，并把每一项明确标注为 Fact、Assumption 或 Decision。
事实必须来自仓库证据，假设保持简短，只记录已经做出的决策。
将刷新后的状态写入 .agent-state/root/TASK_STATE.md，不要创建 subtask state，不要生成 packet、阶段门控或最终交接。
```
