# skill-governance

[English](README.md)

## 概述

`skill-governance` 是用于接手已有代码库并将项目 skill 统一纳入治理的工具。
它帮助你整理本地 skill、明确哪些内容应继续启用，并让项目始终适合清理、发布和持续维护。

## 核心能力

`skill-governance` 关注的是项目 skill 管理中的核心动作：

- 接手已有项目，并整理现有 skill
- 为新项目建立清晰的治理流程
- 为 skill 补充、启用或整理项目上下文
- 在清理、重链、升级或发布前进行安全检查
- 为 CI 和发布流程准备 skill 元数据

## 适用场景

它尤其适合以下场景：

- 接手一个已经有本地 skill 的项目
- 为新项目搭建 skill 治理流程
- 新增一个想长期复用的 skill
- 只在某个项目里启用一个 skill，而不是改动全部
- 在清理、重链、升级或发布前做一次检查
- 为 CI 或发布准备 skill 元数据

如果你是第一次使用，建议先从项目接管、项目搭建或发布前检查开始。

## 安装

安装 `skill-governance` 时，请先使用 Codex 工作区中的标准安装路径，再按需要选择最新发布版本或指定 ref。

关于可直接复制的安装命令和进阶说明，请查看 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。

## 快速上手

通常可以从下面三个动作开始：

1. 接手已有项目目录。
2. 为新项目建立 skill 治理。
3. 在清理或发布前检查项目。

如果你想查看每条路径对应的可直接复制提示词，请参考 [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)。

## 下一步可以做什么

基础流程建立之后，`skill-governance` 还可以继续帮你完成：

- 新增一个 skill
- 在某个项目里启用一个 skill
- 应用可安全自动处理的修复
- 审计注册表或依赖状态
- 为已有 skill 补文档
- 升级或退役一个 skill

如需更多示例和直接的命令模式，请查看 [references/use-cases.md](references/use-cases.md)。

## 文档

- 命令参考与进阶用法: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English task guide: [references/use-cases.md](references/use-cases.md)
- 提示词模板: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 维护者发布说明: [docs/publishing-with-skill-installer.zh-CN.md](docs/publishing-with-skill-installer.zh-CN.md)
