import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer

# Constants
YES_NO_QUESTION = 1
ENTITY_QUESTION = 2


class AnswerExtractor:

    def __init__(self):
        self._yes_nomodel = AutoModelForSequenceClassification.from_pretrained("nfliu/roberta-large_boolq")
        self._yes_no_tokenizer = AutoTokenizer.from_pretrained("nfliu/roberta-large_boolq")

    def extract_answer(self, question, answer, entities):
        """
        Extracts the answer from the given question and answer.

        :param question: question to be answered
        :param answer: answer to the question
        """

        question_type = self.get_question_type(question, answer)

        if question_type == YES_NO_QUESTION:
            return self.answer_yes_no_question(question, answer)
        else:
            return self.answer_entity_question(question, answer, entities)

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

    def answer_yes_no_question(self, question, answer):
        """
        Answers a yes/no question. Uses a pre-trained model based on
        'boolq' dataset: 

        :param question: question to be answered
        :param answer: answer to the question
        """

        sequence = self._yes_no_tokenizer.encode_plus(question, answer, 
                                                      return_tensors="pt")['input_ids'].to('cpu')

        with torch.no_grad():
            logits = self._yes_nomodel(sequence)[0]
            probabilities = torch.softmax(logits, dim=1).detach().cpu().tolist()[0]

        return 'yes' if probabilities[0] < probabilities[1] else 'no'

    def answer_entity_question(self, question, answer, entities):
        """
        Answers a question about an entity.

        :param question: question to be answered
        :param answer: answer to the question
        :param entities: list of entities in the answer
        """

        return entities[0]