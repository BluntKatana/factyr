extracted_triples_text = [["Its capital", "is", "Rome"], ["is", "located", "North"]]
relation = ["capital"]

result = next(
    (
        item[2]  # Extract the object (third element) from the triple
        for item in extracted_triples_text
        if any(word.lower() in " ".join(item).lower() for word in relation)
    ),
    None,
)

print(result)
