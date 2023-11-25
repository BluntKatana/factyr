from openie import StanfordOpenIE

# https://stanfordnlp.github.io/CoreNLP/openie.html#api
# Default value of openie.affinity_probability_cap was 1/3.
properties = {
    'openie.affinity_probability_cap': 2 / 3,
}

with StanfordOpenIE(properties=properties) as client:
    text = '''Nicaragua, officially the Republic of Nicaragua (Spanish: República de Nicaragua), is a country in Central America bordered by Honduras to the north, Costa Rica to the south, the Pacific Ocean to the west and the Caribbean to the east. Sea. The capital and largest city of the country is Managua.'''
    print('Text: %s.' % text)
    for triple in client.annotate(text):
        print('|-', triple)

    # graph_image = 'graph.png'
    # client.generate_graphviz_graph(text, graph_image)
    # print('Graph generated: %s.' % graph_image)

    with open('playground_KK/new_triplets_extraction/corpus/pg6130.txt', encoding='utf8') as r:
        corpus = r.read().replace('\n', ' ').replace('\r', '')

    triples_corpus = client.annotate(corpus[0:5000])
    print('Corpus: %s [...].' % corpus[0:80])
    print('Found %s triples in the corpus.' % len(triples_corpus))
    for triple in triples_corpus[:3]:
        print('|-', triple)
    print('[...]')
