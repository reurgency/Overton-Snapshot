# Template 1 — Coding / Implementation

Use for a mid-build handoff. Fill the frontmatter (see FORMAT.md), then every section below.

```
---
id: <date>-overton-coding-<slug>
created: <ISO-8601>
scenario: coding
title: <short title>
project: <repo basename>
branch: <git branch>
session_id: <CLAUDE_SESSION_ID>
status: in-progress|blocked|complete
focus: <verbatim focus, omit if none>
tags: [<keywords>]
files: [<key paths touched>]
next_step: <one-line>
related: []
---
```

# <Title> — Overton Snapshot (Coding)

## Primary Intent
<What is being built and why. Front-loaded. Quote the user's explicit request.>

## User Constraints & Feedback (verbatim)
<Quote any "do this / don't do that", conventions, ports, security rules, corrections. _n/a_ if none.>

## Files & Changes
<For each file: `path:line` + what changed/why. New files, edits, and notable reads.>
- `path/to/file.ext:NN` — <what & why>

## Current State — Works / Broken
- **Works:** <what's verified working>
- **Broken / incomplete:** <what's failing or unfinished, with error text if any>

## How to Run & Test
<Exact commands to build, run, and test. Include cwd. e.g. `cd apps/api && bun test ...`>

## Gotchas & Conventions
<Non-obvious traps, project conventions, decisions + rejected alternatives, dead ends already ruled out.>

## Open TODOs
- [ ] <remaining task>

## Next Step (verbatim)
<The immediate next action. Include a direct quote of the most recent user direction or where work stopped.>
