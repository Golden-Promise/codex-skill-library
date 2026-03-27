# skill-phase-gate 提示词模板

当你想在有分量的编码工作前后加一道简洁的 optional operational checkpoint 时，可直接使用这些模板。
如果还需要持续持有 root 状态、subtask 状态或 packet compression，请继续交给兄弟包。

## 适用触发示例

- `请用 skill-phase-gate 在这次多文件修改前生成一个 preflight gate。`
- `请用 skill-phase-gate 在我提交前为这次有分量的修改生成一个 postflight gate。`

## 不适用触发示例

- `别加检查点了，直接把这一行 typo 改掉。`
- `只解释代码，不要生成检查点产物。`
- `先刷新根任务状态，不要加 gate。`
- `把下一轮压成 packet，不要加 gate。`

## Preflight 模板提示词

```text
请用 skill-phase-gate 为这次有分量的编码任务生成一个 preflight gate。
内容要覆盖当前目标、当前约束、预期会改动的文件或模块、
明确不会改动的文件或模块，以及验证计划。
保持简短、可执行、清单化。
不要把它扩展成泛化规划，也不要接管长期状态跟踪。
如果需要持续的 root 状态归属，请交给 skill-context-keeper。
如果需要 subtask local state，请交给 skill-subtask-context。
如果需要 packet compression，请交给 skill-context-packet。
```

## Postflight 模板提示词

```text
请用 skill-phase-gate 为这次有分量的编码任务生成一个 postflight gate。
内容要覆盖实际改动的文件或模块、实际运行的验证、
剩余风险，以及是否建议交接。
保持简短、偏执行视角。
不要把它扩展成最终交接包，也不要从 skill-context-keeper、skill-subtask-context 或 skill-context-packet 手里接管状态归属。
```

## 琐碎改动反例

```text
这只是一个一行 typo 修复，不要使用 skill-phase-gate。
直接修改即可，不需要 preflight 或 postflight 检查点。
```
