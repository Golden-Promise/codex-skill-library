# skill-governance prompt templates

Chinese version: [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)

Use these short prompts when you already know the task.

## Core Prompts

### Take over skill management for one project

```text
$skill-governance Take over skill management for <project-root>, inspect the directory, discover local skills, and organize them into the managed project structure.
```

### Set up a project management skeleton

```text
$skill-governance Set up skill governance for <project-root> and create the project management skeleton.
```

### Add a shared skill

```text
$skill-governance Add <skill-name> as a reusable shared skill. Use it for <purpose>.
```

### Adopt a local package into one project

```text
$skill-governance Add <import-path> for <project-root> and choose the right storage and exposure automatically.
```

### Enable a skill for a project

```text
$skill-governance Enable <skill-name> for <project-root>.
```

### Run health checks before changes

```text
$skill-governance Run doctor for <skill-name> in <project-root> before I clean up, relink, or release it.
```

### Repair safe issues

```text
$skill-governance Repair <skill-name> across <workspace-root>, but only run safe automatic fixes.
```

### Refresh missing SKILL.md sections

```text
$skill-governance Document <skill-name> and fill the missing SKILL.md sections without overwriting the sections that already exist.
```

### Audit platform state

```text
$skill-governance Audit the skill platform state for <workspace-root> and sync the registry and dependency graph first.
```

### Retire a project exposure

```text
$skill-governance Retire <skill-name> from <project-root> without deleting the canonical skill.
```
