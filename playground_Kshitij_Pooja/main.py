from Triple_Extraction_2.triple_extraction import TripleExtraction
from Results_3.calculate_percentage import calculatePercentage
from Results_3.fact_checking import FactChecking
from Results_3.keyword_extraction_for_questions import AnsweringQuestion
from Wikipedia_Links_Texts_1.get_wiki_text import WikipediaText

# <---------------------------Step 1: Take input from the user ----------------------------->
queryInput = input("Enter your query\n")


wiki_text = WikipediaText()
extracted_wiki = wiki_text.store_wiki_text(queryInput)

print("=========================================>", extracted_wiki)

extracted_triples_query = TripleExtraction.extract_openie_triples(queryInput)
print("Extracted Triple:", extracted_triples_query)
# extracted_triples_query = []

if extracted_triples_query:
    # <---------------------------Step 2: Extract Text from wiki -------------------------------->

    # text1 = """Managua (Spanish pronunciation: [maˈnaɣwa]) is the capital and largest city of Nicaragua, and one of the largest cities in Central America. Located on the shores of Lake Managua, the city had an estimated population of 1,055,247 as of 2020,[4] and a population of 1,401,687[4] in its metropolitan area.[6] The city also serves as the seat of Managua Department."""

    # text2 = """Nicaragua (/ˌnɪkəˈrɑːɡwə, -ˈræɡ-, -ɡjuə/ ⓘ; Spanish: [nikaˈɾaɣwa] ⓘ), officially the Republic of Nicaragua (Spanish: República de Nicaraguaⓘ), is the largest country in Central America, bordered by Honduras to the north, the Caribbean to the east, Costa Rica to the south, and the Pacific Ocean to the west. Managua is the country's capital and largest city. As of 2015, it was estimated to be the third largest city in Central America. Nicaragua's multiethnic population of six million includes people of mestizo, Indigenous, European and African heritage. The main language is Spanish. Indigenous tribes on the Mosquito Coast speak their own languages and English."""

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

    # text1 = """Italy (Italian: Italia [iˈtaːlja] ⓘ), officially the Italian Republic (Italian: Repubblica Italiana [reˈpubblika itaˈljaːna]), is a country in Southern[13][14][15] and Western[16][a] Europe. Located in the middle of the Mediterranean Sea, it consists of a peninsula delimited by the Alps and surrounded by several islands.[17] Italy shares land borders with France, Switzerland, Austria, Slovenia and the enclaved microstates of Vatican City and San Marino. It has a territorial exclave in Switzerland (Campione) and an archipelago in the African Plate (Pelagie Islands). Italy covers an area of 301,340 km2 (116,350 sq mi),[3] with a population of nearly 60 million;[18] it is the tenth-largest country by land area in the European continent and the third-most populous member state of the European Union. Its capital and largest city is Rome."""

    text = TripleExtraction.extract_openie_triples(extracted_wiki[0])
    extracted_triples_text_1 = TripleExtraction.extract_openie_triples(text)

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
            for item in extracted_triples_text_1
            if "capital" in str(item.values()).lower()
        ),
        None,
    )

    print(capital_dict)

    sentence_final = " ".join(capital_dict.values())
    keywords_final, entities_final = AnsweringQuestion.extract_keywords(sentence_final)
    # print(f"Keywords in sentence 2: {keywords_final}")
    print(f"Answer {entities_final}")
