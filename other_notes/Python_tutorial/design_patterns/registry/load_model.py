"""This uses the registry pattern to load different models based on a key.
Internally, it uses a singleton to ensure only one instance of each model loader exists."""

import threading
import time
from typing import Any, Protocol

type Data = dict[str, Any] | Any


# ========================================================
# ======================= PROTOCOL =======================
# ========================================================
class ModelInterface(Protocol):
    """Protocol defining the interfaces for prediction models."""

    def predict(self, data: Data) -> Any:
        """Make a prediction on the given data."""
        ...


class ModelLoader:
    """Thread-safe loader with lazy initialiation."""

    def __init__(self) -> None:
        self._model: Any = None
        self._lock: threading.Lock = threading.Lock()
        self._initialized: bool = False

    def load(self) -> None:
        """Load the model if not already loaded."""
        if self._initialized:
            return

        with self._lock:
            if not self._model and not self._initialized:
                # Replace this line with the actual model
                # e.g., loading a machine learning model from disk
                # self._model = load_model_from_disk(model_path="path/to/model")
                print("Loading model...")
                time.sleep(2)  # Simulate time-consuming model loading
                self._model = "the_loaded_model"
                self._initialized = True
                print("Model loaded successfully!")

    def predict(self, data: Data) -> Any:
        """Make a prediction using the loaded model."""
        if not self._initialized:
            raise RuntimeError("Model not loaded. Call load() first.")

        # Replace this with actual prediction logic
        return f"Prediction result for {data} using {self._model}"

    def is_ready(self) -> bool:
        """Check if the model is loaded."""
        return self._initialized

    def unload(self) -> None:
        """Unload the model."""
        with self._lock:
            if self._initialized:
                print("Unloading model...")
                del self._model
                self._model = None
                self._initialized = False
                print("Model unloaded successfully!")


class PredictionService:
    def __init__(self, model: ModelInterface) -> None:
        self._model = model

    def predict(self, data: Data) -> Any:
        """Get prediction from the injected model."""
        return self._model.predict(data)

    def batch_predict(self, data_list: list[Data]) -> list[Any]:
        """Get batch predictions from the injected model."""
        return [self._model.predict(data) for data in data_list]


# Extras
def thread_task(data: str, model_loader: ModelLoader) -> None:
    """Task that each thread will execute."""

    thread_name: str = threading.current_thread().name
    print(f"{thread_name}: Starting...")

    # Each thread will try to load the model (but only one will actually load it)
    model_loader.load()

    # Create a service and make prediction
    service = PredictionService(model_loader)
    result = service.predict(data)
    print(f"{thread_name}: {result}")


# Example usage
if __name__ == "__main__":
    # Ex 1: Simple model loading and prediction
    print("=== Example 1: Simple model loading ===")
    model_1 = ModelLoader()
    model_1.load()
    service_1 = PredictionService(model_1)
    print(service_1.predict("sample_data_1"))

    print()
    print("=== Example 2: Multi-threaded model loading ===")
    shared_model_loader = ModelLoader()

    # Create 3 threads that will all try to use the same model loader
    threads = []
    thread_data: list[tuple[str, str]] = [
        ("data_from_thread_1", "Thread 1 data"),
        ("data_from_thread_2", "Thread 2 data"),
        ("data_from_thread_3", "Thread 3 data"),
    ]

    print("Starting 3 threads that will share the same model loader...")

    # Start all threads
    for _, (_data_key, data_value) in enumerate(thread_data, 1):
        thread = threading.Thread(target=thread_task, args=(data_value, shared_model_loader))
        threads.append(thread)
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    print("\nAll threads completed!\n")

    # Clean up
    shared_model_loader.unload()
    # Check if model is unloaded
    print(f"Model is ready: {shared_model_loader.is_ready()}")
