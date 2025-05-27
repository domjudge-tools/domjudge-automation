import os
import random
import string
from pprint import pprint

from dotenv import load_dotenv

load_dotenv()

CONTEST_BASE_DIR = os.environ.get("CONTEST_BASE_DIR", "")
CONTEST_STATE_NAME = os.environ.get("CONTEST_STATE_NAME", "")

os.makedirs(CONTEST_BASE_DIR, exist_ok=True)


with open(f"{CONTEST_BASE_DIR}/team_uni_names.tsv", encoding="utf8")as f:
    team_uni_names = [l.strip().split(r"\t") for l in f.readlines() if l.strip()]
    
user_names = set()
with open(f"{CONTEST_BASE_DIR}/{CONTEST_STATE_NAME}_credentials.tsv", "w", encoding="utf8") as f:
    f.write("TeamName\tUsername\tPassword\tUniName\n")

    for team_name, uni_name in team_uni_names:
        lower = 10000
        upper = 99999

        while True:
            user_name = random.randint(lower, upper)
            if not user_name in user_names:
                user_names.add(user_name)
                break

        rand_pass = "".join(
            random.choices(string.ascii_letters + string.digits, k=5)
        ).lower()

        f.write(f"{team_name.strip()}\tT{user_name}\t{rand_pass.strip()}\t{uni_name.strip()}\n")
