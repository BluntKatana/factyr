import sys

from Pipeline import Pipeline
from LanguageModel import LanguageModel
from EntityRecognizer_TESTING import NamedEntityRecognizer
from AnswerExtractor import AnswerExtractor

import pandas as pd
import json

import warnings
warnings.filterwarnings("ignore")

if __name__ == "__main__":

    try:
        input = sys.argv[1]
    except IndexError:
        print("Please provide an input file.")
        sys.exit()

    try:
        output = sys.argv[2]
    except IndexError:
        print("Please provide an output file.")
        sys.exit()

    language_model = LanguageModel()
    entity_recognizer = NamedEntityRecognizer("en_core_web_sm")
    answer_extractor = AnswerExtractor()
    pipeline = Pipeline(language_model, entity_recognizer, answer_extractor)

    questions = pd.read_csv(input)
    all_data = []

    for index, question in questions.iterrows():

        if index > 10:
            break
        print(question["QuestionID"], question["Question"])
        answer, extracted_answer, entities, fact_check = pipeline.process_question(question["Question"])

        dict_data = {
            "QuestionID": question["QuestionID"],
            "Question": question["Question"],
            "Answer": answer.replace('\n', ' ').strip(),
            "ExtractedAnswer": extracted_answer,
            "Entities": entities,
            "FactCheck": fact_check
        }

        all_data.append(dict_data)

        print("---------")

    json.dump(all_data, open(output, 'w'), indent=4)