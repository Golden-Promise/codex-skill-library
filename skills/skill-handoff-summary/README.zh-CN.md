# skill-handoff-summary

[English](README.md)

## Overview

`skill-handoff-summary` 用于在长时间编码任务需要暂停或转交时，生成清晰的暂停说明或交接摘要。
它把状态、阻塞点和下一步整理成可直接接手的材料，避免下一位执行者从零翻线程历史。

## Best For

- 一次工作结束时还有未完成事项，需要先暂停
- 把任务交给另一位执行者，并提供可信的重启说明
- 在上下文继续变旧之前，先记录阻塞点、已做决定和下一步动作
- 降低长线程在交接后的恢复成本

## What It Is Not For

- 在继续工作前重建当前任务状态
- 决定一个任务是否需要分阶段或检查点
- 以套件级工作流统筹多个原子包
- 在根本不需要交接时替代最终用户答复

## Install

可通过本仓库中的标准发布路径安装 `skill-handoff-summary`。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-handoff-summary 安装 skill-handoff-summary。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-handoff-summary 安装 skill-handoff-summary，并使用我指定的 release 或 ref。`

## How To Use

当执行即将暂停，或者任务要移交给另一个负责人时，就使用这个包。
说明当前状态、未解决问题、阻塞点以及最先要做的下一步，让它输出一个简洁、可交接的摘要，而不是重新规划整个流程。

## References

- `SKILL.md`：触发路由与包边界
- `references/`：后续面向读者的示例与提示词模式
- `assets/`：后续的交接说明、阻塞点和下一步模板
