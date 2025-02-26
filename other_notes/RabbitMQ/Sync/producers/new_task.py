# type: ignore
import sys

import pika
from utilities import logger


def main() -> None:
    # Connect to RabbitMQ server running on localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Create a queue
    channel.queue_declare(
        queue="hello",
        durable=True,  # Make the queue durable
    )

    # Send a message to the queue using the default exchange
    message: str = " ".join(sys.argv[1:]) or "Hello World!"
    channel.basic_publish(
        exchange="",  # Use the default exchange
        routing_key="hello",  # The name of the queue
        body=message,  # The message to send
        properties=pika.BasicProperties(
            # Make the message persistent
            delivery_mode=pika.DeliveryMode.Persistent,
        ),
    )
    logger.info(f" [x] Sent {message}")
    # Close the connection
    connection.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        sys.exit(0)
