"""
Async HTTP Client Templates - aiohttp & httpx
Best practices for making HTTP requests with proper resource management
"""

import asyncio
import json
from typing import Any

# ============================================================================
# AIOHTTP TEMPLATE
# ============================================================================
import aiohttp


class AioHTTPClient:
    """
    Async HTTPX client with connection pooling and robust error handling.

    Features
    --------
    - Explicit connection pooling configuration
    - Proper timeout handling
    - Comprehensive exception handling
    - Automatic resource cleanup
    """

    def __init__(
        self, base_url: str = "", timeout: int = 30, pool_size: int = 100, pool_timeout: int = 30
    ) -> None:
        self.base_url = base_url
        self.timeout = aiohttp.ClientTimeout(total=timeout)
        self.pool_size = pool_size
        self.pool_timeout = pool_timeout
        self.session: aiohttp.ClientSession | None = None
        self.connector: aiohttp.TCPConnector | None = None

    async def __aenter__(self) -> "AioHTTPClient":
        """Context manager entry - creates session with connection pool"""
        # Create connector with connection pool settings
        self.connector = aiohttp.TCPConnector(
            limit=self.pool_size,  # Total number of connections
            limit_per_host=30,  # Max connections per host
            ttl_dns_cache=300,  # DNS cache TTL in seconds
            enable_cleanup_closed=True,  # Clean up closed connections
        )

        self.session = aiohttp.ClientSession(
            base_url=self.base_url,
            timeout=self.timeout,
            connector=self.connector,
            raise_for_status=False,  # Handle status codes manually
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - ensures session and connector cleanup"""
        if self.session:
            await self.session.close()
        if self.connector:
            await self.connector.close()

    async def get(
        self, url: str, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Make GET request with error handling

        Args:
            url: Endpoint URL
            params: Query parameters
            headers: Request headers

        Returns:
            Dictionary with 'success', 'data', 'status', 'error' keys
        """
        if not self.session:
            return {"success": False, "error": "Session not initialized", "data": None}
        try:
            async with self.session.get(url, params=params, headers=headers) as response:
                # Try to parse JSON response
                try:
                    data = await response.json()
                except (aiohttp.ContentTypeError, json.JSONDecodeError):
                    data = await response.text()

                return {
                    "success": response.status < 400,
                    "status": response.status,
                    "data": data,
                    "headers": dict(response.headers),
                    "error": None if response.status < 400 else f"HTTP {response.status}",
                }

        except aiohttp.ClientConnectorError as e:
            return {"success": False, "error": f"Connection error: {e}", "data": None}
        except aiohttp.ServerTimeoutError:
            return {"success": False, "error": "Request timeout", "data": None}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {e}", "data": None}

    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Make POST request with error handling

        Args:
            url: Endpoint URL
            data: Form data
            json_data: JSON payload
            headers: Request headers

        Returns:
            Dictionary with 'success', 'data', 'status', 'error' keys
        """
        if not self.session:
            return {"success": False, "error": "Session not initialized", "data": None}
        try:
            async with self.session.post(url, data=data, json=json_data, headers=headers) as response:
                try:
                    response_data = await response.json()
                except (aiohttp.ContentTypeError, json.JSONDecodeError):
                    response_data = await response.text()

                return {
                    "success": response.status < 400,
                    "status": response.status,
                    "data": response_data,
                    "headers": dict(response.headers),
                    "error": None if response.status < 400 else f"HTTP {response.status}",
                }

        except aiohttp.ClientConnectorError as e:
            return {"success": False, "error": f"Connection error: {e}", "data": None}
        except aiohttp.ServerTimeoutError:
            return {"success": False, "error": "Request timeout", "data": None}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {e}", "data": None}


# ============================================================================
# HTTPX TEMPLATE
# ============================================================================

from typing import Any

import httpx


class HTTPXClient:
    """
    Async HTTPX client with connection pooling and robust error handling.

    Features
    --------
    - Explicit connection pooling configuration
    - Proper timeout handling
    - Comprehensive exception handling
    - Automatic resource cleanup
    - HTTP/2 support
    """

    def __init__(
        self,
        base_url: str = "",
        timeout: int = 30,
        http2: bool = True,
        pool_max_connections: int = 100,
        pool_max_keepalive: int = 20,
    ) -> None:
        self.base_url = base_url
        self.timeout = timeout
        self.http2 = http2
        self.pool_max_connections = pool_max_connections
        self.pool_max_keepalive = pool_max_keepalive
        self.client: httpx.AsyncClient | None = None

    async def __aenter__(self) -> "HTTPXClient":
        """Context manager entry - creates client with connection pool"""
        # Create limits for connection pool
        limits = httpx.Limits(
            max_connections=self.pool_max_connections,  # Total pool size
            max_keepalive_connections=self.pool_max_keepalive,  # Keep-alive pool
            keepalive_expiry=5.0,  # Keep connections alive for 5 seconds
        )

        self.client = httpx.AsyncClient(
            base_url=self.base_url,
            timeout=self.timeout,
            http2=self.http2,
            follow_redirects=True,
            limits=limits,
        )
        return self

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        """Context manager exit - ensures client cleanup"""
        if self.client:
            await self.client.aclose()

    async def get(
        self, url: str, params: dict[str, Any] | None = None, headers: dict[str, str] | None = None
    ) -> dict[str, Any]:
        """
        Make GET request with error handling

        Args:
            url: Endpoint URL
            params: Query parameters
            headers: Request headers

        Returns:
            Dictionary with 'success', 'data', 'status', 'error' keys
        """
        if not self.client:
            return {"success": False, "error": "Client not initialized", "data": None}

        try:
            response = await self.client.get(url, params=params, headers=headers)

            # Try to parse JSON response
            try:
                data = response.json()
            except json.JSONDecodeError:
                data = response.text

            return {
                "success": response.status_code < 400,
                "status": response.status_code,
                "data": data,
                "headers": dict(response.headers),
                "error": None if response.status_code < 400 else f"HTTP {response.status_code}",
            }

        except httpx.ConnectError as e:
            return {"success": False, "error": f"Connection error: {e}", "data": None}
        except httpx.TimeoutException:
            return {"success": False, "error": "Request timeout", "data": None}
        except httpx.HTTPStatusError as e:
            return {"success": False, "error": f"HTTP error: {e}", "data": None}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {e}", "data": None}

    async def post(
        self,
        url: str,
        data: dict[str, Any] | None = None,
        json_data: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
    ) -> dict[str, Any]:
        """
        Make POST request with error handling

        Args:
            url: Endpoint URL
            data: Form data
            json_data: JSON payload
            headers: Request headers

        Returns:
            Dictionary with 'success', 'data', 'status', 'error' keys
        """
        if not self.client:
            return {"success": False, "error": "Client not initialized", "data": None}
        try:
            response = await self.client.post(url, data=data, json=json_data, headers=headers)

            try:
                response_data = response.json()
            except json.JSONDecodeError:
                response_data = response.text

            return {
                "success": response.status_code < 400,
                "status": response.status_code,
                "data": response_data,
                "headers": dict(response.headers),
                "error": None if response.status_code < 400 else f"HTTP {response.status_code}",
            }

        except httpx.ConnectError as e:
            return {"success": False, "error": f"Connection error: {e}", "data": None}
        except httpx.TimeoutException:
            return {"success": False, "error": "Request timeout", "data": None}
        except httpx.HTTPStatusError as e:
            return {"success": False, "error": f"HTTP error: {e}", "data": None}
        except Exception as e:
            return {"success": False, "error": f"Unexpected error: {e}", "data": None}


# ============================================================================
# USAGE EXAMPLES
# ============================================================================


async def example_aiohttp() -> None:
    """Example usage of AioHTTPClient"""
    print("=== AioHTTP Examples ===\n")

    # Use context manager for automatic cleanup
    async with AioHTTPClient(base_url="https://jsonplaceholder.typicode.com") as client:
        # GET request
        print("1. GET request:")
        result = await client.get("/posts/1")
        if result["success"]:
            print(f"✓ Status: {result['status']}")
            print(f"✓ Data: {result['data']}\n")
        else:
            print(f"✗ Error: {result['error']}\n")

        # POST request
        print("2. POST request:")
        payload = {"title": "Test Post", "body": "This is a test", "userId": 1}
        result = await client.post("/posts", json_data=payload)
        if result["success"]:
            print(f"✓ Status: {result['status']}")
            print(f"✓ Response: {result['data']}\n")
        else:
            print(f"✗ Error: {result['error']}\n")

        # GET with parameters
        print("3. GET with query parameters:")
        result = await client.get("/posts", params={"userId": 1})
        if result["success"]:
            posts = result["data"]
            print(f"✓ Retrieved {len(posts)} posts\n")

        # Error handling example
        print("4. Error handling (invalid URL):")
        result = await client.get("/invalid-endpoint-12345")
        print(f"Success: {result['success']}")
        print(f"Status: {result['status']}")
        print(f"Error: {result['error']}\n")


async def example_httpx() -> None:
    """Example usage of HTTPXClient"""
    print("=== HTTPX Examples ===\n")

    # Use context manager for automatic cleanup
    async with HTTPXClient(base_url="https://jsonplaceholder.typicode.com") as client:
        # GET request
        print("1. GET request:")
        result = await client.get("/posts/1")
        if result["success"]:
            print(f"✓ Status: {result['status']}")
            print(f"✓ Data: {result['data']}\n")
        else:
            print(f"✗ Error: {result['error']}\n")

        # POST request
        print("2. POST request:")
        payload = {"title": "Test Post", "body": "This is a test", "userId": 1}
        result = await client.post("/posts", json_data=payload)
        if result["success"]:
            print(f"✓ Status: {result['status']}")
            print(f"✓ Response: {result['data']}\n")
        else:
            print(f"✗ Error: {result['error']}\n")

        # Multiple concurrent requests
        print("3. Concurrent requests:")
        tasks = [client.get(f"/posts/{i}") for i in range(1, 4)]
        results = await asyncio.gather(*tasks)
        successful = sum(1 for r in results if r["success"])
        print(f"✓ Completed {successful}/{len(results)} requests\n")


async def example_concurrent_requests() -> None:
    """Example of making concurrent requests with multiple clients"""
    print("=== Concurrent Multi-Client Example ===\n")

    async def fetch_with_aiohttp() -> dict[str, Any]:
        async with AioHTTPClient("https://jsonplaceholder.typicode.com") as client:
            return await client.get("/posts/1")

    async def fetch_with_httpx() -> dict[str, Any]:
        async with HTTPXClient("https://jsonplaceholder.typicode.com") as client:
            return await client.get("/posts/2")

    # Run both clients concurrently
    results = await asyncio.gather(fetch_with_aiohttp(), fetch_with_httpx())

    print("AioHTTP result:", "✓" if results[0]["success"] else "✗")
    print("HTTPX result:", "✓" if results[1]["success"] else "✗")


async def main() -> None:
    """Run all examples"""
    await example_aiohttp()
    print("\n" + "=" * 50 + "\n")
    await example_httpx()
    print("\n" + "=" * 50 + "\n")
    await example_concurrent_requests()


if __name__ == "__main__":
    # Run the examples
    asyncio.run(main())
