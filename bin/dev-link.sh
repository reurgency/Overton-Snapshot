#!/bin/sh
# Local development: point your live ~/.claude at this repo via symlinks, so edits
# here are immediately live without installing the plugin. Idempotent.
#
# Run from anywhere:  sh bin/dev-link.sh
# Undo: remove the symlinks and restore from ~/.claude/overton.backup-* if needed.

set -e
REPO="$(cd "$(dirname "$0")/.." && pwd)"
CLAUDE="$HOME/.claude"

link () {  # link <target-in-repo> <path-in-~/.claude>
  target="$1"; dest="$2"
  # Only replace if it is missing or already a symlink (never clobber a real dir/file).
  if [ -e "$dest" ] && [ ! -L "$dest" ]; then
    echo "SKIP (real file/dir exists, not replacing): $dest"
    return 0
  fi
  ln -sfn "$target" "$dest"
  echo "linked: $dest -> $target"
}

link "$REPO/overton"                  "$CLAUDE/overton"
link "$REPO/commands/overton-resume.md"     "$CLAUDE/commands/overton-resume.md"
link "$REPO/commands/overton-statusline.md" "$CLAUDE/commands/overton-statusline.md"
link "$REPO/skills/overton-snapshot"  "$CLAUDE/skills/overton-snapshot"
# Stable launchers: COPIES of the runtime-resolving launcher, same as the
# SessionStart hook installs on real plugin setups (rm first — cp onto a
# leftover symlink from older versions would write through it into repo files).
rm -f "$CLAUDE/overton-statusline.py" "$CLAUDE/overton-statusline-config.py"
cp "$REPO/bin/overton-statusline-launcher.py" "$CLAUDE/overton-statusline.py"
cp "$REPO/bin/overton-statusline-launcher.py" "$CLAUDE/overton-statusline-config.py"
echo "stable statusline launcher: $CLAUDE/overton-statusline.py (resolves \$HOME/.claude/overton, then the installed plugin)"
echo "stable config launcher:     $CLAUDE/overton-statusline-config.py"
echo "Done. (settings.json may point at \$HOME/.claude/overton/statusline.py or \$HOME/.claude/overton-statusline.py)"
