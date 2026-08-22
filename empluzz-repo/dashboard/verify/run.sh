#!/usr/bin/env bash
# Build the fixtures and run all three suites. 41 assertions.
#
#   ./run.sh [path/to/authored-build.html]
#
# Defaults to the current dashboard source in ../ .
#
# Chromium: set ACC_CHROMIUM to a browser binary if Playwright cannot find its
# own. A cloud session has one pre-installed but at a different build number
# than whatever `npm install playwright` pulls, and that session must not
# download browsers, so the explicit path is the supported route there:
#   ACC_CHROMIUM=/opt/pw-browsers/chromium-1194/chrome-linux/chrome ./run.sh
set -euo pipefail
cd "$(dirname "$0")"

SRC="${1:-../application-command-center.html}"
FIX="${ACC_FIX:-/tmp/acc-fixtures}"
BASE="/artifact/da80ff29-3a14-48a4-9d69-762e79ff2594/"

echo "== fixtures from $SRC"
mkdir -p "$FIX"
python3 mklive3.py "$SRC" "$FIX/index.html" --base "$BASE"
python3 shell.py "$SRC" "$FIX/served-nostate.html" --base "$BASE"
python3 mkbase2.py "$FIX/served-nostate.html" "$FIX/base.html"

if ! cmp -s "$SRC" "$FIX/base.html"; then
  echo "WARNING: the source is not its own canonical reconstruction."
  echo "That is not necessarily wrong, but the reconstruction is the edit base, not the file."
fi

fail=0
for s in verify.js verify-upgrade.js verify-upgrade2.js; do
  echo; echo "== $s"
  ACC_FIX="$FIX" node "$s" || fail=1
done

echo; echo "== screenshots"
ACC_FIX="$FIX" node shots.js

if [ "$fail" -ne 0 ]; then echo; echo "SUITE FAILED"; exit 1; fi
echo; echo "ALL SUITES PASSED. Now go and look at the screenshots."
