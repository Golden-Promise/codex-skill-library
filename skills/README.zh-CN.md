# Skills

[English](README.md)

这个目录存放 `codex-skill-library` 中可安装、可发布的 skill 包。

## 如何使用这个索引页

1. 先看下面的表格，找到与你任务最匹配的 skill。
2. 打开该包对应语言的 README。
3. 需要示例、提示词或更细说明时，再继续看包内 `references/`。

## 已发布包

| Skill | 适用场景 | 文档 |
| --- | --- | --- |
| `skill-governance` | 用任务式入口治理 skill 资产，包括新增、启用、体检、修复、审计和补文档 | [EN](skill-governance/README.md) / [中文](skill-governance/README.zh-CN.md) |
| `skill-context-keeper` | 在长任务中刷新或重建状态，不延伸到阶段规划或交接说明 | [EN](skill-context-keeper/README.md) / [中文](skill-context-keeper/README.zh-CN.md) |
| `skill-phase-gate` | 为多步骤编码任务增加阶段边界、检查点和退出条件 | [EN](skill-phase-gate/README.md) / [中文](skill-phase-gate/README.zh-CN.md) |
| `skill-handoff-summary` | 在暂停或转交时生成包含状态、阻塞点和下一步的摘要 | [EN](skill-handoff-summary/README.md) / [中文](skill-handoff-summary/README.zh-CN.md) |
| `skill-task-continuity` | 在上下文、阶段和交接需求同时出现时统筹连续性套件 | [EN](skill-task-continuity/README.md) / [中文](skill-task-continuity/README.zh-CN.md) |

## 包结构约定

- 每个 skill 包都使用 `skills/<skill-name>/` 的固定结构。
- 目录名应与 `SKILL.md` 中的 `name` 字段保持一致。
- 包内 `README.md` 是给使用者最主要的入口。
- `references/` 主要放读者资料，`docs/` 主要放维护者说明。
