import time

import ray

# ray.init()


# View resource usage
# print(ray.available_resources())

database: list[str] = [
    "Learning",
    "Ray",
    "Flexible",
    "Distributed",
    "Python",
    "for",
    "Machine",
    "Learning",
]
# Put the db in Ray's object store so that it can be
# accessed by all workers in the cluster.
db_object_ref = ray.put(database)


def retrieve(item: int) -> tuple[int, str]:
    time.sleep(item / 10)
    return item, database[item]


def print_runtime(input_data: list[tuple[int, str]], start_time: float) -> None:
    """Print the runtime of the operation and the resulting data."""


@ray.remote
def retrieve_task(item: int, db: list[str]) -> tuple[int, str]:
    time.sleep(item / 10)
    return item, db[item]


def synchronous_call() -> None:
    """Execute the main program."""
    start: float = time.time()
    data: list[tuple[int, str]] = [retrieve(item) for item in range(8)]
    print_runtime(data, start)


def parallel_call() -> None:
    """Execute the main program in parallel using Ray.

    Returns
    -------
    None
        The function prints the runtime and retrieved data.

    Notes
    -----
    object_reference : list[ray.ObjectRef]
        List of Ray object references of shape (8,)
    data : list[tuple[int, str]]
        Retrieved data of shape (8, 2)
    """
    start: float = time.time()
    # New! It returns a list of object references (i.e. a future)
    object_reference: list[ray.ObjectRef] = [
        retrieve_task.remote(item, db_object_ref) for item in range(8)
    ]
    # New
    data: list[tuple[int, str]] = ray.get(object_reference)
    print_runtime(data, start)


if __name__ == "__main__":
    # synchronous_call()
    parallel_call()
