"""
NOTE: This is a producer that sends messages to a topic exchange.

# Usage:
python emit_logs_topic.py "kern.critical" "A critical kernel error"
"""

import asyncio
import os
import sys
from datetime import datetime

from aio_pika import DeliveryMode, ExchangeType, Message, connect
from utilities import logger

username: str = "guest"
password: str = "guest"
host: str = "localhost"
URL: str = f"amqp://{username}:{password}@{host}/"
exchange_name: str = "topic_logs"
logger.info("Starting producer")


async def main() -> None:
    # Create a connection
    connection = await connect(URL)

    async with connection:
        # Create channel
        channel = await connection.channel()
        # Create exchange
        logs_exchange = await channel.declare_exchange(
            exchange_name,
            durable=True,
            type=ExchangeType.TOPIC,
        )
        routing_key = sys.argv[1] if len(sys.argv) > 1 else "anonymous.info"
        # Create the message
        message_body: bytes = b" ".join(arg.encode() for arg in sys.argv[2:]) or b"Hello World!"
        message = Message(
            message_body,
            # Make the message persistent
            delivery_mode=DeliveryMode.PERSISTENT,
            timestamp=datetime.now(),
        )
        # Send the message
        await logs_exchange.publish(message=message, routing_key=routing_key)
        logger.info(f" [x] Sent {message!r}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
