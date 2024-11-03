from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json
import pika

# Initialization of the FastAPI app - used to define routes for handling 
app = FastAPI()

# Define a Comment Data Model with single attribute - "text"
class Comment(BaseModel):
    text: str


################################## RabbitMQ Configuration ##################################

# RabbitMQ connection parameters
rabbitmq_host = 'localhost'  # Adjust based on your setup
queue_name = 'comments_queue'


def publish_comment(comment: dict):
    # Establish connection with RabbitMQ server
    connection = pika.BlockingConnection(pika.ConnectionParameters(rabbitmq_host))
    channel = connection.channel()

    # Create a new queue
    channel.queue_declare(queue=queue_name)

    # Message goes through an "exchange" - it is NEVER sent directly to the queue
    channel.basic_publish(exchange='',
                        routing_key=queue_name,
                        body=json.dumps(comment))
    print(f" [x] Comment has been sent: {comment}")

##################################################################################################

# HTTP endpoint "/"
@app.get("/")
async def root():
    return {
            "message": "Hello at Sentiment Analysis! Submit your comment at '/submit-review' endpoint!"
           }

@app.post("/submit-review")
# asynchronous function that takes "comment" as an parameter
async def submit_comment(comment: Comment):
    # "a" add a new comment at the end of the file
    with open("comments.json", "a") as file:
        # comment is converted to a dictionary(model_dump), then converted to a JSON
        file.write(json.dumps(comment.model_dump()) + "\n")
    try:
        # publish comment into a RabbitMQ queue
        publish_comment(comment.model_dump())
        return {"message": "Comment submitted successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to publish comment: {e}")
