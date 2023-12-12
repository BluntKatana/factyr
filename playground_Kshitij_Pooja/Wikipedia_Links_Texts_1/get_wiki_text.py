import requests
from bs4 import BeautifulSoup
from Wikipedia_Links_Texts_1.entity_recognizer import NamedEntityRecognizer
import spacy


class WikipediaText:
    def get_wikipedia_intro(self, url):
        # Send a GET request to the Wikipedia page
        response = requests.get(url)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            # Find the div with id 'mw-content-text' and then find the first two paragraphs inside it
            content_div = soup.find("div", {"class": "mw-content-ltr mw-parser-output"})
            paragraphs = content_div.find_all("p")[:4]

            # Extract text from the paragraphs
            intro_text = "\n".join([paragraph.get_text() for paragraph in paragraphs])

            return intro_text
        else:
            print(
                f"Failed to fetch the Wikipedia page. Status code: {response.status_code}"
            )
            return None

    wiki_texts_list = []

    def store_wiki_text(self, queryInput):
        nlp = spacy.load("en_core_web_sm")

        entity_recognizer = NamedEntityRecognizer(nlp)
        entity_recognizer.extract_entities(queryInput)
        entity_recognizer.disambiguate_entities()
        links = entity_recognizer.print_entities()

        # links = links_call.print_entities()
        wiki_texts_list = []
        for link in links:
            wikipedia_url = link
            intro_text = self.get_wikipedia_intro(wikipedia_url)

            max_length = 1200

            if intro_text:
                if len(intro_text) > max_length:
                    truncated_text = intro_text[:max_length]
                    final_text = truncated_text
                else:
                    final_text = intro_text

            lines = [line for line in final_text.splitlines() if line.strip()]
            result = "\n".join(lines)
            wiki_texts_list.append(result)
        print(wiki_texts_list)
        return wiki_texts_list
