---
description: Capture an Overton Context Window snapshot — a scenario-aware, structured handoff a fresh agent can resume from.
argument-hint: "[1-9 template | blank=auto] [optional focus instructions] — 1=coding 2=planning 3=debugging 4=research 5=strategy 6=meeting 7=creative 8=multimedia 9=general"
---

Read `~/.claude/skills/overton-snapshot/SKILL.md` and follow it exactly.

Raw arguments: $ARGUMENTS

Parse them per SKILL.md **Step 0**:
- If the FIRST token is a digit `1`–`9` → that digit selects the template; everything after it is **focus instructions**.
- Otherwise → auto-detect the template, and treat the ENTIRE argument string as **focus instructions** (if any).

Before you write anything, announce: (a) the chosen template + a one-line rationale, and (b) the focus instructions you will honor (or "none"). Then proceed through Steps 1–4.
