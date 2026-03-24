# skill-governance prompt templates

Chinese version: [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)

Use these short prompts when you already know the task.

## Core Prompts

### Take over skill management for one project

```text
$skill-governance Take over skill management for <project-root>, review the directory, find any local skills, and organize them for me.
```

### Set up a project management skeleton

```text
$skill-governance Set up skill governance for <project-root>.
```

### Add a shared skill

```text
$skill-governance Add <skill-name> as a reusable skill. Use it for <purpose>.
```

### Bring a local package into one project

```text
$skill-governance Bring <import-path> into <project-root> and organize it as part of this project's skill management.
```

### Enable a skill for a project

```text
$skill-governance Make <skill-name> available in <project-root>.
```

### Check a project before changes

```text
$skill-governance Check <skill-name> in <project-root> before I clean up, relink, or release skills.
```

### Repair safe issues across a workspace

```text
$skill-governance Fix the safe skill issues for <skill-name> across <workspace-root>.
```

### Refresh missing SKILL.md sections

```text
$skill-governance Document <skill-name> and fill the missing SKILL.md sections without overwriting the sections that already exist.
```

### Audit platform state

```text
$skill-governance Run a skill governance audit for <workspace-root> and sync the registry and dependency graph first.
```

### Remove a skill from one project

```text
$skill-governance Remove <skill-name> from <project-root> without deleting the shared copy.
```
