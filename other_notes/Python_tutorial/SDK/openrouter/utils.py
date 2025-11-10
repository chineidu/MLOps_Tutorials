import os
from typing import TYPE_CHECKING, Any, cast

import httpx

from src.utilities.openrouter.exceptions import (
    AuthenticationError,
    InternalServerError,
    InvalidClientError,
    InvalidResponseError,
    ModelNotFoundError,
    OpenRouterError,
    PermissionError,
    RateLimitError,
)
from src.utilities.openrouter.types import HttpStatusCodes

if TYPE_CHECKING:
    from src.utilities.openrouter.client import AsyncOpenRouterClient, OpenRouterClient


def _validate_client(client: Any) -> "AsyncOpenRouterClient | OpenRouterClient":
    """Validate that the client is either OpenRouterClient or AsyncOpenRouterClient."""
    if not (hasattr(client, "_request") or hasattr(client, "_arequest")):
        raise InvalidClientError(
            "Client must be an instance of OpenRouterClient or AsyncOpenRouterClient."
        )
    return client


def _validate_model(client: Any, model: str | None) -> str:
    """Validate that the model is specified for chat completions."""
    if (default_model := getattr(client, "default_model", None)) is None:
        raise AttributeError("Client does not have a 'default_model' attribute.")
    model = model or default_model
    if not model:
        raise ModelNotFoundError("Model must be specified for chat completions.")
    return model


def _validate_base_url_attribute(client: Any) -> str:
    """Validate that the client has a base_url attribute."""
    if (base_url := getattr(client, "base_url", None)) is None:
        raise AttributeError("Client does not have a 'base_url' attribute.")
    return base_url


def _validate_request_attribute(client: Any) -> "OpenRouterClient":
    """Validate that the client has a synchronous request method."""
    if hasattr(client, "_request"):
        if getattr(client, "_request", None) is None:
            raise AttributeError("OpenRouterClient does not have a '_request' method.")
    return cast("OpenRouterClient", client)


def _validate_arequest_attribute(client: Any) -> "AsyncOpenRouterClient":
    """Validate that the client has an asynchronous request method."""
    if hasattr(client, "_arequest"):
        if getattr(client, "_arequest", None) is None:
            raise AttributeError(
                "AsyncOpenRouterClient does not have a '_arequest' method."
            )
    return cast("AsyncOpenRouterClient", client)


def _validate_response(client: Any, response: httpx.Response) -> dict[str, Any]:
    """Validate HTTP response from OpenRouter API."""
    if response.status_code == HttpStatusCodes.BAD_REQUEST:
        raise InvalidResponseError("Bad request to OpenRouter API.")

    if response.status_code == HttpStatusCodes.UNAUTHORIZED:
        raise AuthenticationError("Invalid API key for OpenRouter API.")

    if response.status_code == HttpStatusCodes.FORBIDDEN:
        raise PermissionError("Permission denied for OpenRouter API.")

    if response.status_code == HttpStatusCodes.NOT_FOUND:
        raise ModelNotFoundError("Model not found in OpenRouter API.")

    if response.status_code == HttpStatusCodes.TOO_MANY_REQUESTS:
        raise RateLimitError("Rate limit exceeded for OpenRouter API.")

    if response.status_code == HttpStatusCodes.INTERNAL_SERVER_ERROR:
        raise InternalServerError("Internal server error from OpenRouter API.")

    if not response.is_success:
        raise OpenRouterError(
            f"{client.__class__.__name__} error: {response.status_code} - {response.reason_phrase}"
        )

    return response.json()


def get_openrouter_api_keys(api_key: str | None = None) -> str:
    """Retrieve OpenRouter API keys from environment variables or configuration.

    Parameters
    ----------
    api_key : str | None, optional
        The OpenRouter API key. If None, the function will attempt to retrieve it from
        environment variables.

    Returns
    -------
        dict[str, str]
            A dictionary containing the OpenRouter API key.
    """

    if api_key is not None:
        return api_key
    return os.getenv("OPENROUTER_API_KEY", "")
