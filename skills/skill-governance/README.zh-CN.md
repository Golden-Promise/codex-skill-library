# skill-governance

[English](README.md)

## 它是什么

`skill-governance` 帮你更轻松地管理 Codex skill。
当你想接手已有项目、搭建干净的 skill 工作流、添加或启用 skill，或者在清理和发布前确认一切安全时，它都很适合。

## 最适合哪些场景

它特别适合这些场景：

- 接手一个已经有本地 skill 的项目
- 为新项目搭建 skill 治理流程
- 新增一个想长期复用的 skill
- 只在某个项目里启用一个 skill，而不是改动全部
- 在清理、重链、升级或发布前做一次检查
- 为 CI 或发布准备 skill 元数据

如果你刚开始用，先从接管项目、搭建项目骨架、或在清理和发布前做检查开始。

## 安装

在 Codex 里，最自然的说法是直接请求：

“请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-governance 安装 skill-governance。”

如果你想固定到某个版本，也可以直接补一句版本号：

“请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-governance 安装 skill-governance，并使用 v0.5.0。”

如果你想看精确的安装命令和进阶用法，请看 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。

## 快速上手

通常先做这三步：

1. 接管已有项目目录：`接管这个目录的 skill 管理，并把本地 skill 帮我整理好。`
2. 从零搭建项目：`给这个项目搭建 skill 管理骨架。`
3. 在清理或发布前检查：`在我清理或重链 skill 之前，先检查一下这个项目。`

## 接下来可以问什么

当基础流程准备好后，你可以继续让 `skill-governance` 帮你：

- 新增一个 skill
- 在某个项目里启用一个 skill
- 修复安全问题
- 审计注册表或依赖状态
- 为已有 skill 补文档
- 升级或退役一个 skill

如果你想看直接的命令模式和更多示例，请看 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。

## 延伸阅读

- 命令参考与进阶用法: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English task guide: [references/use-cases.md](references/use-cases.md)
- 提示词模板: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 维护者发布说明: [docs/publishing-with-skill-installer.zh-CN.md](docs/publishing-with-skill-installer.zh-CN.md)
