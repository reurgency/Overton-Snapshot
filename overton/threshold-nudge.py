#!/usr/bin/env python3
"""Stop hook: nudges you to run /overton-snapshot when context crosses the threshold.

Wired via ~/.claude/settings.json -> hooks.Stop. Fires when the main agent finishes a
turn. If context usage (derived from the transcript) is at/above the configured
threshold, it emits a non-blocking systemMessage. Throttled so it nudges at most once
per rising 10% band per session (won't repeat every turn at a steady level).
"""
import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from usage import compute  # noqa: E402


def _emit(obj):
    sys.stdout.write(json.dumps(obj))
    sys.exit(0)


def main():
    try:
        payload = json.load(sys.stdin)
    except Exception:
        _emit({})

    info = compute(payload.get("transcript_path"))
    if not info.get("ok"):
        _emit({})

    pct, thr = info["pct"], info["threshold_pct"]
    if pct < thr:
        _emit({})

    # Throttle: only nudge when entering a new, higher 10% band this session.
    session = payload.get("session_id") or "unknown"
    marker = os.path.join(tempfile.gettempdir(), f"overton-nudged-{session}")
    last_band = -1
    try:
        with open(marker) as f:
            last_band = int(f.read().strip())
    except Exception:
        pass
    band = (pct // 10) * 10
    if band <= last_band:
        _emit({})
    try:
        with open(marker, "w") as f:
            f.write(str(band))
    except Exception:
        pass

    _emit({"systemMessage": (
        f"⚠ Context at {pct}% "
        f"({round(info['used']/1000)}k of the {round(info['window']/1000)}k window, "
        f"threshold {thr}%). Consider running /overton-snapshot to checkpoint "
        f"this session before auto-compaction.")})


if __name__ == "__main__":
    main()
