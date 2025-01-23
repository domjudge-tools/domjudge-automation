import json
import requests
from urllib.parse import urljoin
import random, string
from requests_toolbelt import MultipartEncoder
import os

PHPSESSID = os.environ.get("PHPSESSID")
spreadsheet_id = os.environ.get("SPREADSHEET_ID")

# # Universities data
# with open("universities.json", encoding="utf8") as f:
#     universities = json.load(f)

# Dynamics
# URL and headers
cookies = {
    "domjudge_refresh": "1",
    "domjudge_scorefilter": "%5B%5D",
    "domjudge_refresh": "1",
    "PHPSESSID": PHPSESSID,
}


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


def create_affiliations():
    url = "https://bircpc.ir/jury/affiliations/add"

    for uni_fa_name, university in universities.items():
        if university["id"]:
            continue

        # Prepare form data
        files = {
            "team_affiliation[icpcid]": (None, ""),
            "team_affiliation[shortname]": (None, university["shortname"]),
            "team_affiliation[name]": (None, university["name"]),
            "team_affiliation[country]": (None, university["country"]),
            "team_affiliation[internalcomments]": (None, ""),
            "team_affiliation[logoFile]": ("", "", "application/octet-stream"),
            "team_affiliation[save]": (None, ""),
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
            universities[uni_fa_name]["id"] = redirect_url.split("/")[-1]
            print(
                f"Redirect URL for {university['name']}: {universities[uni_fa_name]["id"]}"
            )
        else:
            print(
                f"Failed to create affiliation for {university['name']}: {response.status_code}"
            )

    with open("universities.json", "w", encoding="utf8") as f:
        json.dump(universities, f)


def create_team(team_name, display_name, affiliation_id, username):
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
    users = users_data.split("\n")[1:]

    domjudge_users = {}
    for i, user in enumerate(users):
        _timestamp, email, team_name, uni, _count, _user1, _user2, _user3, _contact = (
            user.split(",")
        )
        username = f"T{random.randint(1000, 9999)}{i}"

        domjudge_users[username] = {
            "team": team_name,
            "uni": uni,
            "email": email,
        }

    with open("domjudge_users.json", "w", encoding="utf8") as f:
        json.dump(domjudge_users, f, ensure_ascii=False, indent=4)

    return users

users = get_users_from_sheet(spreadsheet_id)

# domjudge_users = {}

# for i, user in enumerate(users):
#     _timestamp, email, team_name, uni, _count, _user1, _user2, _user3, _contact = (
#         user.split(",")
#     )
#     affiliation_id = universities.get(uni, {"id": ""})["id"]
#     username = f"T{random.randint(1000, 9999)}{i}"
#     print(", ".join([team_name, team_name, affiliation_id, username]))

#     # TODO check team before creating to not exist
#     team_id = create_team(team_name, team_name, affiliation_id, username)
#     domjudge_users[username] = {
#         "team_id": team_id,
#         "username": username,
#         "team": team_name,
#         "uni": uni,
#         "affiliation": affiliation_id,
#         "email": email,
#     }

#     with open("domjudge_users.json", "w", encoding="utf8") as f:
#         json.dump(domjudge_users, f)
