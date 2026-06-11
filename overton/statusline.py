#!/usr/bin/env python3
"""Claude Code statusLine: a condensed two-line cockpit.

Wired via ~/.claude/settings.json -> statusLine. Reads the statusLine JSON payload
on stdin and renders two lines. With emojis on:

  ✨ model/effort  🎯 ctx% bar used/window [⏰ run /overton-snapshot]  💰 cost  ⏱️ 5h rate%  ⏳ resets
  📁 dir | branch ~changes | worktree

With emojis off (toggle via /overton-statusline), the same data renders with no
emojis and " | " separators throughout:

  model/effort | ctx% bar used/window [⏰ run /overton-snapshot] | cost | 5h rate% @ resets
  dir | branch ~changes | worktree

The context percent mirrors Claude Code's own "% context used" footer — tokens
incl. output over the usable window (raw minus CC's 20k output reserve) — while
the token readout shows raw tokens against the raw window (e.g. "80% … 144k/200k"),
the same split CC makes between its footer percent and /context counts. The
bar/percent is green, turns yellow approaching the threshold, red at/above it, and
appends the "[⏰ run /overton-snapshot]" nudge once over threshold. The rate-limit segment only renders
for Pro/Max sessions once the data is present in the payload.

Separator rule (emoji mode): segments led by an emoji are divided by two spaces (the
emoji is the visual divider); segments with no emoji (branch, worktree) use " | ".
"""
import datetime
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from usage import compute, _config, OUTPUT_RESERVE  # noqa: E402

DIM = "\033[2m"; CYAN = "\033[36m"; GREEN = "\033[32m"
YELLOW = "\033[33m"; RED = "\033[31m"; RESET = "\033[0m"

CONFIG_PATH = os.path.expanduser("~/.claude/overton/config.json")

# Rate-limit colour bands (fixed; the context bar tracks the configured threshold).
RATE_YELLOW_PCT = 75
RATE_RED_PCT = 90


def _emoji_on():
    """Whether to show emoji icons. Reads "statusline": {"emoji": true|false} from the
    same config.json usage.py uses. Missing/invalid -> emojis on."""
    try:
        with open(CONFIG_PATH) as f:
            sl = (json.load(f) or {}).get("statusline") or {}
        if isinstance(sl.get("emoji"), bool):
            return sl["emoji"]
    except Exception:
        pass
    return True


def _git(cwd, *args):
    try:
        return subprocess.run(["git", "-C", cwd, *args],
                              capture_output=True, text=True, timeout=1).stdout
    except Exception:
        return ""


