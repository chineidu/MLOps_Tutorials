"""A thread-safe implementation of the Singleton design pattern using a metaclass.

Not vulnerable to multiple instantiations in multi-threaded scenarios and generally not 
recommended due to complexity.
"""

import threading
from typing import Any


class Singleton(type):
    _instances: dict[type, Any] = {}
    _locks: dict[type, threading.Lock] = {}
    # protects _locks map creation
    _global_lock = threading.Lock()  

    def __call__(cls, *args, **kwargs) -> Any:
        """Control the instantiation of singleton classes in a thread-safe manner."""
        # Fast path: already created
        if cls in cls._instances:
            return cls._instances[cls]

        # Ensure a per-class lock exists
        with cls._global_lock:
            lock = cls._locks.setdefault(cls, threading.Lock())

        # Double-checked locking: only one thread creates the instance
        with lock:
            if cls not in cls._instances:
                print(f"Creating instance of {cls.__name__}")
                instance = super().__call__(*args, **kwargs)  # calls __init__ once
                cls._instances[cls] = instance

        return cls._instances[cls]
