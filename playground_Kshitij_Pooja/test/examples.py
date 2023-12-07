# # Example sentences
# sentence_1 = "What is the capital of Netherlands?"
# sentence_2 = "Who is the president of USA?"
# sentence_3 = "Netherlands is country located in Europe with territories"
# # Extract keywords and entities from the sentences
# keywords_2, entities_2 = extract_keywords(sentence_2)
# keywords_3, entities_3 = extract_keywords(sentence_3)

# wiki_of_netherlands = [
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in Europe with territories",
#     },
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located with territories",
#     },
#     {
#         "subject": "country",
#         "relation": "located with",
#         "object": "overseas territories",
#     },
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in northwestern Europe",
#     },
#     {"subject": "country", "relation": "located in", "object": "northwestern Europe"},
#     {"subject": "overseas territories", "relation": "is in", "object": "Caribbean"},
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in northwestern Europe with overseas territories",
#     },
#     {"subject": "Netherlands", "relation": "is", "object": "country located in Europe"},
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in Europe with overseas territories",
#     },
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located with territories in Caribbean",
#     },
#     {"subject": "country", "relation": "located in", "object": "Europe"},
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in northwestern Europe with territories",
#     },
#     {"subject": "Netherlands", "relation": "is", "object": "country"},
#     {
#         "subject": "country",
#         "relation": "located with",
#         "object": "territories Caribbean",
#     },
#     {"subject": "country", "relation": "located with", "object": "territories"},
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located with overseas territories",
#     },
#     {"subject": "Netherlands", "relation": "is", "object": "country located"},
#     {"subject": "It", "relation": "is", "object": "largest"},
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four constituent countries",
#     },
#     {"subject": "It", "relation": "is largest of", "object": "four countries"},
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four countries of Kingdom of Netherlands",
#     },
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four constituent countries of Kingdom",
#     },
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four countries of Kingdom",
#     },
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four constituent countries of Kingdom of Netherlands",
#     },
#     {"subject": "it", "relation": "Belgium to", "object": "south"},
#     {
#         "subject": "it",
#         "relation": "Belgium with",
#         "object": "North Sea coastline to north",
#     },
#     {"subject": "it", "relation": "borders Germany to", "object": "east"},
#     {
#         "subject": "Belgium",
#         "relation": "is with",
#         "object": "North Sea coastline to north",
#     },
#     {"subject": "it", "relation": "Belgium with", "object": "North Sea coastline"},
#     {"subject": "it", "relation": "borders", "object": "Germany"},
#     {"subject": "it", "relation": "borders to", "object": "east"},
#     {"subject": "Netherlands", "relation": "consists of", "object": "twelve provinces"},
#     {"subject": "It", "relation": "also has", "object": "border with France"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border on split island of Saint Martin in Caribbean",
#     },
#     {"subject": "It", "relation": "has", "object": "border on split island"},
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border on split island of Saint Martin in Caribbean",
#     },
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border on split island of Saint Martin",
#     },
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border with France on split island of Saint Martin",
#     },
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border with France on split island of Saint Martin in Caribbean",
#     },
#     {"subject": "It", "relation": "has", "object": "border with France"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border with France on split island of Saint Martin in Caribbean",
#     },
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border with France on split island of Saint Martin",
#     },
#     {"subject": "border", "relation": "is with", "object": "France"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border with France on split island",
#     },
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border with France on split island in Caribbean",
#     },
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border with France on split island",
#     },
#     {"subject": "It", "relation": "also has", "object": "border"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border with France on split island in Caribbean",
#     },
#     {"subject": "It", "relation": "also has", "object": "border on split island"},
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border on split island of Saint Martin",
#     },
#     {"subject": "split island", "relation": "is in", "object": "Caribbean"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border on split island in Caribbean",
#     },
#     {"subject": "It", "relation": "has", "object": "border"},
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border on split island in Caribbean",
#     },
#     {"subject": "It", "relation": "shares borders with", "object": "United Kingdom"},
#     {"subject": "It", "relation": "shares with", "object": "United Kingdom"},
#     {"subject": "It", "relation": "shares", "object": "maritime borders"},
#     {"subject": "It", "relation": "shares", "object": "borders"},
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language in province",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language in province",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language in province",
#     },
#     {"subject": "official language", "relation": "is", "object": "Dutch"},
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language in province",
#     },
#     {"subject": "language", "relation": "is", "object": "Dutch"},
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language in province of Friesland",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language in province",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language in province of Friesland",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language in province of Friesland",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language in province of Friesland",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language in province of Friesland",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language in province of Friesland",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language in province of Friesland",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language",
#     },
#     {
#         "subject": "secondary official language",
#         "relation": "is in",
#         "object": "province of Friesland",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language in province",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language in province",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language in province",
#     },
#     {"subject": "language", "relation": "is Dutch with", "object": "West Frisian"},
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language in province of Friesland",
#     },
#     {
#         "subject": "Dutch",
#         "relation": "are official in",
#         "object": "Caribbean territories",
#     },
#     {
#         "subject": "English",
#         "relation": "are",
#         "object": "official in Caribbean territories",
#     },
#     {"subject": "Papiamento", "relation": "are official in", "object": "territories"},
#     {"subject": "English", "relation": "are", "object": "official"},
#     {
#         "subject": "English",
#         "relation": "are official in",
#         "object": "Caribbean territories",
#     },
#     {"subject": "Dutch", "relation": "are", "object": "official in territories"},
#     {
#         "subject": "Papiamento",
#         "relation": "are official in",
#         "object": "Caribbean territories",
#     },
#     {
#         "subject": "Dutch",
#         "relation": "are",
#         "object": "official in Caribbean territories",
#     },
#     {"subject": "English", "relation": "are official in", "object": "territories"},
#     {"subject": "Dutch", "relation": "are", "object": "official"},
#     {"subject": "Dutch", "relation": "are official in", "object": "territories"},
#     {"subject": "Papiamento", "relation": "are", "object": "official"},
#     {"subject": "English", "relation": "are", "object": "official in territories"},
#     {"subject": "capital", "relation": "is", "object": "Amsterdam"},
# ]


