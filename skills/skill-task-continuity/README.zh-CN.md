# skill-task-continuity

[English](README.md)

## Overview

`skill-task-continuity` 是长任务连续性套件的入口包。
它负责解释各个连续性包如何组合，并提供一个启动脚本，把下游仓库需要的模板复制进去。
它不会取代原子技能包。

## 包职责

- 解释 `skill-context-keeper`、`skill-phase-gate`、`skill-handoff-summary` 三个原子包如何组合
- 为下游仓库启动 `AGENTS.md` 与 `.agent-state/*.md` 等文件
- 在套件级请求中，把工作路由到真正拥有下一步动作的原子包
- 明确包边界：模板只服务于下游消费者仓库

## What It Is Not For

- 用来替代 `skill-context-keeper` 的普通状态刷新
- 用来替代 `skill-phase-gate` 的常规检查点
- 用来替代 `skill-handoff-summary` 的简单暂停或转交说明
- 把这个公共技能库工作区改造成消费者仓库

## Install

可通过本仓库中的标准发布路径安装 `skill-task-continuity`。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-task-continuity 安装 skill-task-continuity。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-task-continuity 安装 skill-task-continuity，并使用我指定的 release 或 ref。`

如果你想直接运行 `skill-installer`，可使用：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-task-continuity
```

固定到本次连续性套件计划发布版本：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-task-continuity \
  --ref v0.6.0
```

## 启动下游仓库

先用 dry run 预览即将写入的文件：

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo --dry-run
```

确认无误后再真正复制模板：

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo
```

只有在你明确要覆盖已有下游文件时，才使用 `--force`。
脚本要求显式传入 `--target`，并且会拒绝在这个公共技能库工作区内部执行启动。

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

## References

- `SKILL.md`：触发路由与包边界
- [references/composition-guide.zh-CN.md](references/composition-guide.zh-CN.md)：套件组合方式与原子技能调用措辞
- [references/install-playbook.zh-CN.md](references/install-playbook.zh-CN.md)：下游仓库启动流程
- `assets/`：仅供下游消费者复制使用的模板
