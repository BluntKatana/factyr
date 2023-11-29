# Constants
YES_NO_QUESTION = 1
ENTITY_QUESTION = 2


class AnswerExtractor:

    def get_question_type(self, question, answer):
        """
        Determines the type of the question.
        Very simple base: check if the first word in the question is a Wh-word.
        https://www.lawlessenglish.com/learn-english/grammar/questions-wh/

        :param question: question to be checked
        :param answer: answer to the question
        """

        Wh_words = ["who", "whom", "what", "where", "when",
                    "why", "how", "which", "whose"]
        if question.lower().split()[0] in Wh_words:
            return ENTITY_QUESTION

        return YES_NO_QUESTION
