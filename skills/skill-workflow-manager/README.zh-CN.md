# skill-workflow-manager

[English](README.md)

用“全局共享库优先”的方式维护 Codex skill：默认以 `$CODEX_HOME/skills` 为共享库，再按需把 skill 暴露给具体项目。

## 这个包可以帮你做什么

- 在默认 Codex 共享库中创建或刷新 canonical skill 包
- 把已下载的本地 skill 导入该共享库
- 给项目接入、移除或同步 skill 链接
- 仅在你明确需要项目内托管时，为项目自举可管理的本地 skill 结构，并避免遗留重复来源目录
- 把暂存的 skill 包注册到运行时技能目录，供 Codex 直接发现
- 在不写入文件的前提下校验现有 skill 包

## 适合什么场景

如果你希望某个 skill 以 `$CODEX_HOME/skills` 作为权威共享来源，同时又希望多个项目按需通过轻量链接发现和使用它，这个包会很合适。

## 推荐模型

建议按两层来使用：

- 默认共享库：把 canonical skill 放在 `$CODEX_HOME/skills`
- 可选项目链接：通过 `<project-root>/.agents/skills` 暴露给具体项目
- 项目内自举：只有当你明确希望 skill 随项目一起托管时，才使用 `<project-root>/_skill-library`

## 安装方式

从 `codex-skill-library` 安装最新版：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager
```

固定安装已发布的 `v0.1.1` 版本：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo <owner>/codex-skill-library \
  --path skills/skill-workflow-manager \
  --ref v0.1.1
```

也可以直接使用 GitHub tree URL：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --url https://github.com/<owner>/codex-skill-library/tree/main/skills/skill-workflow-manager
```

如果通过 Codex 中的 `skill-installer` 技能安装，可以直接这样说：

- 如果你希望它能被 Codex 直接当作技能使用，可以说：`请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-workflow-manager 安装 skill-workflow-manager。`
- 如果要安装已发布版本，可以说：`请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-workflow-manager 安装 skill-workflow-manager，并使用 v0.1.1。`
- 如果只是想先安装到其他目录暂存或审阅，可以说：`请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-workflow-manager 安装 skill-workflow-manager，并安装到 <目标根目录>。`
- 更准确地说，`<目标根目录>` 会作为安装根，暂存后的目录会是 `<目标根目录>/skill-workflow-manager`。
- 但这种“安装到其他目录”的方式不会自动让 Codex 发现这个技能。若要把它作为技能使用，请安装到 `$CODEX_HOME/skills`，或者把 `<目标根目录>/skill-workflow-manager` 链接到 `$CODEX_HOME/skills/skill-workflow-manager` 或 `<project-root>/.agents/skills/skill-workflow-manager`。

如果已经暂存到其他目录，想让 Codex 直接发现它，可以继续执行：

```bash
python3 <目标根目录>/skill-workflow-manager/scripts/manage_skill.py \
  --register-runtime-skill
```

## 开始阅读

1. 先看主工作流说明 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。
2. 默认优先使用 `$CODEX_HOME/skills` 这条全局共享库路径。
3. 如果你只想快速复制提示词，打开 [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)。
4. 只有在你明确希望 skill 跟项目一起托管时，才使用项目内自举。

## 常用命令

在共享库中创建或刷新一个 skill：

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

把一个已下载的本地 skill 导入共享库：

```bash
python3 scripts/manage_skill.py \
  --import-path <import-path>
```

把共享库中的现有 skill 接入项目：

```bash
python3 scripts/manage_skill.py \
  --project-root <project-root> \
  --project-skills demo-skill
```

无写入地校验当前包：

```bash
python3 scripts/manage_skill.py --validate-only
```

把当前包注册到运行时技能目录：

```bash
python3 scripts/manage_skill.py --register-runtime-skill
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
| `scripts/manage_skill.py` | 创建、导入、链接和校验流程的确定性 CLI |
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
