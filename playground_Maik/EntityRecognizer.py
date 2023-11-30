import spacy
import nltk
import WikipediaAPI


class NamedEntityRecognizer:
    """
    Named entity recognizer using SpaCy's named entity recognition.

    :param spacy_model: the SpaCy model to use for named entity recognition
        (default = "en_core_web_sm")
    """

    def __init__(self, spacy_model):

        self._nlp = spacy.load(spacy_model)
        self._entities = []

    def print_entities(self):

        for entity in self._entities:
            print(f"Entity: {entity['name']}")
            if 'wikipedia_hit' in entity:
                print(f"Entity Wikipedia hit: {entity['wikipedia_hit']['url']}")

    def process_text(self, text: str, current_entity: str = "") -> list:
        """
        Processes a text to be able to compare it with other texts.
        Uses Porter stemming and removes stop words.

        :param text: the text to process
        :param current_entity: the current entity to remove from the text
            because it is not relevant for the comparison
        """

        current_entity_tokenized = nltk.word_tokenize(current_entity)
        text_tokenized = nltk.word_tokenize(text)
        stemmer = nltk.PorterStemmer()
        stop_words = nltk.corpus.stopwords.words('english')

        return [stemmer.stem(word, True) for word in text_tokenized
                if word not in stop_words
                and word not in current_entity_tokenized
                and len(word) > 1]

    def jaccard_similarity(self, a: list, b: list) -> float:
        """
        Calculates the Jaccard similarity between two lists.

        :param a: the first list
        :param b: the second list
        """

        a = set(a)
        b = set(b)

        if len(a.union(b)) == 0:
            return 0

        return len(a.intersection(b)) / len(a.union(b))

    def get_context_words(self, text: str, entity_name: str) -> list:
        return self.process_text(text, entity_name)

    def extract_entities(self, text: str,
                         keep_types: list = ['GPE', 'PERSON', 'ORG']) -> list:
        """
        Extracts entities in the form: [{'name': 'Paris', 'type': 'GPE',
                                         'context': ['France', 'Eiffel']}, ...]
        Uses SpaCy's named entity recognition.

        :param text: the text to extract entities from
        :param keep_types: the types of entities to keep
        """
        doc = self._nlp(text)
        self._entities = []

        for sent in doc.sents:
            sent_nlp = self._nlp(sent.text)
            self._entities.extend([{
                'name': ent.text,
                'type': ent.label_,
                'context': self.get_context_words(sent_nlp.text, ent.text)}
                for ent in sent_nlp.ents
                if ent.label_ in keep_types])

        return self._entities

    def is_full_hit(self, entity_name, candidate_title):
        """
        Determines if the candidate title is a full hit for the entity name.
        Full hit = title is equal to entity name (minus stop words).

        :param entity_name: the entity name
        :param candidate_title: the candidate title
        """

        stop_words = nltk.corpus.stopwords.words('english')

        candidate_title_norm = " ".join([word.lower()
                                         for word in candidate_title.split()
                                         if word.lower() not in stop_words])
        entity_name_norm = " ".join([word.lower()
                                     for word in entity_name.split()
                                     if word.lower() not in stop_words])

        return candidate_title_norm == entity_name_norm

    def disambiguate_entities(self,
                              deboost_other_entity=0.1,
                              boost_first_hit=0.07,
                              boost_full_hit=0.07,
                              boost_same_category=0.2,
                              boost_title_similarity=2):
        """
        Tries to disambiguate entities and find the best Wikipedia article for each entity.
        Uses features:
        1. The similarity between entity context words and Wikipedia article title
        2. The similarity between entity context words and Wikipedia article intro text
        3. Full hit boost if Wikipedia title is equal to entity name
        4. Category boost if entity is same category as first entity hit in Wikipedia article
        5. First hit boost if entity is first hit in results from API
        6. Punish if the found candidate is also an entity in the text
        """

        wikipedia_api = WikipediaAPI.WikipediaAPI()
        entity_names = [entity["name"] for entity in self._entities]

        for entity in self._entities:

            candidates = wikipedia_api.get_candidates_from_title(entity["name"], limit=15)
            entity['wikipedia_hit'] = {'title': "NO HIT", 'url': "NO HIT", 'score': 0}

            for i, candidate in enumerate(candidates):

                if 'disambiguation' in candidate['title'].lower() or 'list of' in candidate['title'].lower():
                    continue

                text, url = wikipedia_api.get_text_url_from_pageid(candidate['title'], candidate["pageid"], candidate["title"][0].upper())
                text_processed = self.process_text(text, entity["name"])
                title_text_processed = self.process_text(candidate["title"], entity["name"])

                if 'may refer to' in text:
                    continue

                # Similarity between context words in text and context words in Wikipedia article title and article
                similarity = self.jaccard_similarity(entity["context"], text_processed)
                title_similarity = self.jaccard_similarity(entity["context"], title_text_processed) * boost_title_similarity
                similarity += title_similarity
                # print(candidate["title"], similarity)

                # Punish if the found candidate is also an entity in the text
                if candidate["title"] in entity_names and candidate["title"] != entity["name"]:
                    similarity -= deboost_other_entity

                # Boost first hit
                if i == 0:
                    similarity += boost_first_hit

                # Boost if title is equal to entity name
                if self.is_full_hit(entity["name"], candidate["title"]):
                    similarity += boost_full_hit

                # Boost if entity is same category as first entity hit in Wikipedia article
                if entity['type'] != 'PERSON':
                    text_nlp = self._nlp(text)
                    if text_nlp.ents:
                        if text_nlp.ents[0].label_ == entity['type']:
                            similarity += boost_same_category if candidate['title'] == text_nlp.ents[0].text else boost_same_category / 2

                # print(candidate["title"], similarity)
                # Update entity with best candidate
                if similarity > entity['wikipedia_hit']['score']:
                    entity['wikipedia_hit'] = {
                        'title': candidate["title"],
                        'url': url,
                        'score': similarity
                    }

        return self._entities

# nlp = spacy.load("en_core_web_sm")
# start_time = time.time()
# entity_recognizer = NamedEntityRecognizer(nlp)
# entity_recognizer.extract_entities("Donald Trump and Biden are both from the United States. Ronaldo is from Portugal.")
# entity_recognizer.disambiguate_entities()
# entity_recognizer.print_entities()
# print("--- %s seconds ---" % (time.time() - start_time))