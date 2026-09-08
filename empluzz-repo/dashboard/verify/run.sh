#!/usr/bin/env bash
# Build the fixtures and run all three suites. 56 assertions.
#
#   ./run.sh [path/to/authored-build.html]
#
# Defaults to the newest authored build committed in ../ .
set -euo pipefail
cd "$(dirname "$0")"

# Never hardcode a build name here. A build is named for the live version it came
# from, so a literal becomes a lie the next time one ships. Pick the newest by the
# version number in the filename.
SRC="${1:-$(ls -1 ../application-command-center-*.html 2>/dev/null | sort -t- -k4,4n | tail -1)}"
if [ -z "$SRC" ]; then echo "no authored build found in ../"; exit 1; fi
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
