import requests
import ujson
import gzip
import time


class WikipediaAPI:

    def __init__(self, wikipedia_file: str):
        self._session = requests.Session()
        self._url = "https://en.wikipedia.org/w/api.php"
        # self.load_wikipedia_file(wikipedia_file)

        self._cache = {}

    def load_wikipedia_file(self, wikipedia_file: str):
        """
        Load Wikipedia file.

        :param wikipedia_file: path to Wikipedia file
        """

        print("Loading Wikipedia file...")

        with gzip.open(wikipedia_file, "rt") as f:
            self._wikipedia_texts = ujson.load(f)

        time.sleep(5)

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
            "srsearch": f'{title} -intitle:"disambiguation" -intitle:"list of"',
            "srlimit": limit,
            "srprop": "pageid|titlesnippet",
        }

        r = self._session.get(url=self._url, params=params)
        data = r.json()

        return data["query"]["search"]


    def get_text_url_from_pageid(self, title, page_id, first_char):
        """
        Use pageid to get text and url from Wikipedia article.

        :param page_id: pageid from Wikipedia article
        """

        # params = {
        #         "action": "query",
        #         "format": "json",
        #         "prop": "info|extracts",
        #         "inprop": "url",
        #         "exintro": True,
        #         "pageids": page_id
        #     }

        # r = self._session.get(url=self._url, params=params)
        # data = r.json()['query']['pages']

        # text = data[list(data.keys())[0]]["extract"]
        # url = data[list(data.keys())[0]]["fullurl"]

        # print(f"Loading Wikipedia file for {first_char}...")

        try:
            text_dict = self._cache[first_char]
        except KeyError:

            try:
                with open(f"NameWikiJSON/{first_char}.json", "r") as f:
                    text_dict = ujson.load(f)
                    self._cache[first_char] = text_dict
            except FileNotFoundError:
                text_dict = {}

        try:
            text = text_dict[title]
        except KeyError:
            text = ""
        url = f"https://en.wikipedia.org/wiki?curid={page_id}"

        return text, url
