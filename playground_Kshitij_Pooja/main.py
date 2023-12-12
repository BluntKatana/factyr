from Triple_Extraction_2.triple_extraction import TripleExtraction
from Results_3.calculate_percentage import calculatePercentage
from Results_3.fact_checking import FactChecking
from Results_3.keyword_extraction_for_questions import AnsweringQuestion
from Wikipedia_Links_Texts_1.get_wiki_text import WikipediaText

# <---------------------------Step 1: Take input from the user ----------------------------->
queryInput = input("Enter your query\n")


wiki_text = WikipediaText()
extracted_wiki = wiki_text.store_wiki_text(queryInput)

extracted_triples_query = TripleExtraction.extract_openie_triples(queryInput)
print("Extracted Triple:", extracted_triples_query)
# extracted_triples_query = []

if extracted_triples_query:
    # <---------------------------Step 3: Perform Triple Extraction -------------------------------->

    # extracted_triples_text_1 = TripleExtraction.extract_openie_triples(text1)
    # print("Extracted Triple 1:", extracted_triples_text_1)
    # extracted_triples = []
    # for text in extracted_wiki:
    #     extraction = TripleExtraction.extract_openie_triples(text)
    #     extracted_triples.append(extraction)
    #     print("Extracted Triple:", extracted_triples)

    extracted_triples_text_1 = TripleExtraction.extract_openie_triples(
        extracted_wiki[0]
    )
    extracted_triples_text_2 = TripleExtraction.extract_openie_triples(
        extracted_wiki[1]
    )

    # <---------------------------Step 4: Calculate percentage from extracted triples ------------------------------->
    percentageEntity = calculatePercentage.calculate_percentage(
        extracted_triples_query, extracted_triples_text_1, extracted_triples_text_2
    )
    print(percentageEntity)

    # <---------------------------Step 5: Check the facts using spacy--------------------------->
    # result = FactChecking.check_query_in_context(query, text1)

    # <--------------------------- Final check --------------------------->
    if percentageEntity > 40:
        print(f"The context agrees with the query: {queryInput}")
    else:
        print(f"The context does not agree with the query: {queryInput}")

else:
    keywords_1, entities_1 = AnsweringQuestion.extract_keywords(queryInput)

    # text = """–\xa0in Europe\xa0(light green &\xa0dark grey)–\xa0in the European Union\xa0(light green)\xa0 –\xa0 [Legend]\nItaly (Italian: Italia [iˈtaːlja] ⓘ), officially the Italian Republic (Italian: Repubblica Italiana [reˈpubblika itaˈljaːna]), is a country in Southern[14][15][16] and Western[17][a] Europe. Located in the middle of the Mediterranean Sea, it consists of a peninsula delimited by the Alps and surrounded by several islands.[18]\nItaly shares land borders with France, Switzerland, Austria, Slovenia and the enclaved microstates of Vatican City and San Marino. It has a territorial exclave in Switzerland (Campione) and an archipelago in the African Plate (Pelagie Islands). Italy covers an area of 301,340\xa0km2 (116,350\xa0sq\xa0mi),[3] with a population of nearly 60 million;[19] it is the tenth-largest country by land area in the European continent and the third-most populous member state of the European Union. Its capital and largest city is Rome."""

    extracted_triples_text = TripleExtraction.extract_openie_triples(extracted_wiki[0])

    # Finding what the relation is (need to make this better)
    relation = [
        element
        for element in keywords_1
        if element.lower() not in (item.lower() for item in entities_1)
    ]
    print(relation)

    # Extracting the dictionary which has that relation
    capital_dict = next(
        (
            item
            for item in extracted_triples_text
            if relation in str(item.values()).lower()
        ),
        None,
    )

    print(capital_dict)

    sentence_final = " ".join(capital_dict.values())
    keywords_final, entities_final = AnsweringQuestion.extract_keywords(sentence_final)
    # print(f"Keywords in sentence 2: {keywords_final}")
    print(f"Answer {entities_final}")
