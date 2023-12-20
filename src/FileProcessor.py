# ------------------------------------------------------ #
#
# FileProcessor.py handles parsing input file and writing
# to the output file according to the required format.
#
# Group 19: Pooja, Kshitij, Floris, Maik
#
# ------------------------------------------------------ #

import re


class FileProcessor:
    """
    Handles parsing input file and writing output file.

    :param in_path: path to input file
    :param out_path: path to output file
    """

    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path

        # Clear output file
        with open(self.out_path, 'w') as file:
            file.write('')

    def parse_input(self) -> list:
        """
        Parses input file and returns list of questions.
        Input example: question-001<TAB>Is Managua the capital of Nicaragua?
        """
        questions = []
        with open(self.in_path, 'r') as file:
            lines = file.readlines()
            for line in lines:

                # Split on 4 spaces or tab
                question_id, question = tuple(re.split(r' {4}|\t', line.strip()))
                questions.append({
                    "question_id": question_id,
                    "question": question
                })

        return questions

    def write_output(self, question_id, question, raw_answer, 
                     extracted_answer, entities, fact_check):
        """
        Writes output to file.

        :param question_id: id of the question
        :param question: question to be processed
        :param raw_answer: raw answer from language model
        :param extracted_answer: extracted answer
        :param entities: list of entities in the answer
        :param fact_check: fact check of the answer
        """

        with open(self.out_path, 'a') as file:

            # Raw answer
            raw_answer = raw_answer.replace('"', "'").replace('\n', ' ')
            file.write(f'{question_id}\tR"{raw_answer}"\n')

            # Extracted answer
            if extracted_answer['type'] == 1:
                file.write(f'{question_id}\tA"{extracted_answer["A"]}"\n')
            else:
                file.write(f'{question_id}\tA"{extracted_answer["A"]["name"]}"\t{extracted_answer["A"]["wikipedia_hit"]["url"]}\n')

            # Fact check
            file.write(f'{question_id}\tC"{fact_check}"\n')

            # Entities
            for entity in entities:
                file.write(f'{question_id}\tE"{entity["name"]}"\t{entity["wikipedia_hit"]["url"]}\n')
