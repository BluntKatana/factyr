import csv
from FactEntityExtraction import FactEntityExtraction
from WikipediaHelper import WikipediaHelper


class FactChecker:
    def __init__(self):
        self.fact_entity_extraction = FactEntityExtraction()
        self.wikipedia_helper = WikipediaHelper()
        pass

    def check_fact(self, fact):
        # get named entities
        named_entities = self.fact_entity_extraction.extract_named_entities(fact)

        named_entities_with_pages = {}

        for entity in named_entities:
            named_entities_with_pages[entity] = self.wikipedia_helper.get_entity_wikipage_cached(entity)
        
        print("Extracted name entites and found the Wikipedia Page header: ", named_entities_with_pages)

# Creating an instance of FactChecker
fact_checker_instance = FactChecker()
# Calling check_fact on the instance
fact_checker_instance.check_fact('i am amsterdam and Amsterdam, Netherlands')