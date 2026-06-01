---
description: Capture an Overton Context Window snapshot — a scenario-aware, structured handoff a fresh agent can resume from.
argument-hint: "[1-9 template | blank=auto] [--here to save into this repo for a committed handoff] [focus instructions] — 1=coding 2=planning 3=debugging 4=research 5=strategy 6=meeting 7=creative 8=multimedia 9=general"
---

Read `~/.claude/skills/overton-snapshot/SKILL.md` (or `${CLAUDE_PLUGIN_ROOT}/skills/overton-snapshot/SKILL.md` if installed as a plugin) and follow it exactly.

Raw arguments: $ARGUMENTS

Parse them per SKILL.md **Step 0**:
- If the FIRST token is a digit `1`–`9` → that digit selects the template.
- A `--here` (or `--repo`) token anywhere → write the snapshot **into the current repo** for a committed handoff (Step 4), using **repo-relative paths**. Without it, save to the global `~/.claude/snapshots/`.
- Everything left over → **focus instructions**.

Before you write anything, announce: (a) the chosen template + a one-line rationale, (b) the focus instructions you will honor (or "none"), and (c) the destination (global archive vs this repo). Then proceed through Steps 1–4.
