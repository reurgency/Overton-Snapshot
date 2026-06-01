#!/usr/bin/env python3
"""Claude Code statusLine: shows model, git branch, and a context-usage bar.

Wired via ~/.claude/settings.json -> statusLine. Reads the statusLine JSON payload
on stdin, derives context usage from the transcript (see usage.py), and renders a
single line. Turns yellow approaching, red at/above, the configured threshold and
appends a "/overton-snapshot" nudge once over threshold.
"""
import json
import os
import subprocess
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from usage import compute  # noqa: E402

DIM = "\033[2m"; CYAN = "\033[36m"; GREEN = "\033[32m"
YELLOW = "\033[33m"; RED = "\033[31m"; RESET = "\033[0m"


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        payload = {}

    model = ((payload.get("model") or {}).get("display_name")
             or (payload.get("model") or {}).get("id") or "claude")
    cwd = (payload.get("cwd")
           or (payload.get("workspace") or {}).get("current_dir")
           or os.getcwd())
    transcript = payload.get("transcript_path")

    branch = ""
    try:
        branch = subprocess.run(
            ["git", "-C", cwd, "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True, text=True, timeout=1).stdout.strip()
    except Exception:
        pass

    parts = [f"{DIM}{model}{RESET}"]
    if branch:
        parts.append(f"{CYAN}{branch}{RESET}")

    info = compute(transcript)
    if info["ok"]:
        pct, used, window, thr = (info["pct"], info["used"],
                                  info["window"], info["threshold_pct"])
        filled = max(0, min(10, round(pct / 10)))
        bar = "▓" * filled + "░" * (10 - filled)
        color = RED if pct >= thr else YELLOW if pct >= thr * 0.8 else GREEN
        # "~" marks a pre-first-turn estimate (fresh start or just-resumed session,
        # before any token usage has been recorded for this session).
        label = f"ctx ~{pct}%" if info.get("estimated") else f"ctx {pct}%"
        seg = f"{color}{label} {bar} {round(used/1000)}k/{round(window/1000)}k{RESET}"
        if pct >= thr:
            seg += f" {RED}⚠ /overton-snapshot{RESET}"
        parts.append(seg)
    else:
        parts.append(f"{DIM}ctx --{RESET}")

    sys.stdout.write("  ".join(parts))


if __name__ == "__main__":
    main()
