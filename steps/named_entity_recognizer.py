import spacy

class NamedEntityRecognizer:
    def __init__(self):
        """
        Initialize using python -m spacy download en_core_web_s
        """
        self.nlp = spacy.load("en_core_web_sm")

    def extract_entities(self, text):
        doc = self.nlp(text)
        return [ent.text for ent in doc.ents]

    def disambiguate_entities(self, entities):
        # Implement logic to disambiguate entities
        return entities