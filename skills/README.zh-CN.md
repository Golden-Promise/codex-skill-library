# Skills

[English](README.md)

这个目录存放 `codex-skill-library` 中可安装、可发布的 skill 包。

## 选择合适的连续性技能

先看这份快速指南：

- 我暂停了一个任务，现在需要重新拼出当前图景。
  先用 `skill-context-keeper`。
- 我需要把工作拆成一个边界清楚、独立维护的子任务。
  先用 `skill-subtask-context`。
- 我需要为下一轮只准备最小必要上下文。
  先用 `skill-context-packet`。
- 我马上要做一个高风险或多文件改动。
  先用 `skill-phase-gate`。
- 我现在要停下来，并留下一个可以直接续做的重启说明。
  先用 `skill-handoff-summary`。
- 我第一次想在仓库里装好整套连续性工作流。
  先用 `skill-task-continuity`。

## 如何使用这个索引页

1. 如果你处理的是连续性工作流或连续性搭建问题，先看上面的快速选型块。
2. 再看下面的表格，找到与你下一步动作最匹配的包。
3. 打开该包对应语言的 README。
4. 当你需要示例、提示词或更细的边界说明时，再去看包里的 `references/` 页面。

## 已发布包

| Skill | 适用场景 | 文档 |
| --- | --- | --- |
| `skill-governance` | 用任务式入口治理 skill 资产，包括新增、启用、体检、修复、审计和补文档 | [EN](skill-governance/README.md) / [中文](skill-governance/README.zh-CN.md) |
| `skill-context-keeper` | 刷新并压缩可信的 root 任务状态，但不接管子任务状态或 handoff | [EN](skill-context-keeper/README.md) / [中文](skill-context-keeper/README.zh-CN.md) |
| `skill-subtask-context` | 为子任务建立、刷新和关闭局部状态，避免根任务上下文膨胀 | [EN](skill-subtask-context/README.md) / [中文](skill-subtask-context/README.zh-CN.md) |
| `skill-context-packet` | 把下一轮真正需要的上下文压缩成最小注入对象 | [EN](skill-context-packet/README.md) / [中文](skill-context-packet/README.zh-CN.md) |
| `skill-phase-gate` | 在 risky edits 前后增加可选的 operational checkpoint，但不接管状态归属 | [EN](skill-phase-gate/README.md) / [中文](skill-phase-gate/README.zh-CN.md) |
| `skill-handoff-summary` | 为 root 任务或子任务生成紧凑、面向续做的交接摘要，保留状态、阻塞点和下一步 | [EN](skill-handoff-summary/README.md) / [中文](skill-handoff-summary/README.zh-CN.md) |
| `skill-task-continuity` | 启动 `INDEX.md`、root packet、subtask 目录和整套连续性组合说明 | [EN](skill-task-continuity/README.md) / [中文](skill-task-continuity/README.zh-CN.md) |

## 包结构约定

- 每个 skill 包都使用 `skills/<skill-name>/` 的固定结构。
- 目录名应与 `SKILL.md` 中的 `name` 字段保持一致。
- 包内 `README.md` 是给使用者最主要的入口。
- `references/` 主要放读者资料，`docs/` 主要放维护者说明。
- 对长任务连续性流程来说，只有在需要套件级启动或组合说明时才从 `skill-task-continuity` 开始；如果只需要某个具体动作，直接安装对应的原子包或 packet 工具。
