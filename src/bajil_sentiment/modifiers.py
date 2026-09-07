"""Words that modify sentiment direction or strength."""


NEGATIONS = {
    "not",
    "no",
    "never",
    "neither",
    "hardly",
    "cannot",
    "can't",
    "cant",
    "isn't",
    "isnt",
    "wasn't",
    "wasnt",
    "don't",
    "dont",
    "didn't",
    "didnt",
    "won't",
    "wont",
    "wouldn't",
    "wouldnt",
    "shouldn't",
    "shouldnt",
    "couldn't",
    "couldnt",
}


INTENSIFIERS = {
    "very": 1.50,
    "really": 1.40,
    "extremely": 2.00,
    "absolutely": 1.80,
    "incredibly": 1.70,
    "so": 1.30,
    "too": 1.30,
    "highly": 1.50,
    "totally": 1.50,
    "completely": 1.60,
    "super": 1.50,
}


DIMINISHERS = {
    "slightly": 0.50,
    "somewhat": 0.70,
    "little": 0.70,
    "barely": 0.50,
    "fairly": 0.80,
    "partly": 0.70,
    "almost": 0.80,
    "rather": 0.80,
}