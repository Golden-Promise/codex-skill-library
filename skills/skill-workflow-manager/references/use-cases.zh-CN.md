# Skill Workflow Manager 使用场景

English version: [use-cases.md](use-cases.md)

这份文件是 `skill-workflow-manager` 的主参考文档。
阅读方式也很明确：先选模式，再在该模式里选择具体操作。

## 开始阅读

- `skill-workflow-manager` 明确支持两种模式：共享 skill 和项目托管 skill。
- 如果你已经知道工作流、只想直接复制请求，打开 [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)。
- 如果你还不确定该选哪种模式，先看下面的模式选择器。
- 如果你需要给 CI 或自动化脚本使用，只读模式都可以追加 `--format json`。

## 模式选择器

| 模式 | 什么时候选它 | canonical 位置 | 常见后续动作 |
| --- | --- | --- | --- |
| 共享 skill | 这个 skill 需要跨项目复用 | `$CODEX_HOME/skills/<skill-name>` | 按需链接到一个或多个项目 |
| 项目托管 skill | 这个 skill 是私有的、需要版本固定，或应随单个仓库一起演进 | `<project-root>/_skill-library/<skill-name>` | 在同一项目内部链接和使用 |

## 最常见路径

| 目标 | 最推荐的第一步 | 常见命令 |
| --- | --- | --- |
| 创建可复用的共享 skill | 共享创建 | `<skill-name> --purpose "<purpose>"` |
| 创建项目专属 skill | 项目托管创建 | `<skill-name> --library-root <project-root>/_skill-library --project-root <project-root>` |
| 把下载包接入共享库 | 共享接管 | `--adopt <import-path>` |
| 把下载包接入项目托管库 | 项目托管接管 | `--adopt <import-path> --library-root <project-root>/_skill-library --project-root <project-root>` |
| 把已有共享 skill 暴露给某个项目 | 项目链接 | `--project-skills ... --project-root <project-root>` |
| 在改动前检查 skill 或项目链接 | 体检 | `--doctor` |

## 通用占位符

| 占位符 | 含义 |
| --- | --- |
| `<skill-dir>` | 当前 skill 包所在目录 |
| `<skill-name>` | canonical 的连字符命名 skill 名称 |
| `<library-root>` | 当前选择的 canonical skill 库根目录 |
| `<project-root>` | 目标项目根目录 |
| `<import-path>` | 当前所选库之外、待接管的本地 skill 目录 |
| `<purpose>` | 目标 skill 的 frontmatter `description` |

## 工作规则

- 先选模式，不要把共享流程和项目托管流程混在一起。
- 如果 skill 需要跨项目复用，优先选择共享模式。
- 如果 skill 应该私有化、固定在项目内，或随仓库一起演进，优先选择项目托管模式。
- 高风险改动前，优先使用 `--inspect-import`、`--doctor` 或 `--dry-run`。
- 默认使用 `copy` 导入；只有当接管后的副本要成为唯一正式来源时才使用 `move`。
- `.agents/skills` 负责暴露 skill，不负责定义 canonical 来源。

## 1. 创建或刷新共享 Skill

适用场景：

- skill 应该住在 `$CODEX_HOME/skills`
- 用户希望这一份 canonical skill 能跨项目复用

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --purpose "<purpose>"
```

补充说明：

- 这是可复用 skill 的默认模式。
- 只有当同一请求还要顺手保证项目链接存在时，才加 `--project-root`。
- 只有在用户明确要求时，才加 `--overwrite-skill-md` 或 `--overwrite-openai`。

## 2. 创建或刷新项目托管 Skill

适用场景：

- skill 应该留在某个项目内
- 这个项目需要拥有 canonical 副本

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --library-root <project-root>/_skill-library \
  --project-root <project-root> \
  --purpose "<purpose>"
```

补充说明：

- 这会把 canonical 副本创建在项目内，而不是 `$CODEX_HOME/skills`。
- 项目发现链接仍然通过 `.agents/skills` 来维护。
- 适合私有 skill、项目专属 skill，或需要随仓库一起演进的 skill。

