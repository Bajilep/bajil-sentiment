"""Main sentiment-analysis class."""

import math
from collections.abc import Iterable
from .context import find_context_score
from .lexicon import build_lexicon
from .modifiers import (
    NEGATIONS,
    INTENSIFIERS,
    DIMINISHERS,
)
from .symbols import SYMBOL_SCORES
from .tokenizer import tokenize


class SentimentAnalyzer:
    """Classify text and explain the result."""

    def __init__(self):
        self.lexicon = build_lexicon()
        self.negations = NEGATIONS
        self.intensifiers = INTENSIFIERS
        self.diminishers = DIMINISHERS
        self.symbol_scores = SYMBOL_SCORES

    def predict(self, text):
        """Analyse one sentence."""

        self._validate_text(text)

        original_words, words = tokenize(text)

        if "but" in words:
            contrast_index = words.index("but")
        else:
            contrast_index = None

        contributions = []
        raw_score = 0.0

        positive_items = 0
        negative_items = 0

        for index, word in enumerate(words):

            nearby_words = (
                    words[max(0, index - 3):index]
                    + words[index + 1:index + 4]
            )

            context_score = find_context_score(
                word,
                nearby_words
            )

            applied_modifiers = []

            if context_score is not None:
                base_score = context_score
                applied_modifiers.append("context")

            elif word in self.lexicon:
                base_score = self.lexicon[word]

            else:
                continue

            final_score = base_score

            previous_words = words[
                max(0, index - 3):index
            ]

            # Words before "but" must not control words after it
            if "but" in previous_words:
                but_position = previous_words.index("but")

                previous_words = previous_words[
                    but_position + 1:
                ]

            # Negation
            if any(
                previous in self.negations
                for previous in previous_words
            ):
                final_score *= -1
                applied_modifiers.append("negation")

            # Intensity
            if index > 0:
                previous_word = words[index - 1]

                if previous_word in self.intensifiers:
                    multiplier = self.intensifiers[
                        previous_word
                    ]

                    final_score *= multiplier

                    applied_modifiers.append(
                        f"intensifier ×{multiplier}"
                    )

                elif previous_word in self.diminishers:
                    multiplier = self.diminishers[
                        previous_word
                    ]

                    final_score *= multiplier

                    applied_modifiers.append(
                        f"diminisher ×{multiplier}"
                    )

            # Capital-letter emphasis
            original_word = original_words[index]

            if (
                original_word.isupper()
                and len(original_word) > 1
            ):
                final_score *= 1.25
                applied_modifiers.append("CAPS ×1.25")

            # Contrast using "but"
            if contrast_index is not None:

                if index < contrast_index:
                    contrast_multiplier = 0.50
                else:
                    contrast_multiplier = 1.50

                final_score *= contrast_multiplier

                applied_modifiers.append(
                    f"contrast ×{contrast_multiplier}"
                )

            raw_score += final_score

            if final_score > 0:
                positive_items += 1

            elif final_score < 0:
                negative_items += 1

            contributions.append({
                "item": original_word,
                "base_score": base_score,
                "modifiers": applied_modifiers,
                "final_score": round(final_score, 3),
            })

        # Analyse emojis and emoticons
        symbol_result = self._analyse_symbols(text)

        raw_score += symbol_result["score"]
        positive_items += symbol_result["positive_items"]
        negative_items += symbol_result["negative_items"]
        contributions.extend(symbol_result["contributions"])

        # Punctuation emphasis
        exclamation_count = min(text.count("!"), 4)

        if exclamation_count > 0 and raw_score != 0:

            punctuation_multiplier = (
                1 + exclamation_count * 0.10
            )

            old_score = raw_score
            raw_score *= punctuation_multiplier

            punctuation_change = raw_score - old_score

            contributions.append({
                "item": "!" * exclamation_count,
                "base_score": 0.0,
                "modifiers": [
                    f"punctuation ×"
                    f"{round(punctuation_multiplier, 2)}"
                ],
                "final_score": round(
                    punctuation_change,
                    3
                ),
            })

        compound = self._calculate_compound(raw_score)
        sentiment = self._get_label(compound)

        proportions = self._calculate_proportions(
            total_words=len(words),
            positive_items=positive_items,
            negative_items=negative_items,
        )

        return {
            "text": text,
            "sentiment": sentiment,
            "compound": compound,
            "proportions": proportions,
            "contributions": contributions,
        }

    def predict_batch(self, texts):
        """Analyse multiple sentences."""

        if (
            isinstance(texts, (str, bytes))
            or not isinstance(texts, Iterable)
        ):
            raise TypeError(
                "Input must be a collection of sentences."
            )

        return [
            self.predict(text)
            for text in texts
        ]

    def add_word(self, word, score):
        """Add a custom sentiment word."""

        if not isinstance(word, str) or not word.strip():
            raise ValueError(
                "Word must be non-empty text."
            )

        if not isinstance(score, (int, float)):
            raise TypeError(
                "Score must be a number."
            )

        if score == 0 or score < -4 or score > 4:
            raise ValueError(
                "Score must be between -4 and +4 "
                "and cannot be zero."
            )

        clean_word = word.lower().strip()

        self.lexicon[clean_word] = float(score)

    @property
    def vocabulary_size(self):
        """Return the number of sentiment words."""

        return len(self.lexicon)

    def _validate_text(self, text):
        if not isinstance(text, str):
            raise TypeError("Input must be text.")

        if not text.strip():
            raise ValueError("Text cannot be empty.")

    def _analyse_symbols(self, text):
        score = 0.0
        positive_items = 0
        negative_items = 0
        contributions = []

        remaining_text = text

        # Process long symbols first.
        # This prevents :) from being counted inside :-).
        sorted_symbols = sorted(
            self.symbol_scores,
            key=len,
            reverse=True
        )

        for symbol in sorted_symbols:

            count = remaining_text.count(symbol)

            if count == 0:
                continue

            symbol_score = (
                self.symbol_scores[symbol] * count
            )

            score += symbol_score

            if symbol_score > 0:
                positive_items += count
            else:
                negative_items += count

            modifiers = []

            if count > 1:
                modifiers.append(
                    f"repeated ×{count}"
                )

            contributions.append({
                "item": symbol,
                "base_score": self.symbol_scores[symbol],
                "modifiers": modifiers,
                "final_score": round(symbol_score, 3),
            })

            remaining_text = remaining_text.replace(
                symbol,
                ""
            )

        return {
            "score": score,
            "positive_items": positive_items,
            "negative_items": negative_items,
            "contributions": contributions,
        }

    @staticmethod
    def _calculate_compound(raw_score):
        """Convert raw score to a value from -1 to +1."""

        if raw_score == 0:
            return 0.0

        compound = raw_score / math.sqrt(
            raw_score ** 2 + 16
        )

        return round(compound, 4)

    @staticmethod
    def _get_label(compound):
        """Convert compound score into a label."""

        if compound >= 0.05:
            return "positive"

        if compound <= -0.05:
            return "negative"

        return "neutral"

    @staticmethod
    def _calculate_proportions(
        total_words,
        positive_items,
        negative_items
    ):
        neutral_items = max(
            total_words
            - positive_items
            - negative_items,
            0
        )

        total_items = (
            positive_items
            + negative_items
            + neutral_items
        )

        if total_items == 0:
            return {
                "positive": 0.0,
                "negative": 0.0,
                "neutral": 1.0,
            }

        return {
            "positive": round(
                positive_items / total_items,
                3
            ),
            "negative": round(
                negative_items / total_items,
                3
            ),
            "neutral": round(
                neutral_items / total_items,
                3
            ),
        }