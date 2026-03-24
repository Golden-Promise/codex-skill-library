# skill-workflow-manager

[English](README.md)

用“全局共享库优先”的方式维护 Codex skill：先把 canonical skill 放到 `$CODEX_HOME/skills`，再按需把它暴露给具体项目。

## 3 条主路径

- 在 `$CODEX_HOME/skills` 中创建或刷新一个共享 skill
- 把已下载的本地 skill 接入这个共享库
- 通过 `<project-root>/.agents/skills` 给项目接入共享 skill

## 进阶路径

- 想先体检再动手时，用 `--doctor` / `--check`
- 做发布检查或 CI 校验时，用 `--validate-only`
- 想先盘点现状时，用 `--list-library-skills` 或 `--list-project-skills`
- 只有在你明确要项目内托管时，才用 `--bootstrap-project-layout`

## 安装方式

从 `codex-skill-library` 安装最新版：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager
```

固定安装已发布的 `v0.2.0` 版本：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager \
  --ref v0.2.0
```

也可以直接使用 GitHub tree URL：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/codex-skill-library/tree/main/skills/skill-workflow-manager
```

如果通过 Codex 中的 `skill-installer` 技能安装，可以直接这样说：

- 如果你希望它能被 Codex 直接当作技能使用，可以说：`请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-workflow-manager 安装 skill-workflow-manager。`
- 如果要安装已发布版本，可以说：`请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-workflow-manager 安装 skill-workflow-manager，并使用 v0.2.0。`

如果你只是把它安装到其他目标目录做手动审阅或脚本执行，Codex 不会把那个目录自动当成运行时技能目录。要在 Codex 里直接使用，仍然建议安装到默认的 `$CODEX_HOME/skills`。

## 5 分钟上手

1. 先把 `skill-workflow-manager` 安装到默认的 Codex 共享库。
2. 在 `$CODEX_HOME/skills` 中创建或接管一个共享 skill。
3. 通过 `.agents/skills` 把这个共享 skill 接入一个项目。
4. 在清理、重链或发布前先跑一次 `--doctor`，确认当前 skill 状态正常。

## 平台提醒

项目接入依赖 symlink。若你在 Windows 或受限文件系统里创建链接失败，请先检查符号链接权限、开发者模式，以及目标文件系统是否支持 symlink。

## 可以直接这样对 Codex 说

- `用 $skill-workflow-manager 在共享库里创建或刷新 <skill-name>，并在最后校验。`
- `用 $skill-workflow-manager 把 <import-path> 接入共享库。`
- `用 $skill-workflow-manager 把 <skill-name> 接入 <project-root>。`
- `用 $skill-workflow-manager 在修改前检查 <skill-name>，并同时检查它在 <project-root> 里的项目链接。`

## 开始阅读

1. 先看主工作流说明 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。
2. 如果你是第一次使用，先走上面的“5 分钟上手”。
3. 如果你只想快速复制提示词，打开 [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)。
4. 只有在你明确希望 skill 跟项目一起托管时，才使用项目内自举。

## 常用命令

在共享库中创建或刷新一个 skill：

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

把一个已下载的本地 skill 接入共享库：

```bash
python3 scripts/manage_skill.py \
  --adopt <import-path>
```

把共享库中的现有 skill 接入项目：

```bash
python3 scripts/manage_skill.py \
  --project-root <project-root> \
  --project-skills demo-skill
```

在修改前检查一个 skill 及其项目链接：

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --project-root <project-root> \
  --doctor
```

无写入地校验当前包：

```bash
python3 scripts/manage_skill.py --validate-only
```

仅当你希望 skill 变成项目内托管结构时，再做项目自举：

```bash
python3 scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

以机器可读格式列出共享库中的 skill：

```bash
python3 scripts/manage_skill.py \
  --list-library-skills \
  --format json
```

## 包内结构

| 区域 | 作用 |
| --- | --- |
| `SKILL.md` | Codex 运行时入口 |
| `agents/openai.yaml` | 元数据和默认 prompt 配置 |
| `scripts/manage_skill.py` | 创建、接管、体检、链接、自举和校验流程的确定性 CLI |
| `references/` | 面向读者的工作流说明和提示词参考 |
| `docs/` | 面向维护者的发布说明 |
| `tests/` | 管理脚本的回归测试 |

## 阅读入口

- English workflow guide: [references/use-cases.md](references/use-cases.md)
- 中文工作流说明: [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)
- English prompt templates: [references/prompt-templates.en.md](references/prompt-templates.en.md)
- 中文提示词模板: [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)
- English publishing notes: [docs/publishing-with-skill-installer.md](docs/publishing-with-skill-installer.md)
- 中文发布说明: [docs/publishing-with-skill-installer.zh-CN.md](docs/publishing-with-skill-installer.zh-CN.md)

## 给维护者

- 仓库首页: [../../README.zh-CN.md](../../README.zh-CN.md)
- 仓库发布说明: [../../docs/publishing.zh-CN.md](../../docs/publishing.zh-CN.md)
- 发布前执行：

```bash
python3 scripts/manage_skill.py --validate-only
python3 -m unittest discover -s tests -p 'test_*.py' -v
```
