# skill-governance 命令参考

English version: [use-cases.md](use-cases.md)

这一页是 `skill-governance` 的命令与进阶用法参考。这里记录安装命令、子命令、命令模式、自动决策、治理校验和仓库配置。

README 提供落地页概览。

## 安装命令

安装当前仓库里的最新版：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance
```

安装指定发布版本：

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path skills/skill-governance \
  --ref v0.6.1
```

## 命令总览

- `manage`：检查项目目录，发现本地 skill，并纳入 `skill-governance`
- `setup`：创建治理所需的项目目录
- `add`：新建一个 skill，或导入一个本地包
- `enable`：让一个受管 skill 在某个项目里可用
- `doctor`：在清理、重链、升级或发布前检查健康度和重叠情况
- `repair`：只执行安全自动修复
- `audit`：为 CI 或发布校验注册表和依赖图
- `document`：补齐 `SKILL.md` 缺失章节；如需整篇重写，使用 `--overwrite-skill-md`
- `upgrade`：用本地来源包刷新一个受管 skill
- `retire`：把一个 skill 从某个项目里移除，但不删除共享副本

## 命令模式

接管一个项目目录的 skill 管理：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  manage <project-root>
```

为 skill governance 搭建项目管理目录：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  setup <project-root>
```

新增一个可复用共享 skill：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  add <skill-name> \
  --purpose "<purpose>"
```

把一个本地包接入某个项目：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  add <import-path> \
  --project <project-root>
```

把已有 skill 让某个项目可用：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  enable <skill-name> \
  --project <project-root>
```

在清理、重链或发布前检查一个 skill：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  doctor <skill-name> \
  --project <project-root>
```

执行安全自动修复：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  repair <skill-name> \
  --workspace-root <workspace-root>
```

用本地来源包刷新一个受管 skill：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  upgrade <import-path> \
  --library-root <library-root>
```

把一个 skill 从某个项目里移除，但不删除共享副本：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  retire <skill-name> \
  --project-root <project-root>
```

补齐 `SKILL.md` 缺失章节：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  document <skill-name> \
  --library-root <library-root>
```

整篇重写 `SKILL.md`：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  document <skill-name> \
  --library-root <library-root> \
  --overwrite-skill-md
```

写入或校验平台状态：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  audit \
  --workspace-root <workspace-root> \
  --sync-platform-state
```

## 自动决策

- `manage` 会找到本地 skill 包，并自动整理好。
- `setup` 会创建项目 skill 目录和治理状态目录。
- 不带 `--project` 时，`add` 默认使用共享库。
- 带 `--project` 时，`add` 会把 skill 留在这个项目里。
- `auto` 模式会在 CI 中选 `manifest`，在 Windows 上选 `copy`，在 Linux 或 macOS 上选 `symlink`。
- `enable`、`doctor`、`repair`、`retire` 可以从当前工作目录推断项目根目录。
- `document` 会保留已有章节，除非你显式要求 `--overwrite-skill-md`。

## 治理输出与校验

`doctor` 会输出：

- 健康分和质量维度
- 相似或重叠的 skill
- 受影响项目和 workspace 引用图
- 治理建议和下一步动作
- `repair_plan`、`work_queue`、`batch_repair_preview`

`repair` 只会执行 `safe_auto_fix`。

`audit` 会写入或校验：

- `.skill-platform/registry.json`
- `.skill-platform/dependency-graph.json`

`audit` 也会把治理元数据当作 CI 和发布门禁：

- `active`、`review`、`deprecated`、`blocked` 状态的 skill 应该有 `owner`
- `active`、`review`、`deprecated`、`blocked` 状态的 skill 应该有 semver 风格的 `version`
- `review` 状态的 skill 还应该有 `reviewer`
- `active` 和 `review` 状态的 skill 通常也应该有 `team`

示例：

```bash
python3 scripts/manage_skill.py \
  add demo-skill \
  --purpose "Use this skill when the user wants help with demo skill tasks." \
  --owner "platform@example.com" \
  --team "core-platform" \
  --version "1.2.0"
```

## 仓库配置

如果你想自定义路径，可以使用 `skill-governance.toml`：

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

## 相关文档

- [README.zh-CN.md](../README.zh-CN.md)：概览
- [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)：提示词模板
- [prompt-templates.en.md](prompt-templates.en.md)：English prompt templates
