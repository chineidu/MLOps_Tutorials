# ThreadPoolExecutor Patterns And Best Practices

Covers common patterns for concurrent execution with threads in Python

```py
from concurrent.futures import ThreadPoolExecutor, as_completed, wait, FIRST_COMPLETED
from typing import list, Callable, Any, Dict
import time
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')
logger = logging.getLogger(__name__)
```

## PATTERN 1: Basic Context Manager

```py
def basic_executor():
    """Use context manager for automatic cleanup"""
    def task(n):
        time.sleep(0.1)
        return n * 2
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit returns a Future object immediately
        futures = [executor.submit(task, i) for i in range(10)]
        
        # Get results (blocks until complete)
        results = [f.result() for f in futures]
    
    return results

```

## PATTERN 2: Map - Simple Parallel Execution

- Map maintains order of inputs

```py
def executor_map():
    """Use map() for simple cases - maintains order"""
    def process_item(item):
        time.sleep(0.1)
        return item.upper()
    
    items = ['apple', 'banana', 'cherry', 'date']
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        # map() returns results in original order
        results = list(executor.map(process_item, items))
    
    return results

```

## PATTERN 3: As Completed

- Process Results as They Finish

```py
def as_completed_pattern():
    """Process results as soon as they're available"""
    def task(n):
        time.sleep(n * 0.1)  # Variable delay
        return n * 2
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        # Submit all tasks
        future_to_input = {executor.submit(task, i): i for i in range(5)}
        # === Without saving order ===
        # futures = [executor.submit(task, i) for i in range(5)]
        
        # Process as they complete (not in submission order)
        results = []
        for future in as_completed(future_to_input):
            original_input = future_to_input[future]
            try:
                result = future.result()
                logger.info(f"Input {original_input} -> Result {result}")
                results.append(result)
            except Exception as e:
                logger.error(f"Task {original_input} failed: {e}")
        
        return results
```

## PATTERN 4: Error Handling

```py
def error_handling_pattern():
    """Proper error handling with futures"""
    def risky_task(n):
        if n == 3:
            raise ValueError(f"Task {n} failed!")
        return n * 2
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(risky_task, i) for i in range(5)]
        
        results = []
        errors = []
        
        for i, future in enumerate(futures):
            try:
                result = future.result(timeout=5)  # Add timeout
                results.append(result)
            except ValueError as e:
                logger.error(f"Task {i} raised ValueError: {e}")
                errors.append((i, e))
            except TimeoutError:
                logger.error(f"Task {i} timed out")
                errors.append((i, "timeout"))
            except Exception as e:
                logger.error(f"Task {i} unexpected error: {e}")
                errors.append((i, e))
        
        return results, errors
```

## PATTERN 5: Timeout Handling

```py
def timeout_pattern():
    """Handle timeouts gracefully"""
    def slow_task(n):
        time.sleep(n)
        return n * 2
    
    with ThreadPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(slow_task, i) for i in [0.1, 0.2, 5.0]]
        
        results = []
        for i, future in enumerate(futures):
            try:
                result = future.result(timeout=1.0)
                results.append(result)
            except TimeoutError:
                logger.warning(f"Task {i} exceeded timeout")
                future.cancel()  # Attempt to cancel (may not work if running)
                results.append(None)
        
        return results
```

## PATTERN 6: Wait with Different Strategies

```py
def wait_strategies():
    """Use wait() for more control over completion"""
    def task(n):
        time.sleep(n * 0.1)
        return n * 2
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = [executor.submit(task, i) for i in range(5)]
        
        # Wait for all to complete (default)
        done, pending = wait(futures)
        logger.info(f"All complete: {len(done)} done, {len(pending)} pending")
        
        # Wait for first completion
        futures2 = [executor.submit(task, i) for i in range(5)]
        done, pending = wait(futures2, return_when=FIRST_COMPLETED)
        logger.info(f"First complete: {len(done)} done, {len(pending)} pending")
        
        # Wait with timeout
        futures3 = [executor.submit(task, i) for i in range(5)]
        done, pending = wait(futures3, timeout=0.3)
        logger.info(f"After timeout: {len(done)} done, {len(pending)} pending")
        
        # Cancel pending tasks
        for f in pending:
            f.cancel()
        
        return [f.result() for f in done if f.done()]
```

## PATTERN 7: Chaining with Callbacks

