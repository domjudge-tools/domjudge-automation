import os

import requests
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.environ["DOMJUDGE_API_BASE"]
PHPSESSID = os.environ["PHPSESSID"]

cookies = {
    "PHPSESSID": PHPSESSID,
}

headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
}

params = {
    "_": "1743686975009",
}

users_start, users_end = 4, 300
teams_start, teams_end = 4, 300
unis_start, unis_end = 1000, 1000

for i in range(users_start, users_end):
    url = f"{BASE_URL}/jury/users/{i}/delete"
    response = requests.post(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(f"User {i}/{users_end} deleted.", end="\r")
print("All Users have been Deleted")

for i in range(teams_start, teams_end):
    url = f"{BASE_URL}/jury/teams/{i}/delete"
    response = requests.post(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(f"Team {i}/{teams_end} deleted.", end="\r")

print("All Teams have been Deleted")

for i in range(unis_start, unis_end):
    url = f"{BASE_URL}/jury/affiliations/{i}/delete"
    response = requests.post(
        url,
        params=params,
        cookies=cookies,
        headers=headers,
    )
    print(f"University {i}/{unis_end} deleted.", end="\r")

print("All Unis have been Deleted")
