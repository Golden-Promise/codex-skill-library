# skill-phase-gate

[English](README.md)

## 概述

`skill-phase-gate` 用于在有分量的编码工作前后加入紧凑的 preflight / postflight 检查点。
如果“加一道检查点”这件事本身就有价值，就该用它。

## 30 秒快速开始

- 什么时候用：你马上要做高风险、多文件，或其他明显有分量的改动。
- 你会得到什么：一个紧凑的检查点，把范围、约束、验证方式和剩余风险说清楚。
- 典型产物：一个按 `assets/PREFLIGHT.template.md` 组织的 preflight 说明，以及一个按 `assets/POSTFLIGHT.template.md` 组织的 postflight 说明。

如果你想直接告诉 Codex 怎么做：

先这样对 Codex 说：

- `请用 skill-phase-gate 在这次高风险多文件修改前生成一个 preflight gate。`

## 安装

你可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-phase-gate 安装 skill-phase-gate。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-phase-gate 安装 skill-phase-gate，并使用 ref v0.6.1。`

如果你想看精确的 shell 命令，可以直接跳到后面的 [安装细节](#安装细节)。

## 会创建或更新什么文件？

这个包通常会创建或刷新一份 preflight 检查点说明、一份 postflight 检查点说明，或者两者都写。

它自带的两个模板就是最直接的起点：

- [assets/PREFLIGHT.template.md](assets/PREFLIGHT.template.md)
- [assets/POSTFLIGHT.template.md](assets/POSTFLIGHT.template.md)

## 不适合什么时候用

- 这次改动只是一个琐碎的一行编辑
- 这次工作只是纯解释、纯说明
- 当前真正的问题是任务状态过旧，而不是检查点缺失
- 你需要的是暂停或转交 handoff，而不是流程检查点

这个包不适合 trivial one-line edits，也不适合 pure explanation tasks。

## 相关技能

- `skill-context-keeper`：适合在重要工作前后重建任务状态
- `skill-handoff-summary`：适合暂停或转交时写 handoff
- `skill-task-continuity`：适合第一次搭建整套流程和做套件级路由

## 文档

- 触发路由与包边界：`SKILL.md`
- 参考索引：[references/README.zh-CN.md](references/README.zh-CN.md)
- 使用场景与触发示例：[references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English use cases: [references/use-cases.md](references/use-cases.md)
- 中文提示词模板：[references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- preflight 清单：[assets/PREFLIGHT.template.md](assets/PREFLIGHT.template.md)
- postflight 清单：[assets/POSTFLIGHT.template.md](assets/POSTFLIGHT.template.md)

## 安装细节

把 `/path/to/install-skill-from-github.py` 换成你本地 `skill-installer` 仓库里的实际脚本路径。

```bash
python3 /path/to/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-phase-gate \
  --ref v0.6.1
```
