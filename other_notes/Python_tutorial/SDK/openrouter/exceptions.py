"""Exceptions for OpenRouter-related errors."""


class OpenRouterError(Exception):
    """Base exception for OpenRouter-related errors."""

    pass


class NetworkError(OpenRouterError):
    """Exception raised for network-related issues."""

    pass


class AuthenticationError(OpenRouterError):
    """Exception raised for authentication failures."""

    pass


class PermissionError(OpenRouterError):
    """Exception raised for permission-related issues."""

    pass


class RateLimitError(OpenRouterError):
    """Exception raised when rate limits are exceeded."""

    pass


class InvalidResponseError(OpenRouterError):
    """Exception raised for invalid responses from the OpenRouter API."""

    pass


class InvalidClientError(OpenRouterError):
    """Exception raised for invalid client usage."""

    pass


class InternalServerError(OpenRouterError):
    """Exception raised for server-side errors."""

    pass


class ModelNotFoundError(OpenRouterError):
    """Exception raised when a specified model is not found."""

    pass
