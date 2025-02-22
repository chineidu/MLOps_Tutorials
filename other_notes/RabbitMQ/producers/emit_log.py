import sys

import pika
from utilities import logger

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.exchange_declare(exchange="logs", exchange_type="fanout")
message: str = " ".join(sys.argv[1:]) or "info: Hello World!"

# Publish the message to the exchange
channel.basic_publish(
    exchange="logs",  # The name of the exchange
    routing_key="",  # The routing key is empty for fanout exchanges
    body=message,
)
logger.info(f" [x] Sent {message}")
connection.close()
