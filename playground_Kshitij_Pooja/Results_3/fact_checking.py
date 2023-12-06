import spacy

class FactChecking:
    def check_query_in_context(query, context):
        # Load the spaCy model
        nlp = spacy.load("en_core_web_sm")

        # Process the query and context
        doc_query = nlp(query)
        doc_context = nlp(context)

        # Extract named entities and relationships from the query
        query_entities = {ent.text.lower() for ent in doc_query.ents}
        print("query_entities",query_entities)
        query_relationships = {token.text.lower() for token in doc_query if token.dep_ == "attr"}
        print("queryrelations",query_relationships)

        # Check if the query entities and relationships are mentioned in the context
        is_query_in_context = (
            all(entity.text.lower() in context.lower() for entity in doc_query.ents)
            and all(relationship.lower() in context.lower() for relationship in query_relationships)
        )

        return is_query_in_context
