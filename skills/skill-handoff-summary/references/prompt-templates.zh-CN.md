# skill-handoff-summary 提示词模板

当你希望 `skill-handoff-summary` 生成一份紧凑、面向续做的交接摘要，而且不要偏离到整项目文档、长期状态管理或工作流门控时，可以直接复用下面这些模板。

## 适用触发示例

- `请使用 skill-handoff-summary 在暂停这个任务前生成一份续做交接。`
- `请把当前状态、需保留的约束、开放问题和精确下一步写入 .agent-state/HANDOFF.md。`
- `请为下一位代理准备一份简洁的转交说明，并在结尾附上可复用的 resume prompt。`

## 不适用触发示例

- `直接在聊天里给我一个简短状态更新，不要写任何持久文件。`
- `为未来维护者把整个仓库写成完整文档。`
- `重建当前任务状态，并决定下一个工作流 gate。`

## 生成紧凑交接

```text
请使用 skill-handoff-summary 生成一份紧凑、面向续做的交接摘要。
目标路径是 .agent-state/HANDOFF.md。
总结任务、当前状态、本次会话中的变更、需要保留的硬约束、
相关文件或模块、开放问题，以及精确的下一步动作。
最后附上一段下一次会话可直接复用的 resume prompt。
不要把它扩展成整项目文档、长期状态或工作流门控。
```

## Resume Prompt

```text
Resume this task from .agent-state/HANDOFF.md.
Continue from the recorded status, preserve the listed constraints, inspect the files of interest,
resolve the open problems in priority order, perform the exact next action first,
and update the handoff if anything material changes.
```
