# skill-handoff-summary 使用场景

`skill-handoff-summary` 适用于在编码工作即将暂停，或即将转交给另一位执行者时，生成紧凑、面向续做的交接摘要。
当下一次会话需要一个可信的重启说明时使用它；如果只是随手在聊天里汇报进度，或者要写成整项目文档，就不该由这个包接管。

## 适用触发示例

- `请使用 skill-handoff-summary 在今天暂停前写一份紧凑交接。`
- `请生成 .agent-state/HANDOFF.md，让下一次会话不用重读整个线程也能继续。`
- `把当前状态、必须保留的硬约束、开放问题和精确下一步整理给下一位接手的人。`
- `这个线程要转给另一位开发者了，请准备一份附带 resume prompt 的简洁续做交接。`
- `在停下来之前，把这次会话整理成短交接说明，而不是完整项目回顾。`

## 不适用触发示例

- `直接在聊天里给我一句今天做了什么的状态更新。`
- `请为整个仓库写一套完整项目文档，方便新团队成员上手。`
- `继续编码前，先根据仓库刷新当前任务状态。`
- `决定下一阶段的 gate，并告诉我现在能不能开始实现。`
- `把规划、长期状态和最终交接合成一份大总结。`

## 什么时候该写交接

当工作要暂停一段有意义的时间，或者任务即将交给另一条线程、另一位代理时，就该先写交接。
如果下一次会话否则就得从零重建阻塞点、需保留的约束，或者“第一步究竟做什么”，这个包就很合适。

## 什么时候不该用这个技能

如果只是想在聊天里简单汇报一下当前进度，而不需要留下可复用的持久产物，就不要用这个包。
也不要把它用于整项目文档、长期任务状态重建，或工作流门控判断。

## 可复用的 Resume Prompt 表达

当你希望下一次会话拿来就继续做时，可以直接使用这句：

`Resume this task from .agent-state/HANDOFF.md. Continue from the recorded status, preserve the listed constraints, inspect the files of interest, resolve the open problems in priority order, perform the exact next action first, and update the handoff if anything material changes.`
