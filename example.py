from pprint import pprint

from bajil_sentiment import SentimentAnalyzer


analyzer = SentimentAnalyzer()

print("Bajil Sentiment Analyser")
print("------------------------")

sentence = input("Enter a sentence: ")

result = analyzer.predict(sentence)

print("\nAnalysis result:")
pprint(result)