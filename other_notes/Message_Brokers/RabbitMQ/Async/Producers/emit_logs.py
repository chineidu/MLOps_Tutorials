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
queue_name: str = "logs"
logger.info("Starting producer")


async def main() -> None:
    # Connect to a broker
    connection = await connect(URL)

    async with connection:
        # Create a channel
        channel = await connection.channel()
        # Create exchange
        logs_exchange = await channel.declare_exchange(
            queue_name,
            durable=True,
            type=ExchangeType.FANOUT,
        )
        # Create the message
        message_body: bytes = b" ".join(arg.encode() for arg in sys.argv[1:]) or b"Hello World!"
        message = Message(
            message_body,
            # Make the message persistent
            delivery_mode=DeliveryMode.PERSISTENT,
            timestamp=datetime.now(),
        )
        # Send the message
        await logs_exchange.publish(message=message, routing_key=queue_name)
        logger.info(f" [x] Sent {message!r}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Interrupted")
        try:
            logger.info("Gracefully shutting down")
            sys.exit(0)
        except SystemExit:
            logger.info("Forcefully shutting down")
            os._exit(0)
