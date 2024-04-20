from bs4 import BeautifulSoup
import re

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
    print(aphorisms[1])