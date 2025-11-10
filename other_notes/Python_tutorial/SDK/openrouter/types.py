from enum import Enum


class HttpStatusCodes(str, Enum):
    OK = "200"
    CREATED = "201"
    ACCEPTED = "202"
    NO_CONTENT = "204"
    BAD_REQUEST = "400"  # Malformed request syntax
    UNAUTHORIZED = "401"  # Lacks valid authentication credentials
    FORBIDDEN = "403"  # Authenticated but does not have permission
    NOT_FOUND = "404"
    TOO_MANY_REQUESTS = "429"  # Rate limiting
    INTERNAL_SERVER_ERROR = "500"
    BAD_GATEWAY = "502"
    SERVICE_UNAVAILABLE = "503"
    GATEWAY_TIMEOUT = "504"


class RequestMethods(str, Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


class OpenRouterClientPaths(str, Enum):
    BASE_URL = "https://openrouter.ai/api/v1"

    # All POST endpoints below
    CHAT_COMPLETIONS = "chat/completions"
    COMPLETIONS = "completions"
    EMBEDDINGS = "embeddings"

    # All GET endpoints below
    MODEL_COUNT = "models/count"
    LIST_MODELS_AND_PROPERTIES = "models"
    LIST_ALL_EMBEDDING_MODELS = "models/embeddings"

    # All GET endpoints below
    MODEL_SUPPORTED_PARAMETERS = "parameters"
    LIST_ALL_PROVIDERS = "providers"
    USER_ACTIVITY = "activity"
    REMAINING_CREDITS = "credits"
    GENERATION_METADATA = "generation"  # requires generation ID
