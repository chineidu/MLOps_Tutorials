# Import Dask
from dask.distributed import Client, LocalCluster

# from tqdm import tqdm
from rich.console import Console
from rich.theme import Theme

custom_theme = Theme(
    {
        "info": "#76FF7B",
        "warning": "#FBDDFE",
        "error": "#FF0000",
    }
)
console = Console(theme=custom_theme)


if __name__ == "__main__":
    # ======= ThreadPoolExecutor Example =======
    # start_time = time.time()
    # outputs: list[Any] = []
    # futures: list[Any] = []

    # with ThreadPoolExecutor(max_workers=4) as executor:
    #     for inp in tqdm(range(10)):
    #         future: Any = executor.submit(double, inp)
    #         futures.append(future)
    #     outputs = [future.result() for future in futures]

    # stop_time = time.time()

    # console.print(f"It took {(stop_time - start_time):.2}s to process the data")
    # console.print(f"{outputs=}")

    # ======= ProcessPoolExecutor Example =======
    # start_time = time.time()
    # outputs: list[Any] = []
    # futures: list[Any] = []

    # with ProcessPoolExecutor(max_workers=4) as executor:
    #     for inp in trange(10):
    #         future: Any = executor.submit(double, inp)
    #         futures.append(future)
    #     outputs = [future.result() for future in futures]

    # stop_time = time.time()

    # console.print(f"It took {(stop_time - start_time):.2}s to process the data")
    # console.print(f"{outputs=}")

    # ======= Dask Futures Example 1 =======
    # client = Client(n_workers=8)

    # start_time = time.time()
    # futures: list[Any] = []

    # for inp in trange(10):
    #     future: Any = client.submit(double, inp)
    #     futures.append(future)
    # outputs: list[Any] = [future.result() for future in futures]

    # stop_time = time.time()

    # console.print(f"It took {(stop_time - start_time):.2}s to process the data")
    # console.print(f"{outputs=}")
    # del futures

    # ======= Dask Futures Example 2 =======
    # client = Client(n_workers=8)

    # start_time = time.time()

    # inputs: list[Any] = list(range(10))
    # futures: list[Any] = client.map(double, inputs)
    # outputs = client.gather(futures)

    # stop_time = time.time()

    # console.print(f"It took {(stop_time - start_time):.2}s to process the data")
    # console.print(f"{outputs=}")
    # del futures, outputs, inputs

    # ======= Dask Local Cluster Example 1 =======
    cluster = LocalCluster()
    client = Client(cluster)

    console.print(f" {cluster.scheduler=} ")
    console.print(f" {cluster.workers=} ")
    console.print(f" {client=} ")
