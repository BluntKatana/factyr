import spacy


class AnsweringQuestion:
    def extract_keywords(sentence):
        # Load the spaCy model
        nlp = spacy.load("en_core_web_sm")

        # Process the sentence
        doc = nlp(sentence)

        # Filter out stopwords and extract relevant keywords
        keywords = [
            token.text.lower() for token in doc if token.is_alpha and not token.is_stop
        ]

        # Identify named entities
        entities = [ent.text for ent in doc.ents]

        return keywords, entities

    # Print the results
