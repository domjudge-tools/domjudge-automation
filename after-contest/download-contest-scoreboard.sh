#!/usr/bin/env bash
set -euo pipefail

# contest_id=1
read -p "Enter bircpc contest_id: " contest_id

username="admin"

read -p "Enter bircpc password: " password

echo

cookie_file=$(mktemp)

echo "🌐 Fetching login page..."
login_url="https://bircpc.ir/login"
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

zip_base="https://bircpc.ir/jury/contests/$contest_id/scoreboard-zip"

echo "⬇️ Downloading unfrozen scoreboard..."
curl -s -b "$cookie_file" -L -o "contest${contest_id}_unfrozen_scoreboard.zip" "$zip_base/unfrozen/contest.zip"
echo "✅ Saved as contest${contest_id}_unfrozen_scoreboard.zip"

echo "⬇️ Downloading frozen scoreboard..."
curl -s -b "$cookie_file" -L -o "contest${contest_id}_frozen_scoreboard.zip" "$zip_base/public/contest.zip"
echo "✅ Saved as contest${contest_id}_frozen_scoreboard.zip"

rm -f "$cookie_file"
echo "🧹 Cleaned up session. All done! 🎉"
