# Skill Workflow Manager 提示词速查

English version: [prompt-templates.en.md](prompt-templates.en.md)

当你已经知道工作流、只想直接复制请求时，使用这份文件。
如果你还需要先判断模式、查看 CLI 细节或理解取舍，请先看 [use-cases.zh-CN.md](use-cases.zh-CN.md)。

> 复制最接近的模板，再把尖括号里的占位符替换掉即可。

## 常用占位符

| 占位符 | 含义 |
| --- | --- |
| `<skill-name>` | skill 名称，例如 `git-commit-coach` |
| `<project-root>` | 目标项目根目录 |
| `<import-path>` | 待预检或接管的本地 skill 目录 |
| `<purpose>` | 目标 skill 的用途说明 |
| `<selected-skills>` | 要接入或保留的 skill 列表 |

## 共享 Skill 提示词

### 创建共享 Skill

```text
$skill-workflow-manager 在 $CODEX_HOME/skills 中创建或刷新 <skill-name> 这个共享 skill，用途是 <purpose>，最后校验。
```

### 接管到共享库

```text
$skill-workflow-manager 把 <import-path> 接管到共享库。如果没有特别说明，默认使用更安全的 copy 模式。
```

### 把共享 Skill 接入一个项目

```text
$skill-workflow-manager 把 <selected-skills> 接入 <project-root>，不要复制真实的共享 skill。
```

## 项目托管 Skill 提示词

### 创建项目托管 Skill

```text
$skill-workflow-manager 在 <project-root>/_skill-library 中创建或刷新 <skill-name> 这个项目托管 skill，并把它链接到同一项目。
```

### 接管到项目托管库

```text
$skill-workflow-manager 把 <import-path> 接管到 <project-root>/_skill-library，并把它链接到同一项目。
```

### 把独立下载包自举成项目托管布局

```text
$skill-workflow-manager 把当前这个单独下载的 skill 包转成项目托管布局。请自动推断 project root，创建 _skill-library 和 .agents/skills，并在最后校验结果。
```

## 诊断与安全

### 改动前体检

```text
$skill-workflow-manager 在改动前检查 <skill-name> 以及它在 <project-root> 里的项目链接。先告诉我结构问题、重复副本和损坏链接，再决定是否继续。
```

### 接管前预检下载包

```text
$skill-workflow-manager 先预检 <import-path>，先不要接管。告诉我结构是否完整、名称是否冲突，以及它更适合做共享 skill 还是项目托管 skill。
```

### 预演高风险操作

```text
$skill-workflow-manager 先预演这次操作，只告诉我会创建、更新、删除或重建哪些路径，不要真正执行。
```

## 清单与项目链接

### 列出共享库中的 Skill

```text
$skill-workflow-manager 列出共享库里现在有哪些 canonical skill。
```

### 列出项目链接

```text
$skill-workflow-manager 列出 <project-root> 当前接入了哪些 skill，并告诉我哪些是受管链接、坏链接或本地阻塞项。
```

### 从项目中移除一个链接

```text
$skill-workflow-manager 从 <project-root> 中移除 <skill-name> 的项目链接，但不要删除 canonical skill。
```

### 精确同步项目 Skill 集合

```text
$skill-workflow-manager 把 <project-root> 的项目 skill 精确同步为 <selected-skills>，多余的项目链接一并移除。
```