# # Triple Extraction
# question = "What is the capital of Italy"
# query = "Is Rome the capital of Italy"
# text1 = """Rome ( Italian : Roma ) is the capital of Italy and the administrative center of the Lazio region and the Città Metropolitana di Roma Capitale (formerly the Province of Rome ). The city has approximately 2.9 million inhabitants, the population of the metropolitan region is 4.4 million. It is the largest city in Italy. The Tiber and Aniene flow through the city, located in the midwest of the Apennine Peninsula . Worth seeing are the Colosseum , the Roman Forum , the Pantheon , St. Peter's Basilica , the Trevi Fountain and the Monument to Victor Emanuel II ."""

# #Keyword Extraction
# wiki_of_rome = [
#     {"subject": "Rome", "relation": "center of", "object": "Lazio region"},
#     {"subject": "Rome", "relation": "is", "object": "capital"},
#     {
#         "subject": "Rome",
#         "relation": "administrative center of",
#         "object": "Lazio region",
#     },
#     {"subject": "Rome", "relation": "is capital of", "object": "Italy"},
#     {
#         "subject": "city",
#         "relation": "has",
#         "object": "approximately 2.9 million inhabitants",
#     },
#     {"subject": "It", "relation": "is", "object": "largest city"},
#     {"subject": "largest city", "relation": "is in", "object": "Italy"},
#     {"subject": "It", "relation": "is largest city in", "object": "Italy"},
#     {"subject": "It", "relation": "is", "object": "city"},
#     {"subject": "It", "relation": "is city in", "object": "Italy"},
#     {"subject": "Aniene", "relation": "flow through", "object": "city"},
#     {"subject": "Tiber", "relation": "flow through", "object": "city"},
#     {"subject": "Worth seeing", "relation": "are", "object": "Colosseum"},
#     {"subject": "seeing", "relation": "are", "object": "Colosseum"},
#     {"subject": "seeing", "relation": "Monument to", "object": "Victor Emanuel II"},
#     {"subject": "St. Peter", "relation": "has", "object": "Basilica"},
#     {
#         "subject": "Worth seeing",
#         "relation": "Monument to",
#         "object": "Victor Emanuel II",
#     },
# ]

