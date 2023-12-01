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
sentence_3 = "Netherlands is country located in Europe with territories"
# Extract keywords and entities from the sentences
keywords_1, entities_1 = extract_keywords(sentence_1)
keywords_2, entities_2 = extract_keywords(sentence_2)
keywords_3, entities_3 = extract_keywords(sentence_3)



wiki_of_netherlands = [
    {
        "subject": "Netherlands",
        "relation": "is",
        "object": "country located in Europe with territories",
    },
    {
        "subject": "Netherlands",
        "relation": "is",
        "object": "country located with territories",
    },
    {
        "subject": "country",
        "relation": "located with",
        "object": "overseas territories",
    },
    {
        "subject": "Netherlands",
        "relation": "is",
        "object": "country located in northwestern Europe",
    },
    {"subject": "country", "relation": "located in", "object": "northwestern Europe"},
    {"subject": "overseas territories", "relation": "is in", "object": "Caribbean"},
    {
        "subject": "Netherlands",
        "relation": "is",
        "object": "country located in northwestern Europe with overseas territories",
    },
    {"subject": "Netherlands", "relation": "is", "object": "country located in Europe"},
    {
        "subject": "Netherlands",
        "relation": "is",
        "object": "country located in Europe with overseas territories",
    },
    {
        "subject": "Netherlands",
        "relation": "is",
        "object": "country located with territories in Caribbean",
    },
    {"subject": "country", "relation": "located in", "object": "Europe"},
    {
        "subject": "Netherlands",
        "relation": "is",
        "object": "country located in northwestern Europe with territories",
    },
    {"subject": "Netherlands", "relation": "is", "object": "country"},
    {
        "subject": "country",
        "relation": "located with",
        "object": "territories Caribbean",
    },
    {"subject": "country", "relation": "located with", "object": "territories"},
    {
        "subject": "Netherlands",
        "relation": "is",
        "object": "country located with overseas territories",
    },
    {"subject": "Netherlands", "relation": "is", "object": "country located"},
    {"subject": "It", "relation": "is", "object": "largest"},
    {
        "subject": "It",
        "relation": "is largest of",
        "object": "four constituent countries",
    },
    {"subject": "It", "relation": "is largest of", "object": "four countries"},
    {
        "subject": "It",
        "relation": "is largest of",
        "object": "four countries of Kingdom of Netherlands",
    },
    {
        "subject": "It",
        "relation": "is largest of",
        "object": "four constituent countries of Kingdom",
    },
    {
        "subject": "It",
        "relation": "is largest of",
        "object": "four countries of Kingdom",
    },
    {
        "subject": "It",
        "relation": "is largest of",
        "object": "four constituent countries of Kingdom of Netherlands",
    },
    {"subject": "it", "relation": "Belgium to", "object": "south"},
    {
        "subject": "it",
        "relation": "Belgium with",
        "object": "North Sea coastline to north",
    },
    {"subject": "it", "relation": "borders Germany to", "object": "east"},
    {
        "subject": "Belgium",
        "relation": "is with",
        "object": "North Sea coastline to north",
    },
    {"subject": "it", "relation": "Belgium with", "object": "North Sea coastline"},
    {"subject": "it", "relation": "borders", "object": "Germany"},
    {"subject": "it", "relation": "borders to", "object": "east"},
    {"subject": "Netherlands", "relation": "consists of", "object": "twelve provinces"},
    {"subject": "It", "relation": "also has", "object": "border with France"},
    {
        "subject": "It",
        "relation": "also has",
        "object": "border on split island of Saint Martin in Caribbean",
    },
    {"subject": "It", "relation": "has", "object": "border on split island"},
    {
        "subject": "It",
        "relation": "has",
        "object": "border on split island of Saint Martin in Caribbean",
    },
    {
        "subject": "It",
        "relation": "also has",
        "object": "border on split island of Saint Martin",
    },
    {
        "subject": "It",
        "relation": "also has",
        "object": "border with France on split island of Saint Martin",
    },
    {
        "subject": "It",
        "relation": "has",
        "object": "border with France on split island of Saint Martin in Caribbean",
    },
    {"subject": "It", "relation": "has", "object": "border with France"},
    {
        "subject": "It",
        "relation": "also has",
        "object": "border with France on split island of Saint Martin in Caribbean",
    },
    {
        "subject": "It",
        "relation": "has",
        "object": "border with France on split island of Saint Martin",
    },
    {"subject": "border", "relation": "is with", "object": "France"},
    {
        "subject": "It",
        "relation": "also has",
        "object": "border with France on split island",
    },
    {
        "subject": "It",
        "relation": "has",
        "object": "border with France on split island in Caribbean",
    },
    {
        "subject": "It",
        "relation": "has",
        "object": "border with France on split island",
    },
    {"subject": "It", "relation": "also has", "object": "border"},
    {
        "subject": "It",
        "relation": "also has",
        "object": "border with France on split island in Caribbean",
    },
    {"subject": "It", "relation": "also has", "object": "border on split island"},
    {
        "subject": "It",
        "relation": "has",
        "object": "border on split island of Saint Martin",
    },
    {"subject": "split island", "relation": "is in", "object": "Caribbean"},
    {
        "subject": "It",
        "relation": "also has",
        "object": "border on split island in Caribbean",
    },
    {"subject": "It", "relation": "has", "object": "border"},
    {
        "subject": "It",
        "relation": "has",
        "object": "border on split island in Caribbean",
    },
    {"subject": "It", "relation": "shares borders with", "object": "United Kingdom"},
    {"subject": "It", "relation": "shares with", "object": "United Kingdom"},
    {"subject": "It", "relation": "shares", "object": "maritime borders"},
    {"subject": "It", "relation": "shares", "object": "borders"},
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as language",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as official language in province",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary language",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary language in province",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as language",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary official language",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary official language in province",
    },
    {"subject": "official language", "relation": "is", "object": "Dutch"},
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as language in province",
    },
    {"subject": "language", "relation": "is", "object": "Dutch"},
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as language in province of Friesland",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as language in province",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary language",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary language in province of Friesland",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary official language in province of Friesland",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as official language in province of Friesland",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as official language in province of Friesland",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary official language in province of Friesland",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as official language",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary language in province of Friesland",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as official language",
    },
    {
        "subject": "secondary official language",
        "relation": "is in",
        "object": "province of Friesland",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary language in province",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as official language in province",
    },
    {
        "subject": "language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary official language in province",
    },
    {"subject": "language", "relation": "is Dutch with", "object": "West Frisian"},
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as secondary official language",
    },
    {
        "subject": "official language",
        "relation": "is Dutch with",
        "object": "West Frisian as language in province of Friesland",
    },
    {
        "subject": "Dutch",
        "relation": "are official in",
        "object": "Caribbean territories",
    },
    {
        "subject": "English",
        "relation": "are",
        "object": "official in Caribbean territories",
    },
    {"subject": "Papiamento", "relation": "are official in", "object": "territories"},
    {"subject": "English", "relation": "are", "object": "official"},
    {
        "subject": "English",
        "relation": "are official in",
        "object": "Caribbean territories",
    },
    {"subject": "Dutch", "relation": "are", "object": "official in territories"},
    {
        "subject": "Papiamento",
        "relation": "are official in",
        "object": "Caribbean territories",
    },
    {
        "subject": "Dutch",
        "relation": "are",
        "object": "official in Caribbean territories",
    },
    {"subject": "English", "relation": "are official in", "object": "territories"},
    {"subject": "Dutch", "relation": "are", "object": "official"},
    {"subject": "Dutch", "relation": "are official in", "object": "territories"},
    {"subject": "Papiamento", "relation": "are", "object": "official"},
    {"subject": "English", "relation": "are", "object": "official in territories"},
    {"subject": "capital", "relation": "is", "object": "amsterdam"},

]



# Print the results
print(f"Keywords in sentence 1: {keywords_1}")
print(f"Named entities in sentence 1: {entities_1}")
print()
print(f"Keywords in sentence 2: {keywords_2}")
print(f"Named entities in sentence 2: {entities_2}")

#Take the paragraph of named entity and in that find the other entity (in this case capital) and in that capital triplet find subject / object

array1 = ['capital', 'netherlands']
array2 = ['Netherlands']

# Finding what the relation is (need to make this better)
relation = [element for element in keywords_1 if element.lower() not in (item.lower() for item in entities_1)]
print(relation)

# Extracting the dictionary which has that relation
capital_dict = next(item for item in wiki_of_netherlands if relation[0] in item.values())
print(capital_dict)

sentence_final = " ".join(capital_dict.values())
keywords_final, entities_final = extract_keywords(sentence_final)
print(f"Keywords in sentence 2: {keywords_final}")
print(f"Named entities in sentence 2: {entities_final}")