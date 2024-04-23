import datetime
import random
import math
import sqlite3
import json
from github import Github
import os


def generate_new_aphorism():
    NUM_ENTRIES=297

    # Generate a random number seeded by the day, mapped to number of entries in sqlilite db
    now = datetime.datetime.now()
    seed_value = f"{now.year}{now.month}{now.day}"
    random.seed(seed_value)

    entry_id = math.floor(random.random()*297)
    print(f"using seed: {entry_id}")

    conn = sqlite3.connect('aphorisms.db')
    cursor = conn.cursor()

    cursor.execute(f"SELECT * FROM aphorisms WHERE id = {entry_id}")
    row = cursor.fetchone()

    if row:
        [dump, aphorism, number, work, work_link] = row
        json_data = {
            "aphorism": aphorism,
            "number": number,
            "work": work,
            "workLink": work_link
        }
        print(json_data)
        return json_data
    else:
        print(f"No entry found with id {entry_id}")

def commit_new_aphorism():
    try:
        aphorism_dict = generate_new_aphorism()
        token = os.environ['GITHUB_TOKEN']
        g = Github(token)
        repo = g.get_user().get_repo('aphorism-a-day')
        file_path = 'website/aphorism.json'  # Path to the file you want to update
        commit_message = f'🤖 update aphorism / {aphorism_dict["number"]} {aphorism_dict["work"]} / {datetime.date.today() } 🤖'  # Commit message
        new_content = json.dumps(aphorism_dict, ensure_ascii=False)  # New content for the file

        contents = repo.get_contents(file_path)
        repo.update_file(contents.path, commit_message, new_content, contents.sha)

        print('Commit created successfully!')
    except Exception as e:
        print(f'Error: {e}')

commit_new_aphorism()