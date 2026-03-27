# skill-context-keeper

[English](README.md)

## 概述

`skill-context-keeper` 是一个专注型包，用于做 root-state refresh 和 compression。
当根任务还没结束，但你手上的 root task 图景已经变旧、变散，或者已经膨胀到不适合继续直接注入时，就该用它。

## 30 秒快速开始

- 什么时候用：根任务仍在继续，但当前图景已经陈旧、分散，或者已经大到不适合原样继续用。
- 你会得到什么：一个紧凑、可信的根任务快照，把事实、假设、决策、风险和下一步动作分清楚。
- 典型产物：更新 `.agent-state/root/TASK_STATE.md`。

如果你想直接告诉 Codex 怎么做：

先这样对 Codex 说：

- `请用 skill-context-keeper 根据仓库现状刷新根任务状态。`

## 安装

你可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-keeper 安装 skill-context-keeper。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-keeper 安装 skill-context-keeper，并使用 ref <tag-or-commit>。`

如果你想看精确的 shell 命令，可以直接跳到后面的 [安装细节](#安装细节)。

## 会创建或更新什么文件？

最典型的下游文件是 `.agent-state/root/TASK_STATE.md`。

当你希望刷新或重写这个 root 任务状态文件，让下一轮可以从一个可信摘要继续时，就该用这个包。它通常会帮助你整理：

- 当前目标
- 仓库里的已验证事实
- 已完成工作
- 开放问题和风险
- 需要压缩或归档的陈旧细节
- 下一步推荐动作

## 不适合什么时候用

- 你需要为高风险改动加 preflight 或 postflight 检查点
- 你需要一个拥有独立局部状态的子任务
- 你需要 packet compression，而不是完整 root 状态刷新
- 你需要写一份可交接、可暂停的 handoff
- 你是第一次在仓库里搭建整套连续性工作流
- 你想要的是泛化的流程控制，而不是状态刷新

这个包负责 root-state refresh 和 compression，不负责 subtask state，不负责 workflow gating，也不负责 final handoffs。

## 相关技能

- `skill-subtask-context`：适合处理 `.agent-state/subtasks/<slug>/TASK_STATE.md`
- `skill-context-packet`：适合 packet-sized context 注入
- `skill-phase-gate`：适合高价值的 preflight / postflight 检查点
- `skill-handoff-summary`：适合暂停或转交时写 handoff
- `skill-task-continuity`：适合第一次搭建整套连续性流程

## 文档

- 触发路由与包边界：`SKILL.md`
- 使用场景与触发示例：[references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English use cases: [references/use-cases.md](references/use-cases.md)
- 中文提示词模板：[references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 任务状态模板：[assets/TASK_STATE.template.md](assets/TASK_STATE.template.md)

## 安装细节

把 `/path/to/install-skill-from-github.py` 换成你本地 `skill-installer` 仓库里的实际脚本路径。

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-context-keeper \
  --ref <tag-or-commit>
```
