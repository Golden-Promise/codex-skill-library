# skill-context-keeper

[English](README.md)

## Overview

`skill-context-keeper` 是一个边界明确的包，专门用于在长编码线程里恢复和刷新结构化任务状态。
它帮助下一轮从当前最可信的工作图景继续，而不会扩展到阶段门控或最终交接说明。
这个包只负责维护结构化长任务状态。
它默认下游状态文件可能位于 `.agent-state/TASK_STATE.md` 之类的路径，但不负责流程门控，也不负责最终交接。

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

## Package Boundary

当任务需要刷新“当前状态”时，就应该使用这个包。
它负责重建已验证的代码库事实、保留未解决问题，并为下游继续执行更新一个紧凑的任务状态产物。

边界应保持收敛：

- 维护进行中任务的结构化状态
- 刷新或重写 `.agent-state/TASK_STATE.md` 这类产物
- 明确区分事实、假设和决策

这个包不运行阶段门控，不负责流程门控，也不负责最终交接。

## Install

可通过本仓库中的标准发布路径安装 `skill-context-keeper`。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-keeper 安装 skill-context-keeper。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-keeper 安装 skill-context-keeper，并使用我指定的 release 或 ref。`

如果你想直接运行 `skill-installer`，可使用：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-context-keeper
```

固定到本次连续性套件计划发布版本：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-context-keeper \
  --ref v0.6.0
```

## How To Use

当任务在继续执行前需要一次可靠的状态刷新时，就从这个包开始。
说明哪些摘要、待办或上下文已经过时，然后让它重建当前任务图景、延续未完成工作，并把输出限制在“当前状态”而不是流程规划或交接总结。
如果你希望产出明确落到某个文件，可以直接说：`请刷新当前任务状态，并更新 .agent-state/TASK_STATE.md。`

## References

- `SKILL.md`：触发路由与包边界
- [references/use-cases.md](references/use-cases.md)：正向与反向触发示例
- [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)：中文触发示例
- [references/prompt-templates.en.md](references/prompt-templates.en.md)：英文状态刷新提示词模板
- [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)：中文状态刷新提示词模板
- [assets/TASK_STATE.template.md](assets/TASK_STATE.template.md)：紧凑任务状态模板
