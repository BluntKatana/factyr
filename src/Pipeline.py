# ------------------------------------------------------ #
#
# LanguageModel.py is a class that loads a language model,
# and uses it to answer a question.
#
# Group 19: Pooja, Kshitij, Floris, Maik
#
# ------------------------------------------------------ #

try:
    from LanguageModel import LanguageModel
except ModuleNotFoundError:
    from src.LanguageModel import LanguageModel

import os

# Suppress warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

class Pipeline:
    """
    Pipeline that processes a question and returns all parts of the pipeline.
    - Uses a language model to get an answer from the question.
    - Uses an entity recognizer to find entities in the answer.
    - Uses an answer extractor to extract the answer from the question and answer.
    - Uses a fact checker to check the answer.

    :param entity_recognizer: entity recognizer to find entities in the answer
    :param answer_extractor: answer extractor to extract the answer from the question and answer
    :param fact_checker: fact checker to check the answer
    :param verbose: whether to print extra information
    """

    def __init__(self, entity_recognizer, answer_extractor, fact_checker, verbose=True):
        self.entity_recognizer = entity_recognizer
        self.answer_extractor = answer_extractor
        self.fact_checker = fact_checker
        self.verbose = verbose

    def verbose_print(self, text):
        """
        Prints text if verbose is True.

        :param text: text to be printed
        """
        if self.verbose:
            print(text)

    def get_language_model_answer(self, question):
        """
        Gets an answer from the language model.

        :param question: question to be processed
        """

        self.verbose_print(" ########## Question processing ##########\n")
        self.verbose_print(f" Question: {question}")

        llm = LanguageModel('models', self.verbose)
        answer = llm.get_answer(question)
        llm = None

        self.verbose_print(f" Answer: {answer}")
        self.verbose_print("\n #########################################\n")

        return answer
    
    def get_entities_from_text(self, text):
        """
        Gets entities from text.

        :param text: text to be processed
        """

        self.verbose_print(" ########## Entity recognition and linking ##########\n")

        entities = self.entity_recognizer.get_entities(text)
        if self.verbose:
            self.entity_recognizer.print_entities()

        self.verbose_print("\n ###################################################\n")

        return entities
    
    def get_extracted_answer(self, question, answer, entities):
        """
        Gets the extracted answer from the question and answer.

        :param question: question to be processed
        :param answer: answer to be processed
        :param entities: entities in the answer
        """

        self.verbose_print(" ########## Answer extraction ##########\n")
        self.verbose_print(f" Question type: {self.answer_extractor.classify_question(question)} = {'Yes/No' if self.answer_extractor.classify_question(question) == 1 else 'Entity'}")

        extracted_answer, answer_text = self.answer_extractor.extract_answer(question, answer, entities)

        self.verbose_print(f" Extracted Answer: {answer_text}")
        self.verbose_print("\n #######################################\n")

        return extracted_answer
    
    def get_fact_check(self, question, extracted_answer):
        """
        Gets the fact check of the answer.

        :param question: question to be processed
        :param extracted_answer: extracted answer
        """

        self.verbose_print(" ########## Fact checking ##########\n")

        fact_check = self.fact_checker.check(question, extracted_answer)

        self.verbose_print(" Fact check: " + str(fact_check))
        self.verbose_print("\n ###################################\n")

        return fact_check

    def process_question(self, question, question_id):
        """
        Processes a question and returns the answer.

        :param question: question to be processed
        :param question_id: id of the question
        """

        self.verbose_print(f"--------- {question_id}, {question} ---------\n")

        # Get answer from language model
        answer = self.get_language_model_answer(question)

        # Entity recognition and linking
        entities = self.get_entities_from_text(answer)

        # Answer extraction
        extracted_answer = self.get_extracted_answer(question, answer, entities)

        # Fact checking
        fact_check = self.get_fact_check(question, extracted_answer)

        self.verbose_print("------------------------------------------------------\n")

        return answer, extracted_answer, entities, fact_check
