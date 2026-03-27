# skill-context-packet

[English](README.md)

## 概述

`skill-context-packet` 是一个窄边界包，专门负责为下一轮 root 或 subtask 生成“最小上下文对象”。
当完整状态文件会浪费上下文预算，而下一步只需要一份紧凑执行包时，就用它。

## 30 秒快速开始

- 什么时候用：下一轮只需要最小可用上下文，而不需要整份状态刷新。
- 你会得到什么：一份包含精确目标、范围、输入、事实、约束、风险、退出条件和下一条命令的 packet。
- 典型产物：更新 `.agent-state/root/PACKET.md` 或 `.agent-state/subtasks/<slug>/PACKET.md`。

如果你想直接告诉 Codex 怎么做：

先这样对 Codex 说：

- `请用 skill-context-packet 把下一轮压缩到 .agent-state/root/PACKET.md，只保留仍然必要的最小事实和约束。`

## 安装

你可以直接用自然语言让 Codex 安装：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-packet 安装 skill-context-packet。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-context-packet 安装 skill-context-packet，并固定到 <tag-or-commit>。`

如果你想看精确的 shell 命令，可以直接跳到 [安装细节](#安装细节)。

## 会创建或更新什么文件？

典型的下游文件是 `.agent-state/root/PACKET.md` 和 `.agent-state/subtasks/<slug>/PACKET.md`。

当你希望把下一轮压成一个 minimum context object 时，就使用这个包，保留：

- 这一次的精确目标
- 收敛后的范围和明确非目标
- 真正值得加载的最小文件或输入
- 仍然必须保留的事实和约束
- 退出条件和下一条命令

## 不适合什么时候用

- 你需要完整重建 root task state 或 subtask state
- 你需要高风险改动前后的 workflow gate
- 你需要暂停或转交 handoff
- 你第一次在仓库里启动整套连续性工具链

这个包负责 minimum context object，不负责 root task state，也不负责 workflow gates。

## 相关技能

- `skill-context-keeper`：处理 `.agent-state/root/TASK_STATE.md`
- `skill-subtask-context`：处理 `.agent-state/subtasks/<slug>/TASK_STATE.md`
- `skill-phase-gate`：处理 preflight / postflight 检查点
- `skill-handoff-summary`：处理暂停和转交说明
- `skill-task-continuity`：处理套件级 bootstrap 和路由

## 文档

- 触发路由与包边界：`SKILL.md`
- 用例与触发示例：[references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English use cases: [references/use-cases.md](references/use-cases.md)
- 提示词模板：[references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- packet 模板：[assets/PACKET.template.md](assets/PACKET.template.md)

## 安装细节

把 `/path/to/install-skill-from-github.py` 换成你本地 `skill-installer` 仓库里的实际脚本路径。

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-context-packet \
  --ref <tag-or-commit>
```
