# OpenRouter Python SDK

A Python SDK for interacting with the OpenRouter API, providing both synchronous and asynchronous clients.

## Overview

This SDK provides a convenient way to interact with the OpenRouter API. It features:

- Both synchronous and asynchronous clients.
- A resource-based architecture, making the API easy to explore.
- Full type hinting for better editor support and code quality.
- Specific exceptions for clear error handling.

## Table of Contents

- [OpenRouter Python SDK](#openrouter-python-sdk)
  - [Overview](#overview)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Getting Started](#getting-started)
  - [Client Initialization](#client-initialization)
    - [Synchronous Client](#synchronous-client)
    - [Asynchronous Client](#asynchronous-client)
  - [Usage and Examples](#usage-and-examples)
    - [Chat Completions](#chat-completions)
    - [Text Completions](#text-completions)
    - [Embeddings](#embeddings)
    - [Models](#models)
    - [Credits](#credits)
    - [Generation Metadata](#generation-metadata)
    - [Providers](#providers)
    - [Supported Parameters](#supported-parameters)
  - [Error Handling](#error-handling)
  - [Configuration](#configuration)
    - [Environment Variables](#environment-variables)
    - [Custom Configuration](#custom-configuration)
  - [License](#license)

## Features

- **Dual Client Support**: Both synchronous (`OpenRouterClient`) and asynchronous (`AsyncOpenRouterClient`) implementations.
- **Resource-Based Architecture**: API endpoints are organized into logical resource classes.
- **Type Safety**: Full type hints throughout the codebase.
- **Comprehensive Error Handling**: Specific exception types for different error scenarios.
- **Flexible Configuration**: Customizable base URLs, timeouts, and default models.
- **HTTP/2 Support**: Uses `httpx` for efficient HTTP requests.
- **Context Manager Support**: Proper resource management with context managers.

## Installation

This SDK is an internal utility within the `smart-rag` project and is not intended for standalone installation. Ensure all dependencies from `pyproject.toml` are installed.
The `httpx` library is a direct dependency.

```bash
# Install dependencies using uv
uv pip install -r requirements.txt
# or if you have all dependencies in pyproject.toml
uv pip install .

# httpx is required
uv add httpx
```

## Getting Started

Here's a quick example of how to use the asynchronous client to get chat completions.

### Using Context Manager (Recommended)

```python
import asyncio
from src.utilities.openrouter.client import AsyncOpenRouterClient
from src.utilities.openrouter.exceptions import OpenRouterError

async def main():
    # It's recommended to use an environment variable for the API key
    async with AsyncOpenRouterClient() as client:
        try:
            response = await client.chat.acompletions(
                messages=[{"role": "user", "content": "Hello, how are you?"}],
                model="anthropic/claude-3-haiku"
            )
            print(response)
        except OpenRouterError as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    asyncio.run(main())
```

### Manual Resource Management

```python
import asyncio
from src.utilities.openrouter.client import AsyncOpenRouterClient
from src.utilities.openrouter.exceptions import OpenRouterError

async def main():
    # It's recommended to use an environment variable for the API key
    client = AsyncOpenRouterClient()

    try:
        response = await client.chat.acompletions(
            messages=[{"role": "user", "content": "Hello, how are you?"}],
            model="anthropic/claude-3-haiku"
        )
        print(response)
    except OpenRouterError as e:
        print(f"An error occurred: {e}")
    finally:
        await client.aclose()

if __name__ == "__main__":
    asyncio.run(main())
```

## Client Initialization

You can initialize a synchronous or asynchronous client.

### Synchronous Client

```python
from src.utilities.openrouter.client import OpenRouterClient

# Initialize with api_key, or it will be read from OPENROUTER_API_KEY environment variable
client = OpenRouterClient(api_key="your-openrouter-api-key")

# Use it
with client:
    response = client.models.list_models()
    print(response)
```

### Asynchronous Client

```python
from src.utilities.openrouter.client import AsyncOpenRouterClient

# Initialize with api_key, or it will be read from OPENROUTER_API_KEY environment variable
client = AsyncOpenRouterClient(api_key="your-openrouter-api-key")

async def use_async_client():
    async with client:
        response = await client.models.alist_models()
        print(response)

asyncio.run(use_async_client())
```

## Usage and Examples

The client provides access to various API resources.

### Chat Completions

The `chat` resource is used to generate chat-based completions.

```python
# Async
response = await client.chat.acompletions(
    messages=[{"role": "user", "content": "Hello!"}],
    model="anthropic/claude-3-haiku",
    temperature=0.7
)

# Sync
response = client.chat.completions(
    messages=[{"role": "user", "content": "Hello!"}],
    model="anthropic/claude-3-haiku",
    temperature=0.7
)
```

### Text Completions

The `completions` resource is for legacy text completions.

```python
# Async
response = await client.acompletions(
    prompt="Write a haiku about programming",
    model="anthropic/claude-3-haiku"
)

# Sync
response = client.completions(
    prompt="Write a haiku about programming",
    model="anthropic/claude-3-haiku"
)
```

### Embeddings

Create embeddings for text using the `embeddings` resource.

```python
# Async
response = await client.embeddings.acreate(
    input="Hello, world!",
    model="openai/text-embedding-3-small"
)

# Sync
response = client.embeddings.create(
    input="Hello, world!",
    model="openai/text-embedding-3-small"
)
```

### Models

List available models and their properties.

```python
# Async: List all models
models = await client.models.alist_models()

# Sync: List models by category
ai_models = client.models.list_models(category=["programming", "technology"])

# Async: Count models
count = await client.models.acount()

# Sync: List embedding models
embeddings = client.models.embeddings()
```

### Credits

Check your remaining credits and usage.

```python
# Async
credits_data = await client.aget_credits_data()
print(f"Credits remaining: {credits_data.get('credits', 'N/A')}")

# Sync
credits_data = client.get_credits_data()
print(f"Total usage: {credits_data.get('total_usage', 'N/A')}")
```

### Generation Metadata

Retrieve metadata for a specific generation.

```python
# Async
metadata = await client.ageneration_metadata(id="gen-1234567890")

# Sync
metadata = client.generation_metadata(id="gen-1234567890")
```

### Providers

List all available providers.

```python
# Async
providers = await client.alist_providers()

# Sync
providers = client.list_providers()
```

### Supported Parameters

Get the supported parameters for a specific model.

```python
# Async
params = await client.parameters.alist_supported(author="openai", slug="gpt-4")

# Sync
params = client.parameters.list_supported(author="openai", slug="gpt-4")
```

## Error Handling

The SDK raises specific exceptions for different types of errors, all inheriting from `OpenRouterError`.

- **`OpenRouterError`**: Base exception for all SDK errors.
- **`AuthenticationError`**: Invalid or missing API key.
- **`PermissionError`**: Insufficient permissions.
- **`RateLimitError`**: API rate limit exceeded.
- **`ModelNotFoundError`**: The specified model was not found.
- **`InvalidResponseError`**: The API returned a malformed response.
- **`InternalServerError`**: A server-side error occurred.
- **`NetworkError`**: A network connectivity issue occurred.
- **`InvalidClientError`**: The client was configured incorrectly.

Example of handling exceptions:

```python
import asyncio
from src.utilities.openrouter.client import AsyncOpenRouterClient
from src.utilities.openrouter.exceptions import AuthenticationError, RateLimitError, OpenRouterError

async def error_handling_example():
    client = AsyncOpenRouterClient(api_key="invalid-key")
    try:
        await client.chat.acompletions(messages=[{"role": "user", "content": "Hello!"}])
    except AuthenticationError:
        print("Authentication failed: Please check your API key.")
    except RateLimitError:
        print("Rate limit exceeded. Please try again later.")
    except OpenRouterError as e:
        print(f"An OpenRouter error occurred: {e}")
    finally:
        await client.aclose()

asyncio.run(error_handling_example())
```

## Configuration

### Environment Variables

The SDK will automatically pick up the `OPENROUTER_API_KEY` from your environment variables if you don't pass it to the client constructor.

#### Setting Environment Variables

**Bash/Zsh:**

```bash
export OPENROUTER_API_KEY="your-api-key"
```

**Windows Command Prompt:**

```cmd
set OPENROUTER_API_KEY=your-api-key
```

**Windows PowerShell:**

```powershell
$env:OPENROUTER_API_KEY = "your-api-key"
```

**Python (temporary for current session):**

```python
import os
os.environ["OPENROUTER_API_KEY"] = "your-api-key"
```

#### Using Environment Variables with the SDK

Once set, you can initialize clients without explicitly passing the API key:

```python
# The API key will be automatically read from OPENROUTER_API_KEY
client = OpenRouterClient()  # No api_key parameter needed

# Or asynchronously
async_client = AsyncOpenRouterClient()  # No api_key parameter needed
```

**Note:** If both an environment variable and a parameter are provided, the parameter takes precedence.

### Custom Configuration

You can customize the client's behavior by passing arguments to its constructor.

```python
from src.utilities.openrouter.client import AsyncOpenRouterClient

client = AsyncOpenRouterClient(
    api_key="your-api-key",
    base_url="https://custom.openrouter.endpoint/v1",  # Custom endpoint
    default_model="anthropic/claude-3-opus",          # Custom default model
    timeout=60                                        # Custom timeout
)
```

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.
