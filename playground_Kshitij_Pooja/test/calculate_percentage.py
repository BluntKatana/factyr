def calculate_percentage(question, rel1, rel2):
    combined_relations = rel1 + rel2
    matching_relations = set()

    for q in question:
        for rel in combined_relations:
            if (
                q["subject"] == rel["subject"]
                or q["subject"] == rel["object"]
                or q["object"] == rel["subject"]
                or q["object"] == rel["object"]
            ):
                matching_relations.add(tuple(rel.items()))

        print("Matching relation-------------------------->", matching_relations)

    x = len(matching_relations)
    print("X=====================>", x)
    y = len(combined_relations)
    print("Y================================?", y)
    print((x / y) * 100)


question = [
    {"subject": "Rome", "relation": "Is capital of", "object": "Italy"},
    {"subject": "Rome", "relation": "Is", "object": "capital"},
]
Rome = [
    {"subject": "Rome", "relation": "is", "object": "capital city of Italy"},
    {"subject": "Rome", "relation": "is", "object": "capital city"},
    {"subject": "It", "relation": "is", "object": "capital"},
    {"subject": "It", "relation": "centre of", "object": "Metropolitan City of Rome"},
    {"subject": "It", "relation": "is", "object": "also capital"},
    {"subject": "It", "relation": "is also capital of", "object": "Lazio region"},
    {"subject": "It", "relation": "centre of", "object": "Metropolitan City"},
    {"subject": "It comune", "relation": "named", "object": "Comune di Roma Capitale"},
    {
        "subject": "It special comune",
        "relation": "named",
        "object": "Comune di Roma Capitale",
    },
    {"subject": "It", "relation": "is capital of", "object": "Lazio region"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents country 's populated comune by population",
    },
    {"subject": "2,860,009 residents", "relation": "is in", "object": "1,285 km2"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents country 's comune",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents country 's comune by population",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "country 's most populated comune by population",
    },
    {
        "subject": "Rome",
        "relation": "third populous city in",
        "object": "European Union",
    },
    {"subject": "Rome", "relation": "is", "object": "country 's comune by population"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents in 1,285 km2 country 's populated comune",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents in 1,285 km2 country 's most populated comune by population",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "country 's populated comune by population",
    },
    {
        "subject": "country 's populated comune",
        "relation": "is With",
        "object": "2,860,009 residents in 1,285 km2",
    },
    {"subject": "Rome", "relation": "is", "object": "country 's most populated comune"},
    {"subject": "Rome", "relation": "is", "object": "country 's comune"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents in 1,285 km2 country 's populated comune by population",
    },
    {"subject": "Rome", "relation": "populous city in", "object": "European Union"},
    {
        "subject": "Rome",
        "relation": "most populous city in",
        "object": "European Union",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents in 1,285 km2 country 's comune",
    },
    {"subject": "third populous city", "relation": "is in", "object": "European Union"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents in 1,285 km2 country 's most populated comune",
    },
    {"subject": "Rome", "relation": "third city in", "object": "European Union"},
    {"subject": "Rome", "relation": "is", "object": "country 's populated comune"},
    {"subject": "Rome", "relation": "city in", "object": "European Union"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents country 's populated comune",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents country 's most populated comune",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents country 's most populated comune by population",
    },
    {
        "subject": "Rome",
        "relation": "third most populous city in",
        "object": "European Union",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "With 2,860,009 residents in 1,285 km2 country 's comune by population",
    },
    {
        "subject": "Metropolitan City",
        "relation": "is with",
        "object": "population of 4,355,725 residents",
    },
    {
        "subject": "Metropolitan City",
        "relation": "is most populous metropolitan city in",
        "object": "Italy",
    },
    {
        "subject": "Metropolitan City",
        "relation": "is most populous city in",
        "object": "Italy",
    },
    {"subject": "Metropolitan City", "relation": "is", "object": "city"},
    {"subject": "Metropolitan City", "relation": "is", "object": "metropolitan city"},
    {
        "subject": "Metropolitan City",
        "relation": "is metropolitan city in",
        "object": "Italy",
    },
    {"subject": "Metropolitan City", "relation": "is", "object": "most populous city"},
    {"subject": "Metropolitan City", "relation": "is", "object": "populous city"},
    {
        "subject": "Metropolitan City",
        "relation": "is",
        "object": "most populous metropolitan city",
    },
    {
        "subject": "Metropolitan City",
        "relation": "is populous city in",
        "object": "Italy",
    },
    {"subject": "populous metropolitan city", "relation": "is in", "object": "Italy"},
    {
        "subject": "Metropolitan City",
        "relation": "is",
        "object": "populous metropolitan city",
    },
    {
        "subject": "Metropolitan City",
        "relation": "is populous metropolitan city in",
        "object": "Italy",
    },
    {"subject": "Metropolitan City", "relation": "is city in", "object": "Italy"},
    {"subject": "Its area", "relation": "is", "object": "populous"},
    {
        "subject": "Its metropolitan area",
        "relation": "is populous within",
        "object": "Italy",
    },
    {"subject": "Its metropolitan area", "relation": "is", "object": "populous"},
    {
        "subject": "Its metropolitan area",
        "relation": "is third-most populous within",
        "object": "Italy",
    },
    {"subject": "Its area", "relation": "is", "object": "third-most populous"},
    {"subject": "Its area", "relation": "is populous within", "object": "Italy"},
    {
        "subject": "Its area",
        "relation": "is third-most populous within",
        "object": "Italy",
    },
    {
        "subject": "Its metropolitan area",
        "relation": "is",
        "object": "third-most populous",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in portion along shores of Tiber",
    },
    {"subject": "Rome", "relation": "is located in", "object": "portion"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located within Lazio Latium along shores",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion of Italian Peninsula along shores",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in portion of Italian Peninsula within Lazio Latium",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located within Lazio Latium along shores of Tiber",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion along shores of Tiber",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in portion of Italian Peninsula along shores of Tiber",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion of Italian Peninsula within Lazio Latium along shores",
    },
    {"subject": "Rome", "relation": "is", "object": "located"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion of Italian Peninsula within Lazio Latium",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in portion within Lazio Latium along shores",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in portion within Lazio Latium along shores of Tiber",
    },
    {"subject": "Rome", "relation": "is located in", "object": "western portion"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion within Lazio Latium along shores",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion within Lazio Latium along shores",
    },
    {
        "subject": "Rome",
        "relation": "is located in",
        "object": "western portion of Italian Peninsula",
    },
    {"subject": "Rome", "relation": "is located along", "object": "shores of Tiber"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion of Italian Peninsula within Lazio Latium along shores of Tiber",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in portion within Lazio Latium",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion within Lazio Latium",
    },
    {
        "subject": "Rome",
        "relation": "is located in",
        "object": "central western portion",
    },
    {"subject": "Rome", "relation": "is", "object": "located in portion along shores"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion within Lazio Latium",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion along shores",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion along shores of Tiber",
    },
    {"subject": "Rome", "relation": "is located within", "object": "Lazio Latium"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion of Italian Peninsula within Lazio Latium along shores",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion of Italian Peninsula along shores of Tiber",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion within Lazio Latium along shores of Tiber",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in portion of Italian Peninsula within Lazio Latium along shores",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion of Italian Peninsula along shores",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion along shores",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion of Italian Peninsula within Lazio Latium along shores of Tiber",
    },
    {"subject": "Rome", "relation": "is located along", "object": "shores"},
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion within Lazio Latium along shores of Tiber",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in portion of Italian Peninsula within Lazio Latium along shores of Tiber",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in portion of Italian Peninsula along shores",
    },
    {
        "subject": "Rome",
        "relation": "is located in",
        "object": "portion of Italian Peninsula",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in western portion of Italian Peninsula along shores of Tiber",
    },
    {
        "subject": "Rome",
        "relation": "is located in",
        "object": "central western portion of Italian Peninsula",
    },
    {
        "subject": "Rome",
        "relation": "is",
        "object": "located in central western portion of Italian Peninsula within Lazio Latium",
    },
    {
        "subject": "Vatican City",
        "relation": "is country inside",
        "object": "city boundaries of Rome",
    },
    {
        "subject": "Vatican City",
        "relation": "is independent country inside",
        "object": "city boundaries of Rome",
    },
    {"subject": "Vatican City", "relation": "is", "object": "country"},
    {"subject": "City", "relation": "is independent", "object": "boundaries"},
    {
        "subject": "Vatican City",
        "relation": "is independent country inside",
        "object": "city boundaries",
    },
    {"subject": "Vatican City", "relation": "is", "object": "independent country"},
    {
        "subject": "Vatican City",
        "relation": "is country inside",
        "object": "city boundaries",
    },
    {
        "subject": "city boundaries",
        "relation": "inside country is",
        "object": "only existing example of country within city",
    },
    {
        "subject": "independent country",
        "relation": "example of",
        "object": "country within city",
    },
    {"subject": "smallest country", "relation": "is in", "object": "world"},
    {"subject": "Rome", "relation": "is referred to", "object": "to City of Seven"},
    {
        "subject": "Rome",
        "relation": "is often referred due",
        "object": "its geographic location",
    },
    {"subject": "Rome", "relation": "is referred due", "object": "its location"},
    {
        "subject": "Rome",
        "relation": "is often referred to",
        "object": "to City of Seven",
    },
    {"subject": "Rome", "relation": "is referred to", "object": "to City"},
    {"subject": "Rome", "relation": "is", "object": "often referred"},
    {"subject": "Seven", "relation": "of City is", "object": "Hills"},
    {"subject": "Rome", "relation": "is referred to", "object": "Hills"},
    {"subject": "Rome", "relation": "is often referred to", "object": "Hills"},
    {"subject": "Rome", "relation": "is often referred to", "object": "to City"},
    {"subject": "Rome", "relation": "is often referred due", "object": "its location"},
    {"subject": "Rome", "relation": "is", "object": "referred"},
    {
        "subject": "Rome",
        "relation": "is referred due",
        "object": "its geographic location",
    },
    {
        "subject": "Rome",
        "relation": "is generally considered",
        "object": "to cradle of civilization",
    },
    {"subject": "Rome", "relation": "is", "object": "considered"},
    {"subject": "Rome", "relation": "is generally considered", "object": "to cradle"},
    {
        "subject": "Rome",
        "relation": "is generally considered",
        "object": "cradle of civilization",
    },
    {"subject": "Rome", "relation": "is generally considered", "object": "cradle"},
    {"subject": "Rome", "relation": "be cradle of", "object": "Western civilization"},
    {"subject": "Rome", "relation": "is considered", "object": "to cradle"},
    {"subject": "Rome", "relation": "be", "object": "cradle"},
    {"subject": "Rome", "relation": "be cradle of", "object": "civilization"},
    {"subject": "Rome", "relation": "is", "object": "generally considered"},
    {
        "subject": "Rome",
        "relation": "is generally considered",
        "object": "cradle of Western civilization",
    },
    {
        "subject": "Rome",
        "relation": "is considered",
        "object": "to cradle of civilization",
    },
    {
        "subject": "Rome",
        "relation": "is considered",
        "object": "to cradle of Western civilization",
    },
    {
        "subject": "Rome",
        "relation": "is considered",
        "object": "cradle of civilization",
    },
    {
        "subject": "Rome",
        "relation": "is generally considered",
        "object": "to cradle of Western civilization",
    },
    {
        "subject": "Rome",
        "relation": "is considered",
        "object": "cradle of Western civilization",
    },
    {"subject": "Rome", "relation": "is considered", "object": "cradle"},
]
Italy = [
    {"subject": "country", "relation": "is in", "object": "Southern"},
    {"subject": "Italy", "relation": "is country in", "object": "Southern"},
    {"subject": "Italy", "relation": "is", "object": "country"},
    {"subject": "it", "relation": "Located in", "object": "middle"},
    {"subject": "it", "relation": "consists of", "object": "peninsula"},
    {
        "subject": "it",
        "relation": "Located in",
        "object": "middle of Mediterranean Sea",
    },
    {"subject": "Italy shares land borders", "relation": "is with", "object": "France"},
    {"subject": "It", "relation": "has", "object": "territorial exclave"},
    {"subject": "archipelago", "relation": "is in", "object": "African Plate"},
    {"subject": "It", "relation": "has", "object": "exclave"},
    {"subject": "territorial exclave", "relation": "is in", "object": "Switzerland"},
    {"subject": "It", "relation": "has", "object": "exclave in Switzerland"},
    {
        "subject": "It",
        "relation": "has",
        "object": "territorial exclave in Switzerland",
    },
    {
        "subject": "it",
        "relation": "is country by",
        "object": "land area in European continent",
    },
    {"subject": "it", "relation": "is", "object": "tenth country"},
    {"subject": "it", "relation": "is tenth country by", "object": "land area"},
    {"subject": "Italy", "relation": "covers", "object": "area"},
    {"subject": "it", "relation": "is country by", "object": "land area in continent"},
    {
        "subject": "it",
        "relation": "is tenth country by",
        "object": "land area in European continent",
    },
    {
        "subject": "it",
        "relation": "is tenth country by",
        "object": "land area in continent",
    },
    {"subject": "Italy", "relation": "covers area with", "object": "population"},
    {"subject": "it", "relation": "is", "object": "country"},
    {"subject": "land area", "relation": "is in", "object": "European continent"},
    {
        "subject": "Italy",
        "relation": "covers area with",
        "object": "population of nearly 60 million",
    },
    {"subject": "Italy", "relation": "covers", "object": "area of 301,340 km2"},
    {"subject": "it", "relation": "is country by", "object": "land area"},
    {"subject": "Its capital", "relation": "is", "object": "Rome"},
    {"subject": "largest city", "relation": "is", "object": "Rome"},
    {"subject": "city", "relation": "is", "object": "Rome"},
]

calculate_percentage(question, Rome, Italy)
