# skill-governance 任务说明

English version: [use-cases.md](use-cases.md)

如果你只想快速找到常用命令模式，读这一页就够了。

## 一句话理解

- `add`：新增或接管一个 skill
- `enable`：把 skill 启用到一个项目
- `doctor`：检查健康度和治理状态
- `repair`：只执行安全自动修复
- `audit`：为 CI 写入或校验平台状态
- `document`：补齐 `SKILL.md` 缺失章节
- `upgrade`：用本地包刷新已受管 skill
- `retire`：移除一个项目暴露

## 最常用流程

新增一个可复用共享 skill：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  add <skill-name> \
  --purpose "<purpose>"
```

把一个本地下载包接入某个项目：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  add <import-path> \
  --project <project-root>
```

把已有 skill 启用到项目：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  enable <skill-name> \
  --project <project-root>
```

在清理、重链或发布前做体检：

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

如需整篇重写 `SKILL.md`：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  document <skill-name> \
  --library-root <library-root> \
  --overwrite-skill-md
```

落盘或校验平台状态：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  audit \
  --workspace-root <workspace-root> \
  --sync-platform-state
```

## 工具会自动判断什么

- 不带 `--project`：默认走共享库。
- 带 `--project`：`add` 默认更偏向项目内托管。
- `auto` 暴露模式会在 CI 中选 `manifest`，在 Windows 上选 `copy`，在 Linux/macOS 上选 `symlink`。
- 对 `enable`、`doctor`、`repair`、`retire`，工具可以从当前目录自动推断项目根目录。
- 对 `document`，默认保留已有章节，只补齐缺失内容；只有显式传 `--overwrite-skill-md` 才整篇重写。

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

- [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)：可直接复制的中文提示词
- [prompt-templates.en.md](prompt-templates.en.md)：English prompt templates
