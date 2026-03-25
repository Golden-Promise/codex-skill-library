# skill-handoff-summary

[English](README.md)

## 概述

`skill-handoff-summary` 是一个专注型包，用于写出面向续做的暂停说明或转交说明。
它服务的是诸如 `.agent-state/HANDOFF.md` 这样的紧凑下游产物，而不是整项目文档。

## 30 秒快速开始

- 什么时候用：工作马上要暂停、换人，或者切进新的会话。
- 你会得到什么：一份紧凑的重启说明，里面有当前状态、硬约束、开放问题和精确下一步。
- 典型产物：更新 `.agent-state/HANDOFF.md`。

如果你需要一份耐用的重启说明，就用它。
如果你只是想在聊天里快速同步状态，就不要用它。

如果你想直接告诉 Codex 怎么做：

先这样对 Codex 说：

- `请用 skill-handoff-summary 在暂停前写一个紧凑、面向续做的交接摘要。`

## 安装

你可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-handoff-summary 安装 skill-handoff-summary。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-handoff-summary 安装 skill-handoff-summary，并使用 ref v0.6.1。`

如果你想看精确的 shell 命令，可以直接跳到后面的 [安装细节](#安装细节)。

## 会创建或更新什么文件？

最典型的下游文件是 `.agent-state/HANDOFF.md`。

当你希望这个文件帮你保留下列信息时，就该用这个包：

- 任务摘要
- 当前状态
- 本次会话改了什么
- 需要保留的硬约束
- 开放问题
- 精确下一步动作
- 一段可复用的 resume prompt

## 不适合什么时候用

- 你需要在继续工作前先重建当前任务状态
- 你需要给高风险或多文件改动加检查点
- 你只是想在当前聊天里快速同步一下状态
- 你要写的是整项目说明，而不是 continuation-oriented handoff

## 相关技能

- `skill-context-keeper`：适合刷新 `.agent-state/TASK_STATE.md`
- `skill-phase-gate`：适合 preflight / postflight 检查点
- `skill-task-continuity`：适合第一次搭建流程和做套件级路由

## 文档

- 触发路由与包边界：`SKILL.md`
- 参考索引：[references/README.zh-CN.md](references/README.zh-CN.md)
- 使用场景与触发示例：[references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English use cases: [references/use-cases.md](references/use-cases.md)
- 中文提示词模板：[references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 交接模板：[assets/HANDOFF.template.md](assets/HANDOFF.template.md)

## 安装细节

把 `/path/to/install-skill-from-github.py` 换成你本地 `skill-installer` 仓库里的实际脚本路径。

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-handoff-summary \
  --ref v0.6.1
```
