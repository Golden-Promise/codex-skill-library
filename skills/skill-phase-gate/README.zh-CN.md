# skill-phase-gate

[English](README.md)

## 概述

`skill-phase-gate` 用于在有分量的编码工作前后加入紧凑的 preflight / postflight 检查点。
它帮助高风险执行保持清晰，但不会接管长期任务状态、泛化规划或最终交接。

## 核心能力

`skill-phase-gate` 聚焦的是把高价值检查点做得清楚、可重复。

- 围绕目标、约束、范围和验证计划定义 preflight 检查点
- 围绕实际改动、实际验证和剩余风险记录 postflight 检查点
- 只在有分量的改动中显式使用检查点，而不是给每个小动作都加门
- 把长期状态交给 `skill-context-keeper`，把交接交给 `skill-handoff-summary`

## 适用场景

- 在重构、迁移或多文件改动前做 preflight
- 在完成一次有分量的修改后做 postflight，核对实际改动和验证结果
- 对高风险编辑先明确预期修改范围、明确不改动的范围以及验证计划
- 在提交前增加一次有意义的检查点

如果价值主要来自“先停下来确认范围和验证方式”，这个包就是更合适的入口。

## 检查点门槛

只有当“加一道检查点”本身有价值时才适合使用：

- 适合：重构、多文件修改、高风险编辑、提交前检查点
- 不适合：typo 修复、极小的一行改动、纯说明类请求、泛化规划

## 不适用场景

- 不适合琐碎的一行改动
- 不适合纯解释或纯讲解任务
- 重建过时或缺失的任务上下文
- 在中断后刷新当前状态
- 为另一个执行者撰写暂停或转交说明
- 持有本应由 `skill-context-keeper` 维护的长期状态
- 统筹整套长任务连续性套件

## 安装

安装 `skill-phase-gate` 时，请使用本仓库中的标准发布路径，并按你的工作流选择 release 或 ref。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-phase-gate 安装 skill-phase-gate。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-phase-gate 安装 skill-phase-gate，并使用 ref v0.6.1。`

关于触发示例和提示词措辞，可查看 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。

## 常用路径

可以先从下面三条路径开始：

1. 在重构、迁移或高风险多文件改动前做 preflight。
2. 在完成有分量的实现后做 postflight。
3. 在提交前为重要改动增加一次有意识的检查点。

如果你想直接套用提示词模板，请查看 [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)。

## 直接告诉 Codex 怎么做

如果你想直接用自然语言告诉 Codex，可以这样说：

- `请用 skill-phase-gate 在这次高风险多文件修改前生成一个 preflight gate。`
- `请用 skill-phase-gate 在我提交前为这次有分量的改动生成一个 postflight gate。`

## 文档

- 触发路由与包边界：`SKILL.md`
- 参考索引：[references/README.zh-CN.md](references/README.zh-CN.md)
- 使用场景与触发示例：[references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English use cases: [references/use-cases.md](references/use-cases.md)
- 中文提示词模板：[references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- preflight 清单：[assets/PREFLIGHT.template.md](assets/PREFLIGHT.template.md)
- postflight 清单：[assets/POSTFLIGHT.template.md](assets/POSTFLIGHT.template.md)
