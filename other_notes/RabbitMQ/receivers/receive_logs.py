import pika
from utilities import logger

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()

channel.exchange_declare(exchange="logs", exchange_type="fanout")

result = channel.queue_declare(
    queue="",
    exclusive=True,  # Make the queue only accessible by the current connection
)
queue_name = result.method.queue

channel.queue_bind(exchange="logs", queue=queue_name)

logger.info(" [*] Waiting for logs. To exit press CTRL+C")


def callback(ch, method, properties, body: bytes) -> None:
    logger.info(f" [x] {method.routing_key}: {body.decode()}")
    for handler in logger.handlers:
        handler.flush()  # Explicitly flush logs


channel.basic_consume(
    queue=queue_name,
    on_message_callback=callback,
    auto_ack=True,  # Automatically acknowledge messages
)

channel.start_consuming()
