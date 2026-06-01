---
description: Resume from an Overton snapshot — load a handoff file and pick up the work where it left off.
argument-hint: "[blank = list snapshots to choose from] [path or filename substring to load directly] [latest = newest, no prompt]"
---

Resume work from an Overton snapshot. Raw argument: $ARGUMENTS

This command is convenience sugar — a snapshot is plain Markdown, so anyone can resume without this
plugin by just reading the file. Follow these steps:

### 1. Choose the snapshot
Build a candidate list of `*.md` from these locations, **newest first across all of them**:
`./.claude/handoffs/`, `./docs/handoffs/`, `~/.claude/snapshots/` (skip any that don't exist).

Interpret `$ARGUMENTS`:
- **Looks like a path** (contains `/`, ends in `.md`, or starts with `~`) → load that exact file. If it doesn't exist, say so and stop.
- **`latest`** → load the single most-recent candidate without asking.
- **Any other text** → treat it as a **filename substring** and match against candidates: exactly one match → load it; several → show the numbered list (below); none → say so and stop.
- **Empty** →
  - **exactly one** candidate → load it (announce which).
  - **more than one** → **do NOT auto-pick the newest.** Show a numbered list, newest first:
    `N.  YYYY-MM-DD · <scenario> · <title>   (<location>)`
    reading `scenario`/`title` from each file's frontmatter. Then **stop and ask** the user to reply
    with a number (or a path/substring). Load whichever they choose.

Cap the list at the ~10 most recent and note if older ones were omitted. If no candidates exist anywhere, tell the user and stop.

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
