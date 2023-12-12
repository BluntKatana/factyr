import re

extracted_triples_text = [{'subject': 'Southern', 'relation': 'in country is', 'object': '14'}, {'subject': 'Southern', 'relation': 'in country is', 'object': '15'}, {'subject': 'country', 'relation': 'is in', 'object': 'Southern'}, {'subject': 'Europe', 'relation': 'is in', 'object': 'European Union'}, {'subject': 'Europe', 'relation': 'in Italy is', 'object': 'country in Southern'}, {'subject': 'Europe', 'relation': 'in Italy is', 'object': 'Italian'}, {'subject': 'Europe', 'relation': 'in Italy is', 'object': 'officially Italian Republic'}, {'subject': 'Italy', 'relation': 'country in', 'object': 'Southern'}, {'subject': 'Europe', 'relation': 'in Italy is', 'object': 'Legend'}, {'subject': 'Italy', 'relation': 'is in', 'object': 'Europe in European Union'}, {'subject': 'it', 'relation': 'Located in', 'object': 'middle'}, {'subject': 'it', 'relation': 'consists of', 'object': 'peninsula'}, {'subject': 'it', 'relation': 'Located in', 'object': 'middle of Mediterranean Sea'}, {'subject': 'Italy shares land borders', 'relation': 'is with', 'object': 'France'}, {'subject': 'It', 'relation': 'has', 'object': 'territorial exclave'}, {'subject': 'archipelago', 'relation': 'is in', 'object': 'African Plate'}, {'subject': 'It', 'relation': 'has', 'object': 'exclave'}, {'subject': 'territorial exclave', 'relation': 'is in', 'object': 'Switzerland'}, {'subject': 'It', 'relation': 'has', 'object': 'exclave in Switzerland'}, {'subject': 'It', 'relation': 'has', 'object': 'territorial exclave in Switzerland'}, {'subject': 'it', 'relation': 'is country by', 'object': 'land area in European continent'}, {'subject': 'it', 'relation': 'is', 'object': 'tenth country'}, {'subject': 'it', 'relation': 'is tenth country by', 'object': 'land area'}, {'subject': 'Italy', 'relation': 'covers', 'object': 'area'}, {'subject': 'it', 'relation': 'is country by', 'object': 'land area in continent'}, {'subject': 'it', 'relation': 'is tenth country by', 'object': 'land area in European continent'}, {'subject': 'it', 'relation': 'is tenth country by', 'object': 'land area in continent'}, {'subject': 'Italy', 'relation': 'covers area with', 'object': 'population'}, {'subject': 'it', 'relation': 'is', 'object': 'country'}, {'subject': 'land area', 'relation': 'is in', 'object': 'European continent'}, {'subject': 'Italy', 'relation': 'covers area with', 'object': 'population of nearly 60 million'}, {'subject': 'Italy', 'relation': 'covers', 'object': 'area of 301,340 km2'}, {'subject': 'it', 'relation': 'is country by', 'object': 'land area'}, {'subject': 'Its capital', 'relation': 'is', 'object': 'Rome'}, {'subject': 'largest city', 'relation': 'is', 'object': 'Rome'}, {'subject': 'city', 'relation': 'is', 'object': 'Rome'}]

relation_keywords = ["capital"]

exists = any(any(keyword.lower() in item[field].lower() for keyword in relation_keywords) for item in extracted_triples_text for field in ['subject', 'relation', 'object'])


print(exists)

matching_dict = next(
    (item for item in extracted_triples_text if any(keyword.lower() in item[field].lower() for keyword in relation_keywords for field in ['subject', 'relation', 'object'])),
    None
)

print(matching_dict)

