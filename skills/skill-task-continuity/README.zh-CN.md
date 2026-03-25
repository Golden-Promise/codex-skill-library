# skill-task-continuity

[English](README.md)

## 概述

`skill-task-continuity` 是长任务连续性套件的入口包。
它负责解释各个连续性包如何组合，并提供一个启动脚本，把下游仓库需要的模板复制进去。
它不会取代原子技能包。

## 核心能力

`skill-task-continuity` 聚焦的是组合说明和下游初始化。

- 解释 `skill-context-keeper`、`skill-phase-gate`、`skill-handoff-summary` 三个原子包如何组合
- 为下游仓库启动 `AGENTS.md` 与 `.agent-state/*.md` 等文件
- 在套件级请求中，把工作路由到真正拥有下一步动作的原子包
- 明确公共包边界，让模板保持为下游资产，而不是仓库根目录里的运行时文件

## 适用场景

- 第一次在下游仓库中采用连续性工作流
- 在长任务开始前为下游仓库准备模板
- 判断下一步到底该由哪个原子包负责
- 向维护者或下游用户解释整套连续性流程，而不打乱包边界

## 不适用场景

- 用来替代 `skill-context-keeper` 的普通状态刷新
- 用来替代 `skill-phase-gate` 的常规检查点
- 用来替代 `skill-handoff-summary` 的简单暂停或转交说明
- 把这个公共技能库工作区改造成消费者仓库

## 安装

安装 `skill-task-continuity` 时，请使用本仓库中的标准发布路径，并按你的工作流选择 release 或 ref。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-task-continuity 安装 skill-task-continuity。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-task-continuity 安装 skill-task-continuity，并使用 ref v0.6.1。`

关于下游启动流程和提示词措辞，可查看 [references/install-playbook.zh-CN.md](references/install-playbook.zh-CN.md)。

## 推荐的下游布局

```text
AGENTS.md
.agent-state/
  TASK_STATE.md
  HANDOFF.md
  DECISIONS.md
  RUN_LOG.md
```

`TASK_STATE.md` 与 `HANDOFF.md` 是从原子包复制过来的重复模板，目的是方便下游仓库一次性完成启动。
它们的真实来源和行为边界仍然属于对应的原子包。

## 常用路径

可以先从下面三条路径开始：

1. 为下游仓库启动 `AGENTS.md` 和 `.agent-state/` 模板。
2. 先读组合说明，再决定下一步该交给哪个原子包。
3. 只有在下游仓库确实需要时，才补充轻量的 repo-local wrapper。

启动脚本要求显式传入目标路径，并且会拒绝在这个公共技能库工作区内执行。
你可以先运行 `python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo --dry-run` 预览变更，再去掉 `--dry-run` 正式应用。

## 套件如何组合

在下游工作中，仍然直接调用原子技能：

- `Use $skill-context-keeper to refresh .agent-state/TASK_STATE.md before more implementation work.`
- `Use $skill-phase-gate for a preflight before this risky multi-file change.`
- `Use $skill-handoff-summary to write .agent-state/HANDOFF.md before we pause.`

推荐的长任务循环如下：

1. 恢复工作前先读取状态文件。
2. 当检查点本身有价值时，为重要改动加上 gate。
3. 完成有意义的工作后刷新任务状态。
4. 暂停或转交时写出 handoff。

仓库本地的 `.agents/skills/` 包装或示例是可选的。
如果使用，建议保持轻量，并继续回指原子技能，而不是自行替代它们。

## 文档

- 触发路由与包边界：`SKILL.md`
- 套件组合说明：[references/composition-guide.zh-CN.md](references/composition-guide.zh-CN.md)
- English composition guide: [references/composition-guide.md](references/composition-guide.md)
- 下游仓库启动流程：[references/install-playbook.zh-CN.md](references/install-playbook.zh-CN.md)
- English install playbook: [references/install-playbook.md](references/install-playbook.md)
- 启动脚本复制的下游模板：`assets/`
