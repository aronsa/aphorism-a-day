from bs4 import BeautifulSoup
import re
import sqlite3


# Read the HTML file
with open('beyond-good-and-evil.html', 'r') as file:
    html_content = file.read()
    soup = BeautifulSoup(html_content, 'html.parser')
    aphorisms = {}
    prev_number = -1
    for p in soup.find_all('p'):
        t = p.text
        # find first period
        splits = re.split(r'\.', t, 1)
        if(len(splits) == 2):
            try:
                string_containing_aphorism_number = str(int(splits[0]))
                aphorism_number = int(re.match(r"[0-9]*", string_containing_aphorism_number).group())
                print(aphorism_number)
                prev_number = aphorism_number
                aphorism_text = splits[1]
                aphorisms[aphorism_number]= aphorism_text
            except ValueError:
                aphorisms[prev_number] = aphorisms[prev_number] + splits[0]

# Now, load all of the aphorisms in to the DB
conn = sqlite3.connect('aphorisms.db')
cursor = conn.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS aphorisms (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        aphorism TEXT NOT NULL,
        number INTEGER NOT NULL,
        work TEXT NOT NULL,
        work_link TEXT NOT NULL
    )
""")
link = "https://gutenberg.org/ebooks/4363"
book = "Beyond Good and Evil"
for aphorism_number in range(0,len(aphorisms)):
    aphorism_text = aphorisms[aphorism_number]
    command = f"""
        INSERT INTO aphorisms (aphorism, number, work, work_link)
        VALUES (?, ?, ?, ?)
    """
    values= (aphorism_text, aphorism_number, book, link)
    print(command)
    cursor.execute(command, values)
    conn.commit()

