# Asynchronous Python Programming

## Table of Contents

<!-- TOC -->

- [Asynchronous Python Programming](#asynchronous-python-programming)
  - [Table of Contents](#table-of-contents)
  - [Introduction to Asynchronous Programming](#introduction-to-asynchronous-programming)
  - [Core Concepts](#core-concepts)
    - [Note](#note)
  - [Workflow](#workflow)
  - [Basic Examples](#basic-examples)
    - [Simple Coroutine](#simple-coroutine)
    - [Running Multiple Coroutines Concurrently](#running-multiple-coroutines-concurrently)
    - [Run An Async Function In A Non-concurrent Manner Not Recommended](#run-an-async-function-in-a-non-concurrent-manner-not-recommended)
  - [Converting Synchronous Code to Asynchronous Code](#converting-synchronous-code-to-asynchronous-code)

<!-- /TOC -->
## Introduction to Asynchronous Programming

- Asynchronous programming allows you to write concurrent code that can perform multiple operations simultaneously without blocking the main thread.
- In Python, this is primarily achieved using the asyncio library and the async/await syntax.

## Core Concepts

Before diving into code examples, let's understand some key concepts:

- **Coroutines**: Functions defined with async def that can be paused and resumed.
- **Tasks**: Wrappers around coroutines that run them in an event loop.
- **Event** Loop: The central execution mechanism that manages and distributes tasks.
- **await**: The keyword used to pause execution until an awaitable completes.

### Note

- Without creating a task, coroutines do not run concurrently.

- They need to be scheduled in the event loop using functions like `asyncio.create_task()`, `asyncio.gather()` or `asyncio.TaskGroup()` with context managers.

## Workflow

- Create async functions using `async def`.
- Create tasks to run coroutines concurrently.
- Use `await` to pause execution until a coroutine completes.

## Basic Examples

### Simple Coroutine

```py
import asyncio

async def hello_world():
    print("Hello")
    await asyncio.sleep(1)  # Non-blocking sleep
    print("World")

# Run the coroutine
asyncio.run(hello_world())
```

### Running Multiple Coroutines Concurrently

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

### Run An Async Function In A Non-concurrent Manner (Not Recommended)

- This example demonstrates running async functions sequentially without concurrency, which is generally not recommended as it negates the benefits of asynchronous programming.

```py
import asyncio
import time


async def simple_coroutine(delay: float) -> None:
    # Simulate work (Non-blocking)
    await asyncio.sleep(delay)
    print(f"Hello after {delay} seconds...")


async def main() -> None:
    start_time = time.perf_counter()

    # Running coroutines sequentially (not concurrent)
    await simple_coroutine(2)
    await simple_coroutine(3)

    duration = time.perf_counter() - start_time
    print(f"Duration: {duration:.2f} seconds")  # Should be ~5 seconds
```

## Converting Synchronous Code to Asynchronous Code

- Identify blocking operations (e.g., I/O operations, network requests).
- This can be best done using profilers or code analysis tools. e.g. `scalene`, `py-spy`, `cProfile`, etc.
- If async libraries are not available, consider using thread or process pools to run blocking code without blocking the event loop.
- If async libraries are available, refactor the code to use async/await syntax.
  - e.g. Replace `requests` with `httpx` or `aiohttp` for HTTP requests.
  - replace file I/O with `aiofiles` for asynchronous file operations.
  - Use `asyncio.sleep()` instead of `time.sleep()`.
  - Test the refactored code to ensure it behaves as expected and benefits from concurrency.
