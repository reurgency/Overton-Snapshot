#!/bin/sh
# Run a Python script with whatever interpreter this machine actually has.
# macOS/Linux ship `python3`; Windows installs usually have `python` or `py`
# and NO `python3` (or worse, the Microsoft Store stub that only prints an
# install prompt). Probing with `-c ""` filters out the stub, which can't run
# code. Exits 0 when no interpreter is found so a missing Python degrades to
# "feature off" instead of a visible hook error on every trigger.
#
# Usage: run-python.sh <script.py> [args...]   (stdin passes through)

script="$1"
[ -n "$script" ] && shift || exit 0
for py in python3 python py; do
  if "$py" -c "" >/dev/null 2>&1; then
    exec "$py" "$script" "$@"
  fi
done
exit 0