# wiki_of_italy = [
#     {"subject": "country", "relation": "is in", "object": "Southern"},
#     {"subject": "Italy", "relation": "is country in", "object": "Southern"},
#     {"subject": "Italy", "relation": "is", "object": "country"},
#     {"subject": "it", "relation": "Located in", "object": "middle"},
#     {"subject": "it", "relation": "consists of", "object": "peninsula"},
#     {
#         "subject": "it",
#         "relation": "Located in",
#         "object": "middle of Mediterranean Sea",
#     },
#     {"subject": "Italy shares land borders", "relation": "is with", "object": "France"},
#     {"subject": "It", "relation": "has", "object": "territorial exclave"},
#     {"subject": "archipelago", "relation": "is in", "object": "African Plate"},
#     {"subject": "It", "relation": "has", "object": "exclave"},
#     {"subject": "territorial exclave", "relation": "is in", "object": "Switzerland"},
#     {"subject": "It", "relation": "has", "object": "exclave in Switzerland"},
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "territorial exclave in Switzerland",
#     },
#     {
#         "subject": "it",
#         "relation": "is country by",
#         "object": "land area in European continent",
#     },
#     {"subject": "it", "relation": "is", "object": "tenth country"},
#     {"subject": "it", "relation": "is tenth country by", "object": "land area"},
#     {"subject": "Italy", "relation": "covers", "object": "area"},
#     {"subject": "it", "relation": "is country by", "object": "land area in continent"},
#     {
#         "subject": "it",
#         "relation": "is tenth country by",
#         "object": "land area in European continent",
#     },
#     {
#         "subject": "it",
#         "relation": "is tenth country by",
#         "object": "land area in continent",
#     },
#     {"subject": "Italy", "relation": "covers area with", "object": "population"},
#     {"subject": "it", "relation": "is", "object": "country"},
#     {"subject": "land area", "relation": "is in", "object": "European continent"},
#     {
#         "subject": "Italy",
#         "relation": "covers area with",
#         "object": "population of nearly 60 million",
#     },
#     {"subject": "Italy", "relation": "covers", "object": "area of 301,340 km2"},
#     {"subject": "it", "relation": "is country by", "object": "land area"},
#     {"subject": "Its capital", "relation": "is", "object": "Rome"},
#     {"subject": "largest city", "relation": "is", "object": "Rome"},
#     {"subject": "city", "relation": "is", "object": "Rome"},
# ]

# wiki_of_amsterdam = [
#     {"subject": "Amsterdam", "relation": "is capital of", "object": "Netherlands"},
#     {"subject": "Amsterdam", "relation": "is", "object": "capital"},
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of Amsterdam of same name in province",
#     },
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of same name in province",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of Amsterdam of name in province",
#     },
#     {
#         "subject": "same name",
#         "relation": "is in",
#         "object": "province of North Holland",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of Amsterdam of same name in province of North Holland",
#     },
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of same name",
#     },
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of name in province of North Holland",
#     },
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of Amsterdam of name in province of North Holland",
#     },
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of Amsterdam of same name in province of North Holland",
#     },
#     {"subject": "city", "relation": "is located in", "object": "municipality of name"},
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of same name",
#     },
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of Amsterdam of name in province",
#     },
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of Amsterdam of name",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of Amsterdam of same name",
#     },
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of Amsterdam",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of name",
#     },
#     {"subject": "city", "relation": "is located in", "object": "municipality"},
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of name in province",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of name in province",
#     },
#     {"subject": "city", "relation": "is", "object": "located"},
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of same name in province of North Holland",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of Amsterdam of same name in province",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of Amsterdam",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of same name in province",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of Amsterdam of name",
#     },
#     {
#         "subject": "city",
#         "relation": "is located in",
#         "object": "municipality of Amsterdam of same name",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of same name in province of North Holland",
#     },
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of name in province of North Holland",
#     },
#     {"subject": "city", "relation": "is located on", "object": "IJ"},
#     {
#         "subject": "city",
#         "relation": "is",
#         "object": "located on IJ in municipality of Amsterdam of name in province of North Holland",
#     },
#     {"subject": "city", "relation": "is", "object": "located on IJ in municipality"},
#     {
#         "subject": "Amsterdam",
#         "relation": "is largest city In",
#         "object": "terms of population",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms largest city in Netherlands with 873,338 inhabitants",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms city in Netherlands with 873,338 inhabitants",
#     },
#     {"subject": "Amsterdam", "relation": "is largest city In", "object": "terms"},
#     {"subject": "Amsterdam", "relation": "is", "object": "largest city"},
#     {"subject": "Amsterdam", "relation": "is city In", "object": "terms of population"},
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms of population city in Netherlands",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is largest city with",
#         "object": "873,338 inhabitants",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "largest city in Netherlands with 873,338 inhabitants",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms city with 873,338 inhabitants",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "city in Netherlands with 873,338 inhabitants",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms city in Netherlands",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms of population city with 873,338 inhabitants",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms of population largest city in Netherlands with 873,338 inhabitants",
#     },
#     {"subject": "Amsterdam", "relation": "is largest city in", "object": "Netherlands"},
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms largest city with 873,338 inhabitants",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms of population city in Netherlands with 873,338 inhabitants",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is city with",
#         "object": "873,338 inhabitants",
#     },
#     {"subject": "largest city", "relation": "is in", "object": "Netherlands"},
#     {"subject": "largest city", "relation": "is with", "object": "873,338 inhabitants"},
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms largest city in Netherlands",
#     },
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms of population largest city in Netherlands",
#     },
#     {"subject": "Amsterdam", "relation": "is city in", "object": "Netherlands"},
#     {"subject": "largest city", "relation": "is In", "object": "terms of population"},
#     {"subject": "Amsterdam", "relation": "is city with", "object": "January 1 2021"},
#     {
#         "subject": "Amsterdam",
#         "relation": "is",
#         "object": "In terms of population largest city with 873,338 inhabitants",
#     },
#     {"subject": "Amsterdam", "relation": "is", "object": "city"},
#     {"subject": "Amsterdam", "relation": "is city In", "object": "terms"},
#     {
#         "subject": "Amsterdam",
#         "relation": "is largest city with",
#         "object": "January 1 2021",
#     },
#     {
#         "subject": "Greater Amsterdam metropolitan region",
#         "relation": "has",
#         "object": "1,459,402 inhabitants",
#     },
#     {
#         "subject": "Greater Amsterdam region",
#         "relation": "has",
#         "object": "1,459,402 inhabitants",
#     },
# ]

