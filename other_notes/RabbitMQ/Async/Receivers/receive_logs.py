import asyncio
import os
import sys

from aio_pika import ExchangeType, connect
from aio_pika.abc import AbstractIncomingMessage
from utilities import logger

username: str = "guest"
password: str = "guest"
host: str = "localhost"
URL: str = f"amqp://{username}:{password}@{host}/"
queue_name: str = "logs"
logger.info("Starting consumer")


async def on_messgae_callback(message: AbstractIncomingMessage) -> None:
    async with message.process():
        logger.info(f" [x] Received message is {message.body.decode()!r}")


async def main() -> None:
    # Connect to a broker
    connection = await connect(URL)

    async with connection:
        # Create a channel
        channel = await connection.channel()
        # Set prefetch count
        await channel.set_qos(prefetch_count=1)
        # Declare exchange
        logs_exchange = await channel.declare_exchange(
            queue_name,
            durable=True,
            type=ExchangeType.FANOUT,
        )
        # Delcare queue
        # Exclusive queue: deletes the queue when we close the consumer
        queue = await channel.declare_queue(exclusive=True)
        # Bind queue to exchange
        await queue.bind(logs_exchange)
        # Start listening
        await queue.consume(on_messgae_callback)
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
