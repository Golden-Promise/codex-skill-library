# Skill Workflow Manager Prompt Cheat Sheet

Chinese version: [prompt-templates.zh-CN.md](prompt-templates.zh-CN.md)

Use this file when you already know the workflow and only need copy-ready prompts.
For workflow selection, CLI details, and tradeoffs, read [use-cases.md](use-cases.md).

> Copy the closest prompt, then replace the angle-bracket slots.

## Fill-In Slots

| Slot | Meaning |
| --- | --- |
| `<skill-name>` | A skill name such as `git-commit-coach` |
| `<project-root>` | The target project root |
| `<import-path>` | The local skill directory to inspect or adopt |
| `<purpose>` | The target skill purpose description |
| `<selected-skills>` | The skills to attach or keep |

## Core Tasks

### Create

```text
$skill-workflow-manager Create <skill-name> in the shared Codex library, use it for <purpose>, and validate it at the end.
```

### Update

```text
$skill-workflow-manager Update <skill-name>, add <the content to change>, keep the current structure, and validate it at the end.
```

### Adopt

```text
$skill-workflow-manager Adopt <import-path> into the shared Codex library. Use the safer copy mode unless I say otherwise.
```

### Attach

```text
$skill-workflow-manager Attach <selected-skills> to <project-root>. Only add the skills I named.
```

## Advanced Tasks

### Check

```text
$skill-workflow-manager Check <skill-name> in the shared library and also inspect its project link in <project-root> before making changes.
```

### Preview

```text
$skill-workflow-manager Preview this operation first. Only tell me which paths would be created, updated, removed, or relinked. Do not execute it.
```

## Inventory And Project Links

### List Library Skills

```text
$skill-workflow-manager List the canonical skills in the shared library.
```

### List Project Skills

```text
$skill-workflow-manager List the skills attached to <project-root> and tell me which ones are managed shared-library links.
```

### Remove One Project Skill

```text
$skill-workflow-manager Remove the project link for <skill-name> from <project-root>, but do not delete the real skill from the shared library.
```

### Exact-Sync A Project

```text
$skill-workflow-manager Sync the project skills in <project-root> to exactly <selected-skills> and remove any extra project links.
```

### Repair One Project Link

```text
$skill-workflow-manager Rebuild the project discovery link for <skill-name> in <project-root> so it points back to the canonical skill.
```

## Adoption And Bootstrap

### Inspect An Adoption Candidate

```text
$skill-workflow-manager Inspect <import-path> first. Do not adopt it yet. Tell me whether the structure is complete, whether the name conflicts, and which import mode you recommend.
```

If you are already in the target project directory:

```text
$skill-workflow-manager I am already in the target project directory. Adopt <import-path> into the managed layout for this project without asking me for project-root again.
```

### Bootstrap A Standalone Skill Package

```text
$skill-workflow-manager Turn this standalone downloaded skill package into a project-local managed layout. Infer the project root, create _skill-library and .agents/skills, and validate the result at the end.
```
