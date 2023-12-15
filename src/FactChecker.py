import spacy
from EntityRecognizer_TESTING import NamedEntityRecognizer
from WikiAPI import WikiAPI
from AnswerExtractor import YES_NO_QUESTION, ENTITY_QUESTION
import requests
from bs4 import BeautifulSoup
from src.utils.openie import StanfordOpenIE
import difflib
import re

class FactChecker:

    def __init__(self, entity_recognizer):
        self._wiki_api = WikiAPI()
        self._open_ie = StanfordOpenIE()
        self._entity_recognizer = entity_recognizer
        self._nlp = spacy.load("en_core_web_sm")

    def relations_from_question(self, question, entities):
        """
        Use Stanford's OpenIE to extract relations from the question.
        If question is an entity question, replace the 'PRON' with the entity.
        Replace objects and subjects with entities where possible.

        :param question: question to be answered
        :param entities: entities extracted from the question
        """

        relations = self._open_ie.annotate(question)
        entity_names = [entity['name'] for entity in entities]

        new_relations = []
        for relation in relations:

            new_relation = relation
            new_relation['nr_entities'] = 0

            # Replace with entities
            if relation['subject'] in entity_names:
                new_relation['subject'] = [entity for entity in entities if entity['name'] == relation['subject']][0]
                new_relation['nr_entities'] += 1
            if relation['object'] in entity_names:
                new_relation['object'] = [entity for entity in entities if entity['name'] == relation['object']][0]
                new_relation['nr_entities'] += 1

            # Remove stopwords
            new_relation['relation'] = " ".join([str(word) for word in self._nlp(relation['relation']) if not word.is_stop])

            if new_relation['relation']:
                print(new_relation['relation'])
                new_relations.append(new_relation)

        return new_relations

    def extract_relations_to_check(self, question, answer):
        """
        Creates relations from the question and answer in the form
        <subject, relation, object>. Replaces relevant part of relation
        to entity if possible.

        :param question: question to be answered
        :param answer: (extracted) answer to the question
        """

        if answer['type'] == YES_NO_QUESTION:

            self._entity_recognizer.extract_entities(question)
            entities = self._entity_recognizer.disambiguate_entities(return_first=True)

            return self.relations_from_question(question, entities)

        else:
 
            # Replace PRON with entity
            nlp = spacy.load("en_core_web_sm")
            doc = nlp(question)
            new_question = " ".join([token.text if token.pos_ != "PRON" else answer['A']['name'] for token in doc])

            # Extract entities from new question
            self._entity_recognizer.extract_entities(new_question)

            # Extract entities from question and answer
            entities = self._entity_recognizer.disambiguate_entities(return_first=True)
            entities.append(answer['A'])

            return self.relations_from_question(new_question, entities)

    def check_with_wikidata(self, relations):
        """
        From the extracted relations from the question, check if
        Wikidata agrees with this relations.

        :param relations: relations extracted from the question
        """

        for relation in relations:
            if relation['nr_entities'] == 2:

                wikidata_relations = self._wiki_api.get_relations_wikidata(
                    relation['object']['wikipedia_hit']['wikidata_id'],
                    relation['subject']['wikipedia_hit']['wikidata_id']
                )

                if self.match_relations(relation['relation'], wikidata_relations) == 'yes':
                    return 'yes'

        return 'no'
    
    def match_relations(self, query_relation, all_relations):
        """
        Matches the relation of the query with the relations from Wikidata.
        Approves if the similarity is above 0.6.

        :param query_relation: relation from the query
        :param all_relations: all relations from Wikidata
        """
        for relation in all_relations:
            similarity = difflib.SequenceMatcher(None, query_relation, relation).ratio()
            if similarity >= 0.6:
                return 'yes'
        return 'no'
    
    def get_relations_wikipedia(self, page_ids, titles, match_type='and', full_rel=False):
        """
        Extracts the relations from the Wikipedia page of the entities.

        :param url1: URL of the first entity
        :param url2: URL of the second entity
        """

        relations = []
        for page_id in page_ids:
            intro, _, _ = self._wiki_api.get_text_url_from_pageid(page_id)

            if match_type == 'and':
                relations += [rel['relation'] if not full_rel else rel for rel in self._open_ie.annotate(intro) if rel['object'] in titles and rel['subject'] in titles]
            elif match_type == 'or':
                relations += [rel['relation'] if not full_rel else rel for rel in self._open_ie.annotate(intro) if rel['object'] in titles or rel['subject'] in titles]

        return relations
    
    def relation_similarity(self, relation1, relation2):
        """
        Very creative function to calculate the similarity between
        2 relations. It does this by comparing the similarity of
        the object, relation and subject of both relations.

        :param relation1: first relation
        :param relation2: second relation
        """

        if relation1 == relation2:
            return 1
        
        total_score = 0
        
        # These are the pairs of strings to compare
        to_check = [
            (relation1['object'], relation2['object']),
            (relation1['relation'], relation2['relation']),
            (relation1['subject'], relation2['subject']),
            (relation1['relation'], relation2['object']),
            (relation1['relation'], relation2['subject'])
        ]

        # Calculate the similarity for each pair and add it to the total score
        for pair in to_check:
            total_score += difflib.SequenceMatcher(None, pair[0], pair[1]).ratio()
    
        return total_score / len(to_check)

    def check_with_wikipedia(self, relations):
        """
        Uses Wikipedia to check if the relations extracted from the
        question are correct according to Wikipedia.

        :param relations: relations extracted from the question
        """

        for relation in relations:
            if relation['nr_entities'] == 2:

                wikipedia_relations = self.get_relations_wikipedia(
                    [relation['object']['wikipedia_hit']['page_id'],
                    relation['subject']['wikipedia_hit']['page_id']],
                    [relation['object']['wikipedia_hit']['title'],
                    relation['subject']['wikipedia_hit']['title']],
                    match_type='and'
                )

                if self.match_relations(relation['relation'], wikipedia_relations) == 'yes':
                    return 'yes'
            

            else:

                entity = None                    
                if isinstance(relation['object'], dict):
                    entity = relation['object']
                    cleaned_relation = {
                        'object': entity['name'],
                        'relation': relation['relation'],
                        'subject': relation['subject']
                    }
                elif isinstance(relation['subject'], dict):
                    entity = relation['subject']
                    cleaned_relation = {
                        'object': relation['object'],
                        'relation': relation['relation'],
                        'subject': entity['name']
                    }
            
                wikipedia_relations = self.get_relations_wikipedia(
                    [entity['wikipedia_hit']['page_id']],
                    [entity['wikipedia_hit']['title']],
                    match_type='or', full_rel=True
                )

                for wikirel in wikipedia_relations:
                    
                    if self.relation_similarity(cleaned_relation, wikirel) >= 0.5:
                        return 'yes'

        return 'no'
    
    def get_wikipedia_table(self,url):
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
    
    def find_sublists_by_relation(self, text_list, relation):
        pattern = re.compile(relation)
        matching_sublists = []

        for sublist in text_list:
            for item in sublist:
                if pattern.search(item.lower()):
                    matching_sublists.append(sublist)
                    break  # Break after finding the first match in the sublist

        return matching_sublists
    
    def check_with_infobox(self, relations):

        for relation in relations:

            entities = []
            if isinstance(relation['object'], dict):
                entities.append(relation['object'])
            if isinstance(relation['subject'], dict):
                entities.append(relation['subject'])

            for entity in entities:

                infobox = self.get_wikipedia_table(entity['wikipedia_hit']['url'])
                result_sublists = self.find_sublists_by_relation(infobox, relation['relation'])
                if result_sublists:
                    for sublist in result_sublists:
                        pattern = re.compile(r"([^\d]+)")

                        if len(sublist) > 1:
                            # Use the regular expression to extract the city name
                            match = pattern.search(sublist[1])
                            infobox_answer = match.group(1).strip()
                            
                            other_entity = relation['object'] if relation['object'] != entity else relation['subject']
                            if difflib.SequenceMatcher(None, infobox_answer, other_entity['name']).ratio() >= 0.6:
                                return 'yes'
                        
        return 'no'



    def check(self, question, answer):
        """
        Main function, checks if the given answer to a question is correct.

        :param question: question to be answered
        :param answer: (extracted) answer to the question
        """

        # Try 1: Use Wikidata to check if the relation exists
        rels = self.extract_relations_to_check(question, answer)
        check = self.check_with_wikidata(rels)
        if answer['type'] == YES_NO_QUESTION:
            if check == answer['A'] and answer['A'] == 'yes':
                return 'correct'
        else:
            if check == 'yes':
                return 'correct'
        
        # Try 2: Use Wikipedia infobox to check if the relation exists
        check = self.check_with_infobox(rels)
        if answer['type'] == YES_NO_QUESTION:
            if check == answer['A'] and answer['A'] == 'yes':
                return 'correct'
        else:
            if check == 'yes':
                return 'correct'
            
        # Try 3: Use Wikipedia to check if the relation exists
        check = self.check_with_wikipedia(rels)
        if answer['type'] == YES_NO_QUESTION:
            if check == answer['A'] and answer['A'] == 'yes':
                return 'correct'
        else:
            if check == 'yes':
                return 'correct'

        return 'incorrect' if check == 'yes' else 'correct'

fc = FactChecker(NamedEntityRecognizer('en_core_web_sm'))
print(fc.check("What is the longest river in the world?", {'A':{'name': 'Nile', 'wikipedia_hit': {'page_id': 21244, 'url': 'https://en.wikipedia.org/wiki/Nile', 'title': "Nile"}}, 'type': ENTITY_QUESTION}))

# print(fc.relation_similarity({'object': 'Emmanuel Macron', 'relation': 'is president of', 'subject': 'France'}, {'object': 'Macron', 'relation': 'was elected', 'subject': 'president of France'}))