```py
def callback_pattern():
    """Add callbacks to futures"""
    results = []
    
    def task(n):
        time.sleep(0.1)
        return n * 2
    
    def callback(future):
        try:
            result = future.result()
            results.append(result)
            logger.info(f"Callback received result: {result}")
        except Exception as e:
            logger.error(f"Callback error: {e}")
    
    with ThreadPoolExecutor(max_workers=4) as executor:
        futures = []
        for i in range(5):
            future = executor.submit(task, i)
            future.add_done_callback(callback)
            futures.append(future)
        
        # Wait for all to complete
        wait(futures)
    
    return results
```

## PATTERN 8: Batching

```py
def batched_execution(items: list[Any], batch_size: int = 10):
    """Process items in batches to control concurrency"""
    def process(item):
        time.sleep(0.1)
        return item * 2
    
    all_results = []
    
    with ThreadPoolExecutor(max_workers=batch_size) as executor:
        for i in range(0, len(items), batch_size):
            batch = items[i:i + batch_size]
            futures = [executor.submit(process, item) for item in batch]
            batch_results = [f.result() for f in futures]
            all_results.extend(batch_results)
            logger.info(f"Completed batch {i//batch_size + 1}")
    
    return all_results
```

## PATTERN 9: Reusable Executor

```py
class TaskProcessor:
    """Reusable executor for long-running applications"""
    
    def __init__(self, max_workers=4):
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
    
    def process(self, task_fn: Callable, items: list[Any]) -> list[Any]:
        """Process items using the executor"""
        futures = [self.executor.submit(task_fn, item) for item in items]
        return [f.result() for f in as_completed(futures)]
    
    def shutdown(self):
        """Clean shutdown"""
        self.executor.shutdown(wait=True)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.shutdown()
```

## PATTERN 10: Running With Async Code

```py
# 1: Running Blocking Code in Asyncio (Python 3.9+)
import asyncio

async def modern_async_blocking():
    """Python 3.9+ has built-in asyncio.to_thread()"""
    
    def blocking_io_task(n):
        # Simulating blocking I/O (database, file, legacy library)
        time.sleep(1)
        return f"Result {n}"
    
    # Run blocking function in thread pool automatically
    result = await asyncio.to_thread(blocking_io_task, 42)
    return result


# 2: Using run_in_executor for blocking operations
async def run_in_executor_basic():
    """Use run_in_executor for blocking operations"""
    
    def blocking_operation(x):
        time.sleep(1)
        return x * 2
    
    loop = asyncio.get_event_loop()
    
    # None = use default executor (ThreadPoolExecutor)
    result = await loop.run_in_executor(None, blocking_operation, 5)
    return result


# 3: Using custom executor for better control
async def run_in_executor_custom():
    """Use custom executor for better control"""
    
    def cpu_bound_task(n):
        # For CPU-bound, you'd use ProcessPoolExecutor instead
        return sum(i * i for i in range(n))
    
    loop = asyncio.get_event_loop()
    
    # Custom executor with specific max_workers
    with ThreadPoolExecutor(max_workers=4) as executor:
        result = await loop.run_in_executor(executor, cpu_bound_task, 1000000)
    
    return result


# 4: Running multiple blocking tasks concurrently
async def concurrent_blocking_tasks():
    """Run multiple blocking tasks concurrently"""
    
    def fetch_from_db(query_id):
        # Simulating database query
        time.sleep(0.5)
        return f"Data for query {query_id}"
    
    loop = asyncio.get_event_loop()
    
    # Run multiple blocking operations concurrently
    results = await asyncio.gather(
        loop.run_in_executor(None, fetch_from_db, 1),
        loop.run_in_executor(None, fetch_from_db, 2),
        loop.run_in_executor(None, fetch_from_db, 3),
    )
    
    return results
```

## KEY BEST PRACTICES

1. Use context managers (with statement) for automatic cleanup
2. ThreadPoolExecutor is for I/O-bound tasks (network, file, database)
3. For CPU-bound tasks, use ProcessPoolExecutor instead
4. Always handle exceptions from future.result()
5. Set reasonable timeouts to prevent hanging
6. Use as_completed() for processing results as they arrive
7. Use map() for simple cases where order matters
8. Limit max_workers to avoid resource exhaustion (typical: 5-20 for I/O)
9. Use locks (threading.Lock) for shared mutable state
10. Consider using asyncio for modern async I/O instead

### COMMON PITFALLS

- Don't use ThreadPoolExecutor for CPU-bound tasks (GIL limits parallelism)
- Don't forget to handle exceptions in futures
- Don't set max_workers too high (diminishing returns, resource waste)
- Don't share mutable state without synchronization
- Don't forget to call shutdown() if not using context manager
