import requests
from bs4 import BeautifulSoup
import re


def get_wikipedia_table(url):
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, "html.parser")

        # Find the table on the Wikipedia page
        infobox_tables = soup.find_all("table", {"class": "infobox"})
        all_infoboxes = []
        # Extract data from the table
        for infobox_table in infobox_tables:
            rows = infobox_table.find_all("tr")
            infobox_data = []
            for row in rows:
                columns = row.find_all(["td", "th"])
                infobox_data.append([column.get_text(strip=True) for column in columns])

            print(infobox_data)
            for info in infobox_data:
                all_infoboxes.append(info)
            print("---------------------------------------", all_infoboxes)
    return all_infoboxes


# Example usage
url = "https://en.wikipedia.org/wiki/India"
row_data = get_wikipedia_table(url)
print(row_data)


def find_sublists_by_relation(text_list, relation):
    pattern = re.compile(relation)
    matching_sublists = []

    for sublist in text_list:
        for item in sublist:
            if pattern.search(item):
                matching_sublists.append(sublist)
                break  # Break after finding the first match in the sublist

    return matching_sublists


relation_to_find = "capital".capitalize()
result_sublists = find_sublists_by_relation(row_data, relation_to_find)
print(result_sublists)
if result_sublists:
    print(f"Sublists with '{relation_to_find}' in relation list:")
    for sublist in result_sublists:
        print(sublist)
        pattern = re.compile(r"([^\d]+)")
        # Use the regular expression to extract the city name
        match = pattern.search(sublist[1])
        print(match.group(1).strip())
        break

else:
    print(f"No sublists found with '{relation_to_find}' in relation list.")
