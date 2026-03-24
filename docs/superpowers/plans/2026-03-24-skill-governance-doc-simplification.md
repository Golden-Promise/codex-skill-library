# Skill Governance Documentation Simplification Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Simplify `skill-governance` so the runtime skill entry is discovery-first, the README is human-first, and prompt templates use plain user language instead of internal governance terminology.

**Architecture:** Keep `SKILL.md` minimal and trigger-oriented, move human guidance into the package README, and keep command-line detail in the reference guides. No behavior changes are planned in `manage_skill.py`; this is a documentation and positioning cleanup.

**Tech Stack:** Markdown docs, YAML frontmatter, existing `manage_skill.py --validate-only`, existing unittest suite

---

### Task 1: Simplify The Runtime Skill Entry

**Files:**
- Modify: `skills/skill-governance/SKILL.md`
- Reference: `skills/skill-governance/README.md`
- Reference: `skills/skill-governance/references/use-cases.md`

- [ ] **Step 1: Rewrite the frontmatter description as trigger-only discovery text**

Replace the current description with a sentence that only answers when this skill should be loaded.

Target shape:

```yaml
description: Use when the user wants to take over skill management for a project, set up skill management for a project, or inspect, repair, audit, document, upgrade, or retire Codex skills.
```

- [ ] **Step 2: Reduce the body to runtime guidance only**

Keep only these sections:

- `# Skill Governance`
- `## Overview`
- `## Use This Skill When`
- `## Core Rules`
- `## References`

Remove the `## Core Commands` block entirely.

- [ ] **Step 3: Rephrase the rules around task choice instead of implementation detail**

Make sure the rules emphasize:

- prefer `manage` and `setup` for project onboarding
- prefer `doctor` before risky changes
- prefer `audit` for CI/release checks
- keep `document` as fill-missing-sections by default

Avoid wording about storage internals, exposure internals, or hidden mechanics unless strictly required.

- [ ] **Step 4: Verify the runtime entry stays short and discovery-friendly**

Run:

```bash
python3 - <<'PY'
from pathlib import Path
import yaml

path = Path("skills/skill-governance/SKILL.md")
text = path.read_text()
frontmatter = text.split("---", 2)[1]
data = yaml.safe_load(frontmatter)
print(len(data["description"]))
print(data["description"])
PY
```

Expected:

- description stays comfortably under 500 characters
- description starts with `Use when`
- description does not explain workflow or internal mechanics

Run:

```bash
rg -n "Core Commands|python3 <path-to-skill-governance>|storage paths from context|project exposure" \
  skills/skill-governance/SKILL.md
```

Expected: no matches

- [ ] **Step 5: Commit the runtime-entry cleanup**

```bash
git add skills/skill-governance/SKILL.md
git commit -m "docs: simplify skill-governance runtime entry"
```

### Task 2: Rewrite The README As The Human Entry Point

**Files:**
- Modify: `skills/skill-governance/README.md`
- Modify: `skills/skill-governance/README.zh-CN.md`
- Reference: `skills/skill-governance/references/use-cases.md`
- Reference: `skills/skill-governance/references/use-cases.zh-CN.md`

- [ ] **Step 1: Make natural-language installation the primary installation path**

Move the natural-language install request to the top of `## Install`.

Keep command-line install details secondary. Do not remove them completely, but stop making them the first thing a new reader sees.

Target English emphasis:

```text
Use skill-installer to install skill-governance from Golden-Promise/codex-skill-library at skills/skill-governance.
```

Target Chinese emphasis:

```text
请用 skill-installer 从 Golden-Promise/codex-skill-library 的 skills/skill-governance 安装 skill-governance。
```

- [ ] **Step 2: Rewrite Quick Start around the two onboarding requests**

Make the first screen focus on these two actions:

- take over skill management for an existing project
- set up a clean project skill-management skeleton

Keep the wording natural and user-facing. Do not lead with command names or internal terms.

- [ ] **Step 3: Keep the rest of the README outcome-oriented**

Review `## What It Is Best For`, `## Main Tasks`, and `## What The Tool Decides Automatically` so they explain outcomes in plain language.

Keep these ideas:

- what the tool is good at
- what tasks exist
- what decisions the tool makes automatically

