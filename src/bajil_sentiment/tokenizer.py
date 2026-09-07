"""Functions for separating text into words."""

import re


def tokenize(text):
    original_words = re.findall(
        r"[A-Za-z]+(?:'[A-Za-z]+)?",
        text
    )

    lowercase_words = [
        word.lower()
        for word in original_words
    ]

    return original_words, lowercase_words