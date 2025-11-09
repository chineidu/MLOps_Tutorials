import asyncio
import math
import random

import aiofiles
import httpx
import requests
from tqdm import tqdm


def download_file(url: str, savepath: str) -> None:
    """Download a large file from a URL and save it locally with a progress bar."""
    # Set a chunk size for streaming (e.g., 100 KB)
    CHUNK_SIZE: int = 102_400

    try:
        # Use stream=True to prevent reading the entire response content into memory
        with requests.get(url, stream=True, timeout=20) as response:
            # Raise an HTTPError for bad responses (4xx or 5xx)
            response.raise_for_status()

            # Get total file size from headers
            total_size = int(response.headers.get("content-length", 0))

            # Create progress bar object
            pbar = tqdm(total=total_size, unit="B", unit_scale=True, desc=savepath)

            try:
                # Open the local file in binary write mode ('wb')
                with open(savepath, "wb") as file:
                    # Iterate over the response content in chunks
                    for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                        # Write the chunk to the local file
                        file.write(chunk)
                        # Update progress bar
                        pbar.update(len(chunk))
            finally:
                # Ensure progress bar is closed
                pbar.close()

        print(f"Large file downloaded successfully to {savepath}")

    except requests.exceptions.RequestException as e:  # type: ignore
        print(f"An error occurred: {e}")


def is_prime_cpu_task(n: int) -> bool:
    """Check if a number is prime (trial division)."""
    if n < 2:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False

    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True


def compute_fibonacci(n: int) -> int:
    """
    Calculate the nth Fibonacci number recursively (inefficient by design).
    Good for demonstrating CPU-bound work.

    Examples:
    - compute_fibonacci(30) takes ~0.2s
    - compute_fibonacci(35) takes ~2s
    - compute_fibonacci(38) takes ~6s
    """
    if n <= 1:
        return n
    return compute_fibonacci(n - 1) + compute_fibonacci(n - 2)


# This can be done if no other async version is available
async def download_file_async_v1(url: str, savepath: str) -> None:
    """Asynchronous wrapper for the synchronous download_file function.

    Converts the blocking download_file function into a non-blocking asynchronous function
    by running it in a separate thread using asyncio.to_thread.
    """
    return await asyncio.to_thread(download_file, url, savepath)

def monte_carlo_pi(iterations: int = 1_000_000) -> float:
    """
    Estimate Pi using Monte Carlo method.
    Pure CPU computation with no I/O.
    
    Args:
        iterations: Number of random points (1M = ~0.3s)
    
    Returns:
        Estimated value of Pi
    """
    
    inside_circle = 0
    
    for _ in range(iterations):
        x = random.random()
        y = random.random()
        if x*x + y*y <= 1:
            inside_circle += 1
    
    return 4 * inside_circle / iterations

# ========= ASYNC VERSION =========
async def async_download_file(url: str, savepath: str) -> None:
    """Download a large file from a URL and save it locally with a progress bar."""
    # Set a chunk size for streaming (e.g., 100 KB)
    CHUNK_SIZE: int = 102_400

    try:
        # Use httpx for async HTTP requests with streaming
        async with httpx.AsyncClient() as client:
            async with client.stream("GET", url, timeout=20) as response:
                # Raise an HTTPError for bad responses (4xx or 5xx)
                response.raise_for_status()

                # Get total file size from headers
                total_size = int(response.headers.get("content-length", 0))

                # Create progress bar object
                pbar = tqdm(total=total_size, unit="B", unit_scale=True, desc=savepath)

                try:
                    # Open the local file asynchronously with aiofiles
                    async with aiofiles.open(savepath, "wb") as file:
                        # Iterate over the response content in chunks asynchronously
                        async for chunk in response.aiter_bytes(chunk_size=CHUNK_SIZE):
                            # Write the chunk to the local file asynchronously
                            await file.write(chunk)
                            # Update progress bar
                            pbar.update(len(chunk))
                finally:
                    # Ensure progress bar is closed
                    pbar.close()

        print(f"Large file downloaded successfully to {savepath}")

    except httpx.RequestError as e:
        print(f"An error occurred: {e}")


# Example usage
url: str = "https://calmcode.io/static/data/bigmac.csv"

# download_file(url=url, savepath="./file_1.csv")


# if __name__ == "__main__":
