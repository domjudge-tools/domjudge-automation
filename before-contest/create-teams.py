import json
import requests
from urllib.parse import urljoin
import random, string
from requests_toolbelt import MultipartEncoder
from dotenv import load_dotenv
import os
import requests
import os
import time
from bs4 import BeautifulSoup

# load_dotenv(r"D:\dev\domjudge\docker-compose-scripts\.env")

username = "admin"
password = "rpM7aJH3ZnKifBQ_"
# spreadsheet_id = os.environ.get("SPREADSHEET_ID")
spreadsheet_id = "1C5A4SJK7vEbgasJP5LdTg3FsqhhZuwy9PN6vpNvGyEs"

headers = {
    "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
    "accept-language": "en-US,en;q=0.9,fa;q=0.8",
    "cache-control": "no-cache",
    "dnt": "1",
    "origin": "https://bircpc.ir",
    "pragma": "no-cache",
    "priority": "u=0, i",
    "referer": "https://bircpc.ir/jury/affiliations/add",
    "sec-ch-ua": '"Google Chrome";v="131", "Chromium";v="131", "Not_A Brand";v="24"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"Windows"',
    "sec-fetch-dest": "document",
    "sec-fetch-mode": "navigate",
    "sec-fetch-site": "same-origin",
    "sec-fetch-user": "?1",
    "upgrade-insecure-requests": "1",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0.0.0 Safari/537.36",
}

def login_bircpc():
    # league_prefix = input("Enter prefix for zip files (for different leagues): ")
    # contest_id = input("Enter bircpc contest_id: ")

    login_url = "https://bircpc.ir/login"
    session = requests.Session()

    print("🌐 Waiting for domserver to be ready...")
    for _ in range(30):
        try:
            response = session.get(login_url)
            if response.status_code == 200:
                print("✅ Domserver is up!")
                break
        except requests.RequestException:
            pass
        print("⏳ Domserver not ready yet... retrying in 2s")
        time.sleep(2)
    else:
        print("❌ Domserver not available. Exiting.")
        return

    print("🌐 Fetching login page...")
    login_page_html = response.content

    print("🔍 Extracting CSRF token...")
    soup = BeautifulSoup(login_page_html, "html.parser")
    csrf_input = soup.find('input', {'name': '_csrf_token'})
    if not csrf_input or not csrf_input['value']:
        print("❌ CSRF token not found. Exiting.")
        return

    csrf_token = csrf_input['value']
    print(f"✅ CSRF token extracted., {csrf_token}")

    print(f"🔐 Logging in as '{username}'...")
    login_data = {
        "_username": username,
        "_password": password,
        "_csrf_token": csrf_token
    }

    login_response = session.post(login_url, data=login_data)
    if login_response.ok and "Logout" in login_response.text:
        print("✅ Logged in successfully.")
    else:
        print("❌ Login failed.")
        return
    print(session.cookies)
    return session.cookies

cookies = login_bircpc()


def create_team(team_name, display_name, username, affiliation_id=""):
    url = "https://bircpc.ir/jury/teams/add"
    files = {
        "team[icpcid]": (None, ""),
        "team[label]": (None, ""),
        "team[name]": (None, team_name),
        "team[displayName]": (None, display_name),
        "team[category]": (None, "3"),
        "team[publicdescription]": (None, ""),
        "team[affiliation]": (None, affiliation_id),
        "team[penalty]": (None, "0"),
        "team[location]": (None, ""),
        "team[internalcomments]": (None, ""),
        "team[enabled]": (None, "1"),
        "team[addUserForTeam]": (None, "create-new-user"),
        "team[existingUser]": (None, "1"),
        "team[newUsername]": (None, username),
        "team[photoFile]": ("", "", "application/octet-stream"),
        "team[save]": (None, ""),
    }

    boundary = "----WebKitFormBoundary" + "".join(
        random.sample(string.ascii_letters + string.digits, 16)
    )
    m = MultipartEncoder(fields=files, boundary=boundary)
    headers["Content-Type"] = m.content_type

    # Make POST request
    response = requests.post(
        url, headers=headers, cookies=cookies, data=m, allow_redirects=False
    )

    # Check for redirect
    if response.status_code in [301, 302] and "Location" in response.headers:
        redirect_url = urljoin(url, response.headers["Location"])
        team_id = redirect_url.split("/")[-1]
        print(f"Redirect URL for team {team_name}: {team_id}")
        return team_id
    else:
        print(f"Failed to create team {team_name}: {response.status_code}")


def get_users_from_sheet(spreadsheet_id):
    url = f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv"
    response = requests.get(url)
    users_data = response.content.decode()
    users = users_data.split("\n")[2:]

    domjudge_users = {}
    for i, user in enumerate(users):
        print(user)
        _timestamp, email, team_name, uni, _count, _user1, _user2, _user3, _contact = (
            user.split(",")
        )
        username = f"T{random.randint(1000, 9999)}{i}"

        domjudge_users[username] = {
            "team": team_name,
            "uni": uni,
            "email": email,
        }

    with open("domjudge_users_before.json", "w", encoding="utf8") as f:
        json.dump(domjudge_users, f, ensure_ascii=False, indent=4)

    return users


# TODO it should return cleaned data
users = get_users_from_sheet(spreadsheet_id)

domjudge_users = {}

for i, user in enumerate(users):
    _timestamp, email, team_name, uni, _count, _user1, _user2, _user3, _contact = (
        user.split(",")
    )
    affiliation_id = ""  # universities.get(uni, {"id": ""})["id"]
    username = f"T{random.randint(1000, 9999)}{i}"
    print(", ".join([team_name, team_name, affiliation_id, username]))

    # TODO check team before creating to not exist
    team_id = create_team(
        team_name=team_name,
        display_name=team_name,
        username=username,
        affiliation_id=affiliation_id,
    )
    domjudge_users[username] = {
        "team_id": team_id,
        "username": username,
        "team": team_name,
        "uni": uni,
        "affiliation": affiliation_id,
        "email": email,
    }

    with open("domjudge_users_after.json", "w", encoding="utf8") as f:
        json.dump(domjudge_users, f, indent=4, ensure_ascii=False)
