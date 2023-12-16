import sys

from src.Pipeline import Pipeline
from EntityRecognizer import NamedEntityRecognizer
from src.AnswerExtractor import AnswerExtractor
from src.FileProcessor import FileProcessor
from src.FactChecker import FactChecker
from src.WikiAPI import WikiAPI

import warnings
warnings.filterwarnings("ignore")

import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"

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

    file_processor = FileProcessor(input, output)
    questions = file_processor.parse_input()

    entity_recognizer = NamedEntityRecognizer("en_core_web_sm")
    answer_extractor = AnswerExtractor()
    fact_checker = FactChecker(entity_recognizer)
    wiki_api = WikiAPI()
    pipeline = Pipeline(entity_recognizer, answer_extractor, fact_checker)

    for question in questions:
        print(question["question_id"], question["question"])
        answer, extracted_answer, entities, fact_check = pipeline.process_question(question["question"])
        file_processor.write_output(question["question_id"], question["question"], answer, extracted_answer, entities, fact_check)
        print("---------")
