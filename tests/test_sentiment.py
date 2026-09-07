from bajil_sentiment import SentimentAnalyzer


analyzer = SentimentAnalyzer()


def test_positive():
    result = analyzer.predict(
        "This product is excellent"
    )

    assert result["sentiment"] == "positive"


def test_negative():
    result = analyzer.predict(
        "This product is terrible"
    )

    assert result["sentiment"] == "negative"


def test_neutral():
    result = analyzer.predict(
        "The parcel arrived today"
    )

    assert result["sentiment"] == "neutral"


def test_negation():
    result = analyzer.predict(
        "This product is not good"
    )

    assert result["sentiment"] == "negative"


def test_not_bad():
    result = analyzer.predict(
        "This product is not bad"
    )

    assert result["sentiment"] == "positive"


def test_intensifier():
    normal = analyzer.predict("good")
    intense = analyzer.predict("very good")

    assert (
        intense["compound"]
        > normal["compound"]
    )


def test_diminisher():
    normal = analyzer.predict("good")
    diminished = analyzer.predict(
        "slightly good"
    )

    assert (
        normal["compound"]
        > diminished["compound"]
    )


def test_capital_letters():
    normal = analyzer.predict("great")
    capital = analyzer.predict("GREAT")

    assert (
        capital["compound"]
        > normal["compound"]
    )


def test_punctuation():
    normal = analyzer.predict("great.")
    emphasized = analyzer.predict("GREAT!!!")

    assert (
        emphasized["compound"]
        > normal["compound"]
    )


def test_contrast():
    result = analyzer.predict(
        "The camera is good, "
        "but the battery is terrible"
    )

    assert result["sentiment"] == "negative"


def test_emoji():
    result = analyzer.predict(
        "I love this phone 😍"
    )

    assert result["sentiment"] == "positive"


def test_emoticon():
    result = analyzer.predict(
        "This is good :)"
    )

    assert result["sentiment"] == "positive"


def test_compound_range():
    result = analyzer.predict(
        "This product is absolutely amazing!!!"
    )

    assert -1 <= result["compound"] <= 1


def test_proportions():
    result = analyzer.predict(
        "The camera is good but delivery is bad"
    )

    total = sum(result["proportions"].values())

    assert abs(total - 1.0) < 0.01


def test_contributions():
    result = analyzer.predict(
        "This product is very good"
    )

    assert "contributions" in result
    assert len(result["contributions"]) > 0


def test_custom_word():
    custom_analyzer = SentimentAnalyzer()

    custom_analyzer.add_word(
        "supercalifragilistic",
        3.5
    )

    result = custom_analyzer.predict(
        "This is supercalifragilistic"
    )

    assert result["sentiment"] == "positive"


def test_batch():
    results = analyzer.predict_batch([
        "This is excellent",
        "This is terrible",
    ])

    assert len(results) == 2

def test_highly_recommended():
    result = analyzer.predict("Highly recommended")
    assert result["sentiment"] == "positive"


def test_waste_of_money():
    result = analyzer.predict("This is a waste of money")
    assert result["sentiment"] == "negative"


def test_positive_context():
    result = analyzer.predict("The movie was sick")
    assert result["sentiment"] == "positive"


def test_negative_context():
    result = analyzer.predict("I feel sick")
    assert result["sentiment"] == "negative"


def test_multiple_positive_words():
    result = analyzer.predict(
        "This product is excellent, amazing and perfect"
    )
    assert result["sentiment"] == "positive"


def test_multiple_negative_words():
    result = analyzer.predict(
        "This product is terrible, useless and awful"
    )
    assert result["sentiment"] == "negative"


def test_negative_emoji():
    result = analyzer.predict("I hate this product 😡")
    assert result["sentiment"] == "negative"


def test_positive_emoji_only():
    result = analyzer.predict("😍")
    assert result["sentiment"] == "positive"


def test_negative_emoticon():
    result = analyzer.predict("This is bad :(")
    assert result["sentiment"] == "negative"


def test_empty_text():
    import pytest

    with pytest.raises(ValueError):
        analyzer.predict("")