from typing import TYPE_CHECKING, Any, Literal

from src.utilities.openrouter.types import OpenRouterClientPaths, RequestMethods
from src.utilities.openrouter.utils import (
    _validate_arequest_attribute,
    _validate_base_url_attribute,
    _validate_client,
    _validate_request_attribute,
)

if TYPE_CHECKING:
    from src.utilities.openrouter.client import AsyncOpenRouterClient, OpenRouterClient

type ChatResourceClient = OpenRouterClient | AsyncOpenRouterClient

type CategoryTypes = Literal[
    "programming",
    "roleplay",
    "marketing",
    "marketing/seo",
    "technology",
    "science",
    "translation",
    "legal",
    "finance",
    "health",
    "trivia",
    "academia",
]

type SupportedParameters = Literal[
    "tools",
    "temperature",
    "top_p",
    "top_k",
    "min_p",
    "top_a",
    "frequency_penalty",
    "presence_penalty",
    "repetition_penalty",
    "max_tokens",
    "logit_bias",
    "logprobs",
    "top_logprobs",
    "seed",
    "response_format",
    "structured_outputs",
    "stop",
    "parallel_tool_calls",
    "include_reasoning",
    "reasoning",
    "web_search_options",
    "verbosity",
]


class ModelsSyncResource:
    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    def count(self) -> dict[str, Any]:
        """Count available models from OpenRouter API."""
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.MODEL_COUNT.value}"
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.GET, path)

    def list_models(
        self,
        category: list[CategoryTypes] | None = None,
        supported_parameters: list[SupportedParameters] | None = None,
        use_rss_chat_links: bool = False,
    ) -> dict[str, Any]:
        """List available models from OpenRouter API."""
        params: dict[str, Any] = {}
        if category is not None:
            params["categories"] = ",".join(category)
        if supported_parameters is not None:
            params["supported_parameters"] = ",".join(supported_parameters)
        if use_rss_chat_links:
            params["use_rss_chat_links"] = "true"

        base_url: str = _validate_base_url_attribute(self.client)
        path: str = (
            f"{base_url}/{OpenRouterClientPaths.LIST_MODELS_AND_PROPERTIES.value}"
        )
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.GET, path, params=params)


class ModelsAsyncResource:
    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    async def acount(self) -> dict[str, Any]:
        """Asynchronously count available models from OpenRouter API."""
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.MODEL_COUNT.value}"
        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )

        return await async_client._arequest(RequestMethods.GET, path)

    async def alist_models(
        self,
        category: list[CategoryTypes] | None = None,
        supported_parameters: list[SupportedParameters] | None = None,
        use_rss_chat_links: bool = False,
    ) -> dict[str, Any]:
        """Asynchronously list available models from OpenRouter API."""
        params: dict[str, Any] = {}
        if category is not None:
            params["categories"] = ",".join(category)
        if supported_parameters is not None:
            params["supported_parameters"] = ",".join(supported_parameters)
        if use_rss_chat_links:
            params["use_rss_chat_links"] = "true"

        base_url: str = _validate_base_url_attribute(self.client)
        path: str = (
            f"{base_url}/{OpenRouterClientPaths.LIST_MODELS_AND_PROPERTIES.value}"
        )
        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )

        return await async_client._arequest(RequestMethods.GET, path, params=params)
