from typing import Any

import httpx

from src.utilities.model_config import RemoteModel
from src.utilities.openrouter.types import OpenRouterClientPaths, RequestMethods
from src.utilities.openrouter.utils import _validate_response, get_openrouter_api_keys

CONTENT_TYPE: str = "application/json"
USER_AGENT: str = "openrouter_sdk/0.0.1"


# ==============================================================================
# ================================ SYNC CLIENT =================================
# ==============================================================================
class OpenRouterClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = OpenRouterClientPaths.BASE_URL.value,
        default_model: str = RemoteModel.GEMINI_2_0_FLASH_001.value,
        timeout: int = 20,
    ) -> None:
        self.base_url = base_url
        self.default_model = default_model
        self.timeout = timeout
        self._client = httpx.Client(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                "Authorization": f"Bearer {get_openrouter_api_keys(api_key)}",
                "Content-Type": CONTENT_TYPE,
                "user-agent": USER_AGENT,
            },
        )

        # Import and initialize resources here to avoid circular imports
        from src.utilities.openrouter.resources.chat import (
            ChatSyncResource,
            CompletionsSyncResource,
        )
        from src.utilities.openrouter.resources.embeddings import EmbeddingsSyncResource
        from src.utilities.openrouter.resources.models import ModelsSyncResource
        from src.utilities.openrouter.resources.others import (
            AnalyticsSyncResource,
            CreditsSyncResource,
            GenerationMetadataSyncResource,
            ProvidersSyncResource,
            SupportedParametersSyncResource,
        )

        self.chat = ChatSyncResource(client=self)
        self.completions = CompletionsSyncResource(client=self)
        self.embeddings = EmbeddingsSyncResource(client=self)
        self.models = ModelsSyncResource(client=self)
        self.generations = GenerationMetadataSyncResource(client=self)
        self.analytics = AnalyticsSyncResource(client=self)
        self.parameters = SupportedParametersSyncResource(client=self)
        self.providers = ProvidersSyncResource(client=self)
        self.credits = CreditsSyncResource(client=self)

    def close(self) -> None:
        """Close the HTTP client session."""
        self._client.close()

    # Context manager
    def __enter__(self) -> "OpenRouterClient":
        return self

    def __exit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        self.close()

    def _request(self, method: RequestMethods, path: str, **kwargs: Any) -> Any:
        """Internal method to make HTTP requests."""
        response = self._client.request(method, path, **kwargs)
        return _validate_response(self, response)


# ==============================================================================
# ================================ ASYNC CLIENT ================================
# ==============================================================================


class AsyncOpenRouterClient:
    def __init__(
        self,
        api_key: str | None = None,
        base_url: str = OpenRouterClientPaths.BASE_URL.value,
        default_model: str = RemoteModel.GEMINI_2_0_FLASH_001.value,
        timeout: int = 20,
    ) -> None:
        self.base_url = base_url
        self.default_model = default_model
        self.timeout = timeout
        self._client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            headers={
                "Authorization": f"Bearer {get_openrouter_api_keys(api_key)}",
                "Content-Type": CONTENT_TYPE,
                "user-agent": USER_AGENT,
            },
        )

        # Import and initialize resources here to avoid circular imports
        from src.utilities.openrouter.resources.chat import (
            ChatAsyncResource,
            CompletionsAsyncResource,
        )
        from src.utilities.openrouter.resources.embeddings import (
            EmbeddingsAsyncResource,
        )
        from src.utilities.openrouter.resources.models import ModelsAsyncResource
        from src.utilities.openrouter.resources.others import (
            AnalyticsAsyncResource,
            CreditsAsyncResource,
            GenerationMetadataAsyncResource,
            ProvidersAsyncResource,
            SupportedParametersAsyncResource,
        )

        self.chat = ChatAsyncResource(client=self)
        self.acompletions = CompletionsAsyncResource(client=self)
        self.aembeddings = EmbeddingsAsyncResource(client=self)
        self.models = ModelsAsyncResource(client=self)
        self.generations = GenerationMetadataAsyncResource(client=self)
        self.parameters = SupportedParametersAsyncResource(client=self)
        self.analytics = AnalyticsAsyncResource(client=self)
        self.providers = ProvidersAsyncResource(client=self)
        self.credits = CreditsAsyncResource(client=self)

    async def aclose(self) -> None:
        """Close the HTTP client session."""
        await self._client.aclose()

    # Context manager
    async def __aenter__(self) -> "AsyncOpenRouterClient":
        return self

    async def __aexit__(self, exc_type: Any, exc_value: Any, traceback: Any) -> None:
        await self.aclose()

    async def _arequest(self, method: RequestMethods, path: str, **kwargs: Any) -> Any:
        """Internal method to make asynchronous HTTP requests."""
        response = await self._client.request(method, path, **kwargs)
        return _validate_response(self, response)
