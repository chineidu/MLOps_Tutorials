import asyncio
import os
import sys

from aio_pika import Message, connect
from utilities import logger

username: str = "guest"
password: str = "guest"
host: str = "localhost"
URL: str = f"amqp://{username}:{password}@{host}/"
queue_name: str = "hello"
logger.info("Starting producer")


async def main() -> None:
    connection = await connect(URL)

    async with connection:
        # Create a channel
        channel = await connection.channel()
        # Declare queue
        queue = await channel.declare_queue(queue_name)
        # Send a message
        await channel.default_exchange.publish(
            Message(b"Hello World!"),
            routing_key=queue.name,
        )
        logger.info(" [x] Sent 'Hello World!'")


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
