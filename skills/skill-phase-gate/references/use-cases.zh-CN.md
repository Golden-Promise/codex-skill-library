# skill-phase-gate 使用场景

`skill-phase-gate` 适用于围绕有分量的编码工作增加一个 optional operational checkpoint。
它可以在高风险执行前提供紧凑的 preflight，也可以在完成一次有意义的修改后提供紧凑的 postflight；root-state refresh、subtask state 和 packet compression 仍由其他包持有。

## 适用触发示例

- `请用 skill-phase-gate 在这次多文件重构前写一个 preflight gate。`
- `在我开始改这个迁移之前，加一道检查点，写清楚预期文件、非目标和验证计划。`
- `这次有分量的修改已经做完了，请跑一个 postflight gate，记录实际改动、实际验证和剩余风险。`
- `给这次高风险编辑补一个提交前检查点，先核对范围和验证方式。`

## 不适用触发示例

- `把这个 typo 改掉就行，只有一行。`
- `只解释一下这个包怎么用，不要生成任何检查点产物。`
- `刷新当前任务状态，并在接下来一小时持续维护摘要。`
- `先刷新根任务状态，再继续实现。`
- `把下一轮压成一个很小的 packet，而不是生成 gate。`
- `第一次在这个仓库里启动整套连续性工具链。`
- `给下一个接手的 agent 写最终交接包。`

## 常见使用方式

### 多文件修改前的 Preflight

适合先快速讲清楚：

- 当前目标
- 当前约束
- 预期会改动哪些文件或模块
- 明确不会改动哪些文件或模块
- 打算如何验证

这对重构、迁移或容易范围失控的修改尤其有用。

### 有分量修改完成后的 Postflight

适合在实现完成后补一层检查，记录：

- 实际改动了哪些文件或模块
- 实际运行了哪些验证
- 还剩哪些风险
- 是否建议交接

postflight gate 只是检查点，不替代最终交接包。

## 状态归属边界

如果线程还需要持续维护 root 任务状态，请继续交给 `skill-context-keeper`。
如果线程需要 subtask local state，请交给 `skill-subtask-context`。
如果线程需要 packet-sized 的下一轮上下文，请交给 `skill-context-packet`。
`skill-phase-gate` 可以在检查点里简短提到当前状态，但不拥有长期任务记录。
