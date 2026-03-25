# skill-task-continuity

[English](README.md)

## Overview

`skill-task-continuity` 是一个组合包，面向那些“本身就在处理长任务连续性体系”的工作。
它负责在上下文刷新、阶段门控和交接说明之间做套件级协调，同时保持原子包边界清晰可见。

## Best For

- 把长任务连续性套件作为一个完整包族进行搭建
- 协调应该先触发哪个原子连续性包
- 处理那些确实同时涉及状态刷新、分阶段执行和交接行为的请求
- 当提示同时提到多个连续性问题时，仍然保持套件边界清楚

## What It Is Not For

- 用来替代 `skill-context-keeper` 的普通状态刷新
- 用来替代 `skill-phase-gate` 的常规分阶段决策
- 用来替代 `skill-handoff-summary` 的简单暂停或转交说明
- 仅仅因为提示里关键词很多，就抢走本该由单一包处理的任务

## Install

可通过本仓库中的标准发布路径安装 `skill-task-continuity`。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-task-continuity 安装 skill-task-continuity。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-task-continuity 安装 skill-task-continuity，并使用我指定的 release 或 ref。`

## How To Use

只有当任务本身是在做套件启动或多包连续性协调时，才从这里开始。
说明当前涉及哪些连续性问题、预期哪些原子包协同工作、以及哪些边界必须保持收敛，然后让这个包去路由或搭建套件级流程。

## References

- `SKILL.md`：触发路由与包边界
- [references/README.zh-CN.md](references/README.zh-CN.md)：包边界说明，以及后续面向读者参考资料的范围
- `assets/`：后续的套件启动与协调模板
