# Decorators In Python Template

- Decorators are a powerful feature in Python that allow you to modify the behavior of functions or classes. They are often used for logging, access control, instrumentation, and caching.

- This file provides clean, reusable templates for creating decorators
with proper handling of function signatures, docstrings, and various use cases.

## Tables of Contents

<!-- TOC -->

- [Decorators In Python Template](#decorators-in-python-template)
  - [Tables of Contents](#tables-of-contents)
  - [Templates](#templates)
    - [TEMPLATE 1: Basic Decorator no arguments](#template-1-basic-decorator-no-arguments)
    - [TEMPLATE 2: Decorator with Arguments](#template-2-decorator-with-arguments)
    - [TEMPLATE 2B: Async Decorator with Arguments handles sync/async functions](#template-2b-async-decorator-with-arguments-handles-syncasync-functions)
    - [TEMPLATE 3: Flexible Decorator with or without arguments](#template-3-flexible-decorator-with-or-without-arguments)
    - [TEMPLATE 4: Class-based Decorator](#template-4-class-based-decorator)
  - [PRACTICAL EXAMPLES](#practical-examples)

<!-- /TOC -->

## Templates

### TEMPLATE 1: Basic Decorator (no arguments)

```py

from functools import wraps
from typing import Callable, TypeVar, ParamSpec, Any
import time
import logging

# Type variables for better type hints
P = ParamSpec('P')
R = TypeVar('R')

# Configure logging
logger = logging.getLogger(__name__)


def simple_decorator(func: Callable[P, R]) -> Callable[P, R]:
    """
    Basic decorator template without arguments.

    Usage:
        @simple_decorator
        def my_function():
            pass
    """

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        # Pre-execution logic
        print(f"Calling {func.__name__}")

        # Execute the function
        result = func(*args, **kwargs)

        # Post-execution logic
        print(f"Finished {func.__name__}")

        return result

    return wrapper

```

### TEMPLATE 2: Decorator with Arguments

```py

def decorator_with_args(arg1: str, arg2: int = 10) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator template that accepts arguments.

    Usage:
        @decorator_with_args("test", arg2=5)
        def my_function():
            pass
    """

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Use decorator arguments
            print(f"Decorator args: {arg1}, {arg2}")

            # Execute the function
            result = func(*args, **kwargs)

            return result

        return wrapper

    return decorator

```

### TEMPLATE 2B: Async Decorator with Arguments (handles sync/async functions)

```py
def async_decorator_with_args(arg1: str, arg2: int = 10) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """
    Decorator template for async functions that accepts arguments.
    Can handle both sync and async functions automatically.
    
    Usage:
        @async_decorator_with_args("test", arg2=5)
        async def my_async_function():
            pass
        
        @async_decorator_with_args("test")
        def my_sync_function():
            pass
    """
    import asyncio
    from inspect import iscoroutinefunction
    
    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        if iscoroutinefunction(func):
            @wraps(func)
            async def async_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                print(f"Async decorator args: {arg1}, {arg2}")
                result = await func(*args, **kwargs)
                return result
            return async_wrapper  # type: ignore
        else:
            @wraps(func)
            def sync_wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
                print(f"Sync decorator args: {arg1}, {arg2}")
                result = func(*args, **kwargs)
                return result
            return sync_wrapper  # type: ignore
    
    return decorator
```

### TEMPLATE 3: Flexible Decorator (with or without arguments)

```py
def flexible_decorator(func: Callable[P, R] | None = None, *, option: str = "default") -> Callable:
    """
    Decorator that can be used with or without arguments.

    Usage:
        @flexible_decorator
        def func1():
            pass

        @flexible_decorator(option="custom")
        def func2():
            pass
    """

    def decorator(f: Callable[P, R]) -> Callable[P, R]:
        @wraps(f)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"Option: {option}")
            result = f(*args, **kwargs)
            return result

        return wrapper

    if func is None:
        # Called with arguments: @flexible_decorator(option="custom")
        return decorator
    # Called without arguments: @flexible_decorator
    return decorator(func)
```

### TEMPLATE 4: Class-based Decorator

```py

class ClassDecorator:
    """
    Class-based decorator template.

    Usage:
        @ClassDecorator(param="value")
        def my_function():
            pass
    """

    def __init__(self, param: str = "default"):
        self.param = param

    def __call__(self, func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            print(f"Class decorator with param: {self.param}")
            result = func(*args, **kwargs)
            return result

        return wrapper

```

## PRACTICAL EXAMPLES

```py

def timer(func: Callable[P, R]) -> Callable[P, R]:
    """Measure execution time of a function."""

    @wraps(func)
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        logger.info(f"{func.__name__} took {end_time - start_time:.4f} seconds")
        return result

    return wrapper


def retry(max_attempts: int = 3, delay: float = 1.0) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Retry a function on failure."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            last_exception = None

            for attempt in range(max_attempts):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_exception = e
                    logger.warning(f"Attempt {attempt + 1} failed: {e}")
                    if attempt < max_attempts - 1:
                        time.sleep(delay)

            raise last_exception

        return wrapper

    return decorator


def validate_types(**type_checks: type) -> Callable[[Callable[P, R]], Callable[P, R]]:
    """Validate argument types at runtime."""

    def decorator(func: Callable[P, R]) -> Callable[P, R]:
        @wraps(func)
        def wrapper(*args: P.args, **kwargs: P.kwargs) -> R:
            # Get function signature
            import inspect

            sig = inspect.signature(func)
            bound = sig.bind(*args, **kwargs)
            bound.apply_defaults()

            # Validate types
            for param_name, expected_type in type_checks.items():
                if param_name in bound.arguments:
                    value = bound.arguments[param_name]
                    if not isinstance(value, expected_type):
                        raise TypeError(
                            f"{func.__name__}() argument '{param_name}' must be "
                            f"{expected_type.__name__}, not {type(value).__name__}"
                        )

            return func(*args, **kwargs)

        return wrapper

    return decorator


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

if __name__ == "__main__":
    # Example 1: Simple decorator
    @simple_decorator
    def greet(name: str) -> str:
        return f"Hello, {name}!"

    print(greet("Alice"))

    # Example 2: Decorator with arguments
    @decorator_with_args("custom", arg2=20)
    def calculate(x: int, y: int) -> int:
        return x + y

    print(calculate(5, 3))

    # Example 3: Timer decorator
    @timer
    def slow_function():
        time.sleep(0.1)
        return "Done"

    slow_function()

    # Example 4: Retry decorator
    @retry(max_attempts=3, delay=0.5)
    def unreliable_operation():
        import random

        if random.random() < 0.7:
            raise ValueError("Random failure")
        return "Success"

    # Example 5: Type validation
    @validate_types(name=str, age=int)
    def create_user(name: str, age: int) -> dict:
        return {"name": name, "age": age}

    print(create_user("Bob", 30))

```
