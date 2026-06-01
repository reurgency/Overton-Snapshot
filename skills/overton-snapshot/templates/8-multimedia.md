# Template 8 — Multimedia (PDF / Image)

Use when analyzing PDFs, images, diagrams, or screenshots. Anchor everything to artifact + page/region refs.

```
---
id: <date>-overton-multimedia-<slug>
created: <ISO-8601>
scenario: multimedia
title: <short title>
project: <repo basename or "none">
session_id: <CLAUDE_SESSION_ID>
status: in-progress|blocked|complete
focus: <verbatim focus, omit if none>
tags: [<keywords>]
files: [<artifact paths>]
next_step: <one-line>
related: []
---
```

# <Title> — Overton Snapshot (Multimedia)

## Primary Intent
<What we're analyzing in these artifacts and why. Front-loaded.>

## Artifacts
<Each file with a locator. For PDFs note page ranges; for images note region/what it depicts.>
- `path/to/artifact` — <type, pages/region, one-line description>

## What Each Contains
<Per-artifact summary of the relevant content.>

## Extracted Facts / Figures
<Concrete data pulled out: numbers, names, dates, quotes — with the artifact + page/region cited.>
- <fact> — *(source: `artifact` p.N / region)*

## Interpretation So Far
<What the artifacts mean for the task; conclusions drawn vs still tentative.>

## Questions for the Source
<Ambiguities or gaps in the artifacts that need clarification.>

## Next Analysis
<The specific next thing to read/extract/compare.>

## Next Step (verbatim)
<The immediate next action. Include a direct quote of the most recent user direction or where analysis stopped.>
