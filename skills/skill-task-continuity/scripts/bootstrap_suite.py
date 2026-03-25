#!/usr/bin/env python3

import argparse
import shutil
import sys
from pathlib import Path


PACKAGE_ROOT = Path(__file__).resolve().parents[1]
LIBRARY_ROOT = PACKAGE_ROOT.parents[1]
TEMPLATE_MAP = {
    "AGENTS.md": "assets/AGENTS.repo-template.md",
    ".agent-state/TASK_STATE.md": "assets/agent-state/TASK_STATE.template.md",
    ".agent-state/HANDOFF.md": "assets/agent-state/HANDOFF.template.md",
    ".agent-state/DECISIONS.md": "assets/agent-state/DECISIONS.template.md",
    ".agent-state/RUN_LOG.md": "assets/agent-state/RUN_LOG.template.md",
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Copy long-task continuity starter files into a downstream repository."
    )
    parser.add_argument(
        "--target",
        required=True,
        help="Path to the downstream repository root that should receive the templates.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing downstream files instead of preserving them.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print the operations without writing files.",
    )
    return parser.parse_args()


def is_within(path, root):
    try:
        path.relative_to(root)
        return True
    except ValueError:
        return False


def validate_target(target):
    if is_within(target, LIBRARY_ROOT):
        raise ValueError(
            "Refusing to bootstrap inside the public skill library. "
            "Choose a downstream repository outside this checkout."
        )


def iter_operations(target, force):
    for destination_rel, source_rel in TEMPLATE_MAP.items():
        source = PACKAGE_ROOT / source_rel
        destination = target / destination_rel
        action = "overwrite" if destination.exists() and force else "skip" if destination.exists() else "create"
        yield action, source, destination


def apply_operations(target, force, dry_run):
    validate_target(target)
    created = 0
    overwritten = 0
    skipped = 0

    for action, source, destination in iter_operations(target, force):
        if action == "skip":
            skipped += 1
            print(f"[skip] {destination}")
            continue

        if action == "create":
            created += 1
        else:
            overwritten += 1

        verb = "would copy" if dry_run else "copy"
        print(f"[{action}] {verb} {source} -> {destination}")
        if dry_run:
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, destination)

    print(
        f"Summary: {created} create, {overwritten} overwrite, {skipped} skip"
        + (" (dry-run)" if dry_run else "")
    )


def main():
    args = parse_args()
    target = Path(args.target).expanduser().resolve()

    try:
        apply_operations(target=target, force=args.force, dry_run=args.dry_run)
    except ValueError as error:
        print(f"error: {error}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
