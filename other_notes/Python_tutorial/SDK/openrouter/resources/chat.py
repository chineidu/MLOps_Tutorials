from typing import TYPE_CHECKING, Any

from src.utilities.openrouter.types import OpenRouterClientPaths, RequestMethods
from src.utilities.openrouter.utils import (
    _validate_arequest_attribute,
    _validate_base_url_attribute,
    _validate_client,
    _validate_model,
    _validate_request_attribute,
)

if TYPE_CHECKING:
    from src.utilities.openrouter.client import AsyncOpenRouterClient, OpenRouterClient

type ChatResourceClient = OpenRouterClient | AsyncOpenRouterClient
type CompletionsInput = str | list[str] | list[float] | list[list[float]]


class ChatSyncSubResource:
    """Chat resource for interacting with OpenRouter chat completions."""

    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    def create(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a new chat completion.

        Parameters
        ----------
        messages : list[dict[str, str]]
            The list of messages for the chat completion.
        model : str | None, optional
            The model to use for chat completion. If None, the client's default model is used.
        **kwargs : dict[str, Any]
            Additional keyword arguments to pass to the API.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the chat completions.
        """
        model = _validate_model(self.client, model)

        payload: dict[str, Any] = {"model": model, "messages": messages, **kwargs}
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.CHAT_COMPLETIONS.value}"
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.POST, path, json=payload)


class ChatAsyncSubResource:
    """Chat resource for interacting with OpenRouter chat completions asynchronously."""

    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    async def create(
        self,
        messages: list[dict[str, str]],
        model: str | None = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Asynchronously create a new chat completion.

        Parameters
        ----------
        messages : list[dict[str, str]]
            The list of messages for the chat completion.
        model : str | None, optional
            The model to use for chat completion. If None, the client's default model is used.
        **kwargs : dict[str, Any]
            Additional keyword arguments to pass to the API.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the chat completions.
        """
        model = _validate_model(self.client, model)

        payload: dict[str, Any] = {"model": model, "messages": messages, **kwargs}
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.CHAT_COMPLETIONS.value}"
        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )

        return await async_client._arequest(RequestMethods.POST, path, json=payload)


class CompletionsSyncResource:
    """Chat resource for interacting with OpenRouter completions."""

    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    def create(
        self,
        prompt: CompletionsInput,
        model: str | None = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a new completion.

        Parameters
        ----------
        prompt : CompletionsInput
            Single or multiple prompts for chat completion. Can be a string, list of strings, list of floats, or list of
            lists of floats.
        model : str | None, optional
            The model to use for chat completion. If None, the client's default model is used.
        **kwargs : dict[str, Any]
            Additional keyword arguments to pass to the API.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the completions.
        """
        if not isinstance(prompt, (str, list)):
            raise ValueError("Prompt must be a string or a list of strings.")

        model = _validate_model(self.client, model)

        payload: dict[str, Any] = {"model": model, "prompt": prompt, **kwargs}
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.COMPLETIONS.value}"
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.POST, path, json=payload)


class CompletionsAsyncResource:
    """Chat resource for interacting with OpenRouter completions asynchronously."""

    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    async def create(
        self,
        prompt: CompletionsInput,
        model: str | None = None,
        **kwargs: dict[str, Any],
    ) -> dict[str, Any]:
        """Create a new completion asynchronously.

        Parameters
        ----------
        prompt : CompletionsInput
            Single or multiple prompts for chat completion. Can be a string, list of strings, list of floats, or list of
            lists of floats.
        model : str | None, optional
            The model to use for chat completion. If None, the client's default model is used.
        **kwargs : dict[str, Any]
            Additional keyword arguments to pass to the API.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the completions.
        """
        if not isinstance(prompt, (str, list)):
            raise ValueError("Prompt must be a string or a list of strings.")

        model = _validate_model(self.client, model)

        payload: dict[str, Any] = {"model": model, "prompt": prompt, **kwargs}
        base_url: str = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.COMPLETIONS.value}"
        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )

        return await async_client._arequest(RequestMethods.POST, path, json=payload)


class ChatSyncResource:
    """Chat resource for interacting with OpenRouter chat completions."""

    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)
        self.completions = ChatSyncSubResource(client=self.client)


class ChatAsyncResource:
    """Chat resource for interacting with OpenRouter chat completions."""

    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)
        self.acompletions = ChatAsyncSubResource(client=self.client)
