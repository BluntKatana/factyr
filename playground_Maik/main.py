import sys
import re

from Pipeline import Pipeline
from LanguageModel import LanguageModel
from EntityRecognizer import NamedEntityRecognizer
from FactChecker import FactChecker
from FIleProcessor import FileProcessor

if __name__ == "__main__":
    input = "examples\example_input.txt"
    output = "examples\example_out.txt"

    file_processor = FileProcessor(input, output)
    questions = file_processor.parse_input()

    language_model = LanguageModel()
    entity_recognizer = NamedEntityRecognizer("en_core_web_sm")
    fact_checker = FactChecker()
    pipeline = Pipeline(language_model, entity_recognizer, fact_checker)

    for question in questions:
        print(question["question_id"], question["question"])
        pipeline.process_question(question["question"], question["question_id"])