def _context(payload):
    """Context usage matching Claude Code's native "% context used" footer.

    The footer divides (input + cache + OUTPUT tokens) by the USABLE window — the
    raw window minus a reserved output allowance (min(max_output_tokens, 20k), so
    20k for every current model) — and clamps to 0-100. The payload's pre-computed
    `context_window.used_percentage` does NOT match the footer (it omits output
    tokens and divides by the raw window, reading ~9 points low near the limit),
    so we derive the footer's number from the payload's token counts instead.
    The returned `window` stays RAW for the token readout (144k/200k), matching
    CC's own split between footer percent and /context counts. Older CC lacks
    the block; fall back to the transcript (usage.py, same math).
    """
    thr = _config()["threshold_pct"]
    cw = payload.get("context_window")
    if isinstance(cw, dict) and cw.get("used_percentage") is not None \
            and cw.get("context_window_size"):
        used = cw.get("total_input_tokens")
        if used is not None:
            used += cw.get("total_output_tokens") or 0
        else:
            cu = cw.get("current_usage") or {}
            used = (cu.get("input_tokens", 0)
                    + cu.get("cache_creation_input_tokens", 0)
                    + cu.get("cache_read_input_tokens", 0)
                    + cu.get("output_tokens", 0))
        window = cw["context_window_size"]
        usable = max(1, window - OUTPUT_RESERVE)
        pct = max(0, min(100, round(100 * used / usable)))
        return {"ok": True, "pct": pct, "used": used, "window": window,
                "threshold_pct": thr, "estimated": False}
    return compute(payload.get("transcript_path"))


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    emoji = _emoji_on()

    def seg(icon, body):
        """A rendered segment as (text, emoji_led). In emoji mode an icon prefixes the
        body and marks the segment emoji-led; otherwise just the body, never emoji-led."""
        if emoji and icon:
            return (f"{icon} {body}", True)
        return (body, False)

    def assemble(parts):
        """Join segments: two spaces before an emoji-led segment, " | " otherwise."""
        parts = [p for p in parts if p]
        if not parts:
            return ""
        out = parts[0][0]
        for text, led in parts[1:]:
            out += ("  " if led else f"{DIM} | {RESET}") + text
        return out

    cwd = (payload.get("cwd")
           or (payload.get("workspace") or {}).get("current_dir")
           or os.getcwd())
    ws = payload.get("workspace") or {}

    model = ((payload.get("model") or {}).get("display_name")
             or (payload.get("model") or {}).get("id") or "claude")
    effort = (payload.get("effort") or {}).get("level") if isinstance(
        payload.get("effort"), dict) else None
    cost = (payload.get("cost") or {}).get("total_cost_usd")
    five_hour = (payload.get("rate_limits") or {}).get("five_hour") or {}
    worktree = ws.get("git_worktree") or (payload.get("worktree") or {}).get("name")

    # ---------- line 1: session ----------
    model_text = f"{model}/{effort}" if effort else model
    line1 = [seg("✨", f"{DIM}{model_text}{RESET}")]

    info = _context(payload)
    if info.get("ok"):
        pct, used = info["pct"], info["used"]
        window, thr = info["window"], info["threshold_pct"]
        filled = max(0, min(10, round(pct / 10)))
        bar = "▓" * filled + "░" * (10 - filled)
        color = RED if pct >= thr else YELLOW if pct >= thr * 0.8 else GREEN
        # "~" marks a pre-first-turn estimate (fresh / just-resumed session).
        label = f"~{pct}%" if info.get("estimated") else f"{pct}%"
        body = f"{color}{label} {bar} {round(used/1000)}k/{round(window/1000)}k{RESET}"
        if pct >= thr:
            body += f" {RED}[⏰ run /overton-snapshot]{RESET}"
        line1.append(seg("🎯", body))
    else:
        line1.append(seg("🎯", f"{DIM}--{RESET}"))

    if cost is not None:
        line1.append(seg("💰", f"{GREEN}${cost:.2f}{RESET}"))

    if five_hour.get("used_percentage") is not None:
        rpct = round(five_hour["used_percentage"])
        rcolor = (RED if rpct >= RATE_RED_PCT
                  else YELLOW if rpct >= RATE_YELLOW_PCT else GREEN)
        body = f"{rcolor}5h {rpct}%{RESET}"
        resets = five_hour.get("resets_at")
        if resets:
            try:
                when = datetime.datetime.fromtimestamp(int(resets)).strftime(
                    "%I:%M%p").lstrip("0")
                # emoji mode breaks the reset into its own ⏳ segment (two-space
                # divided); plain mode keeps it inline with an "@" marker.
                body += (f"{RESET}  {DIM}⏳ {when}{RESET}" if emoji
                         else f"{DIM} @ {when}{RESET}")
            except Exception:
                pass
        line1.append(seg("⏱️", body))

    # ---------- line 2: workspace ----------
    line2 = []

    name = os.path.basename(os.path.normpath(cwd)) or cwd
    line2.append(seg("📁", f"{CYAN}{name}{RESET}"))

    branch = _git(cwd, "rev-parse", "--abbrev-ref", "HEAD").strip()
    if branch:
        changes = sum(1 for ln in _git(cwd, "status", "--porcelain").splitlines()
                      if ln.strip())
        label = f"{branch} ~{changes}" if changes else branch
        line2.append(seg(None, f"{GREEN}{label}{RESET}"))

    if worktree:
        line2.append(seg(None, f"{GREEN}{worktree}{RESET}"))
    else:
        line2.append(seg(None, f"{DIM}no worktree{RESET}"))

    lines = [assemble(parts) for parts in (line1, line2) if parts]
    sys.stdout.write("\n".join(lines))


if __name__ == "__main__":
    main()
