import requests


class WikipediaAPI:

    def __init__(self):
        self._session = requests.Session()
        self._url = "https://en.wikipedia.org/w/api.php"

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
            "srsearch": title,
            "srlimit": limit
        }

        r = self._session.get(url=self._url, params=params)
        data = r.json()

        return data["query"]["search"]

    def get_text_url_from_pageid(self, page_id):
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

        return text, url
