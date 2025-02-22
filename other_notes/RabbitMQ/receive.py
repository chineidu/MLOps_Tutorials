# type: ignore
import os
import sys

import pika
from utilities import logger


def main() -> None:
    # Connect to RabbitMQ server running on localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare a queue. Make sure it matches the queue name used by the sender.
    channel.queue_declare(queue="hello")

    def callback(ch, method, properties, body: bytes) -> None:
        logger.info(f" [x] Received {body!r}")

    # Acknowledge the message to remove it from the queue
    channel.basic_consume(queue="hello", on_message_callback=callback, auto_ack=True)
    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
