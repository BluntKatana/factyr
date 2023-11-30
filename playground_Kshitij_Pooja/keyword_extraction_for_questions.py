import spacy


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


# Example sentences
sentence_1 = "What is the capital of Netherlands?"
sentence_2 = "Who is the president of USA?"

# Extract keywords and entities from the sentences
keywords_1, entities_1 = extract_keywords(sentence_1)
keywords_2, entities_2 = extract_keywords(sentence_2)

# Print the results
print(f"Keywords in sentence 1: {keywords_1}")
print(f"Named entities in sentence 1: {entities_1}")
print()
print(f"Keywords in sentence 2: {keywords_2}")
print(f"Named entities in sentence 2: {entities_2}")
