"""This uses the registry pattern to load different models based on a key.
Internally, it uses a singleton to ensure only one instance of each model loader exists."""

import threading
import time
from enum import Enum
from typing import Any, Protocol

type Data = dict[str, Any] | Any


class ModelInterface(Protocol):
    """Protocol defining the interface for prediction models."""

    def predict(self, data: str) -> str:
        """Make a prediction on the given data."""
        ...

    def get_model_info(self) -> dict[str, Any]:
        """Get information about the model."""
        ...


class ModelType(str, Enum):
    """Enum for different model types."""

    SENTIMENT = "sentiment"
    SUMMARIZATION = "summarization"
    TRANSLATION = "translation"


class SentimentModel:
    """Model for sentiment analysis."""

    def __init__(self) -> None:
        self._model: Any = None
        self._lock = threading.Lock()
        self._initialized = False

    def _load_model(self) -> None:
        """Load the sentiment model."""
        print("📊 Loading Sentiment Analysis model...")
        time.sleep(2)  # Simulate loading
        self._model = "sentiment_model_v2"
        print("✅ Sentiment model loaded!")

    def predict(self, data: str) -> str:
        """Analyze sentiment of the input text."""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._load_model()
                    self._initialized = True

        # Simulate sentiment analysis
        if "good" in data.lower() or "great" in data.lower():
            return "Sentiment: POSITIVE (confidence: 0.92)"
        if "bad" in data.lower() or "terrible" in data.lower():
            return "Sentiment: NEGATIVE (confidence: 0.88)"
        return "Sentiment: NEUTRAL (confidence: 0.75)"

    def get_model_info(self) -> dict[str, Any]:
        """Get information about the model."""
        return {"name": "SentimentModel", "version": "2.0", "type": "sentiment_analysis", "loaded": self._initialized}


