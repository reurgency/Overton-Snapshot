# Overton Snapshot — Format & Writing Rules

Shared by all 9 templates. Read this together with the chosen `templates/<n>-*.md`.

## Frontmatter schema

Every snapshot begins with a YAML frontmatter block. Required keys are marked ✱.

```yaml
---
id: <date>-overton-<scenario>-<slug>      # ✱ matches the filename (minus .md), e.g. 2026-05-30-overton-coding-auth-refactor
created: <ISO-8601>                        # ✱ from the environment's current date/time — do NOT invent
scenario: coding|planning|debugging|research|strategy|meeting|creative|multimedia|general  # ✱
title: <short human title>                 # ✱
project: <repo or cwd basename>            # ✱ (or "none" if not in a project)
branch: <git branch>                       # omit if not in a git repo
session_id: <CLAUDE_SESSION_ID>            # the originating session
status: in-progress|blocked|complete       # ✱
focus: <verbatim focus instructions>       # omit if the user gave none
tags: [<searchable keywords>]              # ✱ — drives future search across the archive
files: [<touched/relevant paths>]          # mainly coding/debugging; omit if none
next_step: <one-line>                      # ✱ — the immediate next action
related: [<other snapshot ids>]            # optional cross-links to prior snapshots
---
```

Keep frontmatter values short and machine-friendly; put narrative in the body.

## File naming

`~/.claude/snapshots/YYYY-MM-DD-HHMM-overton-<scenario>-<slug>.md`

- `YYYY-MM-DD-HHMM` — from the environment's current date/time.
- `<scenario>` — the lowercase scenario name (e.g. `coding`).
- `<slug>` — 2–5 kebab-case words from the title (e.g. `auth-refactor`).

## Writing techniques (apply to every snapshot)

These are distilled from Claude Code's own compaction prompt plus the goal of a zero-context handoff:

1. **Front-load intent.** The first body section is always `## Primary Intent`. A reader must grasp
   the goal and why it matters within the first few lines.
2. **Preserve user instructions, feedback, and constraints verbatim.** Quote them. Never paraphrase a
   security rule, a "don't do X", or a correction the user made — paraphrasing causes drift.
3. **Quote the next step verbatim.** `## Next Step (verbatim)` should include a direct quote of the
   most recent user direction or the exact point where work stopped. This is the single biggest
   guard against a fresh agent misinterpreting the task.
4. **Use clickable references.** Cite code as `path/to/file.ext:line` so it's clickable. Include only
   the minimal essential code snippets; link rather than paste large blocks.
5. **Record dead ends and rejected options.** Explicitly note what was tried and ruled out, or
   considered and rejected, so the next agent doesn't re-tread the same ground.
6. **Separate state from action.** "What is true now" (current state) and "what to do next" (action)
   are different sections — never blur them.
7. **Be dense, no filler.** Assume the reader is a capable agent with zero shared history. Every line
   should carry information. Cut pleasantries and restated obvious context.
8. **Honor focus instructions.** Whatever the user's focus names, capture it at higher fidelity —
   verbatim where practical — even if the base template would compress it.
9. **Never silently drop a section.** If a template section doesn't apply, write `_n/a_`.

## Shared sections present in every template

- `## Primary Intent` — the goal, front-loaded.
- `## Next Step (verbatim)` — the immediate next action, with a verbatim quote of where work stopped.

Everything else is scenario-specific (see the template file).
