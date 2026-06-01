# Template 3 — Debugging

Use while chasing a bug. The key value: record what's been ruled OUT so the next agent doesn't repeat it.

```
---
id: <date>-overton-debugging-<slug>
created: <ISO-8601>
scenario: debugging
title: <short title>
project: <repo basename>
branch: <git branch>
session_id: <CLAUDE_SESSION_ID>
status: in-progress|blocked|complete
focus: <verbatim focus, omit if none>
tags: [<keywords>]
files: [<relevant paths>]
next_step: <one-line>
related: []
---
```

# <Title> — Overton Snapshot (Debugging)

## Primary Intent
<What we're trying to fix and why it matters. Front-loaded.>

## Symptom
<The observed failure. Exact error message / stack trace / wrong output, verbatim.>

## Repro Steps
<Exact steps + commands to reproduce. Include environment specifics.>

## Hypotheses Ruled Out
<Each theory tested and disproven, with the evidence that ruled it out. This is the most valuable section.>
- **<hypothesis>** — ruled out because <evidence>

## Current Leading Hypothesis
<The best current theory and why it fits the evidence.>

## Relevant Code Locations
- `path/to/file.ext:NN` — <why this is in scope>

## Next Experiment
<The specific next thing to try to confirm/deny the leading hypothesis.>

## Next Step (verbatim)
<The immediate next action. Include a direct quote of the most recent user direction or where work stopped.>
