# This module uses the direct exchange instead of the fanout exchange.
# The direct exchange routes messages to queues based on the message routing key.
import sys

import pika
from utilities import logger


def main() -> None:
    connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
    channel = connection.channel()

    channel.exchange_declare(exchange="direct_logs", exchange_type="direct")

    result = channel.queue_declare(
        # Auto generated queue name
        queue="",
        # Make the queue only accessible by the current connection
        exclusive=True,
    )
    queue_name: str = result.method.queue
    severities = sys.argv[1:]
    if not severities:
        sys.stderr.write("Usage: %s [info] [warning] [error]\n" % sys.argv[0])
        sys.exit(1)
    for severity in severities:
        # Bind the queue to the exchange with the specified routing key
        channel.queue_bind(
            exchange="direct_logs",
            queue=queue_name,
            routing_key=severity,
        )

    logger.info(" [*] Waiting for logs. To exit press CTRL+C")

    def callback(ch, method, properties, body: bytes) -> None:
        logger.info(f" [x] {method.routing_key}: {body.decode()}")
        for handler in logger.handlers:
            handler.flush()  # Explicitly flush logs

    channel.basic_consume(
        queue=queue_name,
        on_message_callback=callback,
        auto_ack=True,
    )
    channel.start_consuming()
    connection.close()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("Interrupted")
        sys.exit(0)
