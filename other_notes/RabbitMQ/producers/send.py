# type: ignore
import pika
from utilities import logger

# Connect to RabbitMQ server running on localhost
connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

# Create a queue
channel.queue_declare(
    queue="hello",  # The name of the queue
)

# Send a message to the queue using the default exchange
channel.basic_publish(
    exchange="",  # Use the default exchange
    routing_key="hello",  # The name of the queue
    body="Hello World!",  # The message to send
)

logger.info(" [x] Sent 'Hello World!'")

# Close the connection
connection.close()
