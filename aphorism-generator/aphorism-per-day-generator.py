import datetime
import random
import math
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
    print(f"using generated entry number: {entry_id}")
    try:
        return get_aphorism(entry_id)
    except Exception as e:
        print(f"Error: {e}")
        return None


def get_aphorism(entry_id):
    # open json file
    with open('aphorism-store.json', 'r') as file:
        data = json.load(file)
        # for now, only beyond good and evil is supported
        bge = data.get("aphorisms").get("Beyond Good and Evil")
        metadata = data.get("metadata").get("work").get("Beyond Good and Evil")
        print(f"bge: {bge.get(str(entry_id), 'no entry')}")
        aphorism = bge.get(str(entry_id))

        number = entry_id
        work_link = metadata.get("link")
        work = metadata.get("title")

        json_data = {
            "aphorism": aphorism,
            "number": number,
            "work": work,
            "workLink": work_link
        }
        print(json_data)
        return json_data

print("generating new aphorism")
aphorism = generate_new_aphorism()
print(aphorism)
with open('../website/aphorism.json', 'w') as file:
    json.dump(aphorism, file)
