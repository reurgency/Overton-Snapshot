"""Shared context-usage estimation for the Overton Snapshot automation layer.

Estimates how full the current Claude Code context window is by reading the last
assistant turn's token usage from the session transcript (.jsonl). Used by both
statusline.py (visual indicator) and threshold-nudge.py (Stop hook nudge).

Claude Code does not expose context size to statusline/hooks directly, so we derive
it from the transcript, where each assistant message carries a `usage` block:
    input_tokens + cache_creation_input_tokens + cache_read_input_tokens  = prompt sent
    + output_tokens                                                       = becomes next turn's input
"""
import json
import os


def _config():
    # context_window default is None = "auto-detect" (see _window()).
    cfg = {"threshold_pct": 75, "context_window": None}
    cfg_path = os.path.expanduser("~/.claude/overton/config.json")
    try:
        with open(cfg_path) as f:
            loaded = json.load(f)
        if isinstance(loaded.get("threshold_pct"), int):
            cfg["threshold_pct"] = loaded["threshold_pct"]
        cw = loaded.get("context_window")
        if isinstance(cw, int) and cw > 0:   # explicit numeric override only
            cfg["context_window"] = cw        # "auto"/0/null -> stays None
    except Exception:
        pass
    # env overrides win
    tp = os.environ.get("OVERTON_THRESHOLD_PCT")
    if tp:
        try:
            cfg["threshold_pct"] = int(tp)
        except ValueError:
            pass
    cw = os.environ.get("OVERTON_CONTEXT_WINDOW")
    if cw:
        try:
            cfg["context_window"] = int(cw)
        except ValueError:
            pass
    return cfg


def _window(cfg):
    """Resolve the context window to use as the denominator — matching Claude Code's
    own `/context` gauge. Explicit config/env override wins; otherwise detect from the
    same 1M-context env toggle CC uses: disabled -> 200k target, enabled -> 1M.

    We deliberately do NOT clamp usage to <=100%: CC reports >100% (e.g. 178%) when a
    session is over its target window, and that over-target signal is exactly what
    should drive the snapshot nudge."""
    if cfg.get("context_window"):
        return cfg["context_window"]
    disabled = os.environ.get("CLAUDE_CODE_DISABLE_1M_CONTEXT", "").lower() in ("1", "true", "yes")
    return 200_000 if disabled else 1_000_000


def _last_usage(transcript_path, tail_bytes=2_000_000):
    """Return the most recent usage dict in the transcript, or None.

    Reads only the tail of the file to stay fast on large transcripts, then scans
    lines from the end for the last parseable assistant message carrying token usage.
    """
    try:
        size = os.path.getsize(transcript_path)
        with open(transcript_path, "rb") as f:
            if size > tail_bytes:
                f.seek(size - tail_bytes)
            data = f.read()
    except Exception:
        return None
    for raw in reversed(data.split(b"\n")):
        if b'"usage"' not in raw:
            continue
        try:
            obj = json.loads(raw)
        except Exception:
            continue  # partial first line from the tail slice, or non-JSON
        msg = obj.get("message") or {}
        usage = msg.get("usage") or obj.get("usage")
        if usage and usage.get("input_tokens") is not None:
            return usage
    return None


def _tokens(usage):
    """Tokens currently occupying the context window for this turn.

    A single assistant turn may contain several inference iterations (tool-use
    loops, thinking). Claude Code SUMS them into the top-level usage, which
    re-counts the shared cached prefix once per iteration and overstates context.
    The last iteration reflects the true current window occupancy, so prefer it.
    """
    its = usage.get("iterations")
    src = its[-1] if isinstance(its, list) and its else usage
    return (src.get("input_tokens", 0)
            + src.get("cache_creation_input_tokens", 0)
            + src.get("cache_read_input_tokens", 0))


def compute(transcript_path):
    """Return a dict describing current context usage.

    Keys: ok (bool), window, threshold_pct, and when ok: used, pct.
    """
    cfg = _config()
    usage = _last_usage(transcript_path) if transcript_path else None
    if not usage:
        # report the detected window even when usage is unknown
        return {"ok": False, "window": _window(cfg),
                "threshold_pct": cfg["threshold_pct"]}
    used = _tokens(usage)
    window = _window(cfg)
    return {"ok": True, "used": used, "window": window,
            "pct": round(100 * used / window), "threshold_pct": cfg["threshold_pct"]}
