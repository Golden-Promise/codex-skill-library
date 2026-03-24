# skill-governance

[English](README.md)

`skill-governance` 是一个面向任务的 Codex skill 资产治理工具。
它用来完成新增、启用、体检、修复、审计、补文档、升级和退役这些动作，并尽量把存放路径、项目暴露和平台状态这些底层细节藏起来。

## 最适合用来做什么

- 新增一个可复用共享 skill
- 接管一个已下载的本地 skill 包
- 把某个 skill 启用到一个项目里
- 在清理、重链、升级或发布前先做体检
- 执行安全自动修复
- 为 CI 或发布准备注册表、生命周期和依赖图

如果你不确定从哪里开始，优先用 `add`、`enable` 和 `doctor`。

## 安装

从当前仓库安装最新版：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-governance
```

固定安装当前发布版本：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-governance \
  --ref v0.3.0
```

在 Codex 里也可以直接这样说：

```text
请用 skill-installer 从 <owner>/codex-skill-library 的 skills/skill-governance 安装 skill-governance。
```

## 快速上手

新增一个可复用共享 skill：

```bash
python3 scripts/manage_skill.py \
  add demo-skill \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

把一个已下载的 skill 包接入某个项目：

```bash
python3 scripts/manage_skill.py \
  add <import-path> \
  --project <project-root>
```

把已有 skill 启用到项目：

```bash
python3 scripts/manage_skill.py \
  enable demo-skill \
  --project <project-root>
```

在改动前先做体检：

```bash
python3 scripts/manage_skill.py \
  doctor demo-skill \
  --project <project-root>
```

## 主要任务

| 任务 | 作用 |
| --- | --- |
| `add` | 新建 skill，或接管一个本地下载包 |
| `enable` | 把已有 skill 暴露给一个项目 |
| `doctor` | 做健康评分、重叠检测、影响分析和修复建议 |
| `repair` | 只执行当前 `safe_auto_fix` 队列 |
| `audit` | 为 CI 或发布落盘并校验注册表、生命周期和依赖图 |
| `document` | 默认补齐 `SKILL.md` 缺失章节；如需整篇重写，使用 `--overwrite-skill-md` |
| `upgrade` | 用本地来源包刷新一个受管 skill |
| `retire` | 移除一个项目暴露，但不删除 canonical skill |

## 工具会自动帮你判断什么

- 不带 `--project` 时，默认走共享库。
- 带 `--project` 时，`add` 默认更偏向项目内托管。
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
- 治理建议和动作建议
- `repair_plan`、`work_queue`、`batch_repair_preview`

`repair` 只会执行 `safe_auto_fix`，不会自动处理人工清理或治理评审项。

`audit` 会写入或校验：

- `.skill-platform/registry.json`
- `.skill-platform/dependency-graph.json`

## 可选仓库配置

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
