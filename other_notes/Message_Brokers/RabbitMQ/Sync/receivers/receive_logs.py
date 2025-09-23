import os
import sys

import pika
from utilities import logger


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="logs", exchange_type="fanout")

    result = channel.queue_declare(
        # Auto generated queue name
        queue="",
        # Make the queue only accessible by the current connection
        exclusive=True,
    )
    queue_name: str = result.method.queue
    # Bind the queue to the exchange
    channel.queue_bind(exchange="logs", queue=queue_name)
    logger.info(" [*] Waiting for logs. To exit press CTRL+C")

    def callback(ch, method, properties, body: bytes) -> None:
        logger.info(f" [x] {method.routing_key}: {body.decode()}")
        for handler in logger.handlers:
            handler.flush()  # Explicitly flush logs

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        # Automatically acknowledge messages
        # Note: The callback's ch.basic_ack and auto_ack=True are mutually exclusive
        auto_ack=True,  # Automatically acknowledge messages
    )

    channel.start_consuming()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)  # Gracefully exit
        except SystemExit:
            os._exit(0)
