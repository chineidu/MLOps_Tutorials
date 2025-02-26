import asyncio
import time


async def simple_coroutine(delay: float) -> None:
    # Simulate work (Non-blocking)
    await asyncio.sleep(delay)


# Run mulitple coroutines concurrently
async def multiple_coroutines() -> None:
    start_time: float = time.time()
    # Create a list of coroutines
    coroutines = [simple_coroutine(delay) for delay in [4, 1, 2]]
    # Wait for all coroutines to complete
    await asyncio.gather(*coroutines)
    duration: float = time.time() - start_time


async def send_email_1() -> str:
    await asyncio.sleep(3.3)
    return "Successfully received email 1. I will reply you soon."


async def send_email_2() -> str:
    await asyncio.sleep(6)
    return "Successfully received email 2. I will reply you soon."


async def send_email_3() -> str:
    await asyncio.sleep(2.5)
    return "Successfully received email 3. I will reply you soon."


async def send_email_4() -> str:
    await asyncio.sleep(1.7)
    return "Successfully received email 4. I will reply you soon."


async def multiple_coroutines_2() -> None:
    start_time: float = time.time()
    coroutines = [send_email_1(), send_email_2(), send_email_3(), send_email_4()]
    results = await asyncio.gather(*coroutines)
    for res in results:
        pass
    duration: float = time.time() - start_time


if __name__ == "__main__":
    # Run the coroutine
    # asyncio.run(simple_coroutine())

    # Run multiple coroutines concurrently
    # asyncio.run(multiple_coroutines())

    asyncio.run(multiple_coroutines_2())
