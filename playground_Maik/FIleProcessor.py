import re


class FileProcessor:

    def __init__(self, in_path, out_path):
        self.in_path = in_path
        self.out_path = out_path

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
