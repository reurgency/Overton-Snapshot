# Overton Snapshot

A Claude Code plugin for the **Overton Context Window** technique: capture a scenario-aware,
structured snapshot of the current session so a **fresh agent with zero prior context** can pick up
exactly where you left off — no drift, no re-discovery. Ships with a context-usage **statusline** and
an over-threshold **nudge** so you know when to snapshot before compaction.

## What's inside

| Component | What it does |
|-----------|--------------|
| `/overton-snapshot` command + skill | Generates a snapshot using one of 9 scenario templates (coding, planning, debugging, research, strategy, meeting, creative, multimedia, general). Saved as Markdown + YAML frontmatter to `~/.claude/snapshots/`. |
| `overton/statusline.py` | Statusline showing model · git branch · `ctx NN% ▓▓░ used/window`. Mirrors Claude Code's `/context` (auto-detects 200k vs 1M). Turns red + shows `⚠ /overton-snapshot` over your threshold. |
| `overton/threshold-nudge.py` (Stop hook) | One nudge per rising 10% band per session once you cross the threshold. |
| `overton/config.json` | `threshold_pct` (default 75) and `context_window` (`"auto"`). |

## Install (plugin marketplace)

```
/plugin marketplace add reUrgency/Overton-Snapshot
/plugin install overton-snapshot@cc-plugins-by-reurgency
```

### Status line (one-time settings step)

Plugins can't register a status line directly, so add this once to `~/.claude/settings.json`:

```json
"statusLine": {
  "type": "command",
  "command": "python3 \"$HOME/.claude/overton-statusline.py\""
}
```

The plugin's `SessionStart` hook keeps `~/.claude/overton-statusline.py` pointed at the current plugin
version automatically, so this survives updates.

## Configuration

Edit `overton/config.json` (or set env vars `OVERTON_THRESHOLD_PCT`, `OVERTON_CONTEXT_WINDOW`):

- **`threshold_pct`** — when the indicator turns red and the nudge fires (default `75`).
- **`context_window`** — `"auto"` detects 200k vs 1M from `CLAUDE_CODE_DISABLE_1M_CONTEXT`; or force an integer.

## Local development

```
sh bin/dev-link.sh        # symlink ~/.claude at this repo; edits are immediately live
# iterate, then:
/reload-plugins           # (only needed when testing as an installed plugin)
```

`bin/dev-link.sh` never clobbers a real (non-symlink) file in `~/.claude` — it only replaces existing
symlinks, so it's safe to re-run.

## How context usage is computed

Claude Code doesn't expose context size to status lines/hooks, so it's derived from the session
transcript (`.jsonl`): the **last assistant turn's** token usage (`input + cache_creation + cache_read`),
using the **last `iterations[]` entry** to avoid double-counting multi-pass turns. The window divisor
matches Claude Code's own `/context` gauge (200k target when `CLAUDE_CODE_DISABLE_1M_CONTEXT` is set,
else 1M), and values over 100% are shown deliberately — they mean you're over your target window.

Before the first turn writes any usage (a brand-new session, or right after a `/resume`), the figure is
**estimated** from transcript content — system/tools baseline plus the messages that will replay (from the
last compaction summary onward for continued sessions) — and shown with a leading `~` (e.g. `ctx ~18%`).
The exact number replaces the estimate as soon as the first turn completes.

## License

MIT © reUrgency
