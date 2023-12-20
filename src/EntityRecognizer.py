# ------------------------------------------------------ #
#
# EntityRecognizer.py is a class that is used to extract
# and link entities from a given text. The entities are
# link to Wikipedia articles.
#
# Group 19: Pooja, Kshitij, Floris, Maik
#
# ------------------------------------------------------ #

import difflib
import multiprocessing as mp

import nltk
import spacy


class NamedEntityRecognizer:
    """
    Named entity recognizer using SpaCy's named entity recognition.
    Can also link entities to Wikipedia articles.

    :param spacy_model: the SpaCy model to use for named entity recognition
        (default = "en_core_web_sm")
    :param wiki_api: the WikiAPI to use for getting candidates and intro texts
    """

    def __init__(self, spacy_model, wiki_api):

        print("+ Setting up named entity recognizer/linker...")
        self._nlp = spacy.load(spacy_model)
        self._entities = []
        self._wiki_api = wiki_api

    def print_entities(self):
        """
        Prints the entities found in the text.
        """

        for entity in self._entities:
            print(f" Entity: {entity['name']}")
            if 'wikipedia_hit' in entity:
                print(f" Entity Wikipedia hit: {entity['wikipedia_hit']['url']}")

    def get_entities(self, text):
        """
        Full function to extract and disambiguate entities from a text.

        :param text: the text to extract and disambiguate entities from
        """

        self.extract_entities(text)
        return self.disambiguate_entities()

    def process_text(self, text: str, current_entity: str = "", stemmed=True) -> list:
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

        # Remove stop words and stemmed stop words from tokenized text
        context_words = [word for word in text_tokenized
                         if word not in stop_words
                         and stemmer.stem(word) not in stop_words
                         and word not in current_entity_tokenized
                         and stemmer.stem(word) not in current_entity_tokenized
                         and len(word) > 1
                         ]

        # If entity occurence in text is not specified, return all context words
        # (stemmed or not-stemmed)
        if stemmed:
            return [stemmer.stem(word) for word in context_words]
        return context_words


    def get_context_words(self, text: str, current_entity: str, entity_occurence_in_text: int) -> list:
        """
        Retrieves the context words of a certain entity within a text.
        Uses distance to entity to assign normalized weights

        :param text: the text to get the context words from
        :param current_entity: the entity for which the context words have to be found and weighted
        :param entity_occurence_in_text: the occurence of the entity in the text (-1 means not taking into account - equal weights)
        """

        text_tokenized = [word.strip('.') for word in nltk.word_tokenize(text)]
        stemmer = nltk.PorterStemmer()
        context_words = self.process_text(text, current_entity, stemmed=False)

        # If entity occurence in text is specified, we want to give more weight to 
        # the context words that are closer to the entity
        entity_occurence = 1
        
        # Get the index of the entity in the text
        try:
            index_of_entity_in_text = text_tokenized.index(nltk.word_tokenize(current_entity)[0])
        except:
            index_of_entity_in_text = sorted([(i, difflib.SequenceMatcher(None, nltk.word_tokenize(current_entity), word).ratio()) for i, word in enumerate(text_tokenized)], key=lambda x: (x[1], -x[0]), reverse=True)[0][0]

        while entity_occurence < entity_occurence_in_text:
            try:
                index_of_entity_in_text = text_tokenized.index(nltk.word_tokenize(current_entity)[0])
            except:
                index_of_entity_in_text = sorted([(i, difflib.SequenceMatcher(None, nltk.word_tokenize(current_entity), word).ratio()) for i, word in enumerate(text_tokenized)], key=lambda x: (x[1], -x[0]), reverse=True)[0][0]
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

        # Return the stemmed context words with their normalized weights
        stemmer = nltk.PorterStemmer()
        return [{'word': stemmer.stem(word), "weight": distance / sum_of_context_word_distances } 
                    for word, distance in norm_word_distance_to_entity.items() if word in context_words]

    def extract_entities(self, text: str, exclude_types: list = ['ORDINAL', 'CARDINAL', 'TIME', 'QUANTITY',
                                                                 'MONEY', 'PERCENT']) -> list:
        """
        Extracts entities in the form: [{'name': 'Paris', 'type': 'GPE',
                                         'context': [{ word: 'France', weight: '0.7'},
                                                     { word: 'Eiffel', weight: '0.25'}]
                                        }, ...]
        Uses SpaCy's named entity recognition.
        :param text: the text to extract entities from
        :param exclude_types: the types of entities to exclude
        """
        doc = self._nlp(text)
        self._entities = []

        entities_to_add = []
        # Initialize a dict to count occurence of a certain entity
        # within a given text (sentence in this case)
        entity_occurences_in_text = {}

        # For every entity in the text, add it to the list of entities
        for ent, _ in zip(doc.ents, range(len(doc.ents))):
            if ent.label_ not in exclude_types:

                # Keep track of occurences of same entity text
                if ent.text in entity_occurences_in_text:
                    entity_occurences_in_text[ent.text] += 1
                else:
                    entity_occurences_in_text[ent.text] = 1

                # Also add context words to entity
                entities_to_add.append({
                    'name': ent.text,
                    'type': ent.label_,
                    'context': self.get_context_words(doc.text, ent.text, entity_occurences_in_text[ent.text])
                })
        self._entities.extend(entities_to_add)

        return self._entities
    
    def find_entity_wikipedia_hit(self, entity_name):
        """
        Returns the first Wikipedia hit for an entity name.

        :param entity_name: the name of the entity to find the Wikipedia hit for
        """

        try:
            candidates = self._wiki_api.get_candidates_from_title(entity_name, limit=1)
            url, wikidata = self._wiki_api.get_wikipedia_url_from_id(candidates[0]['pageid'])
            return {
                'name': entity_name,
                'wikipedia_hit': {
                    'title': candidates[0]["title"],
                    'page_id': candidates[0]["pageid"],
                    'url': url,
                    'wikidata_id': wikidata,
                    'score': 1
                }
            }
        except:
            return {}

    def disambiguate_entity(self, entity_i, return_dict, return_first=False):
        """
        Disambiguates an entity found in the text. Used by multiprocessing.

        :param entity_i: index of the entity to disambiguate
        :param return_dict: dict to return the entity to
        :param return_first: if True, only the first hit is returned (without score)
        """

        entity = self._entities[entity_i]

        # Dates are very sensitive to mistakes, so we just take the first hit
        if entity['type'] == 'DATE' or return_first:
            entity['wikipedia_hit'] = self.find_entity_wikipedia_hit(entity['name'])
            return_dict[entity_i] = entity
            return

        # Candidate generation
        candidates = self._wiki_api.get_candidates_from_title(entity["name"], limit=15)

        # Start with unlinkable entity
        entity['wikipedia_hit'] = {'title': "NO HIT", 'url': "NO HIT", 'score': 0}

        for i, candidate in enumerate(candidates):

            try:

                # Skip disambiguation pages and lists
                if 'disambiguation' in candidate['title'].lower() or 'list of' in candidate['title'].lower():
                    continue
            
                # Get and process Wikipedia article introtext
                wikipedia_text, url, wikidata_id = self._wiki_api.get_text_url_from_pageid(candidate["pageid"])
                wikipedia_text_processed = self.process_text(wikipedia_text, entity["name"])

                # Add similarity of context words in text and context words in Wikipedia article introtext
                # based on the weight of context weights
                context_score = 0
                nr_of_found_context_words = 0
                for context_word in entity["context"]:
                    if context_word["word"] in wikipedia_text_processed:
                        context_score += context_word["weight"]
                        nr_of_found_context_words += 1

                # Try to find balance between context score and name/title similarity, and position in candidates
                position_boost = 1/(i+1)
                name_title_ratio = difflib.SequenceMatcher(None, entity["name"], candidate["title"]).ratio()
                balance_score = (name_title_ratio + position_boost) * ((nr_of_found_context_words / len(entity["context"])) + context_score + 0.1)
                similarity = balance_score

                # Update entity if similarity is higher than current similarity
                if similarity > entity['wikipedia_hit']['score']:
                    entity['wikipedia_hit'] = {
                        'title': candidate["title"],
                        'url': url,
                        'page_id': candidate["pageid"],
                        'score': similarity,
                        'wikidata_id': wikidata_id
                    }

            except:
                pass

        return_dict[entity_i] = entity

    def disambiguate_entities(self, return_first=False):
        """
        Disambiguates the entities found in the text.
        Adds the Wikipedia hit to the entity.
        Uses multiprocessing to speed up the process.

        :param return_first: if True, only the first hit is returned (without score)
        """

        # Set up multiprocessing
        manager = mp.Manager()
        return_data = manager.dict()
        pool = mp.Pool(mp.cpu_count())

        for i in range(len(self._entities)):
            pool.apply_async(self.disambiguate_entity, args=(i, return_data, return_first))

        pool.close()
        pool.join()

        # Update entities with Wikipedia hits
        for i in range(len(self._entities)):
            self._entities[i] = return_data[i]

        return self._entities
