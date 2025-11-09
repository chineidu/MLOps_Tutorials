import asyncio  # noqa: N999
import time

from utils import download_file_async_v1, monte_carlo_pi  # type: ignore

url: str = "https://calmcode.io/static/data/bigmac.csv"


async def process_data(url: str, x: int, savepath: str) -> None:
    """Process data by downloading a file and running a CPU-bound task asynchronously."""
    N: int = 10
    start_time = time.perf_counter()

    tasks = [download_file_async_v1(url, savepath) for _ in range(N)]
    await asyncio.gather(*tasks)

    loop = asyncio.get_running_loop()
    tasks = [loop.run_in_executor(None, monte_carlo_pi, x) for _ in range(N)]
    results = await asyncio.gather(*tasks)

    duration = time.perf_counter() - start_time

    print(f"RESULTS: {results}\n")
    print(f"\nOperation completed in {duration:.2f} seconds.")


if __name__ == "__main__":
    asyncio.run(process_data(url=url, x=25_378_374, savepath="./file_1.csv"))

# PYTHONPATH=other_notes/Python_tutorial/Async_code uvr -m scalene --html
# --outfile profile_report.html other_notes/Python_tutorial/Async_code/02_async_v2.py;
