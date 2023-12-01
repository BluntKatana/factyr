from triple_extraction import TripleExtraction
from calculate_percentage import calculatePercentage
from fact_checking import FactChecking
from keyword_extraction_for_questions import AnsweringQuestion


# <---------------------------Step 1: Take input from the user ----------------------------->
queryInput = input("Enter your query\n")

extracted_triples_query = TripleExtraction.extract_openie_triples(queryInput)

if extracted_triples_query:
    # <---------------------------Step 2: Extract Text from wiki -------------------------------->

    text1 = """Rome (Italian and Latin: Roma [ˈroːma] ⓘ) is the capital city of Italy. It is also the capital of the Lazio region, the centre of the Metropolitan City of Rome, and a special comune named Comune di Roma Capitale. With 2,860,009 residents in 1,285 km2 (496.1 sq mi),[2] Rome is the country's most populated comune and the third most populous city in the European Union by population within city limits. The Metropolitan City of Rome, with a population of 4,355,725 residents, is the most populous metropolitan city in Italy.[3] Its metropolitan area is the third-most populous within Italy.[4] Rome is located in the central-western portion of the Italian Peninsula, within Lazio (Latium), along the shores of the Tiber. Vatican City (the smallest country in the world)[5] is an independent country inside the city boundaries of Rome, the only existing example of a country within a city. Rome is often referred to as the City of Seven Hills due to its geographic location, and also as the "Eternal City".[6] Rome is generally considered to be the "cradle of Western civilization and Christian culture", and the centre of the Catholic Church.[7][8][9]"""

    text2 = """Italy (Italian: Italia [iˈtaːlja] ⓘ), officially the Italian Republic (Italian: Repubblica Italiana [reˈpubblika itaˈljaːna]), is a country in Southern[13][14][15] and Western[16][a] Europe. Located in the middle of the Mediterranean Sea, it consists of a peninsula delimited by the Alps and surrounded by several islands.[17] Italy shares land borders with France, Switzerland, Austria, Slovenia and the enclaved microstates of Vatican City and San Marino. It has a territorial exclave in Switzerland (Campione) and an archipelago in the African Plate (Pelagie Islands). Italy covers an area of 301,340 km2 (116,350 sq mi),[3] with a population of nearly 60 million;[18] it is the tenth-largest country by land area in the European continent and the third-most populous member state of the European Union. Its capital and largest city is Rome."""

    # <---------------------------Step 3: Perform Triple Extraction -------------------------------->

    extracted_triples_text_1 = TripleExtraction.extract_openie_triples(text1)
    print("Extracted Triple:", extracted_triples_query)

    extracted_triples_text_2 = TripleExtraction.extract_openie_triples(text1)
    print("Extracted Triple:", extracted_triples_query)

    # <---------------------------Step 4: Calculate percentage from extracted triples ------------------------------->
    percentageEntity = calculatePercentage.calculate_percentage(
        extracted_triples_query, extracted_triples_text_1, extracted_triples_text_2
    )
    print(percentageEntity)

    # <---------------------------Step 5: Check the facts using spacy--------------------------->
    # result = FactChecking.check_query_in_context(query, text1)

    # <--------------------------- Final check --------------------------->
    if percentageEntity > 40:
        print(f"The context agrees with the query: {query}")
    else:
        print(f"The context does not agree with the query: {query}")

else:
    keywords_1, entities_1 = AnsweringQuestion(queryInput)

    text1 = """Italy (Italian: Italia [iˈtaːlja] ⓘ), officially the Italian Republic (Italian: Repubblica Italiana [reˈpubblika itaˈljaːna]), is a country in Southern[13][14][15] and Western[16][a] Europe. Located in the middle of the Mediterranean Sea, it consists of a peninsula delimited by the Alps and surrounded by several islands.[17] Italy shares land borders with France, Switzerland, Austria, Slovenia and the enclaved microstates of Vatican City and San Marino. It has a territorial exclave in Switzerland (Campione) and an archipelago in the African Plate (Pelagie Islands). Italy covers an area of 301,340 km2 (116,350 sq mi),[3] with a population of nearly 60 million;[18] it is the tenth-largest country by land area in the European continent and the third-most populous member state of the European Union. Its capital and largest city is Rome."""

    extracted_triples_text_1 = TripleExtraction.extract_openie_triples(text1)

    # Finding what the relation is (need to make this better)
    relation = [
        element
        for element in keywords_1
        if element.lower() not in (item.lower() for item in entities_1)
    ]
    print(relation)

    # Extracting the dictionary which has that relation
    capital_dict = next(
        item for item in extracted_triples_text_1 if relation[0] in item.values()
    )
    print(capital_dict)

    sentence_final = " ".join(capital_dict.values())
    keywords_final, entities_final = extract_keywords(sentence_final)
    # print(f"Keywords in sentence 2: {keywords_final}")
    print(f"Answer {entities_final}")
