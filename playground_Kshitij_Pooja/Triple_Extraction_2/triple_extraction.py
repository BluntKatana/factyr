from openie import StanfordOpenIE


class TripleExtraction:
    def extract_openie_triples(text):
        properties = {
            "openie.affinity_probability_cap": 2 / 3,
        }

        with StanfordOpenIE(properties=properties) as client:
            # Annotate the text
            triples = client.annotate(text)

            return triples
