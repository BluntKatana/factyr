import requests

class WikipediaAPI:

    def __init__(self):
        self._session = requests.Session()
        self._url = "https://en.wikipedia.org/w/api.php"

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
            "prop": "info",
            "inprop": "url",
            "pageids": page_id
        }

        r = self._session.get(url=self._url, params=params)
        data = r.json()['query']['pages']

        return data[list(data.keys())[0]]["fullurl"]

    def get_text_url_from_pageid(self, title, page_id, first_char):
        """
        Use pageid to get text and url from Wikipedia article.

        :param page_id: pageid from Wikipedia article
        """

        params = {
                "action": "query",
                "format": "json",
                "prop": "info|extracts",
                "inprop": "url",
                "exintro": True,
                "pageids": page_id
            }

        r = self._session.get(url=self._url, params=params)
        data = r.json()['query']['pages']

        text = data[list(data.keys())[0]]["extract"]
        url = data[list(data.keys())[0]]["fullurl"]

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

        return text, url
