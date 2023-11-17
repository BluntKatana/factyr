import nltk
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('maxent_ne_chunker')
nltk.download('words')
from nltk.tree import Tree

class FactEntityExtraction:
    def __init__(self):
        pass

    def extract_named_entities(self, sentence):
        processed_sentence = self.pre_process_sentence(sentence)

        named_entity_chunk = nltk.ne_chunk(processed_sentence, binary=True)
        list_of_named_entities = self.get_continuous_chunks(named_entity_chunk)
        
        #print(named_entity_chunk)
        #print(list_of_named_entities)

        return list_of_named_entities


    def pre_process_sentence(self, sentence):
        sentence = sentence.replace('\'', ' ')
        sentence = nltk.word_tokenize(sentence)
        sentence = nltk.pos_tag(sentence)

        print("Sentence with word types: ", sentence)

        return sentence

    @staticmethod
    def get_continuous_chunks(chunk):
        continuous_chunk = []
        current_chunk = []

        for i in chunk:
            # Named entity will be in form of a tree
            if type(i) == Tree:
                current_chunk.append(" ".join([token for token, pos in i.leaves()]))
            elif current_chunk:
                named_entity = " ".join(current_chunk)
                if named_entity not in continuous_chunk:
                    continuous_chunk.append(named_entity)
                    current_chunk = []
            else:
                continue

        if continuous_chunk:
            named_entity = " ".join(current_chunk)
            if named_entity not in continuous_chunk:
                continuous_chunk.append(named_entity)

        return continuous_chunk

    def process_fact(self, fact):
        self.extract_named_entities(fact)
