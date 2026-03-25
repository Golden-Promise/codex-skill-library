# Skills

[English](README.md)

这个目录存放 `codex-skill-library` 中可安装、可发布的 skill 包。

## 如何使用这个索引页

1. 先看下面的表格，找到与你任务最匹配的 skill。
2. 打开该包对应语言的 README。
3. 现在先看包内参考页了解边界说明，后续阶段再继续使用其中补充的示例、提示词或更细说明。

## 已发布包

| Skill | 适用场景 | 文档 |
| --- | --- | --- |
| `skill-governance` | 用任务式入口治理 skill 资产，包括新增、启用、体检、修复、审计和补文档 | [EN](skill-governance/README.md) / [中文](skill-governance/README.zh-CN.md) |
| `skill-context-keeper` | 刷新当前任务状态，但不接管检查点或交接职责 | [EN](skill-context-keeper/README.md) / [中文](skill-context-keeper/README.zh-CN.md) |
| `skill-phase-gate` | 在较大改动前后增加 preflight / postflight 检查点 | [EN](skill-phase-gate/README.md) / [中文](skill-phase-gate/README.zh-CN.md) |
| `skill-handoff-summary` | 生成紧凑、面向续做的交接摘要，保留状态、阻塞点和下一步 | [EN](skill-handoff-summary/README.md) / [中文](skill-handoff-summary/README.zh-CN.md) |
| `skill-task-continuity` | 在保持原子包边界的前提下启动并组合连续性套件 | [EN](skill-task-continuity/README.md) / [中文](skill-task-continuity/README.zh-CN.md) |

## 包结构约定

- 每个 skill 包都使用 `skills/<skill-name>/` 的固定结构。
- 目录名应与 `SKILL.md` 中的 `name` 字段保持一致。
- 包内 `README.md` 是给使用者最主要的入口。
- `references/` 主要放读者资料，`docs/` 主要放维护者说明。
- 对长任务连续性流程来说，只有在需要套件级启动或组合说明时才从 `skill-task-continuity` 开始；如果只需要某个具体动作，直接安装对应的原子包。
