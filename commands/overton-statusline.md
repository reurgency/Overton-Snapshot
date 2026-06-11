---
description: Turn the Overton statusline emojis on or off (off = plain " | " separators).
argument-hint: "[blank = show state] [on] [off] [toggle]"
---

Configure the Overton statusline. Raw argument: `$ARGUMENTS`

Run this exact command (pass `$ARGUMENTS` through verbatim — do not add or change it):

```bash
python3 "$HOME/.claude/overton-statusline-config.py" $ARGUMENTS 2>/dev/null \
  || python "$HOME/.claude/overton-statusline-config.py" $ARGUMENTS 2>/dev/null \
  || python3 "$HOME/.claude/overton/statusline_config.py" $ARGUMENTS
```

(The `python` fallback covers Windows, where `python3` usually doesn't exist; the
last line covers setups from before the stable launcher existed.)

Then show the user the command's output verbatim in one short line.

- `on` → emoji icons (✨ 🎯 💰 ⏱️ ⏳ 📁); `off` → no emojis, segments separated by ` | `.
- `toggle` flips the current setting; no argument just reports the current state.

The change takes effect on the next statusline render (a second or two).
