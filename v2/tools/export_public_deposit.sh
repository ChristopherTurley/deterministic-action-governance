#!/bin/sh
set -eu

if [ "${1:-}" = "" ]; then
  echo "USAGE: v2/tools/export_public_deposit.sh /ABS/PATH/TO/deterministic-action-governance"
  exit 2
fi

DEST="$1"
if [ ! -d "$DEST" ]; then
  echo "ERROR: destination folder does not exist: $DEST"
  exit 2
fi

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

OUT="$DEST/vera_v2_public_deposit"
mkdir -p "$OUT"
mkdir -p "$OUT/public"
mkdir -p "$OUT/scripts"

cp -f v2/docs/demo_index.md "$OUT/" 2>/dev/null || true
cp -f v2/docs/side_effects_contract_v1.md "$OUT/" 2>/dev/null || true
cp -f v2/docs/coat_v1.md "$OUT/" 2>/dev/null || true
cp -f v2/docs/bridge_v1.md "$OUT/" 2>/dev/null || true

cp -f v2/docs/public/README_PUBLIC.md "$OUT/public/"
cp -f v2/docs/public/ONE_PAGER.md "$OUT/public/"
cp -f v2/docs/public/APPLE_GAP_MAP_MONTH12.md "$OUT/public/"

cp -f v2/demo/scripts/run_all_demos.sh "$OUT/scripts/" 2>/dev/null || true

echo "DONE: exported to $OUT"
