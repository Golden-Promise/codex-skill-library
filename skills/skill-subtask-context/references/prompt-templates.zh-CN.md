# skill-subtask-context 提示词模板

当你希望 `skill-subtask-context` 打开或刷新隔离的子任务局部状态，而不是去处理 root-state refresh、packet compression、gate 或 handoff 时，可以使用这些模板。

## 适用触发示例

- `请用 skill-subtask-context 为这段边界清楚的工作打开一个子任务。`
- `请刷新 .agent-state/subtasks/<slug>/TASK_STATE.md，只保留仍然对这个子任务有效的父任务事实。`
- `在继续之前，先更新这个子任务的目标、局部阻塞点、退出条件和 merge notes。`

## 不适用触发示例

- `在下一轮之前先刷新根任务摘要。`
- `把下一轮压缩成一个 packet。`
- `在实现前给这个高风险改动加一个 gate。`
- `给下一位 owner 写暂停 handoff。`

## 打开一个新子任务

```text
请用 skill-subtask-context 打开一个子任务。
写入或刷新 .agent-state/subtasks/<slug>/TASK_STATE.md，
只复制这个子任务必须继承的父任务事实，
定义局部范围、局部风险、退出条件和下一步建议动作，
并保持边界收敛：只处理 local child-task state。
```

## 刷新一个已有子任务

```text
请刷新这个子任务的局部状态，不要重写整份根任务。
假设下游工件位于 .agent-state/subtasks/<slug>/TASK_STATE.md。
记录仍然在局部范围内有效的父任务上下文、新验证的事实、阻塞点、
仍需验证的内容，以及回流给父任务的 merge / closure notes。
不要顺手压 packet，也不要生成 handoff。
```
