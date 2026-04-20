#!/usr/bin/env bash
set -euo pipefail

TARGET="/Users/tglauner/Library/CloudStorage/Dropbox/2) TG Investments and Research/Projects/ing_validation"
SOURCE_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

mkdir -p "$TARGET"
cp -R "$SOURCE_DIR"/* "$TARGET/"

echo "Exported app_architecture contents to: $TARGET"
