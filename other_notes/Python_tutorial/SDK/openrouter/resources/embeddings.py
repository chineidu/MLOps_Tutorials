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
type EmbeddingInput = str | list[str] | list[float] | list[list[float]]


class EmbeddingsSyncResource:
    """Embeddings resource for interacting with OpenRouter embeddings.""" ""

    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    def create(
        self, input: EmbeddingInput, model: str | None = None, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """Create embeddings from OpenRouter API.

        Parameters
        ----------
        input : EmbeddingInput
            The input text(s) to embed. Can be a single string, a list of strings, floats, or a list of lists of floats.
        model : str | None, optional
            The model to use for embeddings. If None, the client's default model is used.
        **kwargs : dict[str, Any]
            Additional keyword arguments to pass to the API.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the embeddings.
        """
        if not isinstance(input, (str, list)):
            raise ValueError("Input must be a string or a list of strings.")

        model = _validate_model(self.client, model)

        payload: dict[str, Any] = {"model": model, "input": input, **kwargs}
        base_url = _validate_base_url_attribute(self.client)
        path: str = f"{base_url}/{OpenRouterClientPaths.EMBEDDINGS.value}"
        sync_client: "OpenRouterClient" = _validate_request_attribute(self.client)

        return sync_client._request(RequestMethods.POST, path, json=payload)


class EmbeddingsAsyncResource:
    def __init__(self, client: ChatResourceClient) -> None:
        self.client: ChatResourceClient = _validate_client(client)

    async def acreate(
        self, input: EmbeddingInput, model: str | None = None, **kwargs: dict[str, Any]
    ) -> dict[str, Any]:
        """Create embeddings asyncronously from OpenRouter API.

        Parameters
        ----------
        input : EmbeddingInput
            The input text(s) to embed. Can be a single string, a list of strings, floats, or a list of lists of floats.
        model : str | None, optional
            The model to use for embeddings. If None, the client's default model is used.
        **kwargs : dict[str, Any]
            Additional keyword arguments to pass to the API.

        Returns
        -------
            dict[str, Any]
                The response from the OpenRouter API containing the embeddings.
        """
        if not isinstance(input, (str, list)):
            raise ValueError("Input must be a string or a list of strings.")

        model = _validate_model(self.client, model)

        payload: dict[str, Any] = {"model": model, "input": input, **kwargs}

        base_url = _validate_base_url_attribute(self.client)

        path: str = f"{base_url}/{OpenRouterClientPaths.EMBEDDINGS.value}"

        async_client: "AsyncOpenRouterClient" = _validate_arequest_attribute(
            self.client
        )
        return await async_client._arequest(RequestMethods.POST, path, json=payload)
