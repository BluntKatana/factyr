import wikipedia

class WikipediaHelper:

    def __init__(self):
        self.cache_dict = {}
        pass

    def get_entity_wikipage_cached(self, entity):
        page = None
        if entity in self.cache_dict:
            page = self.cache_dict[entity]
            print("Cached entity: ", entity)
        else:
            try:
                page = wikipedia.page(entity)
                print("Non-Cached entity: ", entity)

            except wikipedia.exceptions.DisambiguationError:
                print("disambiguation error occured : " + entity)
                page = None
            except:
                print("exception occured wiki : " + entity)
                page = None

            self.cache_dict[entity] = page

        return page

