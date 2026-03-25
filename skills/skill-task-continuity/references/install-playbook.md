# Install Playbook

Use this playbook when a downstream repository wants the full long-task continuity suite starter kit.
The suite package only installs downstream-facing templates and docs.
It must not be pointed back at the public skill library root.

## What Gets Bootstrapped

The bootstrap helper copies these templates into the downstream repo:

- `AGENTS.md`
- `.agent-state/TASK_STATE.md`
- `.agent-state/HANDOFF.md`
- `.agent-state/DECISIONS.md`
- `.agent-state/RUN_LOG.md`

`TASK_STATE.md` and `HANDOFF.md` are duplicated from the atomic packages so consumers can bootstrap from one package while the atomic packages remain the source of truth.

## Bootstrap Walkthrough

1. Install either:
   - just `skill-task-continuity` if you only need the suite entry point first
   - the full long-task continuity suite if you want all four packages available immediately
2. Pick the downstream repository root you want to prepare.
3. Ask Codex directly when you want a natural-language bootstrap flow:

```text
Use skill-task-continuity to bootstrap the long-task continuity starter files into /path/to/downstream-repo.
Preview the file operations first, then apply them if the preview looks correct.
Do not overwrite existing files unless I explicitly ask.
```

4. If you want exact CLI control, preview the file operations:

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo --dry-run
```

5. Run the real bootstrap when the preview looks correct:

```bash
python3 skills/skill-task-continuity/scripts/bootstrap_suite.py --target /path/to/downstream-repo
```

6. Re-run with `--force` only when you intentionally want to overwrite an existing downstream file.

## Full-Suite Install In One Command

If you want all four continuity packages in one command, use the existing multi-path support in `skill-installer`:

```bash
python3 <path-to-skill-installer>/scripts/install-skill-from-github.py \
  --repo Golden-Promise/codex-skill-library \
  --path \
    skills/skill-context-keeper \
    skills/skill-phase-gate \
    skills/skill-handoff-summary \
    skills/skill-task-continuity
```

Add `--ref v0.6.1` when you want the pinned release.

## Expected Downstream Layout

```text
AGENTS.md
.agent-state/
  TASK_STATE.md
  HANDOFF.md
  DECISIONS.md
  RUN_LOG.md
```

The helper creates missing parent directories automatically.
Without `--force`, existing files are preserved.

## Recommended First Use

After bootstrapping:

1. Read `AGENTS.md` in the downstream repo.
2. Adjust repo-local wording only if your team needs thin wrappers or examples.
3. Start invoking the atomic skills directly for real work:
   - `skill-context-keeper` for state refresh
   - `skill-phase-gate` for meaningful checkpoints
   - `skill-handoff-summary` for pauses and transfers

## Optional Repo-Local Wrappers

If the downstream repo wants helper prompts, add them under `.agents/skills/`.
Keep them optional and lightweight.
They should point back to the atomic skills rather than copying their public docs into repo-specific forks.
