import asyncio
import os
import sys

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from utilities import logger

username: str = "guest"
password: str = "guest"
host: str = "localhost"
URL: str = f"amqp://{username}:{password}@{host}/"
queue_name: str = "task_queue"
logger.info("Starting consumer")


async def on_message_callback(message: AbstractIncomingMessage) -> None:
    async with message.process():
        logger.info(f" [x] Received message is {message!r}")
        await asyncio.sleep(message.body.count(b"."))
        logger.info(f"   Mesage body is {message.body.decode()!r}")


async def main() -> None:
    # Create connection
    connection = await connect()

    async with connection:
        # Create channel
        channel = await connection.channel()
        # Set prefetch count
        await channel.set_qos(prefetch_count=1)
        # Declare queue
        queue = await channel.declare_queue(queue_name, durable=True)
        # Start listening
        await queue.consume(on_message_callback)
        logger.info(f" [*] Waiting for messages. To exit press CTRL+C")
        # Wait until the connection is terminated
        await asyncio.Future()


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
