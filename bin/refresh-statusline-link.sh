#!/bin/sh
# SessionStart hook: keep a stable symlink pointing at the plugin's statusline script.
#
# Plugins cannot register a statusLine (it is settings.json-only), and the plugin
# cache path changes on every version bump. So users point settings.json at the
# STABLE path below once, and this hook re-aims it at the current plugin root on
# every session start — surviving plugin updates with no manual edits.
#
# settings.json entry the user adds once:
#   "statusLine": { "type": "command",
#                   "command": "python3 \"$HOME/.claude/overton-statusline.py\"" }

STABLE="$HOME/.claude/overton-statusline.py"
TARGET="${CLAUDE_PLUGIN_ROOT}/overton/statusline.py"

# Stable launcher for the /overton-statusline config CLI (same survives-updates trick).
STABLE_CFG="$HOME/.claude/overton-statusline-config.py"
TARGET_CFG="${CLAUDE_PLUGIN_ROOT}/overton/statusline_config.py"

if [ -n "$CLAUDE_PLUGIN_ROOT" ]; then
  ln -sfn "$TARGET" "$STABLE"
  ln -sfn "$TARGET_CFG" "$STABLE_CFG"
fi
exit 0
