#!/usr/bin/env zsh
set -e
REFERENCE_PATH="$1"
CURRENT_PATH="$2"
diff -u "$REFERENCE_PATH" "$CURRENT_PATH"
