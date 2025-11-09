import asyncio  # noqa: N999
import time
from concurrent.futures import ProcessPoolExecutor

from utils import async_download_file, monte_carlo_pi  # type: ignore

url: str = "https://calmcode.io/static/data/bigmac.csv"


async def process_data(url: str, x: int, savepath: str) -> None:
    """Process data by downloading a file and running a CPU-bound task asynchronously.
    
    Using ProcessPoolExecutor for CPU-bound tasks to avoid GIL limitations is generally more effective
    than ThreadPoolExecutor, especially for intensive computations.
    """
    N: int = 10
    start_time = time.perf_counter()

    tasks = [async_download_file(url, savepath) for _ in range(N)]
    await asyncio.gather(*tasks)

    loop = asyncio.get_running_loop()

    # Process CPU-bound task asynchronously using ProcessPoolExecutor
    with ProcessPoolExecutor() as executor:
        tasks = [loop.run_in_executor(executor, monte_carlo_pi, x) for _ in range(N)]
        results = await asyncio.gather(*tasks)

    duration = time.perf_counter() - start_time

    print(f"RESULTS: {results}\n")
    print(f"\nOperation completed in {duration:.2f} seconds.")


if __name__ == "__main__":
    # multiprocessing.freeze_support()
    asyncio.run(process_data(url=url, x=25_378_374, savepath="./file_1.csv"))
