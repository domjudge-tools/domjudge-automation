#!/usr/bin/env bash
set -euo pipefail

base_dir="$HOME"
MYSQL_PASSWORD="1f7HO2d6Sn"
SQL_DIR="${base_dir}/sql-backup-files"
SCOREBOARD_DIR="${base_dir}/scoreboard"
CONTEST_IDS=(1 2 3)

mkdir -p "$SCOREBOARD_DIR"

for sql_file in "$SQL_DIR"/*.sql; do
    league_prefix=$(basename "$sql_file" .sql)
    echo "🚦 Processing $league_prefix..."

    echo "🛑 Stopping domserver..."
    docker stop domserver

    echo "📥 Importing SQL file: $sql_file..."
    cat "$sql_file" | docker exec -i dj-mariadb mariadb -u root -p"$MYSQL_PASSWORD"

    echo "🚀 Starting domserver..."
    docker start domserver
    sleep 5  # Wait for server to be ready

    echo "🔑 Resetting admin password..."
    new_password=$(docker exec domserver /opt/domjudge/domserver/webapp/bin/console domjudge:reset-user-password admin | grep -oP 'New password for admin is \K.*')
    echo "✅ New password: $new_password"

    for contest_id in "${CONTEST_IDS[@]}"; do
        echo "🌍 Downloading scoreboard for Contest ID $contest_id..."

        if ./download-contest-scoreboard.sh <<< "$league_prefix"$'\n'"$contest_id"$'\n'"$new_password"; then
            zip_file="${base_dir}/scoreboard_zips/contest-${league_prefix}-${contest_id}_unfrozen_scoreboard.zip"
            temp_dir=$(mktemp -d)

            if [[ -f "$zip_file" ]]; then
                echo "📦 Unzipping $zip_file to $temp_dir..."
                if unzip -q "$zip_file" -d "$temp_dir"; then
                    output_file="${SCOREBOARD_DIR}/scoreboard-${league_prefix}-contest-${contest_id}.html"
                    cp "$temp_dir/index.html" "$output_file"
                    echo "✅ Saved scoreboard as $output_file"
                else
                    echo "❌ Failed to unzip $zip_file"
                fi
                rm -rf "$temp_dir"
            else
                echo "❌ Zip file not found even though download script reported success."
                echo "❌ I was searching for ${zip_file}"
                exit 1
            fi
        else
            echo "⚠️ Scoreboard not available for $league_prefix Contest $contest_id — skipping."
        fi
    done

    echo "✅ Done with $league_prefix"
    echo "-----------------------------"
done

echo "🎉 All leagues processed!"
