# ------------------------------------------------------ #
#
# main.py is the main file of the project. It is used to
# parse the input file, throw every question at the pipeline
# and write the output to a file.
#
# Group 19: Pooja, Kshitij, Floris, Maik
#
# ------------------------------------------------------ #

import argparse
import os
import warnings

from src.AnswerExtractor import AnswerExtractor
from src.EntityRecognizer import NamedEntityRecognizer
from src.FactChecker import FactChecker
from src.FileProcessor import FileProcessor
from src.Pipeline import Pipeline
from src.WikiAPI import WikiAPI

# Suppress warnings
os.environ["TOKENIZERS_PARALLELISM"] = "false"
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
warnings.filterwarnings("ignore")

if __name__ == "__main__":

    # Parse arguments
    parser = argparse.ArgumentParser(description='factyr: an answer/entity extraction and fact checking pipeline.')
    parser.add_argument('--input', '-i', type=str, help='input file (txt)', required=True)
    parser.add_argument('--output', '-o', type=str, help='output file (txt)', default='factyr_output.txt')
    parser.add_argument('--verbose', '-v', action='store_true', help='verbose mode')
    args = parser.parse_args()

    # Parse input file
    file_processor = FileProcessor(args.input, args.output)
    questions = file_processor.parse_input()
    
    # Initialize pipeline
    wiki_api = WikiAPI()
    entity_recognizer = NamedEntityRecognizer("en_core_web_sm", wiki_api)
    answer_extractor = AnswerExtractor('models', 'data', entity_recognizer)
    fact_checker = FactChecker(entity_recognizer, wiki_api)
    pipeline = Pipeline(entity_recognizer, answer_extractor, fact_checker, verbose=args.verbose)

    # Process questions
    for question in questions:
        answer, extracted_answer, entities, fact_check = pipeline.process_question(question["question"], question["question_id"])
        file_processor.write_output(question["question_id"], 
                                    question["question"], 
                                    answer, extracted_answer,
                                    entities, fact_check)
