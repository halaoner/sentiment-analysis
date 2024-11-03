# Introduction

This experimental project will deepen the experience in Python, FastAPI, RabbitMQ and MLOps domains.

> The project will change and evolve.

# High Level Communication Flow

1. Comment Submission: A comment is submitted to FastAPI, which publishes it to RabbitMQ.
1. Message Queueing: RabbitMQ stores the comment in `queue_name` variable.
1. Message Processing: The `receive.py` script fetches each comment, performs `sentiment analysis`, and prints the result.

Client (e.g., browser) sends HTTP request --> HTTP request is sent to FastAPI endpoint --> Publish the message in to a queue --> Consume the message from the queue --> perform the sentiment analysis --> Print the result of sentiment analysis in stdout

# Getting Started

### Prerequisites

1. Install Docker Desktop

2. Install `fastapi` library

```bash
pip3 install "fastapi[standard]"
```

3. Install `textblob` library

```bash
pip3 install textblob
```

### Running The Server

1. Start up the FastAPI server

```bash
fastapi dev
```

2. Call FastAPI endpoint

| Endpoint              | HTTP Request Method     |
|-----------------------|-------------------------|
| `/submit-review"`     | POST                    |
| `/`                   | GET                     |


Example:

```bash
curl -X POST "http://127.0.0.1:8000/submit-review" -H "Content-Type: application/json" -d '{"text": "I hate this product!"}'
```

Expected output:

```bash
{"message":"Comment saved successfully!","comment":"I hate this product!"}
```

# Sentiment Analysis Explained

**Sentiment analysis** is a process in AI that checks if a piece of text (like a review or comment) expresses a positive, negative, or neutral feeling. It helps computers understand the emotional tone behind words, like whether someone is happy, angry, or indifferent. This is useful for things like understanding customer feedback or tracking opinions on social media.

### `sentiment_model.py`

```python
# "textblob" library, which provides simple methods for performing natural language processing (NLP) tasks, such as sentiment analysis.
from textblob import TextBlob

def analyze_sentiment(text):               # "text" -> parameter that will be analyzed
    
    negative_keywords = ["never", "sucked", "worst", "terrible", "hate", "awful"] # specific negative keywords to enhance detection

    blob = TextBlob(text)                  # converts the input "text" into a TextBlob object
    polarity = blob.sentiment.polarity     # calculates a polarity score for the text, a value between -1.0 and 1.0

    # Check for strong negative words if polarity is close to neutral
    if any(word in text.lower() for word in negative_keywords) and polarity <= 0:
        return "negative"
    elif polarity > 0.1:                   # if polarity is greater than 0.1, it returns "positive"
        return "positive"                  
    elif polarity < -0.1:                  # if polarity is less than -0.1, it returns "negative
        return "negative"
    else:
        return "neutral"                   # zero indicates neutral sentiment
```

