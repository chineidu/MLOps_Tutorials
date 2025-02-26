# Asynchronous Python Programming

## Table of Contents

- [Asynchronous Python Programming](#asynchronous-python-programming)
  - [Table of Contents](#table-of-contents)
  - [Introduction to Asynchronous Programming](#introduction-to-asynchronous-programming)
  - [Core Concepts](#core-concepts)
  - [Basic Examples](#basic-examples)
    - [1.) Simple Coroutine](#1-simple-coroutine)
    - [2.) Running Multiple Coroutines Concurrently](#2-running-multiple-coroutines-concurrently)

## Introduction to Asynchronous Programming

- Asynchronous programming allows you to write concurrent code that can perform multiple operations simultaneously without blocking the main thread.
- In Python, this is primarily achieved using the asyncio library and the async/await syntax.

## Core Concepts

Before diving into code examples, let's understand some key concepts:

- **Coroutines**: Functions defined with async def that can be paused and resumed.
- **Tasks**: Wrappers around coroutines that run them in an event loop.
- **Event** Loop: The central execution mechanism that manages and distributes tasks.
- **await**: The keyword used to pause execution until an awaitable completes.

## Basic Examples

### 1.) Simple Coroutine

```py
import asyncio

async def hello_world():
    print("Hello")
    await asyncio.sleep(1)  # Non-blocking sleep
    print("World")

# Run the coroutine
asyncio.run(hello_world())
```

### 2.) Running Multiple Coroutines Concurrently

```py
import asyncio
import time

async def say_after(delay, message):
    await asyncio.sleep(delay)
    print(message)

async def main():
    print(f"Started at {time.strftime('%X')}")

    # Run these concurrently
    await asyncio.gather(
        say_after(1, "Hello"),
        say_after(2, "World")
    )

    print(f"Finished at {time.strftime('%X')}")

asyncio.run(main())
```
import asyncio
import time


async def simple_coroutine(delay: float) -> None:
    # Simulate work (Non-blocking)
    await asyncio.sleep(delay)
    print(f"Hello after {delay} seconds...")
