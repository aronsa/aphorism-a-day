import json
from bs4 import BeautifulSoup
import re
import argparse

class work:
    """
        A class to represent a single book from Project Gutenberg, with its title and author
    """


    def filter_from_aphorism_text(self, text:str):
        #find and replace page number markers that look like [Pg 190] 
      return re.sub(r'\[Pg [0-9]+\]', '', text)
    
    def __init__(self,title, link, file_ref):
        self.title = title
        self.link = link
        self.file_ref = file_ref
        with open(self.file_ref, "r") as file:
            html_content = file.read()
            soup = BeautifulSoup(html_content, "html.parser")
            aphorisms = {}
            prev_number = -1
            for p in soup.find_all(["p","h3"]):
                t = p.text.strip()
                print(t)
                splits = re.split(r"\.", t, 1)
                if len(splits) == 2:
                    try:
                        string_containing_aphorism_number = str(int(splits[0]))
                        aphorism_number = int(
                            re.match(r"[0-9]*", string_containing_aphorism_number).group()
                        )
                        print(aphorism_number)
                        prev_number = aphorism_number
                        aphorism_text = splits[1]
                        aphorisms[aphorism_number] = self.filter_from_aphorism_text(aphorism_text)
                    except ValueError:
                        aphorisms[prev_number] = aphorisms[prev_number] + splits[0]
        self.aphorisms = aphorisms
    def getNumberOfAphorisms(self): return len(self.aphorisms)

# Create the parser
parser = argparse.ArgumentParser(
    description="Extract aphorisms from Gutenberg HTML files."
)

parser.add_argument(
    "aphorism_store_location",
    type=str, help="location of the json file used to store aphorisms (or will be)"
)

# Parse the arguments
args = parser.parse_args()

works = [
    work("Beyond Good and Evil", "https://gutenberg.org/ebooks/4363", "works/beyond-good-and-evil.html"),
    work("The Antichrist", "https://www.gutenberg.org/ebooks/19322", "works/antichrist.html"),
    work("The Gay Science", "https://www.gutenberg.org/ebooks/52881", "works/gay-science.html"),
    work("The Genealogy of Morals", "http://www.gutenberg.org/ebooks/52319", "works/geneaology-of-morals.html"),
    work("Human, All Too Human: A Book for Free Spirits", "http://www.gutenberg.org/ebooks/38145", "works/human-all-too-human.html"),
    work("We Philologists", "http://www.gutenberg.org/ebooks/18267", "works/we-philologists.html")
]
metadata = {"work": {}}
aphorisms = {}
totalNumberOfAphorisms = 0
for w in works:
    totalNumberOfAphorisms += w.getNumberOfAphorisms()
    metadata["work"][w.title] = {
        "title": w.title,
        "link": w.link,
        "numberOfAphorisms": w.getNumberOfAphorisms()
    }
    aphorisms[w.title]= w.aphorisms

metadata["global"] = {
    "numberOfAphorisms": totalNumberOfAphorisms
}

aphorism_store_location = args.aphorism_store_location
print(f"imported aphorisms. printing truncated below")
with open(aphorism_store_location, "w") as aphorism_store:
    json.dump({
        "metadata": metadata,
        "aphorisms": aphorisms
    }, aphorism_store, ensure_ascii=False)
print("all done!")


    