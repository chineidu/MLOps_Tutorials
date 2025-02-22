# type: ignore
import sys

import pika
from utilities import logger

# Connect to RabbitMQ server running on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Create a queue
channel.queue_declare(queue="hello")

# Send a message to the queue using the default exchange
message: str = " ".join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(
    exchange="",  # Use the default exchange
    routing_key="hello",  # The name of the queue
    body=message,  # The message to send
)
logger.info(f" [x] Sent {message}")
