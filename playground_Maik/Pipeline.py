from LanguageModel import LanguageModel

class Pipeline:

    def __init__(self, language_model, entity_recognizer, answer_extractor):
        # self.language_model = language_model
        self.entity_recognizer = entity_recognizer
        self.answer_extractor = answer_extractor

    def process_question(self, question):
        """
        Processes a question and returns the answer.

        :param question: question to be processed
        :param question_id: id of the question
        :return: answer to the question
        """
        llm = LanguageModel()
        answer = llm.get_answer(question)
        print(f"Answer: {answer}")
        llm = None

        # Entity recognition and linking
        self.entity_recognizer.extract_entities(answer)
        entities = self.entity_recognizer.disambiguate_entities()
        self.entity_recognizer.print_entities(to_file=question)

        # Answer extraction
        print(f"Question type: {self.answer_extractor.classify_question(question)}")
        extracted_answer, answer_text = self.answer_extractor.extract_answer(question, answer, entities)
        print(f"Extracted Answer: {answer_text}")

        fact_check = "correct"

        return answer, extracted_answer, entities, fact_check

