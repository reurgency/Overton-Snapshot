"""Shared context-usage estimation for the Overton Snapshot automation layer.

Estimates how full the current Claude Code context window is by reading the last
assistant turn's token usage from the session transcript (.jsonl). Used by both
statusline.py (visual indicator) and threshold-nudge.py (Stop hook nudge).

The numbers here deliberately mirror Claude Code's own "% context used" footer,
which computes (verified against CC 2.1.170's source):

    used   = input_tokens + cache_creation_input_tokens
             + cache_read_input_tokens + output_tokens     (last assistant message)
    window = context_window_size - min(max_output_tokens, 20_000)
    pct    = round(100 * used / window)                    (footer clamps to 0-100)

Two things people get wrong (we did too): CC counts the response's output_tokens
as occupying the window (they re-enter as input next turn), and it divides by the
window MINUS a reserved output allowance — 20k for every current model — not the
raw 200k. Both omissions together read ~9 points low near the limit.
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


# Claude Code reserves room for the model's output when judging fullness: its
# footer divides by (window - min(max_output_tokens, 20k)). max_output_tokens is
# >= 32k for every current model, so the reserve is effectively a 20k constant.
OUTPUT_RESERVE = 20_000


def _window(cfg):
    """Resolve the RAW context window. Explicit config/env override wins; otherwise
    detect from the same 1M-context env toggle CC uses: disabled -> 200k, enabled
    -> 1M. compute() subtracts OUTPUT_RESERVE to get the usable denominator.

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

    Matches Claude Code's own count: the message's TOP-LEVEL usage (CC reads it
    directly, not iterations[-1]), INCLUDING output_tokens — the response just
    generated re-enters the window as input on the next turn, and CC counts it.
    """
    return (usage.get("input_tokens", 0)
            + usage.get("cache_creation_input_tokens", 0)
            + usage.get("cache_read_input_tokens", 0)
            + usage.get("output_tokens", 0))


# Approx fixed context loaded before any conversation messages: system prompt +
# system/MCP tools + custom agents + memory files + skills. Used only for the
# pre-first-turn estimate (no token usage exists yet). Rough by nature.
BASELINE_OVERHEAD = 25_000


def _estimate_text_tokens(content):
    """Very rough token estimate (~chars/4) for a message's content, which may be a
    plain string or a list of content blocks (text / tool_use / tool_result)."""
    if isinstance(content, str):
        return len(content) // 4
    total = 0
    if isinstance(content, list):
        for b in content:
            if not isinstance(b, dict):
                total += len(str(b)) // 4
            elif isinstance(b.get("text"), str):
                total += len(b["text"]) // 4
            elif b.get("type") == "tool_result":
                c = b.get("content")
                total += len(c if isinstance(c, str) else json.dumps(c)) // 4
            elif b.get("type") == "tool_use":
                total += len(json.dumps(b.get("input", {}))) // 4
    return total


def _estimate_loaded(transcript_path):
    """Estimate context that WILL load when no token usage exists yet — i.e. the
    pre-first-turn window right after a fresh start or a /resume continuation.

    For a compacted/continued session only the content from the last compaction
    summary onward is replayed, so we count from there; otherwise we count all
    messages. Plus a baseline for system/tools/memory/skills. Approximate.
    """
    try:
        raw_lines = open(transcript_path, "rb").read().split(b"\n")
    except Exception:
        return None
    records = []
    for raw in raw_lines:
        if not raw.strip():
            continue
        try:
            records.append(json.loads(raw))
        except Exception:
            continue
    if not records:
        return None
    start = 0  # replay starts at the most recent compaction summary, if any
    for i, o in enumerate(records):
        if o.get("isCompactSummary"):
            start = i
    tokens = BASELINE_OVERHEAD
    for o in records[start:]:
        if o.get("type") in ("user", "assistant"):
            tokens += _estimate_text_tokens((o.get("message") or {}).get("content"))
    return tokens


def compute(transcript_path):
    """Return a dict describing current context usage.

    Keys: ok (bool), window, threshold_pct, and when ok: used, pct, estimated.
    `used`/`window` are RAW (actual tokens, actual window size — e.g. 144k/200k);
    `pct` divides by the usable window (raw minus OUTPUT_RESERVE) so it matches
    CC's "% context used" footer — same split CC itself shows between the footer
    percent and /context token counts. `estimated` is True when no token usage
    exists yet (pre-first-turn / fresh resume) and the figure is derived from
    transcript content instead.
    """
    cfg = _config()
    window = _window(cfg)
    usable = max(1, window - OUTPUT_RESERVE)
    usage = _last_usage(transcript_path) if transcript_path else None
    if usage:
        used, estimated = _tokens(usage), False
    elif transcript_path:
        used = _estimate_loaded(transcript_path)
        if used is None:
            return {"ok": False, "window": window, "threshold_pct": cfg["threshold_pct"]}
        estimated = True
    else:
        return {"ok": False, "window": window, "threshold_pct": cfg["threshold_pct"]}
    return {"ok": True, "used": used, "window": window,
            "pct": round(100 * used / usable),
            "threshold_pct": cfg["threshold_pct"], "estimated": estimated}
