# codex-skill-library

[English](README.md)

一个用于集中发布可安装 Codex skills 的仓库。

## 这个仓库适合谁

这个仓库主要面向以下人群：

- 想从一个统一入口安装和浏览 Codex skills 的使用者
- 想先阅读说明，再决定是否采用某个 skill 的读者
- 想维护一套规范、可发布、可持续演进 skill 集合的维护者

## 这里能找到什么

| 区域 | 作用 |
| --- | --- |
| `skills/` | 可单独安装的已发布 skill 包 |
| 包内 `README.md` | 某个 skill 最适合用户开始阅读的入口 |
| 包内 `references/` | 面向读者的示例、说明和双语参考资料 |
| 包内 `docs/` | 某些 skill 需要的维护者发布说明 |

## 当前可用 Skill

| Skill | 适用场景 | 文档 |
| --- | --- | --- |
| `skill-governance` | 用任务式入口治理 skill 资产，包括新增、启用、体检、修复、审计和补文档 | [EN](skills/skill-governance/README.md) / [中文](skills/skill-governance/README.zh-CN.md) |
| `skill-context-keeper` | 刷新并压缩可信的 root-task state | [EN](skills/skill-context-keeper/README.md) / [中文](skills/skill-context-keeper/README.zh-CN.md) |
| `skill-subtask-context` | 打开并维护有边界的 child-task state，避免 root summary 持续膨胀 | [EN](skills/skill-subtask-context/README.md) / [中文](skills/skill-subtask-context/README.zh-CN.md) |
| `skill-context-packet` | 为 root 或 subtask 工作写下一轮最小上下文 packet | [EN](skills/skill-context-packet/README.md) / [中文](skills/skill-context-packet/README.zh-CN.md) |
| `skill-phase-gate` | 在有分量的改动前后加入 preflight / postflight 检查点 | [EN](skills/skill-phase-gate/README.md) / [中文](skills/skill-phase-gate/README.zh-CN.md) |
| `skill-handoff-summary` | 在暂停或换人时生成紧凑、面向续做的交接摘要 | [EN](skills/skill-handoff-summary/README.md) / [中文](skills/skill-handoff-summary/README.zh-CN.md) |
| `skill-task-continuity` | 负责连续性套件的启动与组合，但不替代原子包 | [EN](skills/skill-task-continuity/README.md) / [中文](skills/skill-task-continuity/README.zh-CN.md) |

## 快速开始

1. 先看 [skills/README.zh-CN.md](skills/README.zh-CN.md) 浏览当前可用 skill。
2. 进入具体 skill 包的 `README.md` 了解它是否适合你的场景。
3. 按该包 README 中的安装说明安装目标包。
4. 如果你需要整套连续性流程的启动或组合说明，先从 `skill-task-continuity` 开始；如果下一步动作已经明确，也可以直接进入 `skill-context-keeper`、`skill-subtask-context`、`skill-context-packet`、`skill-phase-gate` 或 `skill-handoff-summary`。
5. 现在可先阅读该包下的参考页了解边界说明，后续阶段再继续使用其中补充的示例与提示词资料。

## 阅读入口

- English skill index: [skills/README.md](skills/README.md)
- 中文技能索引: [skills/README.zh-CN.md](skills/README.zh-CN.md)
- `skill-governance` 包说明: [EN](skills/skill-governance/README.md) / [中文](skills/skill-governance/README.zh-CN.md)
- `skill-context-keeper` 包说明: [EN](skills/skill-context-keeper/README.md) / [中文](skills/skill-context-keeper/README.zh-CN.md)
- `skill-subtask-context` 包说明: [EN](skills/skill-subtask-context/README.md) / [中文](skills/skill-subtask-context/README.zh-CN.md)
- `skill-context-packet` 包说明: [EN](skills/skill-context-packet/README.md) / [中文](skills/skill-context-packet/README.zh-CN.md)
- `skill-phase-gate` 包说明: [EN](skills/skill-phase-gate/README.md) / [中文](skills/skill-phase-gate/README.zh-CN.md)
- `skill-handoff-summary` 包说明: [EN](skills/skill-handoff-summary/README.md) / [中文](skills/skill-handoff-summary/README.zh-CN.md)
- `skill-task-continuity` 包说明: [EN](skills/skill-task-continuity/README.md) / [中文](skills/skill-task-continuity/README.zh-CN.md)
- English context protocol migration guide: [docs/context-protocol-migration.md](docs/context-protocol-migration.md)
- 中文迁移说明: [docs/context-protocol-migration.zh-CN.md](docs/context-protocol-migration.zh-CN.md)
- English continuity suite overview: [docs/long-task-suite.md](docs/long-task-suite.md)
- 中文连续性套件总览: [docs/long-task-suite.zh-CN.md](docs/long-task-suite.zh-CN.md)
- English publishing guide: [docs/publishing.md](docs/publishing.md)
- 中文发布说明: [docs/publishing.zh-CN.md](docs/publishing.zh-CN.md)
- English continuity-suite release checklist: [docs/release-checklist-long-task-suite.md](docs/release-checklist-long-task-suite.md)
- 中文连续性套件发布清单: [docs/release-checklist-long-task-suite.zh-CN.md](docs/release-checklist-long-task-suite.zh-CN.md)

## 仓库结构

```text
codex-skill-library/
  README.md
  README.zh-CN.md
  CHANGELOG.md
  docs/
  skills/
    README.md
    README.zh-CN.md
    skill-governance/
    skill-context-keeper/
    skill-subtask-context/
    skill-context-packet/
    skill-phase-gate/
    skill-handoff-summary/
    skill-task-continuity/
```

## 给维护者

仓库级的版本、发布流程和校验说明统一放在 [docs/publishing.zh-CN.md](docs/publishing.zh-CN.md)。
连续性套件发布清单在 [docs/release-checklist-long-task-suite.zh-CN.md](docs/release-checklist-long-task-suite.zh-CN.md)。
协议迁移和套件总览放在 [docs/context-protocol-migration.zh-CN.md](docs/context-protocol-migration.zh-CN.md) 与 [docs/long-task-suite.zh-CN.md](docs/long-task-suite.zh-CN.md)。
包级安装说明统一保留在各自 README 中。
如果你是第一次发布这个仓库，建议先看这些维护者文档，而不是直接从包内运行时说明开始。
