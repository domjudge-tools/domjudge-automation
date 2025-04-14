#!/usr/bin/env bash
set -euo pipefail

read -p "Enter prefix for zip files (for different leagues): " league_prefix
read -p "Enter bircpc contest_id: " contest_id
username="admin"
read -p "Enter bircpc password: " password
echo

base_dir="$HOME"
SCOREBOARD_DIR="$base_dir/scoreboard_zips"
mkdir -p "$SCOREBOARD_DIR"

login_url="https://bircpc.ir/login"
cookie_file=$(mktemp)

echo "🌐 Waiting for domserver to be ready..."
for i in {1..30}; do
    if curl -s -o /dev/null -w "%{http_code}" "$login_url" | grep -q "200"; then
        echo "✅ Domserver is up!"
        break
    fi
    echo "⏳ Domserver not ready yet... retrying in 2s"
    sleep 2
done

echo "🌐 Fetching login page..."
login_page_html=$(curl -s -c "$cookie_file" "$login_url")

echo "🔍 Extracting CSRF token..."
csrf_token=$(echo "$login_page_html" | sed -n 's/.*name="_csrf_token" value="\([^"]*\)".*/\1/p')
if [[ -z "$csrf_token" ]]; then
  echo "❌ CSRF token not found. Exiting."
  rm -f "$cookie_file"
  exit 1
fi
echo "✅ CSRF token extracted."

echo "🔐 Logging in as '$username'..."
curl -s -b "$cookie_file" -c "$cookie_file" -L \
  --data-urlencode "_username=$username" \
  --data-urlencode "_password=$password" \
  --data-urlencode "_csrf_token=$csrf_token" \
  "$login_url" > /dev/null
echo "✅ Logged in successfully."

zip_url="https://bircpc.ir/jury/contests/$contest_id/scoreboard-zip/unfrozen/contest.zip"
output_file="${SCOREBOARD_DIR}/contest-${league_prefix}-${contest_id}_unfrozen_scoreboard.zip"

echo "⬇️ Downloading scoreboard zip..."
status_code=$(curl -s -w "%{http_code}" -o "$output_file" -b "$cookie_file" -L "$zip_url")

rm -f "$cookie_file"

if [[ "$status_code" != "200" ]]; then
    echo "❌ Failed to download scoreboard (HTTP $status_code)"
    rm -f "$output_file"
    exit 1
fi

echo "✅ Zip file saved to: $output_file"
