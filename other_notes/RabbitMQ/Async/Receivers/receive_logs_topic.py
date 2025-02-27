"""
NOTE:
1.) When a queue is bound with "#" (star) binding key - it will receive all the
messages, regardless of the routing key - like in fanout.

2.) When special characters "*" (star) and "#" (hash) aren't used in bindings, the topic
exchange will behave just like a direct one.

- To receive all the logs, run:
python receive_logs_topic.py "#"

- To receive all logs from the facility "kern":
python receive_logs_topic.py "kern.*"

- Or if you want to hear only about "critical" logs:
python receive_logs_topic.py "*.critical"

- You can create multiple bindings:
python receive_logs_topic.py "kern.*" "*.critical"
"""

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
exchange_name: str = "topic_logs"
queue_name: str = "task_queue"
logger.info("Starting consumer")


async def on_message_callback(message: AbstractIncomingMessage) -> None:
    try:
        async with message.process(requeue=False):  # Ensure proper acknowledgment
            logger.info(f" [x] Received message is {message.body.decode()!r}")
    except Exception as e:
        logger.error(f"Error processing message: {e}")


async def main() -> None:
    # Connect to a broker
    connection = await connect(URL)

    async with connection:
        # Create a channel
        channel = await connection.channel()
        # Set prefetch count
        await channel.set_qos(prefetch_count=1)
        # Declare exchange
        topic_logs_exchange = await channel.declare_exchange(
            name=exchange_name,
            durable=True,
            type=ExchangeType.TOPIC,
        )
        # Delcare queue
        queue = await channel.declare_queue(name=queue_name, durable=True)
        binding_keys = sys.argv[1:]
        if not binding_keys:
            logger.error(f"Usage: {sys.argv[0]} [binding_key]...")
            sys.exit(1)

        # Bind queue to exchange
        for binding_key in binding_keys:
            await queue.bind(topic_logs_exchange, routing_key=binding_key)
        # Start listening to queue and process messages
        async with queue.iterator() as queue_iter:
            async for message in queue_iter:
                async with message.process():
                    logger.info(f" [x] Received message is {message.body.decode()!r}")
        # Or using the callback function
        # await queue.consume(on_message_callback)
        # Wait until the connection is terminated
        # await asyncio.Future()


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