# wiki_of_netherlands = [
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in Europe with territories",
#     },
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located with territories",
#     },
#     {
#         "subject": "country",
#         "relation": "located with",
#         "object": "overseas territories",
#     },
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in northwestern Europe",
#     },
#     {"subject": "country", "relation": "located in", "object": "northwestern Europe"},
#     {"subject": "overseas territories", "relation": "is in", "object": "Caribbean"},
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in northwestern Europe with overseas territories",
#     },
#     {"subject": "Netherlands", "relation": "is", "object": "country located in Europe"},
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in Europe with overseas territories",
#     },
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located with territories in Caribbean",
#     },
#     {"subject": "country", "relation": "located in", "object": "Europe"},
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located in northwestern Europe with territories",
#     },
#     {"subject": "Netherlands", "relation": "is", "object": "country"},
#     {
#         "subject": "country",
#         "relation": "located with",
#         "object": "territories Caribbean",
#     },
#     {"subject": "country", "relation": "located with", "object": "territories"},
#     {
#         "subject": "Netherlands",
#         "relation": "is",
#         "object": "country located with overseas territories",
#     },
#     {"subject": "Netherlands", "relation": "is", "object": "country located"},
#     {"subject": "It", "relation": "is", "object": "largest"},
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four constituent countries",
#     },
#     {"subject": "It", "relation": "is largest of", "object": "four countries"},
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four countries of Kingdom of Netherlands",
#     },
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four constituent countries of Kingdom",
#     },
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four countries of Kingdom",
#     },
#     {
#         "subject": "It",
#         "relation": "is largest of",
#         "object": "four constituent countries of Kingdom of Netherlands",
#     },
#     {"subject": "it", "relation": "Belgium to", "object": "south"},
#     {
#         "subject": "it",
#         "relation": "Belgium with",
#         "object": "North Sea coastline to north",
#     },
#     {"subject": "it", "relation": "borders Germany to", "object": "east"},
#     {
#         "subject": "Belgium",
#         "relation": "is with",
#         "object": "North Sea coastline to north",
#     },
#     {"subject": "it", "relation": "Belgium with", "object": "North Sea coastline"},
#     {"subject": "it", "relation": "borders", "object": "Germany"},
#     {"subject": "it", "relation": "borders to", "object": "east"},
#     {"subject": "Netherlands", "relation": "consists of", "object": "twelve provinces"},
#     {"subject": "It", "relation": "also has", "object": "border with France"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border on split island of Saint Martin in Caribbean",
#     },
#     {"subject": "It", "relation": "has", "object": "border on split island"},
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border on split island of Saint Martin in Caribbean",
#     },
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border on split island of Saint Martin",
#     },
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border with France on split island of Saint Martin",
#     },
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border with France on split island of Saint Martin in Caribbean",
#     },
#     {"subject": "It", "relation": "has", "object": "border with France"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border with France on split island of Saint Martin in Caribbean",
#     },
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border with France on split island of Saint Martin",
#     },
#     {"subject": "border", "relation": "is with", "object": "France"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border with France on split island",
#     },
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border with France on split island in Caribbean",
#     },
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border with France on split island",
#     },
#     {"subject": "It", "relation": "also has", "object": "border"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border with France on split island in Caribbean",
#     },
#     {"subject": "It", "relation": "also has", "object": "border on split island"},
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border on split island of Saint Martin",
#     },
#     {"subject": "split island", "relation": "is in", "object": "Caribbean"},
#     {
#         "subject": "It",
#         "relation": "also has",
#         "object": "border on split island in Caribbean",
#     },
#     {"subject": "It", "relation": "has", "object": "border"},
#     {
#         "subject": "It",
#         "relation": "has",
#         "object": "border on split island in Caribbean",
#     },
#     {"subject": "It", "relation": "shares borders with", "object": "United Kingdom"},
#     {"subject": "It", "relation": "shares with", "object": "United Kingdom"},
#     {"subject": "It", "relation": "shares", "object": "maritime borders"},
#     {"subject": "It", "relation": "shares", "object": "borders"},
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language in province",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language in province",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language in province",
#     },
#     {"subject": "official language", "relation": "is", "object": "Dutch"},
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language in province",
#     },
#     {"subject": "language", "relation": "is", "object": "Dutch"},
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language in province of Friesland",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language in province",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language in province of Friesland",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language in province of Friesland",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language in province of Friesland",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language in province of Friesland",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language in province of Friesland",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language in province of Friesland",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language",
#     },
#     {
#         "subject": "secondary official language",
#         "relation": "is in",
#         "object": "province of Friesland",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary language in province",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as official language in province",
#     },
#     {
#         "subject": "language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language in province",
#     },
#     {"subject": "language", "relation": "is Dutch with", "object": "West Frisian"},
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as secondary official language",
#     },
#     {
#         "subject": "official language",
#         "relation": "is Dutch with",
#         "object": "West Frisian as language in province of Friesland",
#     },
#     {
#         "subject": "Dutch",
#         "relation": "are official in",
#         "object": "Caribbean territories",
#     },
#     {
#         "subject": "English",
#         "relation": "are",
#         "object": "official in Caribbean territories",
#     },
#     {"subject": "Papiamento", "relation": "are official in", "object": "territories"},
#     {"subject": "English", "relation": "are", "object": "official"},
#     {
#         "subject": "English",
#         "relation": "are official in",
#         "object": "Caribbean territories",
#     },
#     {"subject": "Dutch", "relation": "are", "object": "official in territories"},
#     {
#         "subject": "Papiamento",
#         "relation": "are official in",
#         "object": "Caribbean territories",
#     },
#     {
#         "subject": "Dutch",
#         "relation": "are",
#         "object": "official in Caribbean territories",
#     },
#     {"subject": "English", "relation": "are official in", "object": "territories"},
#     {"subject": "Dutch", "relation": "are", "object": "official"},
#     {"subject": "Dutch", "relation": "are official in", "object": "territories"},
#     {"subject": "Papiamento", "relation": "are", "object": "official"},
#     {"subject": "English", "relation": "are", "object": "official in territories"},
# ]


# is_rome_capital_of_italy = [
#     {"subject": "Rome", "relation": "is", "object": "capital"},
#     {"subject": "Rome", "relation": "is capital of", "object": "Italy"},
# ]

# is_ams_capital_of_nether = [
#     {"subject": "Amsterdam", "relation": "is capital of", "object": "Netherlands"},
#     {"subject": "Amsterdam", "relation": "is", "object": "capital"},
# ]

# is_rome_capital_of_nether = [
#     {"subject": "Rome", "relation": "is capital of", "object": "Netherlands"},
#     {"subject": "Rome", "relation": "is", "object": "capital"},
# ]
