"""Sentiment scores for emojis and emoticons."""


SYMBOL_SCORES = {
    # Strong positive
    "😍": 3.5,
    "🥰": 3.5,
    "❤️": 3.5,
    "❤": 3.5,
    "🤩": 3.0,

    # Positive
    "😀": 2.5,
    "😃": 2.5,
    "😊": 2.5,
    "😁": 2.0,
    "👍": 2.0,
    "🔥": 2.0,
    "🎉": 2.0,

    # Positive emoticons
    ":-)": 2.0,
    ":)": 2.0,
    ":D": 2.5,

    # Negative
    "😞": -2.0,
    "😢": -2.5,
    "😭": -3.5,
    "😡": -3.5,
    "🤬": -4.0,
    "👎": -2.5,
    "💔": -3.5,
    "😠": -3.0,

    # Negative emoticons
    ":-(": -2.0,
    ":(": -2.0,
    ":/": -1.0,
}