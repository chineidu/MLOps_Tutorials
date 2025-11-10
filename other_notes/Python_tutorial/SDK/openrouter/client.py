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
            ChatResource,
            CompletionsResource,
        )
        from src.utilities.openrouter.resources.embeddings import EmbeddingsResource
        from src.utilities.openrouter.resources.models import ModelsResource
        from src.utilities.openrouter.resources.others import (
            CreditsResource,
            GenerationMetadataResource,
            ProvidersResource,
            SupportedParametersResource,
        )

        self.chat = ChatResource(client=self)
        self._completions = CompletionsResource(client=self)
        self.embeddings = EmbeddingsResource(client=self)
        self.models = ModelsResource(client=self)
        self._generation_metadata = GenerationMetadataResource(client=self)
        self.parameters = SupportedParametersResource(client=self)
        self._providers = ProvidersResource(client=self)
        self._credits = CreditsResource(client=self)

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

    def completions(
        self,
        prompt: str | list[str],
        model: str | None = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Get completions from OpenRouter API.

        Parameters
        ----------
        prompt : str | list[str]
            The prompt(s) for the completion.
        model : str | None, optional
            The model to use for completions. If None, the client's default model is used.
        **kwargs : dict[str, Any]
            Additional keyword arguments to pass to the API.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the completions.
        """
        return self._completions.completions(prompt=prompt, model=model, **kwargs)

    def generation_metadata(self, id: str) -> dict[str, Any]:
        """Get generation metadata resource.

        Parameters
        ----------
        id : str
            The ID of the generation to retrieve metadata for.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the generation metadata.
        """
        return self._generation_metadata.get_metadata(id=id)

    def list_providers(self) -> dict[str, Any]:
        """List available providers from OpenRouter API."""
        return self._providers.list_providers()

    def get_credits_data(self) -> dict[str, Any]:
        """Get credits data from OpenRouter API."""
        return self._credits.get_credits_data()


# ==============================================================================
# ================================ ASYNC CLIENT ================================
# ==============================================================================


class AsyncOpenRouterClient:
    def __init__(
        self,
        api_key: str,
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
            ChatResource,
            CompletionsResource,
        )
        from src.utilities.openrouter.resources.embeddings import EmbeddingsResource
        from src.utilities.openrouter.resources.models import ModelsResource
        from src.utilities.openrouter.resources.others import (
            CreditsResource,
            GenerationMetadataResource,
            ProvidersResource,
            SupportedParametersResource,
        )

        self.chat = ChatResource(client=self)
        self._completions = CompletionsResource(client=self)
        self.embeddings = EmbeddingsResource(client=self)
        self.models = ModelsResource(client=self)
        self._ageneration_metadata = GenerationMetadataResource(client=self)
        self.parameters = SupportedParametersResource(client=self)
        self._providers = ProvidersResource(client=self)
        self._credits = CreditsResource(client=self)

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
        async with self._client as client:
            response = await client.request(method, path, **kwargs)

        return _validate_response(self, response)

    async def acompletions(
        self,
        prompt: str | list[str],
        model: str | None = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Get completions from OpenRouter API.

        Parameters
        ----------
        prompt : str | list[str]
            The prompt(s) for the completion.
        model : str | None, optional
            The model to use for completions. If None, the client's default model is used.
        **kwargs : dict[str, Any]
            Additional keyword arguments to pass to the API.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the completions.
        """
        return await self._completions.acompletions(
            prompt=prompt, model=model, **kwargs
        )

    async def ageneration_metadata(self, id: str) -> dict[str, Any]:
        """Get asynchronous generation metadata resource.

        Parameters
        ----------
        id : str
            The ID of the generation to retrieve metadata for.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the generation metadata.

        """
        return await self._ageneration_metadata.aget_metadata(id=id)

    async def alist_providers(self) -> dict[str, Any]:
        """Asynchronously list available providers from OpenRouter API."""
        return await self._providers.alist_providers()

    async def aget_credits_data(self) -> dict[str, Any]:
        """Asynchronously get credits data from OpenRouter API."""
        return await self._credits.aget_credits_data()