But remove unnecessary wording that sounds like internal platform implementation.

- [ ] **Step 4: Keep CLI-heavy detail out of the first screen**

Leave command patterns in `references/use-cases*.md`.

In the README, point command-oriented readers to the task guide instead of repeating detailed CLI blocks.

- [ ] **Step 5: Verify the English and Chinese README structure stays aligned**

Run:

```bash
rg -n "^## " \
  skills/skill-governance/README.md \
  skills/skill-governance/README.zh-CN.md
```

Expected:

- both READMEs keep the same major section order
- both READMEs still include install, quick start, main tasks, automatic decisions, governance output, optional config, and read more

- [ ] **Step 6: Commit the README rewrite**

```bash
git add \
  skills/skill-governance/README.md \
  skills/skill-governance/README.zh-CN.md
git commit -m "docs: rewrite skill-governance readme for human-first onboarding"
```

### Task 3: Rewrite Prompt Templates In Plain User Language

**Files:**
- Modify: `skills/skill-governance/references/prompt-templates.en.md`
- Modify: `skills/skill-governance/references/prompt-templates.zh-CN.md`

- [ ] **Step 1: Rewrite prompt headings to sound like user intents**

Prefer headings such as:

- take over skill management for a project
- set up skill management for a project
- add a reusable skill
- bring a local skill package into a project
- check a project before cleanup or relinking
- repair safe issues across a workspace

- [ ] **Step 2: Rewrite each template so it reads like something a user would actually say**

Avoid terms such as:

- `managed project structure`
- `canonical skill`
- `storage`
- `exposure`

Prefer phrases such as:

- `organize the skills in this project`
- `set up skill management for this project`
- `bring this downloaded skill into the project`
- `remove this skill from the project without deleting the shared copy`

- [ ] **Step 3: Keep the templates short enough to be copy-ready**

Each prompt should stay one sentence whenever possible.

The template set should remain scannable and not repeat README explanation.

- [ ] **Step 4: Verify internal jargon is gone from the template pages**

Run:

```bash
rg -n "canonical|managed structure|storage|exposure" \
  skills/skill-governance/references/prompt-templates.en.md \
  skills/skill-governance/references/prompt-templates.zh-CN.md
```

Expected: no matches

- [ ] **Step 5: Commit the prompt-template rewrite**

```bash
git add \
  skills/skill-governance/references/prompt-templates.en.md \
  skills/skill-governance/references/prompt-templates.zh-CN.md
git commit -m "docs: rewrite skill-governance prompt templates in plain language"
```

### Task 4: Final Cross-Document Validation

**Files:**
- Review: `skills/skill-governance/SKILL.md`
- Review: `skills/skill-governance/README.md`
- Review: `skills/skill-governance/README.zh-CN.md`
- Review: `skills/skill-governance/references/prompt-templates.en.md`
- Review: `skills/skill-governance/references/prompt-templates.zh-CN.md`
- Test: `skills/skill-governance/tests/test_manage_skill.py`

- [ ] **Step 1: Read the docs in final user order**

Review them in this order:

1. `SKILL.md`
2. `README.md`
3. `README.zh-CN.md`
4. `references/prompt-templates.en.md`
5. `references/prompt-templates.zh-CN.md`

Confirm the reading flow is:

- runtime discovery
- human onboarding
- copy-ready task prompts

- [ ] **Step 2: Run the package validator**

```bash
python3 skills/skill-governance/scripts/manage_skill.py --validate-only
```

Expected: pass

- [ ] **Step 3: Run the regression suite**

```bash
python3 -m unittest discover \
  -s skills/skill-governance/tests \
  -p 'test_*.py'
```

Expected: all tests pass

- [ ] **Step 4: Apply any final wording alignment fixes from validation review**

If any wording inconsistency or leftover jargon is still visible after the read-through, fix it before the final commit.

- [ ] **Step 5: Commit the final doc polish**

```bash
git add \
  skills/skill-governance/SKILL.md \
  skills/skill-governance/README.md \
  skills/skill-governance/README.zh-CN.md \
  skills/skill-governance/references/prompt-templates.en.md \
  skills/skill-governance/references/prompt-templates.zh-CN.md
git commit -m "docs: align skill-governance onboarding language"
```
