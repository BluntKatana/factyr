import spacy
import difflib
import re

try:
    from src.utils.openie import StanfordOpenIE
    from src.AnswerExtractor import YES_NO_QUESTION, ENTITY_QUESTION
except ModuleNotFoundError:
    from utils.openie import StanfordOpenIE
    from AnswerExtractor import YES_NO_QUESTION, ENTITY_QUESTION

class FactChecker:
    """
    Class to check if the extracted answer is correct.
    Uses Wikidata, Wikipedia infoboxes and Wikipedia text.

    :param entity_recognizer: entity recognizer to extract entities from the question
    :param wiki_api: API to access Wikidata and Wikipedia
    """

    def __init__(self, entity_recognizer, wiki_api):
        self._wiki_api = wiki_api
        self._open_ie = StanfordOpenIE()
        self._entity_recognizer = entity_recognizer
        self._nlp = spacy.load("en_core_web_sm")

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

        return 'correct' if answer['A'] == 'no' else 'incorrect'

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
            else:
                new_entity = self._entity_recognizer.find_entity_wikipedia_hit(relation['subject'])
                if new_entity:
                    new_relation['subject'] = new_entity
                    new_relation['nr_entities'] += 1
            if relation['object'] in entity_names:
                new_relation['object'] = [entity for entity in entities if entity['name'] == relation['object']][0]
                new_relation['nr_entities'] += 1
            else:
                new_entity = self._entity_recognizer.find_entity_wikipedia_hit(relation['object'])
                if new_entity:
                    new_relation['object'] = new_entity
                    new_relation['nr_entities'] += 1

            # Remove stopwords
            new_relation['relation'] = " ".join([str(word) for word in self._nlp(relation['relation']) if not word.is_stop])

            if new_relation['relation']:
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
    
    def check_with_wikipedia(self, relations):
        """
        Uses Wikipedia to check if the relations extracted from the
        question are correct according to Wikipedia.

        :param relations: relations extracted from the question
        """

        for relation in relations:
            if relation['nr_entities'] == 2:
                
                # Check both entities Wikipedia pages for relations
                wikipedia_relations = self.get_relations_wikipedia(
                    [relation['object']['wikipedia_hit']['page_id'],
                    relation['subject']['wikipedia_hit']['page_id']],
                    [relation['object']['wikipedia_hit']['title'],
                    relation['subject']['wikipedia_hit']['title']],
                    match_type='and'
                )

                # Check if the relation is in the list of relations
                if self.match_relations(relation['relation'], wikipedia_relations) == 'yes':
                    return 'yes'
            

            else:
                
                # Find entity
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

                if not entity:
                    continue

                # Get relations from Wikipedia with entity as subject or object
                wikipedia_relations = self.get_relations_wikipedia(
                    [entity['wikipedia_hit']['page_id']],
                    [entity['wikipedia_hit']['title']],
                    match_type='or', full_rel=True
                )

                # Create similarity score for each relation, if above 0.5, approve
                for wikirel in wikipedia_relations:

                    if self.relation_similarity(cleaned_relation, wikirel) >= 0.5:
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
    
    def find_sublists_by_relation(self, text_list, relation):
        """
        Find sublists of the infobox in the form of <relation, value>.

        :param text_list: list of lists of strings
        :param relation: relation to search for
        """
        pattern = re.compile(relation)
        matching_sublists = []

        for sublist in text_list:
            for item in sublist:
                if pattern.search(item.lower()):
                    matching_sublists.append(sublist)
                    break  # Break after finding the first match in the sublist

        return matching_sublists
    
    def check_with_infobox(self, relations):
        """
        Uses Wikipedia infoboxes to check if the statement extracted from the
        question and LLM answer are correct according to Wikipedia.

        :param relations: relations extracted from the question
        """

        for relation in relations:
            
            # Find all entities in the relation
            entities = []
            if isinstance(relation['object'], dict):
                entities.append(relation['object'])
            if isinstance(relation['subject'], dict):
                entities.append(relation['subject'])

            # Find the infoboxes of the entities
            for entity in entities:

                infobox = self._wiki_api.get_wikipedia_table(entity['wikipedia_hit']['url'])
                result_sublists = self.find_sublists_by_relation(infobox, relation['relation'])

                # If we found a sublist, check if the answer is in the sublist
                if result_sublists:
                    for sublist in result_sublists:
                        pattern = re.compile(r"([^\d]+)")

                        # Infobox entry has an answer
                        if len(sublist) > 1:
                            match = pattern.search(sublist[1])
                            infobox_answer = match.group(1).strip()
                            
                            # Check if the answer is (roughly) the same as the entity we are searching for
                            other_entity = relation['object'] if relation['object'] != entity else relation['subject']
                            other_name = other_entity['name'].lower() if isinstance(other_entity, dict) else other_entity.lower()
                            if difflib.SequenceMatcher(None, infobox_answer, other_name).ratio() >= 0.6:
                                return 'yes'
        # No proof found
        return 'no'

