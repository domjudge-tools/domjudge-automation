import json
import os
import random
import string

import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
API_BASE = os.environ.get("DOMJUDGE_API_BASE", "https://bircpc.ir")
SPREADSHEET_ID = os.environ.get("SPREADSHEET_ID")
CONTEST_ID = os.environ.get("DOMJUDGE_CONTEST_ID", 3)
DOMJUDGE_USERNAME = os.environ.get("DOMJUDGE_USERNAME", "")
DOMJUDGE_PASSWORD = os.environ.get("DOMJUDGE_PASSWORD", "")

if not DOMJUDGE_USERNAME or not DOMJUDGE_PASSWORD :
    print("Both Username and Password are required.")
    exit()

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
    # Save raw sheet data for inspection
    with open('sheet_raw.csv', 'w', encoding='utf-8') as raw_file:
        raw_file.write(users_data)
    print("💾 Saved raw sheet data to 'sheet_raw.csv' for review")

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
        # ts, email, team, uni, count, user_name, extra1, extra2, phone
        ts, email, team, uni, count, name1, name2, name3 , phone = parts[:9]
        names = ", ".join(name.strip() for name in [name1, name2, name3] if name.strip())
        users.append({
            'team': team.strip(),
            'uni': uni.strip(),
            'email': email.strip(),
            'names': names,
            'phone': phone.strip()
        })
        print(f"  • [{idx}] Parsed row: team='{team}', email='{email}', phone='{phone}'")
    return users

# Fetch existing teams and their IDs
def get_existing_teams_and_ids():
    url = f"{API_BASE}/api/v4/contests/{CONTEST_ID}/teams"
    print(f"🔍 Fetching existing teams from {url}")
    resp = session.get(url)
    resp.raise_for_status()
    teams = resp.json()
    print(f"🧮 Found {len(teams)} existing teams")
    return {t['name']: t['id'] for t in teams}

# Fetch existing users and their IDs
def get_existing_users_and_ids():
    url = f"{API_BASE}/api/v4/users"
    print(f"🔍 Fetching existing users from {url}")
    resp = session.get(url)
    resp.raise_for_status()
    users = resp.json()
    print(f"🧮 Found {len(users)} existing users")
    return {u['username']: u['id'] for u in users}

# Main script
sheet_users = get_sheet_users(SPREADSHEET_ID)
existing_teams = get_existing_teams_and_ids()
existing_users = get_existing_users_and_ids()

# Prepare uniqueness sets
existing_team_names = set(existing_teams.keys())
existing_ids = set(existing_teams.values()) | set(existing_users.values())
existing_usernames = set(existing_users.keys())

# Determine which teams to create
total_rows = len(sheet_users)
to_create = [u for u in sheet_users if u['team'] not in existing_team_names]
print(f"⏳ {len(to_create)} new teams to create out of {total_rows} sheet rows")

# Save preview file
with open('teams_to_create.json', 'w', encoding='utf8') as f:
    json.dump(to_create, f, indent=2, ensure_ascii=False)
print("💾 Written teams_to_create.json. Verify before proceeding.")

confirm = input(f"Check 'teams_to_create.json': found {len(to_create)} non-existing teams. Create them and users? (y/n): ")
if confirm.lower() != 'y':
    print("❌ Aborting.")
    exit(0)

# Helper to generate unique numeric ID
def generate_unique_id(existing_ids, lower=10000, upper=99999):
    while True:
        new_id = random.randint(lower, upper)
        if new_id not in existing_ids:
            existing_ids.add(new_id)
            return new_id

# Accumulate created user info for emailing later
created_users = []

# Create teams and corresponding users
for idx, entry in enumerate(to_create, start=1):
    # Generate a single unique numeric ID
    unique_id = generate_unique_id(existing_ids)
    # Derive username from the same ID
    rand_user = f"T{unique_id}"
    # Ensure username uniqueness
    if rand_user in existing_usernames:
        rand_user = f"T{unique_id}{idx}"
    existing_usernames.add(rand_user)
    # Generate random password
    rand_pass = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

    # Create team with shared ID and description as name and phone
    team_payload = {
        'id': unique_id,
        'name': entry['team'],
        'display_name': entry['team'],
        'organization_id': entry['uni'],
        'description': f"{entry["names"]} | {entry["phone"]}",
    }
    print(f"🚀 [{idx}/{len(to_create)}] Creating team '{entry['team']}' with ID {unique_id}")
    team_resp = session.post(f"{API_BASE}/api/v4/contests/{CONTEST_ID}/teams", json=team_payload)
    if team_resp.status_code != 201:
        print(f"❌ Failed team '{entry['team']}': {team_resp.status_code} - {team_resp.text}")
        continue
    team_id = team_resp.json()["id"]
    print(f"✅ Team '{entry['team']}' created with ID {unique_id}")

    # Create user with same ID and email
    user_payload = {
        'id': unique_id,
        'username': rand_user,
        'name': entry['team'],
        'email': entry['email'],
        'password': rand_pass,
        'enabled': True,
        'team_id': team_id,
        'roles': ['team']
    }
    print(f"👤 Creating user '{rand_user}' with ID {unique_id} for team ID {unique_id}")
    user_resp = session.post(f"{API_BASE}/api/v4/users", json=user_payload)
    if user_resp.status_code == 201:
        print(f"✅ User '{rand_user}' created with password '{rand_pass}'")
        created_users.append({
            'team': entry['team'],
            'id': user_resp.json()["id"],
            'username': rand_user,
            'names': entry['names'],
            'email': entry['email'],
            'phone': entry['phone'],
            'password': rand_pass
        })
    else:
        print(f"❌ Failed user '{rand_user}': {user_resp.status_code} - {user_resp.text}")

# Save created user info for emailing
with open('created_users.json', 'w', encoding='utf-8') as f:
    json.dump(created_users, f, indent=2, ensure_ascii=False)
print("💾 Written created_users.json with all new account details.")