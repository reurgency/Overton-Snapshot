#!/usr/bin/env python3
"""Stable launcher for the Overton statusline (and its config CLI).

Copied to ~/.claude/overton-statusline.py (and overton-statusline-config.py) by
bin/refresh-statusline-link.sh on session start. settings.json points at that
stable path once; the launcher finds the currently-installed plugin at run time,
so the same copy keeps working across plugin updates (whose cache path changes
every version). It is a COPY, not a symlink: Git Bash on Windows silently turns
`ln -s` into a copy of the target file, which strands the script away from its
sibling imports — a launcher that resolves the real location behaves identically
on every platform.

Which script it launches depends on the file name it was copied to:
  overton-statusline.py        -> overton/statusline.py
  overton-statusline-config.py -> overton/statusline_config.py
"""
import glob
import json
import os
import runpy
import sys

TARGETS = {"overton-statusline-config.py": "statusline_config.py"}


def _candidates(target):
    claude = os.path.join(os.path.expanduser("~"), ".claude")
    # 1) dev-link / manual layout: ~/.claude/overton/<target>
    yield os.path.join(claude, "overton", target)
    # 2) the installed plugin, per Claude Code's plugin registry
    try:
        with open(os.path.join(claude, "plugins", "installed_plugins.json")) as f:
            plugins = json.load(f).get("plugins") or {}
        installs = []
        for key, entries in plugins.items():
            if key.split("@")[0] == "overton-snapshot" and isinstance(entries, list):
                installs.extend(e for e in entries if isinstance(e, dict))
        installs.sort(key=lambda e: e.get("lastUpdated") or "", reverse=True)
        for e in installs:
            if e.get("installPath"):
                yield os.path.join(e["installPath"], "overton", target)
    except Exception:
        pass
    # 3) last resort: newest match in the plugin cache
    pattern = os.path.join(claude, "plugins", "cache", "*", "overton-snapshot",
                           "*", "overton", target)
    for p in sorted(glob.glob(pattern), key=os.path.getmtime, reverse=True):
        yield p


def main():
    target = TARGETS.get(os.path.basename(__file__), "statusline.py")
    for path in _candidates(target):
        if os.path.isfile(path):
            sys.argv[0] = path
            runpy.run_path(path, run_name="__main__")
            return
    sys.stderr.write(
        f"overton: {target} not found in ~/.claude/overton or the installed "
        "overton-snapshot plugin\n")
    sys.exit(1)


if __name__ == "__main__":
    main()
