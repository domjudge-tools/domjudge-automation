import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build

# Load scoreboard data
print("📥 Loading scoreboard data...")
df = pd.read_excel('./contest_scoreboard_from_api.xlsx')

# New contest columns
prefix = "7th"
columns = {
    'Rank': f'{prefix} rank',
    'Count of first answers': f'{prefix} First Ans',
    'Count of correct answers': f'{prefix} True Ans',
    'Did they have any submissions': f'{prefix} did submit',
    'Points': f'{prefix} Points'
}

# Authenticate
print("🔐 Authenticating with Google Sheets API...")
SHEET_ID = "18Xmrbqb4uE-5lj3mDgEEBFMW6_rc9-HFvnDDzaku_68"
RANGE_NAME = "Sheet1"
creds = Credentials.from_service_account_file(
    "./chatbot-book-scrapper-ac99a3d0f899.json",
    scopes=["https://www.googleapis.com/auth/spreadsheets"]
)
client = gspread.authorize(creds)
sheet = client.open_by_key(SHEET_ID).worksheet(RANGE_NAME)

# Read current sheet
print("📄 Reading current data from sheet...")
existing_data = sheet.get_all_values()
headers = existing_data[0]
rows = existing_data[1:]

# Team name → row index (1-based)
print("🔍 Indexing existing teams...")
team_column_index = headers.index("Team name")
team_row_map = {row[team_column_index].strip(): idx + 2 for idx, row in enumerate(rows)}

# Insert new contest columns before "Total PTR"
print(f"🧱 Inserting new columns for {prefix} contest before 'Total PTR'...")
insert_at = headers.index("Total PTR")
new_headers = list(columns.values())
headers = headers[:insert_at] + new_headers + headers[insert_at:]
sheet.update(values=[headers], range_name='A1')

# Update existing teams
print("🔁 Updating existing teams with new contest data...")
updated_teams = set()

for _, row in df.iterrows():
    team = row['Team name'].strip()
    updated_teams.add(team)

    if team in team_row_map:
        row_idx = team_row_map[team]

        # Only update the new contest columns
        for key in columns:
            col_name = columns[key]
            col_index = headers.index(col_name) + 1  # 1-based index for gspread

            value = "=CALC_CONTEST_POINTS()" if key == "Points" else row.get(key, "")
            sheet.update_cell(row_idx, col_index, value)

        print(f"✅ Updated: {team}")

# Append new teams
print("➕ Checking for new teams to append...")
current_row_count = len(rows) + 1
for _, row in df.iterrows():
    team = row['Team name'].strip()
    if team not in team_row_map:
        new_row = [''] * len(headers)
        new_row[team_column_index] = team

        for key in columns:
            col_index = headers.index(columns[key])
            if key == "Points":
                new_row[col_index] = "=CALC_CONTEST_POINTS()"
            else:
                value = row.get(key, "")
                try:
                    new_row[col_index] = int(value) if str(value).isdigit() else value
                except:
                    new_row[col_index] = value

        sheet.append_row(new_row, value_input_option="USER_ENTERED")
        print(f"🆕 Added new team to sheet: {team}")

print("✅ All teams processed.")

# Group non-Points columns
print("📊 Grouping non-Points columns...")
service = build('sheets', 'v4', credentials=creds)
group_column_titles = [v for k, v in columns.items() if "Points" not in v]
group_start = headers.index(group_column_titles[0])
group_end = group_start + len(group_column_titles) - 1
sheet_id = sheet._properties['sheetId']

group_request = {
    "requests": [
        {
            "addDimensionGroup": {
                "range": {
                    "sheetId": sheet_id,
                    "dimension": "COLUMNS",
                    "startIndex": group_start,
                    "endIndex": group_end + 1
                }
            }
        }
    ]
}

service.spreadsheets().batchUpdate(
    spreadsheetId=SHEET_ID,
    body=group_request
).execute()

print(f"📦 Grouped columns: {group_column_titles[0]} to {group_column_titles[-1]}")
print("✅ Script finished successfully.")
