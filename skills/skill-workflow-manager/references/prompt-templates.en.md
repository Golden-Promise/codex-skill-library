# Skill Workflow Manager Prompt Cheat Sheet

Chinese version: [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)

Use this file when you already know the workflow and only need copy-ready prompts.
For mode selection, CLI details, and tradeoffs, read [use-cases.md](use-cases.md).

> Copy the closest prompt, then replace the angle-bracket slots.

## Fill-In Slots

| Slot | Meaning |
| --- | --- |
| `<skill-name>` | A skill name such as `git-commit-coach` |
| `<project-root>` | The target project root |
| `<import-path>` | The local skill directory to inspect or adopt |
| `<purpose>` | The target skill purpose description |
| `<selected-skills>` | The skills to attach or keep |

## Shared Skill Prompts

### Create A Shared Skill

```text
$skill-workflow-manager Create or refresh <skill-name> as a shared skill in $CODEX_HOME/skills, use it for <purpose>, and validate it at the end.
```

### Adopt Into The Shared Library

```text
$skill-workflow-manager Adopt <import-path> into the shared library. Use the safer copy mode unless I say otherwise.
```

### Attach A Shared Skill To One Project

```text
$skill-workflow-manager Attach <selected-skills> to <project-root> without copying the real shared skills.
```

## Project-Managed Skill Prompts

### Create A Project-Managed Skill

```text
$skill-workflow-manager Create or refresh <skill-name> as a project-managed skill inside <project-root>/_skill-library, then link it to that same project.
```

### Adopt Into A Project-Managed Library

```text
$skill-workflow-manager Adopt <import-path> into <project-root>/_skill-library and link it to that same project.
```

### Bootstrap A Standalone Package Into A Project-Managed Layout

```text
$skill-workflow-manager Turn this standalone downloaded skill package into a project-managed layout. Infer the project root, create _skill-library and .agents/skills, and validate the result at the end.
```

## Diagnostics And Safety

### Check Before Changing Anything

```text
$skill-workflow-manager Check <skill-name> and its project link in <project-root> before making changes. Tell me about structural issues, duplicate copies, and broken links first.
```

### Inspect A Downloaded Skill Before Adoption

```text
$skill-workflow-manager Inspect <import-path> first. Do not adopt it yet. Tell me whether the structure is complete, whether the name conflicts, and whether it fits better as a shared skill or a project-managed skill.
```

### Preview A Risky Operation

```text
$skill-workflow-manager Preview this operation first. Only tell me which paths would be created, updated, removed, or relinked. Do not execute it.
```

## Inventory And Project Links

### List Shared Skills

```text
$skill-workflow-manager List the canonical skills in the shared library.
```

### List Project Links

```text
$skill-workflow-manager List the skills attached to <project-root> and tell me which ones are managed links, broken links, or local blockers.
```

### Remove One Project Link

```text
$skill-workflow-manager Remove the project link for <skill-name> from <project-root>, but do not delete the canonical skill.
```

### Exact-Sync A Project

```text
$skill-workflow-manager Sync the project skills in <project-root> to exactly <selected-skills> and remove any extra project links.
```
