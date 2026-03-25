# skill-phase-gate

[English](README.md)

## Overview

`skill-phase-gate` 用于判断一个编码任务是否需要在继续执行前先建立明确的阶段、检查点和退出条件。
它让分阶段工作保持清晰和可审阅，避免复杂线程被当成一次性动作直接冲过去。

## Best For

- 在开始实现前拆分一个多步骤任务
- 为高风险重构或迁移增加检查点
- 当多个改动互相依赖时，先把阶段边界讲清楚
- 判断一个任务是可以直接做，还是应该先门控分阶段

## What It Is Not For

- 重建过时或缺失的任务上下文
- 在中断后刷新当前状态
- 为另一个执行者撰写暂停或转交说明
- 统筹整套长任务连续性套件

## Install

可通过本仓库中的标准发布路径安装 `skill-phase-gate`。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-phase-gate 安装 skill-phase-gate。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-phase-gate 安装 skill-phase-gate，并使用我指定的 release 或 ref。`

## How To Use

在任务还没有滑进实现细节之前，就可以先调用这个包。
描述你的多步骤目标、哪些位置需要审阅或验证、以及哪些边界应该先停一下，再让它把这些内容收敛成一个窄而清晰的分阶段计划。

## References

- `SKILL.md`：触发路由与包边界
- `references/`：后续面向读者的示例与提示词模式
- `assets/`：后续的阶段计划、检查点和退出条件模板
