#!/bin/sh
# SessionStart hook: keep stable launcher copies at well-known ~/.claude paths.
#
# Plugins cannot register a statusLine (it is settings.json-only), and the plugin
# cache path changes on every version bump. So users point settings.json at the
# STABLE path below once, and this hook refreshes it on every session start —
# surviving plugin updates with no manual edits.
#
# We COPY bin/overton-statusline-launcher.py (which resolves the installed plugin
# at run time) rather than symlinking the real script: Git Bash on Windows turns
# `ln -s` into a plain copy of the *target*, stranding it away from its sibling
# imports. A launcher copy behaves identically on macOS, Linux, and Git Bash.
#
# settings.json entry the user adds once (Windows: `python` instead of `python3`):
#   "statusLine": { "type": "command",
#                   "command": "python3 \"$HOME/.claude/overton-statusline.py\"" }

LAUNCHER="${CLAUDE_PLUGIN_ROOT}/bin/overton-statusline-launcher.py"
STABLE="$HOME/.claude/overton-statusline.py"
STABLE_CFG="$HOME/.claude/overton-statusline-config.py"

if [ -n "$CLAUDE_PLUGIN_ROOT" ] && [ -f "$LAUNCHER" ]; then
  # rm first: earlier plugin versions left SYMLINKS at these paths, and `cp`
  # onto a symlink writes through it into the plugin's real files.
  rm -f "$STABLE" "$STABLE_CFG"
  cp "$LAUNCHER" "$STABLE"
  cp "$LAUNCHER" "$STABLE_CFG"
fi
exit 0
