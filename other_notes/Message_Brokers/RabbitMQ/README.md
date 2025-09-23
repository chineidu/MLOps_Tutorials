# [RabbitMQ](https://www.rabbitmq.com/)

## Table of Content

- [RabbitMQ](#rabbitmq)
  - [Table of Content](#table-of-content)
  - [Installation](#installation)
  - [Introduction](#introduction)
    - [Using Python Client](#using-python-client)
    - [General Terminologies](#general-terminologies)
    - [Listing Queues](#listing-queues)
    - [Delete Queues](#delete-queues)
    - [List Forgotten Acknowledgements](#list-forgotten-acknowledgements)
    - [Listing Bindings](#listing-bindings)
    - [Types of Exchanges](#types-of-exchanges)
    - [Logging Example](#logging-example)
    - [List](#list)

## [Installation](https://www.rabbitmq.com/docs/download#docker)

- Installation using Docker

```sh
# latest RabbitMQ 4.0.x
docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:4.0-management
```

- Other installation methods include:
  - on linux
  - on macOS
  - on Windows
  - on Kubernetes
  - on cloud providers

## Introduction

- RabbitMQ is a message broker, which means it acts like a post office for your applications.
- It receives messages, stores them, and delivers them to the correct recipients.
- This allows different parts of your application to communicate with each other asynchronously, which can improve performance and scalability.

### Using Python Client

- Install the `pika` library, which is a Python client for RabbitMQ:

```sh
pip install pika
```

- RabbitMQ runs on `loacalhost` and on the standard port `5672` by default.

### General Terminologies

- Producer: The application that sends messages.
- Consumer: The application that receives messages.
- Queue: A buffer that stores messages.

### Listing Queues

- List queues using `rabbitmqctl list_queues`

```sh
rabbitmqctl list_queues
```

### Delete Queues

```sh
rabbitmqctl delete_queue <queue_name>

# E.g.

rabbitmqctl delete_queue my_queue
```

### List Forgotten Acknowledgements

```sh
rabbitmqctl list_queues name messages_ready messages_unacknowledged
```

### Listing Bindings

- Bindings are used to connect queues to exchanges.
- Bindings are used to route messages to queues based on their routing key.

```sh
rabbitmqctl list_bindings
```

### Types of Exchanges

- RabbitMQ uses exchanges to route messages to queues. Here's a breakdown of the main exchange types:

**1.) Direct Exchange**:  A direct exchange delivers messages based on a precise routing key match. i.e. (Like sending mail to a specific address.)

**2.)Fanout Exchange**: A fanout exchange delivers messages to all queues bound to it, regardless of the routing key.  It's like broadcasting a message; everyone gets it.

**3.) Topic Exchange**: Delivers messages based on pattern matching the routing key using wildcards (*, #). (Like subscribing to newspaper topics.)

**4.) Headers Exchange**: A headers exchange delivers messages based on headers in the message, rather than the routing key. It's less common but can be useful in some scenarios.

### Logging Example

- The code can be found in `receivers/receive_log.py`
- To store the logs in a file, use the following command:

```sh
python -m receivers.receive_logs > logs_from_rabbit.log
```

- To display the logs in the terminal, use the following command:

```sh
python -m receivers.receive_logs
```

### List
