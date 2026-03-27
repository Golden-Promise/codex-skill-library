# skill-subtask-context

[English](README.md)

## 概述

`skill-subtask-context` 是一个窄边界包，专门负责在较大的长任务内部打开、刷新和关闭子任务的局部状态。
当某段工作值得拥有独立状态文件，而不应该继续污染根任务摘要时，就用它。

## 30 秒快速开始

- 什么时候用：某个子任务需要独立局部上下文、独立范围和明确的退出条件。
- 你会得到什么：一份聚焦的子任务状态文件，里面包含父任务链接、局部事实、局部风险和合并备注。
- 典型产物：更新 `.agent-state/subtasks/<slug>/TASK_STATE.md`。

如果你想直接告诉 Codex 怎么做：

先这样对 Codex 说：

- `请用 skill-subtask-context 打开或刷新一个子任务，把内容写到 .agent-state/subtasks/<slug>/TASK_STATE.md，并保持父任务上下文最小化。`

## 安装

你可以直接用自然语言让 Codex 安装：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-subtask-context 安装 skill-subtask-context。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-subtask-context 安装 skill-subtask-context，并固定到 <tag-or-commit>。`

如果你想看精确的 shell 命令，可以直接跳到 [安装细节](#安装细节)。

## 会创建或更新什么文件？

典型的下游文件是 `.agent-state/subtasks/<slug>/TASK_STATE.md`。

当你希望打开或刷新这份局部子任务状态时，就使用这个包，让下一轮能够从一份可信摘要继续，包括：

- 子任务目标
- 仍然在局部范围内有效的父任务事实
- 值得优先加载的局部文件和输入
- 局部风险、阻塞点和退出条件
- 合并回父任务时需要吸收的备注

## 不适合什么时候用

- 你真正需要的是刷新 root task state，而不是子任务
- 你真正需要的是 packet compression，而不是局部状态刷新
- 你需要高风险改动前后的检查点
- 你需要的是暂停或转交 handoff，而不是活跃子任务状态

这个包负责 local child-task state，不负责 root task state，也不负责 packet compression。

## 相关技能

- `skill-context-keeper`：处理 `.agent-state/root/TASK_STATE.md`
- `skill-context-packet`：处理 root 或 subtask 的 packet 压缩
- `skill-phase-gate`：处理 preflight / postflight 检查点
- `skill-handoff-summary`：处理暂停和转交说明
- `skill-task-continuity`：处理套件级 bootstrap 和路由

## 文档

- 触发路由与包边界：`SKILL.md`
- 用例与触发示例：[references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English use cases: [references/use-cases.md](references/use-cases.md)
- 提示词模板：[references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 子任务状态模板：[assets/TASK_STATE.template.md](assets/TASK_STATE.template.md)

## 安装细节

把 `/path/to/install-skill-from-github.py` 换成你本地 `skill-installer` 仓库里的实际脚本路径。

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-subtask-context \
  --ref <tag-or-commit>
```
