from openie import StanfordOpenIE


def extract_openie_triples(text):
    properties = {
        "openie.affinity_probability_cap": 2 / 3,
    }

    with StanfordOpenIE(properties=properties) as client:
        # Annotate the text
        triples = client.annotate(text)

        return triples


extract_openie_triples("Is Rome the capital of the Netherlands?")
