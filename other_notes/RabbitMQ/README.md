# [RabbitMQ](https://www.rabbitmq.com/)

## Table of Content

- [RabbitMQ](#rabbitmq)
  - [Table of Content](#table-of-content)
  - [Installation](#installation)
  - [Introduction](#introduction)
    - [Using Python Client](#using-python-client)
    - [General Terminologies](#general-terminologies)
    - [Listing Queues](#listing-queues)

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