## 3. 把下载包接入共享库

适用场景：

- 用户已经有一个共享库之外的本地 skill 目录
- 共享库需要成为这个 skill 的 canonical 来源

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --adopt <import-path>
```

补充说明：

- 这是“把已下载 skill 接入共享库”的默认路径。
- `--import-path <import-path>` 仍然可用，它是 `--adopt <import-path>` 的显式等价写法。
- 只有当同一请求还要顺手把该 skill 接入某个项目时，才额外加 `--project-root`。

## 4. 把下载包接入项目托管库

适用场景：

- 用户已经有一个目标项目之外的本地 skill 目录
- 这个项目需要拥有 canonical 副本

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --adopt <import-path> \
  --library-root <project-root>/_skill-library \
  --project-root <project-root>
```

补充说明：

- 这是共享接管流程在项目托管模式下的等价版本。
- 当项目需要 vendored skill，而不是依赖全局共享副本时，使用它。
- 如果名称冲突，用显式位置参数 `<skill-name>` 重试。

## 5. 接管前预检下载包

适用场景：

- 用户想先检查结构、元信息和重名情况
- 用户还不确定最终应该接入共享库还是项目托管库

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --inspect-import \
  --adopt <import-path>
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --inspect-import \
  --adopt <import-path> \
  --project-root <project-root>
```

补充说明：

- 这是面对陌生下载包时最安全的第一步。
- 预检会告诉你结构是否有效、canonical 名称是否冲突。

## 6. 接入或修复项目链接

适用场景：

- canonical skill 已存在
- 项目需要发现一个或多个 skill，但不想复制它们
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
- 这条路径同时适用于共享 skill 和项目托管 skill，只要 `library-root` 选对即可。

## 7. 移除或精确同步项目链接

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

## 8. 在改动前体检一个 Skill

适用场景：

- 用户想先确认某个 skill 结构是否健康，再决定是否编辑、接管或链接
- 用户想检查某个项目链接是否缺失、损坏、被阻塞，或指向错误

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --doctor
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  <skill-name> \
  --project-root <project-root> \
  --doctor
```

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --adopt <import-path> \
  --doctor
```

补充说明：

- `--doctor` 是回答“这个 skill 现在健康吗、能正常被发现吗？”的最快只读入口。
- 它支持 `--format json`，适合自动化。
- 发现阻塞问题时会返回非零退出码。

## 9. 把独立下载包自举为项目受管布局

适用场景：

- 当前目录是一个独立下载的 skill 包
- 最终目标应该是项目托管布局

命令模式：

```bash
python3 <skill-dir>/scripts/manage_skill.py \
  --bootstrap-project-layout \
  --project-root <project-root>
```

补充说明：

- 这不是创建共享 skill 的默认方式。
- 这是把独立下载包转成项目托管布局的桥接动作。
- 当自举接管项目内的独立下载包时，脚本会在校验通过后清理原始来源目录，避免项目里同时保留两份副本。

## 10. 盘点已有 Skill

适用场景：

- 用户想查看当前已有的 canonical skill
- 用户想在清理或修复前审计某个项目当前接入了哪些 skill

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

- 新项目接入 skill 前，可以先看共享库清单。
- 清理、修复或精确同步之前，可以先看项目清单。

## 11. 无写入地校验

适用场景：

- 你想做发布前检查，或在 CI 里跑结构校验
- 你想校验当前包、某个 canonical skill，或某个待接管目录，而且不希望写入任何内容

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
  --adopt <import-path> \
  --validate-only
```

补充说明：

- 不指定目标时，脚本会校验包含 `manage_skill.py` 的当前包。
- 指定 `<skill-name>` 时，脚本会校验 `<library-root>/<skill-name>` 下的 canonical skill。
- 指定 `--adopt` 或 `--import-path` 时，脚本会直接校验该目录。
