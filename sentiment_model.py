# sentiment_model.py
from textblob import TextBlob

def analyze_sentiment(text):
    # Specific negative keywords to enhance detection
    negative_keywords = ["never", "sucked", "worst", "terrible", "hate", "awful"]

    blob = TextBlob(text)
    polarity = blob.sentiment.polarity

    # Check for strong negative words if polarity is close to neutral
    if any(word in text.lower() for word in negative_keywords) and polarity <= 0:
        return "negative"
    elif polarity > 0.1:
        return "positive"
    elif polarity < -0.1:
        return "negative"
    else:
        return "neutral"
