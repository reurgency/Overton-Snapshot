---
description: Resume from an Overton snapshot — load a handoff file and pick up the work where it left off.
argument-hint: "[path to a snapshot .md | blank = newest handoff in this repo, else newest global snapshot]"
---

Resume work from an Overton snapshot. Raw argument: $ARGUMENTS

This command is convenience sugar — a snapshot is plain Markdown, so anyone can resume without this
plugin by just reading the file. Follow these steps:

### 1. Locate the snapshot
- If `$ARGUMENTS` is a non-empty path → use that file (expand a leading `~`). If it doesn't exist, say so and stop.
- Otherwise pick the **most recently modified** `*.md`, searching in this order and stopping at the first match:
  1. `./.claude/handoffs/`
  2. `./docs/handoffs/`
  3. `~/.claude/snapshots/`
  If a repo handoff and a global snapshot both exist, prefer the repo handoff but mention the global one if it's clearly newer. If nothing is found, tell the user and stop.

### 2. Read it fully
Read the entire file — frontmatter and body.

### 3. Sanity-check portability (cross-machine / cross-checkout handoffs)
- If the snapshot has a `repo_root:` and you're in a different repo, warn.
- If its `branch:` differs from the current git branch, note it (the teammate may need to check out that branch).
- Spot-check 1–2 referenced `path:line` files actually exist here. If they don't resolve, warn that the checkout/branch/repo may not match — don't silently proceed.

### 4. Restate what you loaded (concise)
Report back: the **scenario/template**, the **Primary Intent**, the **current state** (what's done / in-progress / broken), and the **Next Step quoted verbatim** from the snapshot. Keep it tight — this confirms you understood the handoff.

### 5. Confirm before acting
Ask the user whether to proceed with that next step, or wait for direction. Do **not** auto-execute changes — a resumed agent acting immediately is surprising. Once they confirm, continue the work from the snapshot's next step.
