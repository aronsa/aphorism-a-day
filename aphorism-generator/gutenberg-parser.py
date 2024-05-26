import json
from bs4 import BeautifulSoup
import re
import argparse

def read_gutenberg_html(book_location: str):
    # Read the HTML file
    with open(book_location, "r") as file:
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
                    aphorisms[aphorism_number] = aphorism_text
                except ValueError:
                    aphorisms[prev_number] = aphorisms[prev_number] + splits[0]
    return aphorisms


def load_aphorisms_into_json_store(
    data_store_location: str, work_name: str, work_link: str, aphorisms_to_load: dict
):
    with open(data_store_location, "a+") as aphorism_store_file:
        # load in some existing data
        try:
            aphorism_store = json.load(aphorism_store_file)
        except:
            aphorism_store = {
                "metadata": {
                    "global":{
                        "totalNumberOfAphorisms": 0
                    },
                    "work" :{}
                },
                "aphorisms": {}
            }
        aphorism_metadata = aphorism_store["metadata"]
        aphorisms = aphorism_store["aphorisms"]
        aphorism_metadata["global"]["totalNumberOfAphorisms"] += len(aphorisms_to_load)
        aphorism_metadata["work"][work_name] = {
            "numberOfAphorismsInWork": len(aphorisms_to_load),
            "gutenbergLink": work_link
        }
        # load in new data
        aphorism_store_file.seek(0)  # Move the file pointer to the beginning
        aphorism_store_file.truncate()  # Truncate the file content

        aphorism_metadata[work_name] = {
            "numberOfAphorismsInWork": len(aphorisms_to_load),
            "gutenbergLink": work_link,
        }

        aphorisms[work_name] = aphorisms_to_load

        json.dump(aphorism_store, aphorism_store_file, ensure_ascii=False)


# Create the parser
parser = argparse.ArgumentParser(
    description="Extract aphorisms from Gutenberg HTML files."
)

# Add the arguments
parser.add_argument(
    "gutenberg_html_location", type=str, help="Location of the Gutenberg HTML file"
)
parser.add_argument("work_name", type=str, help="Name of the work")
parser.add_argument(
    "gutenberg_link", type=str, help="Link to the Gutenberg project page"
)
parser.add_argument(
    "aphorism_store_location",
    type=str, help="location of the json file used to store aphorisms (or will be)"
)

# Parse the arguments
args = parser.parse_args()

# Access the argument values
gutenberg_html_location = args.gutenberg_html_location
work_name = args.work_name
gutenberg_link = args.gutenberg_link
aphorism_store_location = args.aphorism_store_location
print(f"reading html file {gutenberg_html_location}")
aphorisms = read_gutenberg_html(gutenberg_html_location)
print(f"imported aphorisms. printing truncated below")
print(str(aphorisms)[0:100])
print(f"loading into {aphorism_store_location}")
load_aphorisms_into_json_store(
    data_store_location=aphorism_store_location,
    work_name=work_name,
    work_link=gutenberg_link,
    aphorisms_to_load=aphorisms,
)
print("all done!")


# link = "https://gutenberg.org/ebooks/4363"
# book = "Beyond Good and Evil"
# for aphorism_number in range(0,len(aphorisms)):
#     aphorism_text = aphorisms[aphorism_number]
#     command = f"""
#         INSERT INTO aphorisms (aphorism, number, work, work_link)
#         VALUES (?, ?, ?, ?)
#     """
#     values= (aphorism_text, aphorism_number, book, link)
#     print(command)
#     cursor.execute(command, values)
#     conn.commit()
