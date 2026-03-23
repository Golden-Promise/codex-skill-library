# skill-workflow-manager

[English](README.md)

用共享库工作流维护 Codex skill：保持一个 canonical 来源，并按需把它安全地暴露给一个或多个项目。

## 这个包可以帮你做什么

- 创建或刷新 canonical skill 包
- 把已下载的本地 skill 导入受管共享库
- 给项目接入、移除或同步 skill 链接
- 为项目自举可管理的 skill 目录结构，并避免遗留重复的来源目录
- 把暂存的 skill 包注册到运行时技能目录，供 Codex 直接发现
- 在不写入文件的前提下校验现有 skill 包

## 适合什么场景

如果你希望某个 skill 只有一个权威来源，同时又希望多个项目都能通过轻量链接发现和使用它，这个包会很合适。

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
2. 如果你只想快速复制提示词，打开 [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)。
3. 如果你已经知道自己要用哪种模式，可以直接参考下面的常用命令。

## 常用命令

创建或刷新一个受管 skill：

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --project-root <project-root> \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

导入前检查一个已下载的本地 skill：

```bash
python3 scripts/manage_skill.py \
  --inspect-import \
  --import-path <import-path> \
  --project-root <project-root>
```

无写入地校验当前包：

```bash
python3 scripts/manage_skill.py --validate-only
```

把当前包注册到运行时技能目录：

```bash
python3 scripts/manage_skill.py --register-runtime-skill
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
