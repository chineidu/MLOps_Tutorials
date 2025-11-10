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
type AuthorTypes = Literal[
    "agentica-org",
    "ai21",
    "aion-labs",
    "alfredpros",
    "alibaba",
    "allenai",
    "alpindale",
    "amazon",
    "anthracite-org",
    "anthropic",
    "arcee-ai",
    "arliai",
    "baidu",
    "bytedance",
    "cohere",
    "deepcogito",
    "deepseek",
    "deepseek-ai",
    "eleutherai",
    "google",
    "gryphe",
    "ibm-granite",
    "inception",
    "inclusionai",
    "inflection",
    "kwaipilot",
    "liquid",
    "mancer",
    "meituan",
    "meta-llama",
    "microsoft",
    "minimax",
    "mistralai",
    "moonshotai",
    "morph",
    "neversleep",
    "nousresearch",
    "nvidia",
    "openai",
    "opengvlab",
    "openrouter",
    "perplexity",
    "qwen",
    "raifle",
    "relace",
    "sao10k",
    "stepfun-ai",
    "switchpoint",
    "tencent",
    "thedrummer",
    "thudm",
    "tngtech",
    "undi95",
    "venice",
    "x-ai",
    "z-ai",
]


class GenerationMetadataResource:
    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    def get_metadata(self, id: str) -> dict[str, Any]:
        """Get generation metadata from OpenRouter API.

        Parameters
        ----------
        id : str
            The ID of the generation to retrieve metadata for.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the generation metadata.
        """
        params: dict[str, Any] = {"id": id}
        base_url = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.GENERATION_METADATA.value}"
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.GET, path, params=params)

    async def aget_metadata(self, id: str) -> dict[str, Any]:
        """Get generation metadata from OpenRouter API.

        Parameters
        ----------
        id : str
            The ID of the generation to retrieve metadata for.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the generation metadata.
        """
        params: dict[str, Any] = {"id": id}
        base_url = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.GENERATION_METADATA.value}"
        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )

        return await async_client._arequest(RequestMethods.GET, path, params=params)


class SupportedParametersResource:
    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    def list_supported(self, author: AuthorTypes | str, slug: str) -> dict[str, Any]:
        """Get supported parameters from OpenRouter API.

        Parameters
        ----------
        author : AuthorTypes | str
            The author of the model.
        slug : str
            The slug of the model. i.e. "gpt-4", "gemini-embedding-001", etc.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the generation metadata.
        """
        base_url = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.MODEL_SUPPORTED_PARAMETERS.value}/{author}/{slug}"
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.GET, path)

    async def alist_supported(
        self, author: AuthorTypes | str, slug: str
    ) -> dict[str, Any]:
        """Asynchronously get supported parameters from OpenRouter API.

        Parameters
        ----------
        author : AuthorTypes | str
            The author of the model.
        slug : str
            The slug of the model. i.e. "gpt-4", "gemini-embedding-001", etc.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the generation metadata.
        """
        base_url = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.MODEL_SUPPORTED_PARAMETERS.value}/{author}/{slug}"
        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )

        return await async_client._arequest(RequestMethods.GET, path)


class ProvidersResource:
    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    def list_providers(self) -> dict[str, Any]:
        """List available providers from OpenRouter API."""
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.LIST_ALL_PROVIDERS.value}"
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.GET, path)

    async def alist_providers(self) -> dict[str, Any]:
        """Asynchronously list available providers from OpenRouter API."""
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.LIST_ALL_PROVIDERS.value}"
        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )

        return await async_client._arequest(RequestMethods.GET, path)


class AnalyticsResource:
    """Analytics resource for OpenRouter API.

    NOTE
    ----
    This resource requires `provisioning keys` (special permissions) to access
    """

    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    def user_activity(self) -> dict[str, Any]:
        """Get user activity from OpenRouter API."""
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.USER_ACTIVITY.value}"
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.GET, path)

    async def alist_providers(self) -> dict[str, Any]:
        """Asynchronously list available providers from OpenRouter API."""
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.LIST_ALL_PROVIDERS.value}"
        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )

        return await async_client._arequest(RequestMethods.GET, path)


class CreditsResource:
    """Credits resource for OpenRouter API."""

    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    def get_credits_data(self) -> dict[str, Any]:
        """Get the total credits and usage from OpenRouter API."""
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.REMAINING_CREDITS.value}"
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.GET, path)

    async def aget_credits_data(self) -> dict[str, Any]:
        """Asynchronously get the total credits and usage from OpenRouter API."""
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.REMAINING_CREDITS.value}"
        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )

        return await async_client._arequest(RequestMethods.GET, path)
