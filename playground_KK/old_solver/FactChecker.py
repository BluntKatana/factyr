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

        print('----------------------------------------------')
        
        num_of_common_occurences = 0
        total_num_of_occurences = 0
        compared_entities = set()

        print('compared_entities', compared_entities)

        for subject_entity in named_entities:
            for candidate_entity in named_entities:

                print('subject_entity', subject_entity)
                print('candidate_entity', candidate_entity)
                subject_page = named_entities_with_pages[subject_entity]

                print('subject_page', subject_page)

                if subject_page is None:
                    continue

                comma_seperated_entities = subject_entity + ',' + candidate_entity
                comma_seperated_entities_reverse = candidate_entity + ',' + subject_entity

                print('comma_seperated_entities_reverse', comma_seperated_entities_reverse)

                if subject_entity != candidate_entity and not comma_seperated_entities in compared_entities:

                    # check if entities exist together
                    if candidate_entity in subject_page.content:
                        num_of_common_occurences += 1

                    total_num_of_occurences += 1
                    compared_entities.add(comma_seperated_entities)
                    compared_entities.add(comma_seperated_entities_reverse)
                    print('compared_entities', compared_entities)

        if total_num_of_occurences == 0:
            print(total_num_of_occurences , 0)
            return 0.0

        similarity_percentage = num_of_common_occurences / total_num_of_occurences
        print('similarity_percentage', similarity_percentage)
        if similarity_percentage > 0.7:
            return 1.0
        else:
            return 0.0

# Creating an instance of FactChecker
fact_checker_instance = FactChecker()
# Calling check_fact on the instance
# fact_checker_instance.check_fact('Capital of Netherlands is Utrecht')
fact_checker_instance.check_fact('Capital of Netherlands is Amsterdam')