# skill-task-continuity

[English](README.md)

## 概述

`skill-task-continuity` 是长任务连续性套件面向新手的入口包。
如果你是第一次想在一个项目里搭好连续性工作流，就从这里开始。

## 30 秒快速开始

- 什么时候用：你想把连续性工作流装进一个仓库、理解整套工具链，或者判断下一步该用哪个连续性技能。
- 你会得到什么：一组下游启动文件、一个简单的长任务循环，以及通往三个原子技能的清晰入口。
- 典型产物：下游仓库里的 `AGENTS.md` 和 `.agent-state/` 启动文件。

如果你想直接告诉 Codex 怎么做：

先这样对 Codex 说：

- `请用 skill-task-continuity 把长任务连续性启动文件引导到 /path/to/downstream-repo。先预览文件操作，确认无误后再正式写入；除非我明确要求，否则不要覆盖已有文件。`

## 安装

对于第一次使用的人来说，最轻松的方式是直接用自然语言让 Codex 安装。

你可以先只安装这个入口包：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-task-continuity 安装 skill-task-continuity。`

你也可以让 Codex 直接安装整套工具链：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 一次安装整套长任务连续性工具链，包括 skills/skill-context-keeper、skills/skill-phase-gate、skills/skill-handoff-summary 和 skills/skill-task-continuity。`

安装 `skill-task-continuity` 本身不会自动把另外三个原子包一起装上。
如果你想一次拿到 4 个包，应该显式安装整套；你可以用上面的自然语言提示，也可以在后面的安装细节里用一条命令完成。

如果你想看精确的 shell 命令，可以直接跳到后面的 [安装细节](#安装细节)。

## 你的仓库里会创建什么

bootstrap helper 会为下游仓库准备这些启动文件：

- `AGENTS.md`
- `.agent-state/TASK_STATE.md`
- `.agent-state/HANDOFF.md`
- `.agent-state/DECISIONS.md`
- `.agent-state/RUN_LOG.md`

其中 `TASK_STATE.md` 和 `HANDOFF.md` 是从原子包模板复制来的便利副本，目的是让下游仓库更快起步。

## 最快的开始方式

安装之后，最快的起步路径是：

1. 让 Codex 把启动文件 bootstrap 到你的下游仓库。
2. 查看生成的 `AGENTS.md` 和 `.agent-state/` 文件。
3. 真正开始做任务时，直接调用拥有“下一步动作”的原子技能。

如果你想精确控制 CLI，也可以先运行 `python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo --dry-run` 预览，再去掉 `--dry-run` 正式应用。

## 下一步该用哪个技能

- 当任务还在继续，但状态图景已经变旧时，用 `skill-context-keeper`。
- 当下一步是高风险或多文件改动时，用 `skill-phase-gate`。
- 当你即将暂停或转交工作时，用 `skill-handoff-summary`。

## 不适合什么时候用

- 你只需要某一个原子技能来完成一个立即动作
- 你只需要刷新任务状态
- 你只需要给重要改动加一个检查点
- 你只需要写一份暂停或转交说明

这个包不会替代三个原子技能，也不会把这个公共技能库工作区变成消费者仓库。

## 相关技能

- `skill-context-keeper`：处理 `.agent-state/TASK_STATE.md`
- `skill-phase-gate`：处理 preflight / postflight 检查点
- `skill-handoff-summary`：处理 `.agent-state/HANDOFF.md`

## 文档

- 触发路由与包边界：`SKILL.md`
- 套件组合说明：[references/composition-guide.zh-CN.md](references/composition-guide.zh-CN.md)
- English composition guide: [references/composition-guide.md](references/composition-guide.md)
- 下游仓库启动流程：[references/install-playbook.zh-CN.md](references/install-playbook.zh-CN.md)
- English install playbook: [references/install-playbook.md](references/install-playbook.md)
- 启动脚本复制的下游模板：`assets/`

## 安装细节

把 `/path/to/install-skill-from-github.py` 换成你本地 `skill-installer` 仓库里的实际脚本路径。

只安装这个入口包：

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-task-continuity \
  --ref v0.6.1
```

用一条命令安装整套工具链：

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path \
    skills/skill-context-keeper \
    skills/skill-phase-gate \
    skills/skill-handoff-summary \
    skills/skill-task-continuity \
  --ref v0.6.1
```
