import threading
import time
from typing import Any


class Singleton(type):
    _instances: dict[type, Any] = {}
    _lock: threading.Lock = threading.Lock()

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Control the instantiation of singleton classes."""
        if cls not in cls._instances:
            with cls._lock:
                # Double-checked locking
                if cls not in cls._instances:
                    print(f"Creating instance of {cls.__name__}")
                    cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


class ModelLoader(metaclass=Singleton):
    """Lazy-loaded singleton model loader."""
    def __init__(self) -> None:
        self._loaded: bool = False
        self._model = None
    
    def load_model(self) -> None:
        """Simulate loading a large model."""
        if not self._loaded:
            print("Loading large model...")
            # Simulate time-consuming model loading
            time.sleep(3)  
            self._loaded = True

    def predict(self, data: str) -> str:
        """Simulate a prediction."""
        if not self._loaded:
            raise RuntimeError("Model not loaded. Call load_model() first.")
        # Simulate prediction
        return f"Prediction for {data}"


def predict(data: str, model: ModelLoader) -> str:
    """Get prediction from the singleton ModelLoader instance."""
    return model.predict(data)


def main() -> None:
    """Demonstrate the singleton behavior of ModelLoader class."""
    # The model will only be loaded once and reused thereafter.
    model = ModelLoader()
    model.load_model()
    predictions: list[str] = [predict(f"data_{i}", model) for i in range(5)]

    for pred in predictions:
        print(pred)


if __name__ == "__main__":
    main()
