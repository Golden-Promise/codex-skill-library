# skill-governance 提示词模板

English version: [prompt-templates.en.md](prompt-templates.en.md)

把下面这些请求直接贴到 Codex 里，就能让 `skill-governance` 帮你完成工作。

## 从这里开始

如果你刚开始用，先试这两个：

```text
$skill-governance 接管 <project-root> 的 skill 管理，并帮我整理好本地 skill。
```

```text
$skill-governance 给 <project-root> 搭建 skill 管理骨架。
```

```text
$skill-governance 在我清理、重链或发布之前，先检查这个项目。
```

## 常用请求

```text
$skill-governance 新增 <skill-name> 这个可复用 skill，用途是 <purpose>。
```

```text
$skill-governance 把 <import-path> 接到 <project-root>，并把它整理成适合这个项目的形式。
```

```text
$skill-governance 让 <skill-name> 在 <project-root> 里可用。
```

```text
$skill-governance 在我清理、重链或发布之前，先检查 <project-root> 里的 <skill-name>。
```

```text
$skill-governance 在 <workspace-root> 范围内修复 <skill-name> 的安全问题。
```

```text
$skill-governance 为 <skill-name> 补齐 SKILL.md 缺失章节，不要覆盖已经存在的章节。
```

```text
$skill-governance 为 <workspace-root> 做一次 skill governance 审计，并先同步注册表和依赖图。
```

```text
$skill-governance 从 <project-root> 里移除 <skill-name>，但不要删除共享副本。
```
