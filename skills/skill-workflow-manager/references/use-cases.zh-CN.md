# Skill Workflow Manager 使用场景

English version: [use-cases.md](use-cases.md)

这份文件是 `skill-workflow-manager` 的主参考文档。
适合用来学习工作流、判断应该使用哪种模式，以及查找对应的 CLI 用法。

## 开始阅读

- 如果你已经知道工作流，只想直接复制请求，打开 [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)。
- 如果你还在判断该用哪种操作，先看下面的决策图。
- 如果你需要给 CI 或自动化脚本使用，只读模式都可以追加 `--format json`。

## 决策图

| 目标 | 使用模式 | 核心参数 |
| --- | --- | --- |
| 创建或刷新一个受管 skill | 创建 / 更新 | `<skill-name> --project-root <project-root> --purpose "<purpose>"` |
| 先预览风险改动 | 预演 | `--dry-run` |
| 查看当前已有内容 | 清单 | `--list-library-skills` 或 `--list-project-skills` |
| 给项目接入 skill 或修复链接 | 项目链接 | `--project-skills ...` 或 `<skill-name> --project-root ...` |
| 移除或精确同步项目链接 | 项目清理 | `--unlink-skills ...` 或 `--sync-project-skills ...` |
| 导入前检查本地 skill | 导入预检 | `--inspect-import --import-path <import-path>` |
| 接管一个已下载的本地 skill | 导入 | `--import-path <import-path>` |
| 将独立下载包转为受管布局 | 自举 | `--bootstrap-project-layout` |
| 无写入地校验现有 skill | 校验 | `--validate-only` |

## 通用占位符

| 占位符 | 含义 |
| --- | --- |
| `<skill-dir>` | 当前 skill 包所在目录 |
| `<skill-name>` | canonical 的连字符命名 skill 名称 |
| `<project-root>` | 目标项目根目录 |
| `<import-path>` | 共享库之外、待导入的本地 skill 目录 |
| `<purpose>` | 目标 skill 的 frontmatter `description` |

## 工作规则

- 用户要编辑某一个 canonical skill 时，用创建或更新模式。
- 用户只想查看共享库或项目当前挂载情况时，用清单模式。
- skill 已存在，只想调整项目接入关系时，用项目链接模式。
- 导入陌生的本地 skill 前，优先使用 `--inspect-import`。
- 默认使用 `copy` 导入；只有当共享库副本要成为唯一正式来源时才使用 `move`。

## 1. 创建或刷新受管 Skill

适用场景：

- 用户要创建一个新的 canonical skill
- 用户要更新元信息，或重生成默认文件

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --project-root <project-root> \
  --purpose "<purpose>"
```

补充说明：

- 只有在用户明确要求重写主模板时，才加 `--overwrite-skill-md`。
- 只有在需要重生成 `agents/openai.yaml` 时，才加 `--overwrite-openai`。
- 如果你想直接复制请求措辞，去看 [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)。

## 2. 预演高风险改动

适用场景：

- 操作涉及删除、同步、重建链接或导入
- 用户希望先看会改哪些文件和路径

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --project-root <project-root> \
  --purpose "<purpose>" \
  --dry-run
```

补充说明：

- 大范围项目清理或陌生导入前，优先先跑 `--dry-run`。
- 如果你想直接复制请求措辞，去看 [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)。

## 3. 列出共享库或项目中的 Skill

适用场景：

- 用户想看共享库里已经有哪些 canonical skill
- 用户想审计某个项目当前接入了哪些 skill

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --list-library-skills
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --project-root <project-root> \
  --list-project-skills
```

补充说明：

- 给新项目接入 skill 之前，可以先看共享库清单。
- 做清理、修复或精确同步之前，可以先看项目清单。

## 4. 接入或修复项目链接

适用场景：

- canonical skill 已存在
- 项目需要发现一个或多个现有 skill，而不是复制它们
- 某个项目链接丢失、失效或指向错误

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --project-root <project-root> \
  --project-skills skill-workflow-manager,linux-command-coach
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --project-root <project-root>
```

补充说明：

- 接入多个现有 skill 时，用 `--project-skills`。
- 主要目标是刷新单个 canonical skill 并确保项目链接存在时，用 `<skill-name> --project-root ...`。

## 5. 移除或精确同步项目链接

适用场景：

- 用户想把一个或多个 skill 从项目里摘掉
- 用户希望项目链接集合与指定列表完全一致

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --project-root <project-root> \
  --unlink-skills linux-command-coach
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --project-root <project-root> \
  --sync-project-skills skill-workflow-manager,git-commit-coach
```

补充说明：

- `--unlink-skills` 只移除指定项目链接，不删除 canonical skill。
- `--sync-project-skills` 更强，会让项目链接集合与目标列表完全一致。

## 6. 导入前预检已下载 Skill

适用场景：

- 用户想先检查结构、元信息和冲突情况
- 用户不确定该使用 `copy` 还是 `move`

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --inspect-import \
  --import-path <import-path> \
  --project-root <project-root>
```

补充说明：

- 这是面对陌生下载包时最安全的第一步。
- 如果来源名称冲突，脚本会给出可用的 canonical 名称建议。

## 7. 将已下载 Skill 导入共享库

适用场景：

- 用户已经有一个位于共享库之外的本地 skill 目录
- 共享库需要成为这个 skill 的 canonical 来源

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --import-path <import-path> \
  --project-root <project-root>
```

补充说明：

- 只有在原下载目录不再需要保留时，才使用 `--import-mode move`。
- 如果导入名冲突，用显式位置参数 `<skill-name>` 重试。
- 当导入源位于项目根目录之外时，脚本会把来源记录到 `.agents/skill-workflow-manager/external-sources.json`。

## 8. 将独立下载包自举为受管项目结构

适用场景：

- 当前目录是一个独立下载的 skill 包
- 项目还没有 `_skill-library` 和 `.agents/skills`

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

补充说明：

- 如果脚本能安全推断项目根目录，可以省略 `--project-root`。
- 这是把独立下载包接回共享库工作流的桥接方式。

## 9. 无写入地校验现有 Skill

适用场景：

- 你想做发布前检查，或在 CI 里跑结构校验
- 你想校验当前包、某个 canonical skill，或某个待导入目录，而且不希望写入任何内容

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --validate-only
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --library-root <library-root> \
  --validate-only
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --import-path <import-path> \
  --validate-only
```

补充说明：

- 不指定目标时，脚本会校验包含 `manage_skill.py` 的当前包。
- 指定 `<skill-name>` 时，脚本会校验 `<library-root>/<skill-name>` 下的 canonical skill。
- 指定 `--import-path` 时，脚本会直接校验该目录。
