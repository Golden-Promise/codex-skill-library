# skill-governance 命令参考

English version: [use-cases.md](use-cases.md)

如果你要看命令语法和进阶用法，就读这一页。若你刚开始用，先看 [../README.zh-CN.md](../README.zh-CN.md) 和 [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)。

## 常用命令

- `manage`：检查项目目录，找到本地 skill，并交给 `skill-governance` 处理
- `setup`：创建 skill governance 需要的项目目录
- `add`：新建一个 skill，或接入一个本地包
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

## 工具会自动决定什么

- `manage` 会找到本地 skill 包，并自动整理好。
- `setup` 会创建项目 skill 目录和平台状态目录。
- 不带 `--project` 时，`add` 默认使用共享库。
- 带 `--project` 时，`add` 会把 skill 留在这个项目里。
- `auto` 模式会在 CI 中选 `manifest`，在 Windows 上选 `copy`，在 Linux/macOS 上选 `symlink`。
- `enable`、`doctor`、`repair`、`retire` 可以从当前工作目录推断项目根目录。
- `document` 会保留已有章节，除非你显式要求 `--overwrite-skill-md`。

## 可选仓库配置

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

## 相关文件

- [README.zh-CN.md](../README.zh-CN.md)：如果你刚开始用，先看这里
- [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)：可直接复制的请求
- [prompt-templates.en.md](prompt-templates.en.md)：English copy-ready requests
