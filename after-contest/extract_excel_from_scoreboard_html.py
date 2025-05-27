import pandas as pd
import requests
from bs4 import BeautifulSoup

def fetch_scoreboard_from_html(url_or_path):
    # Step 1: Load HTML
    if url_or_path.startswith("http://") or url_or_path.startswith("https://"):
        response = requests.get(url_or_path)
        response.raise_for_status()
        response.encoding = 'utf-8'  # Ensure correct decoding for Persian/UTF-8
        html = response.text
    else:
        with open(url_or_path, 'r', encoding='utf-8') as f:
            html = f.read()

    soup = BeautifulSoup(html, 'html.parser')
    table = soup.find("table", class_="scoreboard")

    data = []

    for row in table.find("tbody").find_all("tr"):
        if not row or row.select("td.scoresummary"):
            continue  # skip summary row

        cols = row.find_all("td")
        if len(cols) < 5:
            continue  # skip malformed rows

        rank = cols[0].text.strip()
        team_name = cols[2].text.strip()
        solved_count = cols[3].text.strip()
        total_time = cols[4].text.strip()

        problem_cells = cols[5:]
        count_first_answers = 0
        has_submissions = 0

        for cell in problem_cells:
            if "score_correct" in cell.decode():
                has_submissions = 1
                if "score_first" in cell.decode():
                    count_first_answers += 1

        data.append({
            'Team name': team_name,
            'University name': "N/A",  # No affiliation data in HTML
            'Rank': rank if rank else "N/A",
            'Count of correct answers': int(solved_count),
            'Count of first answers': count_first_answers,
            'Did they have any submissions': has_submissions
        })

    return pd.DataFrame(data)

# Replace with the path to your local HTML file or a URL
html_file_path = "http://185.7.212.13:8585/scoreboard-BCPC10-contest-2.html"
df = fetch_scoreboard_from_html(html_file_path)
print(df)

# Save to Excel (UTF-8 supported by default with openpyxl)
excel_file_path = './contest-10-2_scoreboard_from_html.xlsx'
df.to_excel(excel_file_path, index=False, engine='openpyxl')
