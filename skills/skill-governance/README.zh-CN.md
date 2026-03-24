# skill-governance

[English](README.md)

## 它是什么

`skill-governance` 帮你更轻松地管理 Codex skill。
当你想接手已有项目、搭建干净的 skill 工作流、添加或启用 skill，或者在清理和发布前确认一切安全时，它都很适合。

## 最适合哪些场景

它特别适合这些场景：

- 接手一个已经有本地 skill 的项目
- 为新项目搭建 skill 治理流程
- 新增一个想长期复用的 skill
- 只在某个项目里启用一个 skill，而不是改动全部
- 在清理、重链、升级或发布前做一次检查
- 为 CI 或发布准备 skill 元数据

如果你刚开始用，先看 `manage`、`setup` 和 `doctor`。

## 安装

在 Codex 里，最自然的说法是直接请求：

“请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-governance 安装 skill-governance。”

如果你想固定到某个版本，也可以直接补一句版本号：

“请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-governance 安装 skill-governance，并使用 v0.5.0。”

如果你想看更精确的命令模式，请看 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。

## 快速上手

通常先做这三步：

1. 接管已有项目目录：`接管这个目录的 skill 管理，并把本地 skill 帮我整理好。`
2. 从零搭建项目：`给这个项目搭建 skill 管理骨架。`
3. 在清理或发布前检查：`在我清理或重链 skill 之前，先检查一下这个项目。`

## 接下来可以问什么

当基础流程准备好后，你可以继续让 `skill-governance` 帮你：

- 新增一个 skill
- 在某个项目里启用一个 skill
- 修复安全问题
- 审计注册表或依赖状态
- 为已有 skill 补文档
- 升级或退役一个 skill

如果你想看直接的命令模式和更多示例，请看 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。

## 主要任务

| 任务 | 作用 |
| --- | --- |
| `manage` | 审查一个项目目录，发现本地 skill 包，并把它们纳入受管的 skill 管理 |
| `setup` | 为一个项目搭建干净的 skill 管理骨架 |
| `add` | 新建 skill，或把一个本地下载包纳入管理 |
| `enable` | 让一个受管 skill 在某个项目里可用 |
| `doctor` | 做健康评分、重叠检测、影响分析和修复建议 |
| `repair` | 只执行当前 `safe_auto_fix` 队列 |
| `audit` | 为 CI 或发布落盘并校验注册表、生命周期和依赖图 |
| `document` | 默认补齐 `SKILL.md` 缺失章节；如需整篇重写，使用 `--overwrite-skill-md` |
| `upgrade` | 用本地来源包刷新一个受管 skill |
| `retire` | 把一个 skill 从某个项目里移除，但不删除共享副本 |

## 工具会自动帮你判断什么

- `manage` 会检查目标目录、发现本地 skill 包，并自动整理成项目内的受管结构。
- `setup` 会自动创建项目 skill 目录和治理状态目录。
- 不带 `--project` 时，新 skill 默认进入共享库。
- 带 `--project` 时，`add` 默认更偏向跟着项目走。
- `auto` 暴露策略当前会自动选择：
  - CI 中优先 `manifest`
  - Windows 上优先 `copy`
  - Linux 和 macOS 上优先 `symlink`
- 对 `enable`、`doctor`、`repair`、`retire`，如果你在目标项目目录里运行，工具可以自动推断项目根目录。
- 对 `document`，默认保留已有章节，只补齐缺失内容；只有你显式要求时才整篇重写。

## 治理输出

`doctor` 会输出：

- 健康分和质量维度
- 相似或重叠的 skill
- 受影响项目和 workspace 引用图
- 治理建议和下一步动作
- `repair_plan`、`work_queue`、`batch_repair_preview`

`repair` 只会执行 `safe_auto_fix`，不会自动处理人工清理或治理评审项。

`audit` 会写入或校验：

- `.skill-platform/registry.json`
- `.skill-platform/dependency-graph.json`

`audit` 现在也会把治理元数据当作 CI / 发布门禁：

- `active`、`review`、`deprecated`、`blocked` 状态的 skill 应该有 `owner`
- `active`、`review`、`deprecated`、`blocked` 状态的 skill 应该有 semver 风格的 `version`
- `review` 状态的 skill 还应该有 `reviewer`
- `active` 和 `review` 状态的 skill 通常也应该有 `team`

这些字段可以在 `add`、`enable`、`upgrade` 这类任务里顺手写入：

```bash
python3 scripts/manage_skill.py \
  add demo-skill \
  --purpose "Use this skill when the user wants help with demo skill tasks." \
  --owner "platform@example.com" \
  --team "core-platform" \
  --version "1.2.0"
```

## 高级设置

如果你想自定义共享库、项目库或暴露路径，可以在项目根目录放一份 `skill-governance.toml`：

```toml
[skill_registry]
shared_root = ".platform/skills/shared"
project_root = ".platform/skills/project"
exposure_root = ".agents/skills"
exposure_mode = "auto"
workspace_root = ".."
platform_root = ".skill-platform"
```

旧文件名 `skill-workflow.toml` 仍然兼容。

## 延伸阅读

- 任务说明: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English task guide: [references/use-cases.md](references/use-cases.md)
- 提示词模板: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 维护者发布说明: [docs/publishing-with-skill-installer.zh-CN.md](docs/publishing-with-skill-installer.zh-CN.md)
