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

def login():
    login_url = f"{API_BASE}/login"
    print(f"🔗 Connecting to {login_url}")
    # Wait until login page is accessible
    for attempt in range(1, 31):
        try:
            response = session.get(login_url)
            if response.ok:
                print(f"✅ Login page reachable (attempt {attempt})")
                break
        except requests.RequestException as e:
            print(f"⚠️ Attempt {attempt} failed: {e}")
        time.sleep(2)
    else:
        print("❌ Could not reach login page after 30 attempts. Exiting.")
        return False

    print("🌐 Fetching CSRF token from login page")
    soup = BeautifulSoup(response.content, "html.parser")
    csrf_input = soup.find('input', {'name': '_csrf_token'})
    if not csrf_input or not csrf_input.get('value'):
        print("❌ CSRF token not found. Exiting.")
        return False
    csrf_token = csrf_input['value']
    print(f"🔑 CSRF token extracted: {csrf_token}")

    print(f"👤 Logging in as '{DOMJUDGE_USERNAME}'...")
    login_data = {
        '_username': DOMJUDGE_USERNAME,
        '_password': DOMJUDGE_PASSWORD,
        '_csrf_token': csrf_token
    }
    login_resp = session.post(login_url, data=login_data)
    if login_resp.ok and "Logout" in login_resp.text:
        print("🔓 Logged in successfully.")
        return True
    else:
        print(f"❌ Login failed (status {login_resp.status_code}).")
        return False

# Perform login
if not login():
    exit(1)


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

# Create teams with confirmation prompt
for idx, u in enumerate(to_create, start=1):
    prompt = input(f"Create team '{u['team']}' for uni '{u['uni']}' with username '{u['username']}'? (y/n): ")
    if prompt.lower() != 'y':
        print(f"⏭️ Skipped team '{u['team']}'")
        continue
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
