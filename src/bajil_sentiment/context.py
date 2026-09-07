"""Context rules for words with multiple meanings."""


CONTEXT_RULES = {
    "sick": {
        "positive_context": {
            "movie",
            "song",
            "beat",
            "performance",
            "game",
            "design",
        },

        "negative_context": {
            "feel",
            "feeling",
            "became",
            "am",
            "ill",
            "hospital",
        },

        "positive_score": 2.5,
        "negative_score": -2.5,
    },

    "killer": {
        "positive_context": {
            "design",
            "feature",
            "performance",
            "look",
        },

        "negative_context": {
            "murder",
            "crime",
            "attack",
            "police",
        },

        "positive_score": 2.5,
        "negative_score": -3.5,
    },
}


def find_context_score(word, nearby_words):
    rule = CONTEXT_RULES.get(word)

    if rule is None:
        return None

    nearby_set = set(nearby_words)

    if nearby_set & rule["positive_context"]:
        return rule["positive_score"]

    if nearby_set & rule["negative_context"]:
        return rule["negative_score"]

    return None