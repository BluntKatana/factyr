class FactChecker:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

    def check_fact(self, extracted_answer):
        # Implement logic to check correctness by comparing with the knowledge base
        return "correct" if extracted_answer.lower() in self.knowledge_base else "incorrect"