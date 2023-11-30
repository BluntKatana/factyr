from openie import StanfordOpenIE


def extract_openie_triples(text):
    properties = {
        "openie.affinity_probability_cap": 2 / 3,
    }

    with StanfordOpenIE(properties=properties) as client:
        # Annotate the text
        triples = client.annotate(text)

        return triples


# Example usage
query = "What is the capital of Italy"
text = """Rome ( Italian : Roma ) is the capital of Italy and the administrative center of the Lazio region and the Città Metropolitana di Roma Capitale (formerly the Province of Rome ). The city has approximately 2.9 million inhabitants, the population of the metropolitan region is 4.4 million. It is the largest city in Italy. The Tiber and Aniene flow through the city, located in the midwest of the Apennine Peninsula . Worth seeing are the Colosseum , the Roman Forum , the Pantheon , St. Peter's Basilica , the Trevi Fountain and the Monument to Victor Emanuel II ."""

extracted_triples = extract_openie_triples(text)

print("Extracted Triple:", extracted_triples)
