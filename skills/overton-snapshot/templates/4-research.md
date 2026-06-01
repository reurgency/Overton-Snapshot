# Template 4 — Research / Investigation

Use when exploring a codebase or external sources to answer a question. Capture sources + dead ends.

```
---
id: <date>-overton-research-<slug>
created: <ISO-8601>
scenario: research
title: <short title>
project: <repo basename or "none">
branch: <git branch, omit if none>
session_id: <CLAUDE_SESSION_ID>
status: in-progress|blocked|complete
focus: <verbatim focus, omit if none>
tags: [<keywords>]
next_step: <one-line>
related: []
---
```

# <Title> — Overton Snapshot (Research)

## Primary Intent
<The question being investigated and why. Front-loaded. Quote the user's ask.>

## Question(s)
<The precise question(s) driving the research.>

## Sources / Files Examined
<Each source with a one-line takeaway. Use `path:line` for code, URLs for external.>
- `path/or/url` — <what it told us>

## Findings
<What we've learned, with citations back to the sources above. Distinguish confirmed vs tentative.>

## Dead Ends
<Sources/avenues that turned out to be irrelevant or wrong, so they aren't re-checked.>

## Open Unknowns
<What we still don't know that matters.>

## Tentative Conclusion
<Best current answer, with confidence level. _n/a_ if not yet formed.>

## Next Step (verbatim)
<The immediate next action. Include a direct quote of the most recent user direction or where work stopped.>
