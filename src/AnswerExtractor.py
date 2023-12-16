import torch
from transformers import AutoModelForSequenceClassification, AutoTokenizer, AutoModelForQuestionAnswering, pipeline
import spacy
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import LogisticRegression
import re
import pickle
import os
import difflib

# Constants
YES_NO_QUESTION = 1
ENTITY_QUESTION = 2


class AnswerExtractor:

    def __init__(self, model_path, data_path):
        self._model_path = model_path
        self._data_path = data_path
        self.load_models()

    def load_models(self):

        print("+ Loading models for answer extraction...")

        print("++ Loading question classifier...")
        # Load trained models
        if not os.path.exists(f'{self._model_path}/qc_model_cv.pkl') or not os.path.exists(f'{self._model_path}/qc_model_lr.pkl'):
            self.train_question_classifier(f"{self._data_path}/qc_train.csv", self._model_path)
        self._q_cv = pickle.load(open(f'{self._model_path}/qc_model_cv.pkl', 'rb'))
        self._q_lr = pickle.load(open(f'{self._model_path}/qc_model_lr.pkl', 'rb'))

        print("++ Loading pre-trained yes/no question extractor...")
        try:
            self._yes_nomodel = AutoModelForSequenceClassification.from_pretrained(f"{self._model_path}/yes_no_model")
        except:
            self._yes_nomodel = AutoModelForSequenceClassification.from_pretrained("nfliu/roberta-large_boolq")
        self._yes_no_tokenizer = AutoTokenizer.from_pretrained("nfliu/roberta-large_boolq")

        print("++ Loading SpaCy NLP model...")
        self._nlp = spacy.load("en_core_web_sm")

        print("++ Loading entity answer extractor...")
        model_name = "deepset/roberta-base-squad2"
        try:
            model = AutoModelForQuestionAnswering.from_pretrained(f"{self._model_path}/entity_model")
        except:
            model = AutoModelForQuestionAnswering.from_pretrained(model_name)
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._entity_extractor = pipeline('question-answering', model=model, tokenizer=tokenizer)

    def train_question_classifier(self, train_data, save_path):
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

        with open(f'{save_path}/qc_model_cv.pkl', 'wb') as f:
            pickle.dump(cv, f)
        with open(f'{save_path}/qc_model_lr.pkl', 'wb') as f:
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

        yn_answer = 'yes' if probabilities[0] < probabilities[1] else 'no'

        return {'A': yn_answer, 'type': YES_NO_QUESTION}, yn_answer

    def answer_entity_question(self, question, answer, entities):
        """
        Answers a question about an entity.

        :param question: question to be answered
        :param answer: answer to the question
        :param entities: list of entities in the answer
        """

        QA_input = {
            'question': question,
            'context': answer
        }
        extracted_answer = self._entity_extractor(QA_input)

        similarities = [(entity, difflib.SequenceMatcher(None, entity['name'], extracted_answer['answer']).ratio()) for entity in entities]
        most_similar = max(similarities, key=lambda x: x[1])[0]

        return {'A': most_similar, 'type': ENTITY_QUESTION}, most_similar['name']