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
| `skill-workflow-manager` | 管理 canonical skill 共享库、项目链接、导入和校验流程 | [EN](skill-workflow-manager/README.md) / [中文](skill-workflow-manager/README.zh-CN.md) |

## 包结构约定

- 每个 skill 包都使用 `skills/<skill-name>/` 的固定结构。
- 目录名应与 `SKILL.md` 中的 `name` 字段保持一致。
- 包内 `README.md` 是给使用者最主要的入口。
- `references/` 主要放读者资料，`docs/` 主要放维护者说明。
