#!/usr/bin/env zsh
set -e

cd "$(dirname "$0")/.."

OUTDIR="dist"
NAME="trading_gate_pack_v1_device_b"
ZIPFILE="$OUTDIR/$NAME.zip"
SUMFILE="$OUTDIR/SHA256SUMS.txt"

rm -rf "$OUTDIR"
mkdir -p "$OUTDIR"

zip -r -X "$ZIPFILE" VERSION README_NDA.md TRADING_PRECHECK_RUNBOOK.md policy schema reference scripts tools

shasum -a 256 "$ZIPFILE" > "$SUMFILE"
