# skill-phase-gate

[English](README.md)

## Overview

`skill-phase-gate` 用于在有分量的编码工作前后加入紧凑的 preflight / postflight 检查点。
它帮助高风险执行保持清晰，但不会接管长期任务状态、泛化规划或最终交接。

## Best For

- 在重构、迁移或多文件改动前做 preflight
- 在完成一次有分量的修改后做 postflight，核对实际改动和验证结果
- 对高风险编辑先明确预期修改范围、明确不改动的范围以及验证计划
- 在提交前增加一次有意义的检查点

## Meaningful Checkpoint Bar

只有当“加一道检查点”本身有价值时才适合使用：

- 适合：重构、多文件修改、高风险编辑、提交前检查点
- 不适合：typo 修复、极小的一行改动、纯说明类请求、泛化规划

## What It Is Not For

- 不适合琐碎的一行改动
- 不适合纯解释或纯讲解任务
- 重建过时或缺失的任务上下文
- 在中断后刷新当前状态
- 为另一个执行者撰写暂停或转交说明
- 持有本应由 `skill-context-keeper` 维护的长期状态
- 统筹整套长任务连续性套件

## Install

可通过本仓库中的标准发布路径安装 `skill-phase-gate`。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-phase-gate 安装 skill-phase-gate。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-phase-gate 安装 skill-phase-gate，并使用我指定的 release 或 ref。`

## How To Use

在实现前后的关键检查点调用这个包。
如果是 preflight，请说明当前目标、关键约束、预期会改动的文件、明确不改动的文件，以及验证计划；如果是 postflight，请让它记录实际改动、实际验证、剩余风险，以及是否建议交接。

如果你还需要跨长线程保存持续状态，请继续使用 `skill-context-keeper`；这个包只负责当前这一道检查点。

## References

- `SKILL.md`：触发路由与包边界
- [references/README.zh-CN.md](references/README.zh-CN.md)：面向读者的参考索引
- [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)：适用与不适用示例
- [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)：可直接粘贴的提示词模板
- [assets/PREFLIGHT.template.md](assets/PREFLIGHT.template.md)：preflight 清单
- [assets/POSTFLIGHT.template.md](assets/POSTFLIGHT.template.md)：postflight 清单
