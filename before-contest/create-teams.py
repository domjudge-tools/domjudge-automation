import os
import json
import random
import requests
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import time

# Load environment variables
load_dotenv()
API_BASE = os.environ.get("DOMJUDGE_API_BASE", "https://bircpc.ir")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
DOMJUDGE_USERNAME = os.environ.get("DOMJUDGE_USERNAME")
DOMJUDGE_PASSWORD = os.environ.get("DOMJUDGE_PASSWORD")

session = requests.Session()

def get_sheet_users(sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    print(f"📄 Downloading sheet data from {url}")
    resp = requests.get(url)
    resp.raise_for_status()
    
    users_data = resp.content.decode()
    # Save raw sheet data for inspection
    with open('sheet_raw.csv', 'w', encoding='utf-8') as rawf:
        rawf.write(users_data)
    print("💾 Saved raw sheet data to 'sheet_raw.csv'")

    lines = users_data.splitlines()[2:]
    print(f"🧮 Retrieved {len(lines)} records from sheet")
    users = []
    for idx, line in enumerate(lines, start=1):
        if not line.strip():
            continue
        parts = line.split(',')
        if len(parts) < 9:
            print(f"⚠️ Skipping malformed line #{idx}: {line}")
            continue
        ts, email, team, uni, count, u1, u2, u3, contact = parts[:9]
        username = u1 or f"T{random.randint(1000,9999)}"
        users.append({
            'team': team.strip(),
            'uni': uni.strip(),
            'email': email.strip(),
            'username': username.strip()
        })
        print(f"  • [{idx}] Parsed user: username={username}, team={team}, uni={uni}")
    return users


def get_existing_teams():
    url = f"{API_BASE}/api/v4/teams"
    print(f"🔍 Fetching existing teams from {url}")
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()
    print(f"🧮 Found {len(data)} existing teams")
    return {t['name'] for t in data}


def get_existing_usernames():
    url = f"{API_BASE}/api/v4/accounts"
    print(f"🔍 Fetching existing user accounts from {url}")
    resp = session.get(url)
    resp.raise_for_status()
    data = resp.json()
    print(f"🧮 Found {len(data)} existing accounts")
    return {u['username'] for u in data}

# Fetch data
sheet_users = get_sheet_users(SPREADSHEET_ID)
existing_teams = get_existing_teams()
# existing_users = get_existing_usernames()

# Determine which teams to create
new_entries = len(sheet_users)
to_create = [u for u in sheet_users if u['team'] not in existing_teams]
print(f"⏳ {len(to_create)} new teams to create out of {new_entries} sheet entries")

# Save payloads for review
with open('teams_to_create.json', 'w', encoding="utf8") as f:
    json.dump(to_create, f, indent=2, ensure_ascii=False)
print("💾 Written teams_to_create.json")

# Confirmation before creation
confirm = input(f"Check 'teams_to_create.json': found {len(to_create)} non-existing teams. Do you want to create them? (y/n): ")
if confirm.lower() != 'y':
    print("❌ Aborting team creation.")
    exit(0)

# Create teams
for idx, u in enumerate(to_create, start=1):
    payload = {
        'name': u['team'],
        'display_name': u['team'],
        'organization_id': u['uni'],
        'public_description': "",
    }
    print(f"🚀 [{idx}/{len(to_create)}] Creating team '{u['team']}' with payload: {payload}")
    post_url = f"{API_BASE}/api/v4/teams"
    resp = session.post(post_url, json=payload)
    if resp.status_code == 201:
        print(f"✅ Successfully created team '{u['team']}' (201)")
    else:
        print(f"❌ Failed to create '{u['team']}': {resp.status_code} - {resp.text}")
