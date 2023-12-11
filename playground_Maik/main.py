import sys

from Pipeline import Pipeline
from LanguageModel import LanguageModel
from EntityRecognizer_TESTING import NamedEntityRecognizer
from AnswerExtractor import AnswerExtractor
from FileProcessor import FileProcessor

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

    file_processor = FileProcessor(input, output)
    questions = file_processor.parse_input()

    # language_model = LanguageModel()
    entity_recognizer = NamedEntityRecognizer("en_core_web_sm")
    answer_extractor = AnswerExtractor()
    pipeline = Pipeline(None, entity_recognizer, answer_extractor)

    for question in questions:
        print(question["question_id"], question["question"])
        answer, extracted_answer, entities, fact_check = pipeline.process_question(question["question"])
        file_processor.write_output(question["question_id"], question["question"], answer, extracted_answer, entities, fact_check)
        print("---------")
