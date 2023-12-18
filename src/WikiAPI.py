import requests
import difflib
from bs4 import BeautifulSoup

class WikiAPI:

    def __init__(self):
        self._session = requests.Session()
        self._url = "https://en.wikipedia.org/w/api.php"
        self._sparql_url = "https://query.wikidata.org/sparql"

        self._cache = {}


    def get_candidates_from_title(self, title: str, limit: int = 15):
        """
        Use title to get candidate Wikipedia articles.

        :param title: title from Wikipedia article
        :param limit: number of candidates to return
        """

        params = {
            "action": "query",
            "format": "json",
            "list": "search",
            "srwhat": "text",
            "srsearch": f'{title}',
            "srlimit": limit,
        }

        r = self._session.get(url=self._url, params=params)
        data = r.json()

        return data["query"]["search"]

    def get_wikipedia_url_from_id(self, page_id: int):
        """
        Use pageid to get Wikipedia article url.

        :param page_id: pageid from Wikipedia article
        """

        params = {
            "action": "query",
            "format": "json",
            "prop": "info|pageprops",
            "inprop": "url",
            "ppprop": "wikibase_item",
            "pageids": page_id
        }

        r = self._session.get(url=self._url, params=params)
        data = r.json()['query']['pages']

        return data[list(data.keys())[0]]["fullurl"], data[list(data.keys())[0]]["pageprops"]["wikibase_item"]

    def get_text_url_from_pageid(self, page_id):
        """
        Use pageid to get text and url from Wikipedia article.

        :param page_id: pageid from Wikipedia article
        """

        params = {
                "action": "query",
                "format": "json",
                "prop": "info|extracts|pageprops",
                "ppprop": "wikibase_item",
                "inprop": "url",
                "exintro": True,
                "pageids": page_id
            }

        r = self._session.get(url=self._url, params=params)
        data = r.json()['query']['pages']

        text = data[list(data.keys())[0]]["extract"]
        url = data[list(data.keys())[0]]["fullurl"]
        wikidata_id = data[list(data.keys())[0]]["pageprops"]["wikibase_item"]

        # print(f"Loading Wikipedia file for {first_char}...")

        # try:
        #     text_dict = self._cache[first_char]
        # except KeyError:

        #     try:
        #         with open(f"wikidata/{first_char}.json", "r") as f:
        #             text_dict = ujson.load(f)
        #             self._cache[first_char] = text_dict
        #     except FileNotFoundError:
        #         print(f"Failed to load Wikipedia file for {first_char}.")
        #         text_dict = {}

        # try:
        #     text = text_dict[str(page_id)]
        #     print(text[:10])
        # except KeyError:
        #     text = ""
        #     print(f"Failed to load Wikipedia text for {page_id}.")
        # url = f"https://en.wikipedia.org/wiki?curid={page_id}"

        return text, url, wikidata_id
    
    def get_relations_wikidata(self, wikidata_id_1, wikidata_id_2):
        """
        Extract a list of all relations between two wikidata entities.
        Also considers alternative labels of the relations.

        :param wikidata_id_1: wikidata id of the first entity
        :param wikidata_id_2: wikidata id of the second entity
        """

        # The first query retrieves all relations between 2 entities
        query_1 = """
            select ?rel ?rel2
            where {{ {{
            wd:{id_1} ?rel wd:{id_2}.
            }}
            union {{
            wd:{id_2} ?rel wd:{id_1}.
            }}
            }}
        """.format(id_1=wikidata_id_1, id_2=wikidata_id_2)
        r = requests.get(self._sparql_url, params={'format': 'json', 'query': query_1})

        try:
            data = r.json()
        except:
            return []

        all_relations = []
        for res in data['results']['bindings']:

            rel_id = res['rel']['value'].split('/')[-1]

            # The second query retrieves the label of the relation
            query_2 = '''
                SELECT ?wdLabel WHERE {{
                VALUES (?wdt) {{(wdt:{rel_id})}}
                ?wd wikibase:directClaim ?wdt .
                SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en". }}
                }}
                '''.format(rel_id=rel_id)
            r = requests.get(self._sparql_url, params={'format': 'json', 'query': query_2})

            try:
                all_relations.append(r.json()['results']['bindings'][0]['wdLabel']['value'])
            except: pass

            # The third query retrieves the alternative labels of the relation -> unable in 1 query :/
            query_3 = """SELECT (GROUP_CONCAT(DISTINCT(?altLabel); separator = ", ") AS ?altLabel_list) WHERE {{
                    wd:{rel_id} a wikibase:Property .
                    OPTIONAL {{ wd:{rel_id} skos:altLabel ?altLabel . FILTER (lang(?altLabel) = "en") }}
                    SERVICE wikibase:label {{ bd:serviceParam wikibase:language "en" .}}
                }}
                """.format(rel_id=rel_id)
            r = requests.get(self._sparql_url, params={'format': 'json', 'query': query_3})

            try:
                data = r.json()['results']['bindings']
            except:
                continue

            for result in data:
                try:
                    splitted_list = result['altLabel_list']['value'].split(',')
                    for item in splitted_list:
                        all_relations.append(item.strip())
                except: pass

        return all_relations
    
    def get_wikipedia_table(self,url):
        """
        Get the infobox table from a Wikipedia page.

        :param url: url of the Wikipedia page
        """
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

                for info in infobox_data:
                    all_infoboxes.append(info)
        return all_infoboxes

