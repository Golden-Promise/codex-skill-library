# skill-workflow-manager

[English](README.md)

`skill-workflow-manager` 是一个面向 Codex skill 生命周期的管理器。它现在的产品定位是明确的：

- 管理放在 `$CODEX_HOME/skills` 中的共享 skill
- 管理放在 `<project-root>/_skill-library` 中的项目托管 skill
- 在独立下载包、共享库和项目内受管布局之间做干净的迁移与接管

它不只是共享库工具，也不只是项目自举工具，而是连接这两种模型的桥梁。

## 产品定位

当你希望用一个 skill 同时处理下面这些事情时，就适合使用它：

- 维护可跨项目复用的共享 skill
- 维护应随单个仓库一起演进的私有或项目专属 skill
- 把已下载 skill 接管到一个受管位置
- 通过 `.agents/skills` 维护项目发现链接
- 在高风险清理、修复或发布前做体检与校验

## 先选模式

| 模式 | 适合场景 | canonical 位置 | 项目暴露方式 |
| --- | --- | --- | --- |
| 共享 skill | 这个 skill 需要跨项目复用 | `$CODEX_HOME/skills/<skill-name>` | 按需链接到 `<project-root>/.agents/skills/<skill-name>` |
| 项目托管 skill | 这个 skill 是私有的、需要版本固定，或应随项目一起演进 | `<project-root>/_skill-library/<skill-name>` | 链接到同一项目的 `.agents/skills/<skill-name>` |

如果你拿不准，优先从共享模式开始。只有当 skill 明确应该跟某个仓库绑定时，再使用项目托管模式。

## 这个包可以做什么

- 创建新的共享 skill
- 创建新的项目托管 skill
- 把已下载的本地 skill 接管到共享库
- 把已下载的本地 skill 接管到项目托管库
- 把共享 skill 接入项目，而不复制真实 skill
- 把独立下载包自举为项目内受管布局
- 在清理、重链或发布前检查重复副本、坏链接、缺失文件和结构问题

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

- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-workflow-manager 安装 skill-workflow-manager。`
- `请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-workflow-manager 安装 skill-workflow-manager，并使用 v0.2.0。`

如果你希望直接作为运行时 skill 使用，最推荐的目标位置仍然是默认的 `$CODEX_HOME/skills`。

## 快速上手

### 共享 Skill 路径

1. 先把 `skill-workflow-manager` 安装到默认的 Codex 共享库。
2. 在 `$CODEX_HOME/skills` 中创建或接管一个共享 skill。
3. 只有当某个项目需要本地发现时，再把它链接到该项目。
4. 在清理、重链或发布前先跑一次 `--doctor`，确认当前 skill 状态正常。

### 项目托管 Skill 路径

1. 先确定哪个项目应该拥有这个 skill。
2. 在 `<project-root>/_skill-library` 中创建或接管这个 skill。
3. 通过同一项目的 `.agents/skills` 暴露它。
4. 只有在你要把独立下载包转成项目受管布局时，才使用 bootstrap。

## 可以直接这样对 Codex 说

- `用 $skill-workflow-manager 在 $CODEX_HOME/skills 中创建或刷新 <skill-name> 这个共享 skill，并在最后校验。`
- `用 $skill-workflow-manager 在 <project-root>/_skill-library 中创建 <skill-name> 这个项目托管 skill，并把它链接到该项目。`
- `用 $skill-workflow-manager 把 <import-path> 接管到共享库。`
- `用 $skill-workflow-manager 把 <import-path> 接管到 <project-root>/_skill-library，并把它链接到该项目。`
- `用 $skill-workflow-manager 把 <skill-name> 接入 <project-root>，不要复制真实 skill。`
- `用 $skill-workflow-manager 在改动前检查 <skill-name>，并同时检查它在 <project-root> 里的项目链接。`

## 常用命令

在共享库中创建或刷新一个 skill：

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

在项目托管库中创建或刷新一个 skill：

```bash
python3 scripts/manage_skill.py \
  demo-skill \
  --library-root <project-root>/_skill-library \
  --project-root <project-root> \
  --purpose "Use this skill when the user wants help with demo-skill tasks."
```

把一个已下载的本地 skill 接管到共享库：

```bash
python3 scripts/manage_skill.py \
  --adopt <import-path>
```

把一个已下载的本地 skill 接管到项目托管库：

```bash
python3 scripts/manage_skill.py \
  --adopt <import-path> \
  --library-root <project-root>/_skill-library \
  --project-root <project-root>
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

把独立下载包自举为项目受管布局：

```bash
python3 scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

无写入地校验当前包：

```bash
python3 scripts/manage_skill.py --validate-only
```

## 平台提醒

项目接入依赖 symlink。若你在 Windows 或受限文件系统里创建链接失败，请先检查符号链接权限、开发者模式，以及目标文件系统是否支持 symlink。

## 包内结构

| 区域 | 作用 |
| --- | --- |
| `SKILL.md` | Codex 运行时入口 |
| `agents/openai.yaml` | 元数据和默认 prompt 配置 |
| `scripts/manage_skill.py` | 覆盖共享模式和项目托管模式的确定性 CLI |
| `references/` | 面向读者的工作流说明和提示词参考 |
| `docs/` | 面向维护者的发布说明 |
| `tests/` | 管理脚本的回归测试 |

## 开始阅读

1. 先看主工作流说明 [references/use-cases.zh-CN.md](references/use-cases.zh-CN.md)。
2. 先选模式：共享 skill 还是项目托管 skill。
3. 如果你只想快速复制提示词，打开 [references/prompt-templates.zh-CN.md](references/prompt-templates.zh-CN.md)。
4. 只有在你要把独立下载包转成项目受管布局时，才使用 bootstrap。

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
