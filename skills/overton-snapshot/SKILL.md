---
name: Overton Snapshot
description: Capture an "Overton Context Window" snapshot — a scenario-aware, structured summary of the current session that a fresh agent with zero prior context can read and immediately resume from. Use when context is filling up, before a handoff, or any time you want a durable, searchable checkpoint of where things stand.
status: active
embedMode: link
---

# Overton Snapshot

## Capability

An **Overton snapshot** is a deliberate, mid-session checkpoint. Its single goal: produce a document
so complete that a **brand-new agent with zero shared history** can read it (plus whatever comes next)
and continue the work with no drift and no re-discovery. It improves on Claude Code's built-in
compaction by being **scenario-aware** (9 purpose-built templates) and **structured + searchable**
(Markdown body + YAML frontmatter, saved to a durable archive).

Run this whenever the user invokes `/overton-snapshot`. Work through Steps 0–4 in order.

## Step 0 — Parse arguments

You receive a raw argument string. Split it:

- **Leading digit 1–9** → that is the **template id**. Everything after the digit is **focus instructions**.
- **No leading digit** → **auto-detect** the template (Step 1). The entire string (if any) is **focus instructions**.
- **Empty** → auto-detect template, no focus.

**Focus instructions** are a first-class steer from the user — e.g. *"pay particular attention to
preserving the posting-strategy section"* or *"keep every detail of the repro steps."* They tell you
what to capture at **higher fidelity** (verbatim where practical), even if the base template would
normally compress it. Echo the focus back to the user before proceeding, and record it verbatim in
the frontmatter `focus:` field.

Template ids: `1` coding · `2` planning · `3` debugging · `4` research · `5` strategy · `6` meeting ·
`7` creative · `8` multimedia · `9` general.

## Step 1 — Select the scenario

If Step 0 gave you a digit, use that template. Otherwise auto-detect from session signals:

| Signal in the session | Likely template |
|------------------------|-----------------|
| Active code edits, a git diff, build/test runs | **1 coding** |
| Architecture/approach discussion, weighing options, designing | **2 planning** |
| Chasing an error, repro attempts, "why is this failing" | **3 debugging** |
| Heavy WebFetch/WebSearch/Explore, gathering information | **4 research** |
| Long-running strategic/positioning discussion, no single deliverable | **5 strategy** |
| A pasted transcript or notes from a call/meeting | **6 meeting** |
| Drafting prose, story, copy, narrative | **7 creative** |
| Reading/analyzing PDFs, images, diagrams, screenshots | **8 multimedia** |
| Ambiguous or mixed | **9 general** |

**Always announce the chosen template and a one-line rationale** so the user can override.

## Step 2 — Gather context (before you write)

Do a quick chronological analysis pass over the conversation, then collect:

- The user's **explicit requests and intent** — front-load these.
- Any **feedback or corrections** the user gave → preserve **verbatim** (quote them).
- **Constraints**: security rules, "don't touch X", ports, conventions, secrets-handling → **verbatim**.
- Concrete **artifacts**: file paths with line numbers (`path:line`), `git status`/diff if relevant,
  essential code snippets, command outputs, decisions made **and** rejected alternatives, dead ends.
- The **current state** (what works / what's broken / what's in progress) vs the **single next step**.
- Anything named by the **focus instructions** — capture this at the highest fidelity.

## Step 3 — Populate the template

1. Read `${CLAUDE_SKILL_DIR}/templates/<n>-<name>.md` for the selected template.
2. Read `${CLAUDE_SKILL_DIR}/FORMAT.md` for the frontmatter schema and writing-technique rules.
3. Fill **every** section. If a section genuinely doesn't apply, write `_n/a_` — never silently drop it.
4. Apply the writing techniques from FORMAT.md (verbatim constraints, verbatim next step, clickable
   `path:line`, separate state from action, record dead ends, dense/no-filler).
5. **Honor the focus instructions**: expand and preserve whatever they name, even beyond the template default.

## Step 4 — Write the file, then print inline

1. Build the frontmatter (FORMAT.md schema). For `created`, use the current date/time from the
   environment context. For `session_id`, use `${CLAUDE_SESSION_ID}`.
2. Ensure `~/.claude/snapshots/` exists (create it if needed) and write to:
   `~/.claude/snapshots/YYYY-MM-DD-HHMM-overton-<scenario>-<slug>.md`
   (`<slug>` = 2–5 kebab-case words from the title).
3. **Print the full snapshot inline** in your reply, then report the saved file path on the last line.

## Quality bar (self-check before finishing)

- Could a fresh agent with **zero context** resume from this snapshot alone?
- Are user **constraints** and the **next step** quoted **verbatim**?
- Are file references clickable `path:line`?
- Did you honor the **focus instructions**?
- Is the frontmatter valid YAML with all required keys?
