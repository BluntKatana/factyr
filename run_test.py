import sys

from src.LanguageModel import LanguageModel
from src.EntityRecognizer import NamedEntityRecognizer
from src.AnswerExtractor import AnswerExtractor, ENTITY_QUESTION
from src.FactChecker import FactChecker
from src.WikiAPI import WikiAPI

import pandas as pd
import json

import warnings
warnings.filterwarnings("ignore")

def run_test(input, output):

    wiki_api = WikiAPI()
    entity_recognizer = NamedEntityRecognizer("en_core_web_sm", wiki_api)
    answer_extractor = AnswerExtractor('models', 'data')
    fact_checker = FactChecker(entity_recognizer, wiki_api)

    questions = pd.read_csv(input)
    all_data = []

    for index, question in questions.iterrows():

        print(f"Question {index + 1} of {len(questions)}")

        try:
            all_output = json.load(open(output, 'r'))
        except FileNotFoundError:
            all_output = {}

        if question['QuestionID'] in all_output:
            continue

        entities = entity_recognizer.get_entities(question["LLM_Answer"])
        for i in range(len(entities)):
            del entities[i]["context"]

        answer, _ = answer_extractor.extract_answer(question["Question"], question["LLM_Answer"], entities)
        fact_checker_answer = fact_checker.check(question["Question"], answer)


        all_output[question['QuestionID']] = {
            "QuestionID": question["QuestionID"],
            "Question": question["Question"],
            "RawAnswer": question["LLM_Answer"],
            "ExtractedAnswer": answer,
            "Entities": entities,
            "FactCheck": fact_checker_answer,
            "REALAnswer": {
                'title': question['Answer'],
                'url': question['Wikipedia_URL']
            },
            "REALQuestionType": ENTITY_QUESTION
        }


        print("---------")

        json.dump(all_output, open(output, 'w'), indent=4)


def annotate_test(input_f, output_f):

    data = json.load(open(input_f, 'r'))

    for q_id, q_data in data.items():

        try:
            output_data = json.load(open(output_f, 'r'))
        except:
            output_data = {}
        if q_id in output_data:
            continue

        print(f"Question: {q_data['Question']}")
        print(f"Answer: {q_data['RawAnswer']}")
        print(f"Real answer: {q_data['REALAnswer']['url']}")

        question_string = f"Is {q_data['ExtractedAnswer']['A']['name']} correctly extracted?"

        test = input(question_string)
        q_data['ExtractedAnswerCorrect'] = 'yes' if test == 'y' else 'no'

        test = input(f"Is {q_data['ExtractedAnswer']['A']['wikipedia_hit']['url']} the correct answer?")
        q_data['REALFactCheck'] = 'correct' if test == 'y' else 'incorrect'

        for entity in q_data['Entities']:

            print(f"Entity: {entity['name']}")
            test = input(f"Is {entity['wikipedia_hit']['url']} the correct entity?")
            entity['CorrectURL'] = 'yes' if test == 'y' else 'no'

        output_data[q_id] = q_data

        json.dump(output_data, open(output_f, 'w'), indent=4)

def evaluate(input_f):

    data = json.load(open(input_f, 'r'))

    correct_entities = 0
    total_entities = 0

    correct_answers = 0
    correct_fact_checks = 0
    correct_correct_fact_checks = 0
    total_correct = 0
    correct_incorrect_fact_checks = 0
    total_incorrect = 0
    recognition_mistakes = 26

    for q_id, q_data in data.items():

        if q_data['ExtractedAnswerCorrect'] == 'yes':
            correct_answers += 1

        if q_data['REALFactCheck'] == q_data['FactCheck']:
            correct_fact_checks += 1

            if q_data['REALFactCheck'] == 'correct':
                correct_correct_fact_checks += 1

            if q_data['REALFactCheck'] == 'incorrect':
                correct_incorrect_fact_checks += 1

        if q_data['REALFactCheck'] == 'correct':
            total_correct += 1
        if q_data['REALFactCheck'] == 'incorrect':
            total_incorrect += 1

        for entity in q_data['Entities']:
            total_entities += 1
            if entity['CorrectURL'] == 'yes':
                correct_entities += 1
            # else:
            #     test = input(f"Is {entity['name']} {entity['wikipedia_hit']['url']} a recognition mistake?")
            #     if test == 'y':
            #         recognition_mistakes += 1

    wrong_entities = total_entities - correct_entities
    print(f"Correct entities: {correct_entities}/{total_entities} ({correct_entities / total_entities * 100:.2f}%)")
    print(f"From which recognition mistakes: {recognition_mistakes}/{wrong_entities} ({recognition_mistakes / wrong_entities * 100:.2f}%)")
    print(f"Correct answers: {correct_answers}/{len(data)} ({correct_answers / len(data) * 100:.2f}%)")
    print(f"Correct fact checks: {correct_fact_checks}/{len(data)} ({correct_fact_checks / len(data) * 100:.2f}%)")
    print(f"Correctly predicted 'correct': {correct_correct_fact_checks}/{total_correct} ({correct_correct_fact_checks / total_correct * 100:.2f}%)")
    print(f"Correctly predicted 'incorrect': {correct_incorrect_fact_checks}/{total_incorrect} ({correct_incorrect_fact_checks / total_incorrect * 100:.2f}%)")



if __name__ == "__main__":

    try:
        input_f = sys.argv[1]
    except IndexError:
        print("Please provide an input file.")
        sys.exit()

    try:
        output = sys.argv[2]
    except IndexError:
        print("Please provide an output file.")
        sys.exit()

    evaluate(input_f)