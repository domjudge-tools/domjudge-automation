import pandas as pd
import requests

DOMJUDGE_BASE_URL = "https://bircpc.ir"
CONTEST_ID = 3

# Step 1: Fetch scoreboard data
scoreboard_url = f"{DOMJUDGE_BASE_URL}/api/v4/contests/{CONTEST_ID}/scoreboard"
scoreboard_response = requests.get(scoreboard_url, params={"public": True})
scoreboard_response.raise_for_status()
scoreboard_data = scoreboard_response.json()
scoreboard_rows = scoreboard_data.get("rows", [])

# Step 2: Fetch all teams for the contest
teams_url = f"{DOMJUDGE_BASE_URL}/api/v4/teams"
teams_response = requests.get(teams_url, params={"cid": CONTEST_ID})
teams_response.raise_for_status()
teams_list = teams_response.json()

# Build a mapping from team ID to team info (name + affiliation)
team_info_map = {
    team["id"]: {
        "name": team.get("name", "Unknown"),
        "affiliation": team.get("affiliation", "N/A")
    }
    for team in teams_list
}

# Step 3: Combine data
data = []

for team in scoreboard_rows:
    team_id = team["team_id"]
    team_info = team_info_map.get(team_id, {"name": "Unknown", "affiliation": "N/A"})

    rank = team["rank"]
    solved_count = team.get("score", {}).get("num_solved", 0)
    count_first_answers = sum(1 for p in team["problems"] if p.get("first_to_solve", False))
    has_submissions = int(any((p["num_judged"] > 0 or p["num_pending"] > 0) for p in team["problems"]))

    data.append({
        'Team name': team_info["name"],
        'University name': team_info["affiliation"],
        'Rank': rank,
        'Count of correct answers': solved_count,
        'Count of first answers': count_first_answers,
        'Did they have any submissions': has_submissions
    })

# Step 4: Export to DataFrame and Excel
df = pd.DataFrame(data)
print(df)

excel_file_path = './contest_scoreboard_from_api.xlsx'
df.to_excel(excel_file_path, index=False, engine='openpyxl')
