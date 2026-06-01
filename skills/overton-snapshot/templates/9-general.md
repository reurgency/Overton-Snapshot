# Template 9 — General (catch-all)

Use when the session is mixed or ambiguous. This mirrors Claude Code's built-in 9-section compaction
format, lightly adapted, so nothing important is lost regardless of scenario.

```
---
id: <date>-overton-general-<slug>
created: <ISO-8601>
scenario: general
title: <short title>
project: <repo basename or "none">
branch: <git branch, omit if none>
session_id: <CLAUDE_SESSION_ID>
status: in-progress|blocked|complete
focus: <verbatim focus, omit if none>
tags: [<keywords>]
files: [<relevant paths>]
next_step: <one-line>
related: []
---
```

# <Title> — Overton Snapshot (General)

## Primary Intent
<All of the user's explicit requests and intent, in detail. Front-loaded.>

## Key Concepts
<Important technical concepts, technologies, frameworks, or ideas in play.>

## Files & Code Sections
<Files examined/modified/created, each with why it matters and essential snippets via `path:line`.>

## Errors & Fixes
<Errors encountered and how they were fixed; include user feedback on them. _n/a_ if none.>

## Problem Solving
<Problems solved and ongoing troubleshooting.>

## All User Messages (key directives, verbatim)
<List the user's non-tool-result messages, especially constraints/feedback — quoted to prevent drift.>

## Pending Tasks
<Outstanding tasks the user explicitly asked for.>
- [ ] <task>

## Current Work
<Precisely what was being worked on immediately before this snapshot.>

## Next Step (verbatim)
<The immediate next action, DIRECTLY in line with the most recent request. Include a verbatim quote of where work stopped.>
