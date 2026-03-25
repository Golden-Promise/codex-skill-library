# skill-handoff-summary

[English](README.md)

## Overview

`skill-handoff-summary` 是一个边界明确的包，用于在长时间编码任务需要暂停或转交时，生成面向续做的简洁交接摘要。
它把状态、阻塞点、需保留的硬约束，以及“下一步到底做什么”整理成可直接接手的材料，避免下一位执行者从零翻线程历史。
它面向诸如 `.agent-state/HANDOFF.md` 这样的紧凑交接产物，而不是整项目文档。

## Best For

- 一次工作结束时还有未完成事项，需要先暂停
- 把任务交给另一位执行者，并提供可信的重启说明
- 在上下文继续变旧之前，先记录阻塞点、已做决定和下一步动作
- 降低长线程在交接后的恢复成本

## What It Is Not For

- 在继续工作前重建当前任务状态
- 决定一个任务是否需要分阶段或检查点
- 以套件级工作流统筹多个原子包
- 维护覆盖整个任务的长期状态
- 生成整项目说明或仓库导览
- 在根本不需要交接时替代最终用户答复

## Package Boundary

当工作即将暂停，或者任务要换人接手，而下一次会话需要一个快速可复用的重启说明时，就使用这个包。
输出应保持紧凑、面向续做、且拿来就能行动。

这个包只负责交接摘要本身：

- 写入或刷新诸如 `.agent-state/HANDOFF.md` 的紧凑产物
- 保留任务摘要、当前状态、硬约束、开放问题，以及精确的下一步动作
- 给下一次会话附上一段可直接复用的 resume prompt

这个包不拥有长期状态，不拥有工作流门控，也不应膨胀成整项目文档包。

## Install

可通过本仓库中的标准发布路径安装 `skill-handoff-summary`。

你也可以直接这样对 Codex 说：

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-handoff-summary 安装 skill-handoff-summary。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-handoff-summary 安装 skill-handoff-summary，并使用我指定的 release 或 ref。`

如果你想直接运行 `skill-installer`，可使用：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-handoff-summary
```

固定到本次连续性套件计划发布版本：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-handoff-summary \
  --ref v0.6.0
```

## How To Use

当执行即将暂停，或者任务要移交给另一个负责人时，就使用这个包。
说明当前状态、未解决问题、阻塞点、硬约束，以及最先要做的下一步，让它输出一个简洁、面向续做的交接摘要，而不是重新规划整个流程。
如果你希望落到具体文件上，可以明确写出，例如：`把交接写到 .agent-state/HANDOFF.md，并在结尾附上下一次会话可直接复用的 resume prompt。`

## References

- `SKILL.md`：触发路由与包边界
- [references/README.zh-CN.md](references/README.zh-CN.md)：面向读者的参考索引
- [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)：适用与不适用触发示例
- [references/use-cases.md](references/use-cases.md)：英文触发示例
- [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)：可复用的中文交接与续做提示词
- [references/prompt-templates.en.md](references/prompt-templates.en.md)：可复用的英文交接与续做提示词
- [assets/HANDOFF.template.md](assets/HANDOFF.template.md)：紧凑交接模板
