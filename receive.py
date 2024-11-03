#!/usr/bin/env python
import pika, sys, os
import json
from sentiment_model import analyze_sentiment

rabbitmq_host = 'localhost'
queue_name = 'comments_queue'

# Establish connection with RabbitMQ server
def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()

    # Connect to the queue
    channel.queue_declare(queue=queue_name)

    # Sentiment analysis
    def analyze_comments(comment):
        sentiment = analyze_sentiment(comment)
        print(f" [o] Comment: {comment}\n [o] Sentiment: {sentiment}")

    # "callback" function is called whenever a message is received
    def callback(ch, method, properties, body):
        message = json.loads(body)
        comment = message.get("text", "")
        print(f" [x] Received {body}")
        # Analyze the comment and print the sentiment
        analyze_comments(comment)

    # Telling RabbitMQ that this callback function should receiver a message from our "hello-queue" queue
    channel.basic_consume(queue=queue_name,
                        auto_ack=True,
                        on_message_callback=callback)

    # Never-ending loop that waits for data and runs callbacks whenever necessary,
    # and catch "KeyboardInterrupt" during program shutdown.
    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)