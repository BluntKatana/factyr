class calculatePercentage:
    def calculate_percentage(question, rel1, rel2):
        combined_relations = rel1 + rel2
        matching_relations = []

        for q in question:
            for rel in combined_relations:
                if (
                    q["subject"] == rel["subject"]
                    or q["subject"] == rel["object"]
                    or q["object"] == rel["subject"]
                    or q["object"] == rel["object"]
                ):
                    matching_relations.append(rel)

            x = len(matching_relations)
            y = len(combined_relations)
        return (x / y) * 100
