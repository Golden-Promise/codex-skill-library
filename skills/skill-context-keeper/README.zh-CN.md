# skill-context-keeper

[English](README.md)

## 概述

`skill-context-keeper` 是一个专注型包，专门用于在长时间编码任务中恢复和刷新结构化任务状态。
它帮助下一轮从当前最可信、已验证的任务图景继续，而不会扩展成检查点、流程控制或最终交接说明。

## 核心能力

`skill-context-keeper` 只聚焦一件事：让进行中的任务状态保持可信、可续做。

- 根据已验证的仓库事实重建当前任务图景
- 清楚区分事实、假设、决策、风险和下一步动作
- 刷新诸如 `.agent-state/TASK_STATE.md` 的紧凑下游状态文件
- 只保留下一轮继续执行所需的连续性，不膨胀成整套工作流包

## 适用场景

- 任务暂停后重新进入，且上下文已经开始漂移
- 在继续改代码前先重建当前任务状态
- 用一个稳定入口刷新待办、假设和最近变更
- 对齐线程认知与仓库现状，避免带着旧前提继续推进

如果你在几个连续性包之间做选择，而当前主要问题是“任务状态过时或散落”，优先从这个包开始。

## 不适用场景

- 把任务拆成分阶段执行
- 决定检查点规则或阶段退出条件
- 为另一个执行者撰写暂停或转交说明
- 启动整套长任务连续性套件

## 安装

安装 `skill-context-keeper` 时，请使用本仓库中的标准发布路径，并按你的工作流选择 release 或 ref。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-keeper 安装 skill-context-keeper。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-keeper 安装 skill-context-keeper，并使用 ref v0.6.0。`

关于触发示例和提示词措辞，可查看 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。

## 常用路径

可以先从下面三条路径开始：

1. 在任务暂停一段时间后恢复上下文。
2. 在继续实现前刷新当前任务状态。
3. 把事实、未决问题和下一步动作收敛到 `.agent-state/TASK_STATE.md`。

如果你想直接套用提示词模板，请查看 [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)。

## 文档

- 触发路由与包边界：`SKILL.md`
- 使用场景与触发示例：[references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English use cases: [references/use-cases.md](references/use-cases.md)
- 中文提示词模板：[references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 任务状态模板：[assets/TASK_STATE.template.md](assets/TASK_STATE.template.md)
