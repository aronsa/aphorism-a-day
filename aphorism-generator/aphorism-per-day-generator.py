import datetime
import random
import math
import sqlite3
import json
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
    json_data = json.dumps(json_data, ensure_ascii=False)
    print(json_data)
    with(open("../website/aphorism.json","w") as file):
        file.write(json_data)
else:
    print(f"No entry found with id {entry_id}")
