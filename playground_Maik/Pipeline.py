class Pipeline:

    def __init__(self, language_model, entity_recognizer, fact_checker):
        self.language_model = language_model
        self.entity_recognizer = entity_recognizer
        self.fact_checker = fact_checker

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

        # Fact checking
        print(f"Question type: {self.fact_checker.get_question_type(question, answer)}")
        # TODO!
