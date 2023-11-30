class Pipeline:

    def __init__(self, language_model, entity_recognizer, answer_extractor):
        self.language_model = language_model
        self.entity_recognizer = entity_recognizer
        self.answer_extractor = answer_extractor

    def process_question(self, question, question_id):
        """
        Processes a question and returns the answer.

        :param question: question to be processed
        :param question_id: id of the question
        :return: answer to the question
        """

        print(f"Question: {question}")
        answer = self.language_model.get_answer(question)
        print(f"Answer: {answer}")

        # Entity recognition and linking
        self.entity_recognizer.extract_entities(answer)
        entities = self.entity_recognizer.disambiguate_entities()
        self.entity_recognizer.print_entities()

        # Answer extraction
        print(f"Question type: {self.answer_extractor.get_question_type(question, answer)}")
        extracted_answer = self.answer_extractor.extract_answer(question, answer, entities)
        print(f"Answer: {extracted_answer}")

        fact_check = "correct"

        return answer, extracted_answer, entities, fact_check

