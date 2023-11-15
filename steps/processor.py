class Processor:
    def __init__(self, language_model, entity_recognizer, fact_checker):
        self.language_model = language_model
        self.entity_recognizer = entity_recognizer
        self.fact_checker = fact_checker

    def process_question(self, question, question_id):
        # Step 2: Interact with language model
        raw_text = self.language_model.interact(question)

        # Step 3: Extract named entities
        named_entities = self.entity_recognizer.extract_entities(raw_text)

        # Step 4: Extract answer (for simplicity, just take the first named entity)
        extracted_answer = named_entities[0] if named_entities else None

        # Step 5: Check fact using the fact checker
        correctness = self.fact_checker.check_fact(extracted_answer) if extracted_answer else "unknown"

        # Step 6: Output formatting
        output = (f"{question_id}\tR\"{raw_text}\"\n"
                  f"{question_id}\tA\"{extracted_answer}\"\n"
                  f"{question_id}\tC\"{correctness}\"\n"
                  + '\n'.join([f"{question_id}\tE\"{entity}\"\t\"https://en.wikipedia.org/wiki/{entity}\"" for entity in named_entities]))

        return output