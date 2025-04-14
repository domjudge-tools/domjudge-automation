#!/usr/bin/env bash
set -euo pipefail

zip_file="$1"

if [[ ! -f "$zip_file" ]]; then
  echo "❌ File '$zip_file' does not exist."
  exit 1
fi

serve_dir=$(mktemp -d)

cleanup() {
  echo "🧹 Cleaning up temporary files..."
  rm -rf "$serve_dir"
  echo "✅ Done. Goodbye!"
}
trap cleanup EXIT INT TERM

echo "📦 Unzipping '$zip_file' into '$serve_dir'..."
unzip -q "$zip_file" -d "$serve_dir"
echo "✅ Unzipped successfully."

echo "🚀 Serving on http://localhost:3838 ..."
cd "$serve_dir"
python3 -m http.server 3838
