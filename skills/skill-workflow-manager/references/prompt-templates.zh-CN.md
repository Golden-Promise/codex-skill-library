# Skill Workflow Manager 提示词速查

English version: [prompt-templates.en.md](prompt-templates.en.md)

当你已经知道工作流、只想直接复制请求时，使用这份文件。
如果你还需要判断该用哪种模式、查看 CLI 细节或理解取舍，请先看 [use-cases.zh-CN.md](use-cases.zh-CN.md)。

> 复制最接近的模板，再把尖括号里的占位符替换掉即可。

## 常用占位符

| 占位符 | 含义 |
| --- | --- |
| `<skill-name>` | skill 名称，例如 `git-commit-coach` |
| `<project-root>` | 目标项目根目录 |
| `<import-path>` | 待预检或接管的本地 skill 目录 |
| `<purpose>` | 目标 skill 的用途说明 |
| `<selected-skills>` | 要接入或保留的 skill 列表 |

## 核心任务

### 创建

```text
$skill-workflow-manager 在 Codex 共享库里创建 <skill-name>，用途是 <purpose>，最后校验。
```

### 更新

```text
$skill-workflow-manager 更新 <skill-name>，补充 <要新增或修改的内容>，保持现有结构不变，并在最后校验。
```

### 接管

```text
$skill-workflow-manager 把 <import-path> 接入 Codex 共享库。如果没有特别说明，默认使用更安全的 copy 模式。
```

### 接入项目

```text
$skill-workflow-manager 把 <selected-skills> 接入 <project-root>，只加入我指定的这些 skill。
```

## 进阶任务

### 体检

```text
$skill-workflow-manager 在修改前检查共享库里的 <skill-name>，并同时检查它在 <project-root> 里的项目链接。
```

### 预演

```text
$skill-workflow-manager 先预演这次操作，只告诉我会创建、更新、删除或重建哪些路径，不要真正执行。
```

## 清单与项目链接

### 列出共享库中的 Skill

```text
$skill-workflow-manager 列出共享库里现在有哪些 skill。
```

### 列出项目中的 Skill

```text
$skill-workflow-manager 列出 <project-root> 当前接入了哪些 skill，并告诉我哪些是共享库管理的链接。
```

### 从项目中移除一个 Skill

```text
$skill-workflow-manager 从 <project-root> 中移除 <skill-name> 的项目链接，但不要删除共享库里的真实 skill。
```

### 精确同步项目 Skill 集合

```text
$skill-workflow-manager 把 <project-root> 的项目 skill 精确同步为 <selected-skills>，多余的项目链接一并移除。
```

### 修复一个项目链接

```text
$skill-workflow-manager 重建 <project-root> 里 <skill-name> 的项目发现链接，让它重新指向 canonical skill。
```

## 接管与自举

### 接管前预检

```text
$skill-workflow-manager 先预检 <import-path>，不要接入，只告诉我结构是否完整、是否重名、推荐用什么方式导入。
```

如果你已经在目标项目目录里：

```text
$skill-workflow-manager 我现在就在目标项目目录。请把 <import-path> 接入当前项目的受管结构，不用我额外再写 project-root。
```

### 把独立下载包自举成受管项目

```text
$skill-workflow-manager 把当前这个单独下载的 skill 包初始化为项目内受管布局。请自动推断 project root，创建 _skill-library 和 .agents/skills，并在最后校验结果。
```
