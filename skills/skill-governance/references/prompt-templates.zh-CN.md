# skill-governance 提示词模板

English version: [prompt-templates.en.md](prompt-templates.en.md)

当你已经知道任务，只想直接下达请求时，使用这里的短模板。

## 核心模板

### 新增一个共享 skill

```text
$skill-governance 新增 <skill-name> 这个可复用共享 skill，用途是 <purpose>。
```

### 把本地下载包接入某个项目

```text
$skill-governance 把 <import-path> 接入 <project-root>，并自动选择合适的存放位置和暴露方式。
```

### 把 skill 启用到项目

```text
$skill-governance 把 <skill-name> 启用到 <project-root>。
```

### 在改动前做体检

```text
$skill-governance 在清理、重链或发布前，为 <skill-name> 和 <project-root> 运行 doctor。
```

### 执行安全自动修复

```text
$skill-governance 在 <workspace-root> 范围内修复 <skill-name>，但只执行安全自动修复项。
```

### 补齐 SKILL.md 缺失章节

```text
$skill-governance 为 <skill-name> 补齐 SKILL.md 缺失章节，不要覆盖已经存在的章节内容。
```

### 审计平台状态

```text
$skill-governance 为 <workspace-root> 执行 audit，并先同步注册表和依赖图。
```

### 移除一个项目暴露

```text
$skill-governance 从 <project-root> 中 retire <skill-name>，但不要删除 canonical skill。
```
