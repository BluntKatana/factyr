from openie import StanfordOpenIE

# https://stanfordnlp.github.io/CoreNLP/openie.html#api
# Default value of openie.affinity_probability_cap was 1/3.
properties = {
    'openie.affinity_probability_cap': 2 / 3,
}

with StanfordOpenIE(properties=properties) as client:
    text = '''Italy, officially the Italian Republic, is a country in Southern[13][14][15] and Western[16][a] Europe. Located in the middle of the Mediterranean Sea, it consists of a peninsula delimited by the Alps and surrounded by several islands.[17] Italy shares land borders with France, Switzerland, Austria, Slovenia and the enclaved microstates of Vatican City and San Marino. It has a territorial exclave in Switzerland (Campione) and an archipelago in the African Plate (Pelagie Islands). Italy covers an area of 301,340 km2 (116,350 sq mi),[3] with a population of nearly 60 million;[18] it is the tenth-largest country by land area in the European continent and the third-most populous member state of the European Union. Its capital and largest city is Rome. '''

    query = "Rome is the capital of Italy"
    target_word = "capital"
    print('Text: %s.' % text)

    triple = client.annotate(query)
    print("Amsterdam triple", triple)
    relation_query = triple[0]['relation']
    subject_query = triple[0]['subject']
    object_query = triple[0]['object']

    print("Triple[relation]", triple[0]['relation'])

    flag = False
    for triple in client.annotate(text):
        print('|-', triple)

        # if(((triple['subject']) in relation_query) and triple['object'] == subject_query):

        print(relation_query.lower())
        print("1",target_word in relation_query.lower())
        print("2",target_word in triple['subject'].lower())
        print("3", triple['object'] == subject_query)

        if((target_word in relation_query.lower()) and (target_word in triple['subject'].lower()) and triple['object'] == subject_query):
            print("Yes")
            flag = True
            break
        
    if(flag):
        print("The query is correct")
    # graph_image = 'graph.png'
    # client.generate_graphviz_graph(text, graph_image)
    # print('Graph generated: %s.' % graph_image)

    # with open('playground_Kshitij_Pooja/new_triplets_extraction/corpus/pg6130.txt', encoding='utf8') as r:
    #     corpus = r.read().replace('\n', ' ').replace('\r', '')

    # triples_corpus = client.annotate(corpus[0:5000])
    # print('Corpus: %s [...].' % corpus[0:80])
    # print('Found %s triples in the corpus.' % len(triples_corpus))
    # for triple in triples_corpus[:3]:
    #     print('|-', triple)
    # print('[...]')
