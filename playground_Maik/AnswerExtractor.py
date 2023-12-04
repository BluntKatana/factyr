import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import re
import pickle
import os

# Constants
YES_NO_QUESTION = 1
ENTITY_QUESTION = 2


class AnswerExtractor:

    def __init__(self):
        self.load_models()

    def load_models(self):

        print("+ Loading models for answer extraction...")

        print("++ Loading question classifier...")
        # Load trained models
        if not os.path.exists('data/qc_model_cv.pkl') or not os.path.exists('data/qc_model_lr.pkl'):
            self.train_question_classifier("data/qc_train.csv")
        self._q_cv = pickle.load(open('data/qc_model_cv.pkl', 'rb'))
        self._q_lr = pickle.load(open('data/qc_model_lr.pkl', 'rb'))

        print("++ Loading pre-trained yes/no question extractor...")
        self._yes_nomodel = AutoModelForSequenceClassification.from_pretrained("nfliu/roberta-large_boolq")
        self._yes_no_tokenizer = AutoTokenizer.from_pretrained("nfliu/roberta-large_boolq")

        print("++ Loading SpaCy NLP model...")
        self._nlp = spacy.load("en_core_web_sm")

    def train_question_classifier(self, train_data):
        """
        Trains a question classifier based on the given training data.
        Combination of:
        https://www.kaggle.com/datasets/rtatman/questionanswer-dataset
        https://www.kaggle.com/datasets/ananthu017/question-classification

        :param train_data: path to training data file
        """
        def process(text):
            r = re.sub(r'[^a-zA-Z]', ' ', text)
            r = r.lower()
            return r

        print("+++ Training question classifier...")

        data = pd.read_csv(train_data).dropna()
        data['text_proc'] = data['text'].map(process)

        cv = CountVectorizer()
        X_train_cv = cv.fit_transform(data['text_proc'])
        y_train = data['type']

        lr = LogisticRegression(max_iter=1000)
        lr.fit(X_train_cv, y_train)

        with open('data/qc_model_cv.pkl', 'wb') as f:
            pickle.dump(cv, f)
        with open('data/qc_model_lr.pkl', 'wb') as f:
            pickle.dump(lr, f)

    def extract_answer(self, question, answer, entities):
        """
        Extracts the answer from the given question and answer.

        :param question: question to be answered
        :param answer: answer to the question
        """

        question_type = self.classify_question(question)

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

    def classify_question(self, question):
        """
        Classifies the question into yes/no or entity question.
        Uses a trained model based on 'message_types.csv' dataset.
        Combination of:
        https://www.kaggle.com/datasets/rtatman/questionanswer-dataset
        https://www.kaggle.com/datasets/ananthu017/question-classification

        :param question: question to be classified
        """
        def process(text):
            r = re.sub(r'[^a-zA-Z]', ' ', text)
            r = r.lower()
            return r

        q_vector = self._q_cv.transform([process(question)])
        q_pred = self._q_lr.predict(q_vector)

        return YES_NO_QUESTION if q_pred[0] == 'yn' else ENTITY_QUESTION

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

        return {'A': 'yes' if probabilities[0] < probabilities[1] else 'no', 'type': YES_NO_QUESTION}

    def answer_entity_question(self, question, answer, entities):
        """
        Answers a question about an entity.

        :param question: question to be answered
        :param answer: answer to the question
        :param entities: list of entities in the answer
        """

        # Return first entity that is not in the question
        question_nlp = self._nlp(question)
        question_ents = [ent.text for ent in question_nlp.ents]

        return {'A': [entity for entity in entities if entity['name'] not in question_ents][0], 'type': ENTITY_QUESTION}