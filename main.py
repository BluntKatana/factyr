from steps.fact_checker import FactChecker
from steps.language_model import LanguageModel
from steps.named_entity_recognizer import NamedEntityRecognizer
from steps.processor import Processor

if __name__ == "__main__":
    # Example usage:
    language_model = LanguageModel()
    entity_recognizer = NamedEntityRecognizer()
    knowledge_base = ["Managua", "Nicaragua"]  # Your knowledge base of relevant entities

    fact_checker = FactChecker(knowledge_base)
    processor = Processor(language_model, entity_recognizer, fact_checker)

    # Read questions from an input file
    input_file = "input.txt"
    with open(input_file, 'r') as file:
        lines = file.readlines()
        for idx, line in enumerate(lines):
            question_id, question = line.strip().split('<TAB>')
            output = processor.process_question(question, question_id)
            print(output)
