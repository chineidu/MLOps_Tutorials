import asyncio
import sys

from aio_pika import connect
from aio_pika.abc import AbstractIncomingMessage
from utilities import logger

queue_name: str = "hello"


async def on_message_callback(message: AbstractIncomingMessage) -> None:
    async with message.process():
        logger.info(f" [x] Received message is {message}")
        logger.info(f" [x] Received {message.body}")

        logger.info("Before sleep!")
        await asyncio.sleep(5)
        logger.info("After sleep!")


async def main() -> None:
    connection = await connect("amqp://guest:guest@localhost/")
    async with connection:
        #  Create channel
        channel = await connection.channel()

        # Declare queue
        queue = await channel.declare_queue(queue_name)

        # Start listening
        await queue.consume(on_message_callback)

        logger.info(f" [*] Waiting for messages. To exit press CTRL+C")

        # Wait until the connection is terminated
        await asyncio.Future()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        sys.exit(0)
