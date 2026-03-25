# skill-context-keeper

[English](README.md)

## Overview

`skill-context-keeper` 是一个边界明确的包，专门用于在长编码线程里恢复和刷新结构化任务状态。
它帮助下一轮从当前最可信的工作图景继续，而不会扩展到阶段门控或最终交接说明。

## Best For

- 任务暂停后重新进入，且上下文已经开始漂移
- 在继续改代码前先重建当前任务状态
- 用一个稳定入口刷新待办、假设和最近变更
- 对齐线程认知与仓库现状，避免带着旧前提继续推进

## What It Is Not For

- 把任务拆成分阶段执行
- 决定检查点规则或阶段退出条件
- 为另一个执行者撰写暂停或转交说明
- 启动整套长任务连续性套件

## Install

可通过本仓库中的标准发布路径安装 `skill-context-keeper`。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-keeper 安装 skill-context-keeper。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-keeper 安装 skill-context-keeper，并使用我指定的 release 或 ref。`

## How To Use

当任务在继续执行前需要一次可靠的状态刷新时，就从这个包开始。
说明哪些摘要、待办或上下文已经过时，然后让它重建当前任务图景、延续未完成工作，并把输出限制在“当前状态”而不是流程规划或交接总结。

## References

- `SKILL.md`：触发路由与包边界
- `references/`：后续面向读者的示例与提示词模式
- `assets/`：后续的状态快照与连续性笔记模板
