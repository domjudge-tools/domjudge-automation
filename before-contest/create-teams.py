import os
import json
import random
import string
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_BASE = os.environ.get("DOMJUDGE_API_BASE", "https://bircpc.ir")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
DOMJUDGE_USERNAME = os.environ.get("DOMJUDGE_USERNAME")
DOMJUDGE_PASSWORD = os.environ.get("DOMJUDGE_PASSWORD")

# Prepare session with Basic Auth for API calls
session = requests.Session()
session.auth = (DOMJUDGE_USERNAME, DOMJUDGE_PASSWORD)

# Function to download and parse sheet
def get_sheet_users(sheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv"
    print(f"📄 Downloading sheet data from {url}")
    resp = requests.get(url)
    resp.raise_for_status()

    users_data = resp.content.decode()
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
        # ts, email, team, uni, count, user_name, u2, u3, contact
        _, email, team, uni, *_ = parts[:5]
        name = parts[5].strip() or ""
        users.append({
            'team': team.strip(),
            'uni': uni.strip(),
            'email': email.strip(),
            'name': name
        })
        print(f"  • [{idx}] Parsed row: name='{name}', team='{team}', uni='{uni}', email='{email}'")
    return users

# Functions to fetch existing teams and usernames via pure API

def get_existing_teams():
    url = f"{API_BASE}/api/v4/teams"
    print(f"🔍 Fetching existing teams from {url}")
    resp = session.get(url)
    resp.raise_for_status()
    teams = resp.json()
    print(f"🧮 Found {len(teams)} existing teams")
    return {t['name'] for t in teams}


def get_existing_usernames():
    url = f"{API_BASE}/api/v4/users"
    print(f"🔍 Fetching existing usernames from {url}")
    resp = session.get(url)
    resp.raise_for_status()
    users = resp.json()
    usernames = {u['username'] for u in users}
    print(f"🧮 Found {len(usernames)} existing usernames")
    return usernames

# Main flow
sheet_users = get_sheet_users(SPREADSHEET_ID)
existing_teams = get_existing_teams()
existing_usernames = get_existing_usernames()

total_rows = len(sheet_users)
to_create = [u for u in sheet_users if u['team'] not in existing_teams]
print(f"⏳ {len(to_create)} new teams to create out of {total_rows} sheet rows")

# Save preview file
with open('teams_to_create.json', 'w', encoding='utf8') as f:
    json.dump(to_create, f, indent=2, ensure_ascii=False)
print("💾 Written teams_to_create.json")

confirm = input(f"Check 'teams_to_create.json': found {len(to_create)} non-existing teams. Create them and users? (y/n): ")
if confirm.lower() != 'y':
    print("❌ Aborting.")
    exit(0)

# Create teams and users via basic-authenticated API calls
for idx, entry in enumerate(to_create, start=1):
    # Generate unique random username
    while True:
        rand_user = f"T{random.randint(1000,9999)}{idx}"
        if rand_user not in existing_usernames:
            existing_usernames.add(rand_user)
            break
    # Generate random password
    rand_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Create team
    team_payload = {
        'name': entry['team'],
        'display_name': entry['team'],
        'organization_id': entry['uni'],
        'public_description': "",
    }
    print(f"🚀 [{idx}/{len(to_create)}] Creating team '{entry['team']}' via API")
    team_resp = session.post(f"{API_BASE}/api/v4/teams", json=team_payload)
    if team_resp.status_code != 201:
        print(f"❌ Failed team '{entry['team']}': {team_resp.status_code} - {team_resp.text}")
        continue
    team_id = team_resp.json().get('id')
    print(f"✅ Team created with ID {team_id}")

    # Create user
    user_payload = {
        'username': rand_user,
        'name': entry['name'] or rand_user,
        'email': entry['email'],
        'password': rand_pass,
        'enabled': True,
        'team_id': team_id,
        'roles': ['team']
    }
    print(f"👤 Creating user '{rand_user}' for team ID {team_id} via API")
    user_resp = session.post(f"{API_BASE}/api/v4/users", json=user_payload)
    if user_resp.status_code == 201:
        print(f"✅ User '{rand_user}' created with password '{rand_pass}'")
    else:
        print(f"❌ Failed user '{rand_user}': {user_resp.status_code} - {user_resp.text}")
