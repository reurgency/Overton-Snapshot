#!/usr/bin/env python3
"""Turn the Overton statusline emojis on or off.

Edits "statusline": {"emoji": ...} in ~/.claude/overton/config.json (the file
statusline.py reads), preserving every other key. Invoked by the /overton-statusline
slash command; safe to run by hand too.

Usage:
  statusline_config.py            show current state
  statusline_config.py on         show emoji icons
  statusline_config.py off        no emojis (plain " | " separators)
  statusline_config.py toggle     flip the current setting
"""
import json
import os
import sys

CONFIG_PATH = os.path.expanduser("~/.claude/overton/config.json")

ON = {"on", "true", "yes", "emoji", "show", "1"}
OFF = {"off", "false", "no", "pipe", "hide", "plain", "0"}


def _load():
    try:
        with open(CONFIG_PATH) as f:
            return json.load(f) or {}
    except Exception:
        return {}


def _emoji(cfg):
    sl = cfg.get("statusline") or {}
    return sl["emoji"] if isinstance(sl.get("emoji"), bool) else True


def _save(cfg, value):
    cfg.setdefault("statusline", {})
    cfg["statusline"]["emoji"] = value
    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "w") as f:
        json.dump(cfg, f, indent=2)
        f.write("\n")


def main(argv):
    cfg = _load()
    value = _emoji(cfg)

    if argv:
        arg = argv[0].lower()
        if arg == "toggle":
            value = not value
        elif arg in ON:
            value = True
        elif arg in OFF:
            value = False
        else:
            print("usage: overton-statusline [on|off|toggle]")
            return 1
        _save(cfg, value)
        print(f"statusline emojis turned {'on' if value else 'off'}.")
    else:
        print(f"statusline emojis are {'on' if value else 'off'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
