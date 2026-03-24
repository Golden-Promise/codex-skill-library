# skill-governance 提示词模板

English version: [prompt-templates.en.md](prompt-templates.en.md)

当你已经知道任务，只想直接下达请求时，使用这里的短模板。

## 核心模板

### 接管一个项目目录的 skill 管理

```text
$skill-governance 接管 <project-root> 的 skill 管理，检查目录、找到本地 skill，并帮我整理好。
```

### 给项目搭建管理骨架

```text
$skill-governance 给 <project-root> 搭建 skill 管理骨架。
```

### 新增一个共享 skill

```text
$skill-governance 新增 <skill-name> 这个可复用 skill，用途是 <purpose>。
```

### 把本地下载包接入某个项目

```text
$skill-governance 把 <import-path> 接到 <project-root>，并把它整理进这个项目的 skill 管理里。
```

### 把 skill 启用到项目

```text
$skill-governance 让 <skill-name> 在 <project-root> 里可用。
```

### 在改动前做体检

```text
$skill-governance 在我清理、重链或发布 skill 之前，检查 <project-root> 里的 <skill-name>。
```

### 执行安全自动修复

```text
$skill-governance 在 <workspace-root> 范围内修复 <skill-name> 的安全问题。
```

### 补齐 SKILL.md 缺失章节

```text
$skill-governance 为 <skill-name> 补齐 SKILL.md 缺失章节，不要覆盖已经存在的章节内容。
```

### 审计平台状态

```text
$skill-governance 为 <workspace-root> 做一次 skill 治理审计，并先同步注册表和依赖图。
```

### 移除一个项目暴露

```text
$skill-governance 从 <project-root> 里移除 <skill-name>，但不要删除共享副本。
```
