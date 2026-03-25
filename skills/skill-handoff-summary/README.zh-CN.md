# skill-handoff-summary

[English](README.md)

## 概述

`skill-handoff-summary` 是一个专注型包，用于在长时间编码任务需要暂停或转交时，生成面向续做的简洁交接摘要。
它把状态、阻塞点、需保留的硬约束，以及“下一步到底做什么”整理成紧凑的重启说明，避免下一位执行者从零翻线程历史。

## 核心能力

`skill-handoff-summary` 只专注一个结果：写出短小、可信、可直接复用的交接。

- 写入诸如 `.agent-state/HANDOFF.md` 的紧凑下游产物
- 保留当前状态、开放问题、硬约束，以及精确的下一步动作
- 给下一次线程或会话附上一段可直接复用的 resume prompt
- 聚焦续做，而不是膨胀成整项目文档

## 适用场景

- 一次工作结束时还有未完成事项，需要先暂停
- 把任务交给另一位执行者，并提供可信的重启说明
- 在上下文继续变旧之前，先记录阻塞点、已做决定和下一步动作
- 降低长线程在交接后的恢复成本

如果你已经确定工作即将暂停或换人，这个包就是更合适的入口。

## 不适用场景

- 在继续工作前重建当前任务状态
- 决定一个任务是否需要分阶段或检查点
- 以套件级工作流统筹多个原子包
- 维护覆盖整个任务的长期状态
- 生成整项目说明或仓库导览
- 在根本不需要交接时替代最终用户答复

## 安装

安装 `skill-handoff-summary` 时，请使用本仓库中的标准发布路径，并按你的工作流选择 release 或 ref。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-handoff-summary 安装 skill-handoff-summary。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-handoff-summary 安装 skill-handoff-summary，并使用 ref v0.6.1。`

关于触发示例和提示词措辞，可查看 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。

## 常用路径

可以先从下面三条路径开始：

1. 在一次会话结束时暂停仍未完成的工作。
2. 把任务转交给另一位执行者，并保留重启上下文。
3. 在 `.agent-state/HANDOFF.md` 中写下精确下一步和可复用的 resume prompt。

如果你想直接套用提示词模板，请查看 [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)。

## 直接告诉 Codex 怎么做

如果你想直接用自然语言告诉 Codex，可以这样说：

- `请用 skill-handoff-summary 在暂停前写一个紧凑、面向续做的交接摘要。`
- `请用 skill-handoff-summary 把交接写到 .agent-state/HANDOFF.md，并附上下一次会话可复用的 resume prompt。`

## 文档

- 触发路由与包边界：`SKILL.md`
- 参考索引：[references/README.zh-CN.md](references/README.zh-CN.md)
- 使用场景与触发示例：[references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English use cases: [references/use-cases.md](references/use-cases.md)
- 中文提示词模板：[references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 交接模板：[assets/HANDOFF.template.md](assets/HANDOFF.template.md)
