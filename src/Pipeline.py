try:
    from LanguageModel import LanguageModel
except ModuleNotFoundError:
    from src.LanguageModel import LanguageModel

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Pipeline:

    def __init__(self, entity_recognizer, answer_extractor, fact_checker, verbose=True):
        self.entity_recognizer = entity_recognizer
        self.answer_extractor = answer_extractor
        self.fact_checker = fact_checker
        self.verbose = verbose

    def verbose_print(self, text):
        if self.verbose:
            print(text)

    def process_question(self, question, question_id):
        """
        Processes a question and returns the answer.

        :param question: question to be processed
        :param question_id: id of the question
        :return: answer to the question
        """

        self.verbose_print(f"--------- {question_id}, {question} ---------\n")

        # Get answer from language model
        self.verbose_print(" ########## Question processing ##########\n")
        self.verbose_print(f" Question: {question}")
        llm = LanguageModel(self.verbose)
        answer = llm.get_answer(question)
        self.verbose_print(f" Answer: {answer}")
        self.verbose_print("\n #########################################\n")
        llm = None

        # Entity recognition and linking
        self.verbose_print(" ########## Entity recognition and linking ##########\n")
        self.entity_recognizer.extract_entities(answer)
        entities = self.entity_recognizer.disambiguate_entities()
        if self.verbose:
            self.entity_recognizer.print_entities(to_file=question)
        self.verbose_print("\n ###################################################\n")


        # Answer extraction
        self.verbose_print(" ########## Answer extraction ##########\n")
        print(f" Question type: {self.answer_extractor.classify_question(question)} = {'Yes/No' if self.answer_extractor.classify_question(question) == 1 else 'Entity'}")
        extracted_answer, answer_text = self.answer_extractor.extract_answer(question, answer, entities)
        print(f" Extracted Answer: {answer_text}")
        self.verbose_print("\n #######################################\n")

        # Fact checking
        self.verbose_print(" ########## Fact checking ##########\n")
        fact_check = self.fact_checker.check(question, extracted_answer)
        self.verbose_print(" Fact check: " + str(fact_check))
        self.verbose_print("\n ###################################\n")

        self.verbose_print("------------------------------------------------------\n")

        return answer, extracted_answer, entities, fact_check
    
