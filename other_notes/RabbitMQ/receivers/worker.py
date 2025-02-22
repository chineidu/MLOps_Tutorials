# type: ignore

import os
import sys
import time

import pika
from utilities import logger


def main() -> None:
    # Connect to RabbitMQ server running on localhost
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    # Declare a queue. Make sure it matches the queue name used by the sender.
    channel.queue_declare(queue="hello", durable=True)

    def callback(ch, method, properties, body: bytes) -> None:
        logger.info(f" [x] Received {body.decode()}")
        # Simulate work
        time.sleep(body.count(b"."))
        logger.info(" [x] Done")
        # Acknowledge the message to remove it from the queue
        # If the worker dies without acknowledging the message,
        # it will be redelivered.
        ch.basic_ack(delivery_tag=method.delivery_tag)

    # Set the prefetch count to 1. This means the server will only send
    # one message to a worker at a time. When the worker processes a message,
    # and sends an acknowledgement, the server will send another message.
    channel.basic_qos(prefetch_count=1)
    # Acknowledge the message to remove it from the queue
    channel.basic_consume(
        queue="hello",
        on_message_callback=callback,
        # auto_ack=True, # Automatically acknowledge messages
    )
    logger.info(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()

    # Close the connection
    connection.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
