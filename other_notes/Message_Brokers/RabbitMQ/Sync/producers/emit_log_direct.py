# This module uses the direct exchange instead of the fanout exchange.
# The direct exchange routes messages to queues based on the message routing key.
import os
import sys

import pika
from utilities import logger


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

    # If no args are passed, default to info
    severity = sys.argv[1] if len(sys.argv) > 1 else "info"
    message: str = " ".join(sys.argv[2:]) or "Hello World!"
    channel.basic_publish(
        exchange="direct_logs",
        routing_key=severity,
        body=message,
    )
    logger.info(f" [x] Sent {severity}:{message}")

    connection.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
