import spacy
import nltk
import WikipediaAPI
import ujson


class NamedEntityRecognizer:
    """
    Named entity recognizer using SpaCy's named entity recognition.

    :param spacy_model: the SpaCy model to use for named entity recognition
        (default = "en_core_web_sm")
    """

    def __init__(self, spacy_model):

        self._nlp = spacy.load(spacy_model)
        self._entities = []

    def print_entities(self, to_file: str | None = None):
        """
        Prints the entities found in the text.
        """
        if to_file:
            ujson.dump(self._entities, open(f"question_entities/{to_file}.json", "w"), indent=4)

        for entity in self._entities:
            print(f"Entity: {entity['name']}")
            if 'wikipedia_hit' in entity:
                print(f"Entity Wikipedia hit: {entity['wikipedia_hit']['url']}")

    def process_text(self, text: str, current_entity: str = "", entity_occurence_in_text: int = -1) -> list:
        """
        Processes a text to be able to compare it with other texts.
        Uses Porter stemming and removes stop words.

        :param text: the text to process
        :param current_entity: the current entity to remove from the text
            because it is not relevant for the comparison
        :param entity_occurence_in_text: the occurence of the entity in the text (-1 means not taking into account - equal weights)
        """

        current_entity_tokenized = nltk.word_tokenize(current_entity)
        text_tokenized = nltk.word_tokenize(text)
        stemmer = nltk.PorterStemmer()
        stop_words = nltk.corpus.stopwords.words('english')

        # Remove stop words and stemmed stop words from tokenized text
        context_words = [word for word in text_tokenized
                         if word not in stop_words
                         and stemmer.stem(word) not in stop_words
                         and word not in current_entity_tokenized
                         and stemmer.stem(word) not in current_entity_tokenized
                         and len(word) > 1
                         ]

        # If entity occurence in text is not specified, return all stemmed context words
        if entity_occurence_in_text == -1:
            return [{'word': stemmer.stem(word), "weight": 1 } for word in context_words]

        # If entity occurence in text is specified, we want to give more weight to 
        # the context words that are closer to the entity
        entity_occurence = 1
        # TODO: Perhaps use different method to get index of entity in text (supporting entity with multiple words)
        index_of_entity_in_text = text_tokenized.index(current_entity.split()[0])

        while entity_occurence < entity_occurence_in_text:
            index_of_entity_in_text = text_tokenized.index(current_entity.split()[0])
            entity_occurence += 1

        # Retrieve the absolute distance of each word to the entity in the text
        word_distance_to_entity = {}
        for idx, word in enumerate(text_tokenized):
            if word != current_entity:
                word_distance_to_entity[word] = abs(idx - index_of_entity_in_text)


        # Noramlize the disatnce of each word based on the highest distance
        # (longer texts have higher distances than shorter texts)
        highest_distance = max(word_distance_to_entity.values())
        norm_word_distance_to_entity = {}
        for word, distance in word_distance_to_entity.items():
            norm_word_distance_to_entity[word] = distance / highest_distance

        # Get the sum of all CONTEXT WORD distances and normalize the distances to add up to 1
        sum_of_context_word_distances = sum([distance for word, distance in norm_word_distance_to_entity.items() if word in context_words])

        # Return the context words with their normalized weights
        return [{'word': stemmer.stem(word), "weight": distance / sum_of_context_word_distances } 
                    for word, distance in norm_word_distance_to_entity.items() if word in context_words]


    def get_context_words(self, text: str, entity_name: str, entity_occurence_in_text: int) -> list:
        return self.process_text(text, entity_name, entity_occurence_in_text)

    def extract_entities(self, text: str, keep_types: list = ['GPE', 'PERSON', 'ORG']) -> list:
        """
        Extracts entities in the form: [{'name': 'Paris', 'type': 'GPE',
                                         'context': [{ word: 'France', weight: '0.7'},
                                                     { word: 'Eiffel', weight: '0.25'}]
                                        }, ...]
        Uses SpaCy's named entity recognition.
        :param text: the text to extract entities from
        :param keep_types: the types of entities to keep
        """
        doc = self._nlp(text)
        self._entities = []

        for sent in doc.sents:
            sent_nlp = self._nlp(sent.text)

            entities_to_add = []
            # Initialize a dict to count occurence of a certain entity
            # within a given text (sentence in this case)
            entity_occurences_in_text = {}

            for ent, idx in zip(sent_nlp.ents, range(len(sent_nlp.ents))):
                if ent.label_ in keep_types:
                    if ent.text in entity_occurences_in_text:
                        entity_occurences_in_text[ent.text] += 1
                    else:
                        entity_occurences_in_text[ent.text] = 1

                    entities_to_add.append({
                        'name': ent.text,
                        'type': ent.label_,
                        'context': self.get_context_words(sent_nlp.text, ent.text, entity_occurences_in_text[ent.text])
                    })
            self._entities.extend(entities_to_add)

        return self._entities


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

        # TODO: Find a better balance between the weight of features
        """

        wikipedia_api = WikipediaAPI.WikipediaAPI()
        entity_names = [entity["name"] for entity in self._entities]

        for entity in self._entities:

            candidates = wikipedia_api.get_candidates_from_title(entity["name"], limit=15)
            entity['wikipedia_hit'] = {'title': "NO HIT", 'url': "NO HIT", 'score': 0}

            for i, candidate in enumerate(candidates):

                if 'disambiguation' in candidate['title'].lower() or 'list of' in candidate['title'].lower():
                    continue

                wikipedia_text, url = wikipedia_api.get_text_url_from_pageid(candidate['title'], candidate["pageid"], candidate["title"][0].upper())
                wikipedia_text_processed = self.process_text(wikipedia_text, entity["name"])
                wikipedia_title_text_processed = self.process_text(candidate["title"], entity["name"])

                if 'may refer to' in wikipedia_text:
                    continue

                # Initialize the similarity value - used to check the similarity between an entity and candidate
                similarity = 0

                # Similarity between context words in text and context words in Wikipedia article title and article
                similarity += self.jaccard_similarity(entity["context"], wikipedia_text_processed)
                similarity += self.jaccard_similarity(entity["context"], wikipedia_title_text_processed) * boost_title_similarity

                # Boost if there is a full hit (entity name === canadidate title)
                if self.is_full_hit(entity["name"], candidate["title"]):
                    similarity += boost_full_hit

                # Punish if the found candidate is also an entity in the text
                if candidate["title"] in entity_names and candidate["title"] != entity["name"]:
                    similarity -= deboost_other_entity

                # Boost first hit
                if i == 0:
                    similarity += boost_first_hit


                # Add similarity of context words in text and context words in Wikipedia article introtext
                # based on the weight of context weights
                for context_word in entity["context"]:
                    if self.is_word_in_processed_text(context_word["word"], wikipedia_text_processed):
                        similarity += context_word["weight"]

                # Boost if entity is same category as first entity hit in Wikipedia article
                if entity['type'] != 'PERSON':
                    text_nlp = self._nlp(wikipedia_text)
                    if text_nlp.ents:
                        if text_nlp.ents[0].label_ == entity['type']:
                            similarity += boost_same_category if candidate['title'] == text_nlp.ents[0].text else boost_same_category / 2

                # print(candidate["title"], similarity)
                # Update entity with best candidate
                if similarity > entity['wikipedia_hit']['score']:
                    entity['wikipedia_hit'] = {
                        'title': candidate["title"],
                        'url': wikipedia_api.get_wikipedia_url_from_id(candidate['pageid']),
                        'score': similarity
                    }

        return self._entities

    # ------
    # BELOW ARE ALL DISAMBIGUATION FEATURES
    # ------
    def jaccard_similarity(self, list_1: list, list_2: list) -> float:
        """
        Calculates the Jaccard similarity between two lists of strings.
        :param a: the first list
        :param b: the second list
        """
        # Return 0 if one of the lists is empty
        if len(list_1) == 0 or len(list_2) == 0:
            return 0
        list_1 = set([parsed_word["word"] for parsed_word in list_1])
        list_2 = set([parsed_word["word"] for parsed_word in list_2])
        return len(list_1.intersection(list_2)) / len(list_1.union(list_2))

    def is_full_hit(self, word_1: str, word_2: str):
        """
        Determines if a word is a full hit with another word
        Full hit = word 1 is equal to word 2 (minus stop words).
        :param word_1: the first word to determine full hit for
        :param word_2: the second word to determine full hit for
        """
        stopwords = nltk.corpus.stopwords.words('english')
        word_1_norm = [word.lower() for word in word_1.split() if word.lower() not in stopwords]
        word_2_norm = [word.lower() for word in word_2.split() if word.lower() not in stopwords]
        return word_1_norm == word_2_norm

    def is_word_in_processed_text(self, word: str, processed_text: list):
        """
        Determines if there is a word in a certain processed_text,
        meaning a text which is parsed with the NamedEntityRecognizer.process_text function
        resulting in a list with obejcts
        """
        return word in [processed_word["word"] for processed_word in processed_text]