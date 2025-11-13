# Python Async Operations Reference

## Table of Contents
<!-- TOC -->

- [Python Async Operations Reference](#python-async-operations-reference)
  - [Table of Contents](#table-of-contents)
  - [1. I/O-bound functions in synchronous libraries](#1-io-bound-functions-in-synchronous-libraries)
  - [2. CPU-bound work](#2-cpu-bound-work)
  - [3. Native async HTTP with `aiohttp`](#3-native-async-http-with-aiohttp)
  - [3b. Async file I/O with `aiofiles`](#3b-async-file-io-with-aiofiles)
  - [4. Controlled error handling with `asyncio.gather`](#4-controlled-error-handling-with-asynciogather)
  - [5. Rate limiting with semaphores](#5-rate-limiting-with-semaphores)
  - [6. Timeout control with `asyncio.wait_for`](#6-timeout-control-with-asynciowait_for)
  - [7. Background, fire-and-forget tasks](#7-background-fire-and-forget-tasks)
  - [8. Progress tracking with `tqdm`](#8-progress-tracking-with-tqdm)
  - [9. Retry logic with `tenacity`](#9-retry-logic-with-tenacity)
  - [10. Async context managers](#10-async-context-managers)
  - [11. Async generators for streaming data](#11-async-generators-for-streaming-data)
  - [12. Queue-based worker pattern](#12-queue-based-worker-pattern)
  - [13. Entry point for async scripts](#13-entry-point-for-async-scripts)
  - [14. Real-world scraping example](#14-real-world-scraping-example)
  - [Quick decision tree](#quick-decision-tree)

<!-- /TOC -->
> This app-note reorganizes the runnable Python snippets into narrative
> sections that explain when and why each pattern is appropriate. Code
> examples remain untouched so you can copy/paste directly.

## 1. I/O-bound functions in synchronous libraries

- **Problem:** You depend on a blocking library such as `requests` or `time.sleep`, but you want to keep your async event loop responsive.
- **Solution:** Wrap the blocking call with `asyncio.to_thread()` (Python 3.9+). That delegates work to a separate thread so your async loop can continue.

```python
import asyncio
import requests
import time

def fetch_url_sync(url: str) -> str:
    time.sleep(0.1)  # simulate delay
    resp = requests.get(url)
    return resp.text

async def fetch_url(url: str) -> str:
    return await asyncio.to_thread(fetch_url_sync, url)
```

## 2. CPU-bound work

- **Problem:** CPU-heavy tasks (e.g., math or data processing) are slowed by the Global Interpreter Lock (GIL).
- **Solution:** Use `ProcessPoolExecutor` to bypass the GIL for CPU work, or `ThreadPoolExecutor` plus `run_in_executor()` for I/O-bound helper functions.

```python
import math
from concurrent.futures import ProcessPoolExecutor, ThreadPoolExecutor

def cpu_heavy(n: int) -> float:
    return sum(math.sqrt(i) for i in range(n))

async def async_cpu_heavy(n: int) -> float:
    loop = asyncio.get_running_loop()
    with ProcessPoolExecutor() as pool:
        return await loop.run_in_executor(pool, cpu_heavy, n)

async def async_thread_work(func, *args):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, func, *args)
```

## 3. Native async HTTP with `aiohttp`

- **Problem:** You must issue multiple HTTP requests efficiently within asyncio.
- **Solution:** Reuse a single `aiohttp.ClientSession` and combine requests with `asyncio.gather()` for maximum throughput.

```python
import aiohttp
from typing import List, Dict

async def fetch_json(session: aiohttp.ClientSession, url: str) -> Dict:
    """Fetch JSON from URL using async HTTP client."""
    async with session.get(url) as response:
        return await response.json()

async def fetch_multiple_urls(urls: List[str]) -> List[Dict]:
    """Fetch multiple URLs concurrently with connection pooling."""
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_json(session, url) for url in urls]
        return await asyncio.gather(*tasks)
```

## 3b. Async file I/O with `aiofiles`

- **Problem:** Synchronous file operations would block the event loop.
- **Solution:** Use `aiofiles` to read/write JSON asynchronously while preserving standard file semantics.

```python
import aiofiles
import json
from pathlib import Path

users_data = [
    {"id": 1, "name": "Alice", "email": "alice@example.com"},
    {"id": 2, "name": "Bob", "email": "bob@example.com"},
    {"id": 3, "name": "Charlie", "email": "charlie@example.com"}
]

async def write_user_json(user: dict, output_dir: Path) -> Path:
    """Write a single user dict to a JSON file asynchronously."""
    filepath = output_dir / f"user_{user['id']}.json"
    
    async with aiofiles.open(filepath, mode="w", encoding="utf-8") as f:
        await f.write(json.dumps(user, indent=2))
    
    print(f"✅ Wrote {filepath.name}")
    return filepath

async def read_user_json(filepath: Path) -> dict:
    """Read and parse a user JSON file asynchronously."""
    async with aiofiles.open(filepath, mode="r", encoding="utf-8") as f:
        content = await f.read()
    return json.loads(content)

async def backup_users_concurrently(output_dir: Path) -> List[Path]:
    """Write all users to files *concurrently*."""
    output_dir.mkdir(exist_ok=True)
    tasks = [write_user_json(user, output_dir) for user in users_data]
    return await asyncio.gather(*tasks)
```

## 4. Controlled error handling with `asyncio.gather`

- **Problem:** Failures in one task cancel others by default.
- **Solution:** Pass `return_exceptions=True` to `asyncio.gather()` to collect successes and failures separately.

```python
async def safe_fetch(url: str) -> Dict:
    """Fetch that might fail."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            return await resp.json()

async def fetch_with_error_handling(urls: List[str]) -> List:
    """Handle errors gracefully - continue even if some fail."""
    tasks = [safe_fetch(url) for url in urls]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    successes = [r for r in results if not isinstance(r, Exception)]
    failures = [r for r in results if isinstance(r, Exception)]
    
    print(f"✅ {len(successes)} succeeded, ❌ {len(failures)} failed")
    return successes
```

## 5. Rate limiting with semaphores

- **Problem:** You are throttling against third-party APIs or want to avoid overwhelming an endpoint.
- **Solution:** Wrap each request within an `asyncio.Semaphore` context to cap concurrency.

```python
async def fetch_with_limit(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> Dict:
    """Fetch with concurrency control."""
    async with semaphore:  # Only N concurrent requests
        async with session.get(url) as resp:
            return await resp.json()

async def fetch_rate_limited(urls: List[str], max_concurrent: int = 5) -> List[Dict]:
    """Limit concurrent requests to avoid overwhelming servers."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_with_limit(session, url, semaphore) for url in urls]
        return await asyncio.gather(*tasks)
```

## 6. Timeout control with `asyncio.wait_for`

- **Problem:** Requests might hang indefinitely.
- **Solution:** Wrap fetches with `asyncio.wait_for()` and handle `asyncio.TimeoutError` to recover.

```python
async def fetch_with_timeout(url: str, timeout_secs: float = 5.0) -> Dict:
    """Fetch with timeout - raises TimeoutError if too slow."""
    try:
        async with aiohttp.ClientSession() as session:
            return await asyncio.wait_for(
                fetch_json(session, url),
                timeout=timeout_secs
            )
    except asyncio.TimeoutError:
        print(f"⏱️ {url} timed out after {timeout_secs}s")
        return {}
```

## 7. Background, fire-and-forget tasks

- **Problem:** Some work should continue while you proceed with other logic.
- **Solution:** Use `asyncio.create_task()` to start background work and collect results later with `asyncio.gather()`.

```python
async def process_item(item: Dict) -> None:
    """Simulate processing work."""
    await asyncio.sleep(1)
    print(f"Processed: {item['name']}")

async def main_with_background_tasks():
    """Start tasks and continue without waiting."""
    items = [{"name": f"Item-{i}"} for i in range(5)]
    
    tasks = [asyncio.create_task(process_item(item)) for item in items]
    
    print("All tasks started, continuing main work...")
    await asyncio.sleep(0.5)
    print("Main work done, now waiting for background tasks...")
    
    await asyncio.gather(*tasks)
```

## 8. Progress tracking with `tqdm`

- **Problem:** Long-running async work needs visibility in a CLI.
- **Solution:** Use `tqdm.asyncio.gather` to wrap `asyncio.gather()` and display a live progress bar.

```python
from tqdm.asyncio import tqdm

async def process_with_progress(items: List[Dict]) -> List:
    """Show progress bar for async operations."""
    tasks = [process_item(item) for item in items]
    
    return await tqdm.gather(*tasks, desc="Processing items")
```

## 9. Retry logic with `tenacity`

- **Problem:** Intermittent network failures should trigger retries with exponential backoff.
- **Solution:** Decorate coroutines with `tenacity.retry` and configure stop/wait rules plus exception filters.

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10),
    retry=retry_if_exception_type(aiohttp.ClientError)
)
async def fetch_with_retry(url: str) -> Dict:
    """Auto-retry on network errors with exponential backoff."""
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            resp.raise_for_status()
            return await resp.json()
```

## 10. Async context managers

- **Problem:** Async resources need deterministic setup and teardown.
- **Solution:** Implement `__aenter__` and `__aexit__` alongside helper methods.

```python
class AsyncDatabaseConnection:
    """Example async context manager for DB connections."""
    
    def __init__(self, connection_string: str):
        self.conn_str = connection_string
        self.connection = None
    
    async def __aenter__(self):
        """Open connection when entering context."""
        print(f"🔌 Connecting to {self.conn_str}")
        await asyncio.sleep(0.1)  # Simulate connection
        self.connection = "mock_connection"
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Close connection when exiting context."""
        print("🔌 Closing connection")
        await asyncio.sleep(0.1)  # Simulate cleanup
        self.connection = None
    
    async def query(self, sql: str) -> List[Dict]:
        """Execute a query."""
        await asyncio.sleep(0.2)
        return [{"id": 1, "result": "data"}]

async def use_async_context_manager():
    async with AsyncDatabaseConnection("db://localhost") as db:
        results = await db.query("SELECT * FROM users")
        print(f"Got {len(results)} results")
```

## 11. Async generators for streaming data

- **Problem:** You want to consume paginated APIs without buffering everything.
- **Solution:** Write async generators (coroutines that `yield`) and `async for` loops to process streams lazily.

```python
async def fetch_paginated_data(base_url: str, max_pages: int = 5):
    """Yield results page by page without loading all into memory."""
    async with aiohttp.ClientSession() as session:
        for page in range(1, max_pages + 1):
            url = f"{base_url}?page={page}"
            async with session.get(url) as resp:
                data = await resp.json()
                yield data
            
            await asyncio.sleep(0.1)

async def consume_paginated():
    async for page_data in fetch_paginated_data("https://api.example.com/items"):
        print(f"Processing page with {len(page_data)} items")
```

## 12. Queue-based worker pattern

- **Problem:** You want a bounded buffer and multiple workers coordinating via a queue.
- **Solution:** Use `asyncio.Queue`, producers, and consumers that signal completion with sentinel values.

```python
async def producer(queue: asyncio.Queue, n_items: int):
    """Produce items and put them in queue."""
    for i in range(n_items):
        await queue.put(f"item-{i}")
        await asyncio.sleep(0.1)
    
    await queue.put(None)

async def consumer(queue: asyncio.Queue, consumer_id: int):
    """Consume items from queue until None received."""
    while True:
        item = await queue.get()
        
        if item is None:
            queue.task_done()
            await queue.put(None)
            break
        
        print(f"Consumer-{consumer_id} processing {item}")
        await asyncio.sleep(0.2)
        queue.task_done()

async def run_producer_consumer():
    """Classic producer-consumer pattern with async queue."""
    queue = asyncio.Queue(maxsize=10)
    
    tasks = [
        asyncio.create_task(producer(queue, 20)),
        asyncio.create_task(consumer(queue, 1)),
        asyncio.create_task(consumer(queue, 2)),
        asyncio.create_task(consumer(queue, 3))
    ]
    
    await asyncio.gather(*tasks)
```

## 13. Entry point for async scripts

- **Problem:** How to bootstrap async code from a synchronous CLI script.
- **Solution:** Wrap your application logic in `async def` and execute it with `asyncio.run()` when the module is run as a script.

```python
async def my_async_app():
    """Main async application."""
    results = await fetch_multiple_urls([
        "https://api.example.com/1",
        "https://api.example.com/2"
    ])
    return results

if __name__ == "__main__":
    results = asyncio.run(my_async_app())
    print(f"Got {len(results)} results")
```

## 14. Real-world scraping example

- **Problem:** You scrape multiple articles with rate limiting, timeouts, and retries.
- **Solution:** Combine semaphores, `aiohttp` timeouts, and dataclasses for structured results.

```python
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Article:
    title: str
    url: str
    fetched_at: datetime

async def scrape_article(session: aiohttp.ClientSession, url: str, semaphore: asyncio.Semaphore) -> Article:
    """Scrape single article with rate limiting."""
    async with semaphore:
        try:
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                html = await resp.text()
                title = f"Article from {url}"
                return Article(title=title, url=url, fetched_at=datetime.now())
        except Exception as e:
            print(f"❌ Failed to scrape {url}: {e}")
            return None

async def scrape_website(urls: List[str], max_concurrent: int = 5) -> List[Article]:
    """Scrape multiple URLs with rate limiting, timeout, and error handling."""
    semaphore = asyncio.Semaphore(max_concurrent)
    
    async with aiohttp.ClientSession() as session:
        tasks = [scrape_article(session, url, semaphore) for url in urls]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        articles = [r for r in results if isinstance(r, Article)]
        return articles
```

## Quick decision tree

Use this checklist when choosing the right async tool for each kind of work.

```text
WHICH PATTERN TO USE?

├─ Sync I/O function (requests, time.sleep)?
│  └─ Use: asyncio.to_thread()
│
├─ CPU-intensive work (heavy computation)?
│  └─ Use: ProcessPoolExecutor + run_in_executor()
│
├─ HTTP requests?
│  ├─ Few requests → Use: aiohttp with asyncio.gather()
│  └─ Many requests → Use: aiohttp + Semaphore (rate limiting)
│
├─ File operations?
│  └─ Use: aiofiles
│
├─ Need error handling?
│  └─ Use: asyncio.gather(..., return_exceptions=True)
│
├─ Need timeouts?
│  └─ Use: asyncio.wait_for()
│
├─ Background tasks?
│  └─ Use: asyncio.create_task()
│
├─ Streaming/pagination?
│  └─ Use: async generator (async def + yield)
│
├─ Worker queue pattern?
│  └─ Use: asyncio.Queue
│
└─ Need retry logic?
   └─ Use: tenacity decorator
```