class SummarizationModel:
    """Model for text summarization."""

    def __init__(self) -> None:
        self._model: Any = None
        self._lock = threading.Lock()
        self._initialized = False

    def _load_model(self) -> None:
        """Load the summarization model."""
        print("📝 Loading Summarization model...")
        time.sleep(3)  # Simulate loading (larger model)
        self._model = "summarization_model_t5"
        print("✅ Summarization model loaded!")

    def predict(self, data: str) -> str:
        """Summarize the input text."""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._load_model()
                    self._initialized = True

        # Simulate summarization
        words = data.split()
        summary_length = min(10, len(words) // 2)
        return f"Summary: {' '.join(words[:summary_length])}..."

    def get_model_info(self) -> dict[str, Any]:
        """Get information about the model."""
        return {"name": "SummarizationModel", "version": "1.5", "type": "text_summarization", "loaded": self._initialized}


class TranslationModel:
    """Model for language translation."""

    def __init__(self) -> None:
        self._model: Any = None
        self._lock = threading.Lock()
        self._initialized = False

    def _load_model(self) -> None:
        """Load the translation model."""
        print("🌍 Loading Translation model...")
        time.sleep(2.5)  # Simulate loading
        self._model = "translation_model_opus"
        print("✅ Translation model loaded!")

    def predict(self, data: str) -> str:
        """Translate the input text (English to Spanish simulation)."""
        if not self._initialized:
            with self._lock:
                if not self._initialized:
                    self._load_model()
                    self._initialized = True

        # Simulate translation (very basic)
        translations = {"hello": "hola", "world": "mundo", "good": "bueno", "morning": "mañana"}

        words = data.lower().split()
        translated = [translations.get(word, word) for word in words]
        return f"Translation (ES): {' '.join(translated)}"

    def get_model_info(self) -> dict[str, Any]:
        """Get information about the model."""
        return {"name": "TranslationModel", "version": "3.1", "type": "translation", "loaded": self._initialized}


class ModelRegistry:
    """Registry for managing multiple shared model instances."""

    _instances: dict[str, ModelInterface] = {}
    _lock = threading.Lock()

    # Model factory mapping
    _model_factories: dict[ModelType, type[ModelInterface]] = {
        ModelType.SENTIMENT: SentimentModel,
        ModelType.SUMMARIZATION: SummarizationModel,
        ModelType.TRANSLATION: TranslationModel,
    }

    @classmethod
    def get_model(cls, model_type: ModelType) -> ModelInterface:
        """Get or create a model instance by type."""
        model_key = model_type.value

        if model_key not in cls._instances:
            with cls._lock:
                if model_key not in cls._instances:
                    factory = cls._model_factories.get(model_type)
                    if factory is None:
                        raise ValueError(f"Unknown model type: {model_type}")
                    cls._instances[model_key] = factory()

        return cls._instances[model_key]

    @classmethod
    def get_all_models_info(cls) -> dict[str, dict[str, Any]]:
        """Get information about all loaded models."""
        return {key: model.get_model_info() for key, model in cls._instances.items()}

    @classmethod
    def is_loaded(cls, model_type: ModelType) -> bool:
        """Check if a specific model is loaded."""
        return model_type.value in cls._instances

    @classmethod
    def clear(cls) -> None:
        """Clear all cached models (useful for testing)."""
        with cls._lock:
            cls._instances.clear()
            print("🧹 All models cleared from registry")


class PredictionService:
    """Service that uses dependency injection for models."""

    def __init__(self, model: ModelInterface) -> None:
        self._model = model

    def predict(self, data: str) -> str:
        """Get prediction using the injected model."""
        return self._model.predict(data)

    def get_info(self) -> dict[str, Any]:
        """Get model information."""
        return self._model.get_model_info()


def main() -> None:
    """Demonstrate using ModelRegistry with 3 different models."""

    print("=" * 60)
    print("EXAMPLE: Using ModelRegistry with Multiple Models")
    print("=" * 60)

    # Example 1: Sentiment Analysis
    print("\n--- 1. SENTIMENT ANALYSIS ---")
    sentiment_model: ModelInterface = ModelRegistry.get_model(ModelType.SENTIMENT)
    sentiment_service = PredictionService(sentiment_model)

    texts: list[str] = ["This is a great product!", "Terrible experience, very bad", "It's okay, nothing special"]

    for text in texts:
        result = sentiment_service.predict(text)
        print(f"Input: '{text}'")
        print(f"Result: {result}\n")

    # Example 2: Text Summarization
    print("\n--- 2. TEXT SUMMARIZATION ---")
    summarization_model = ModelRegistry.get_model(ModelType.SUMMARIZATION)
    summary_service = PredictionService(summarization_model)

    long_text = (
        "Artificial intelligence and machine learning are transforming "
        "industries across the globe by enabling automation and data-driven "
        "decision making in ways never before possible in human history"
    )

    result = summary_service.predict(long_text)
    print(f"Input: '{long_text}'")
    print(f"Result: {result}\n")

    # Example 3: Translation
    print("\n--- 3. TRANSLATION ---")
    translation_model: ModelInterface = ModelRegistry.get_model(ModelType.TRANSLATION)
    translation_service = PredictionService(translation_model)

    phrases: list[str] = ["hello world", "good morning"]

    for phrase in phrases:
        result = translation_service.predict(phrase)
        print(f"Input: '{phrase}'")
        print(f"Result: {result}\n")

    # Demonstrate reusing models (no reload)
    print("\n--- 4. REUSING MODELS (No Reload) ---")
    print("Getting sentiment model again (should be instant)...")
    sentiment_model_2 = ModelRegistry.get_model(ModelType.SENTIMENT)

    # Verify it's the same instance
    print(f"Same instance? {sentiment_model is sentiment_model_2}")

    result = sentiment_model_2.predict("Another good test")
    print(f"Result: {result}\n")

    # Show all loaded models
    print("\n--- 5. ALL LOADED MODELS INFO ---")
    all_models_info: dict[str, dict[str, Any]] = ModelRegistry.get_all_models_info()
    for model_key, info in all_models_info.items():
        print(f"{model_key}: {info}")

    # Cleanup
    print("\n--- 6. CLEANUP ---")
    ModelRegistry.clear()
    print(f"Models loaded after clear: {len(ModelRegistry._instances)}")


if __name__ == "__main__":
    main()
