# Dask

## Table of Content

- [Dask](#dask)
  - [Table of Content](#table-of-content)
  - [Installation](#installation)
  - [Dask: Best Practices](#dask-best-practices)
    - [1. Start Small](#1-start-small)
    - [2. Use The Dashboard](#2-use-the-dashboard)
    - [3. Avoid Very Large Partitions](#3-avoid-very-large-partitions)
    - [3. Avoid Very Large Graphs](#3-avoid-very-large-graphs)
    - [4. Learn Techniques For Customization](#4-learn-techniques-for-customization)
    - [5. Stop Using Dask When No Longer Needed](#5-stop-using-dask-when-no-longer-needed)
    - [6. Persist When You Can](#6-persist-when-you-can)
    - [7. Store Data Efficiently](#7-store-data-efficiently)
    - [8. Processes and Threads](#8-processes-and-threads)
    - [9. Load Data with Dask](#9-load-data-with-dask)
    - [10. Avoid calling compute repeatedly](#10-avoid-calling-compute-repeatedly)

## Installation

- Visit the official docs for [installation](https://docs.dask.org/en/stable/install.html#dask-installation) guide.

```sh
conda install dask

conda install dask -c conda-forge

python -m pip install "dask[complete]"    # Install everything
python -m pip install dask                # Install only core parts of dask
```

## [Dask: Best Practices](https://docs.dask.org/en/stable/best-practices.html)

### 1. Start Small

```text
- Parallelism brings extra complexity and overhead. Sometimes it’s necessary for larger problems, but often it’s not.
- Before adding a parallel computing system like Dask to your workload you may want to first try some alternatives:
- Use better algorithms or data structures: NumPy, pandas, Scikit-learn may have faster functions for what you’re trying to do.
```

- Use built-in functions: Explore NumPy, pandas, Scikit-learn for optimized functions.
- Choose efficient formats: Use binary formats for faster access to large datasets.
- Compile code: Consider Numba or Cython for speed boosts.
- Sample smartly: Analyze if using all your data is necessary.
- Profile first: Identify bottlenecks before jumping to parallelism.


### 2. Use The Dashboard

- Dask’s dashboard helps you to understand the state of your workers.
- This information can help to guide you to efficient solutions.

### 3. Avoid Very Large Partitions

- Your chunks of data should be small enough so that many of them fit in a worker’s available memory at once.
- You often control this when you select partition size in Dask DataFrame (see [DataFrame Partitions](https://docs.dask.org/en/stable/dataframe-design.html#dataframe-design-partitions)) or chunk size in Dask Array (see [Array Chunks](https://docs.dask.org/en/stable/array-chunks.html)).
- Dask will likely manipulate as many chunks in parallel on one machine as you have cores on that machine.
- So if you have 1 GB chunks and ten cores, then Dask is likely to use at least 10 GB of memory.
- If you have a machine with 100 GB and 10 cores, then you might want to choose chunks in the 1GB range.
- You have space for ten chunks per core which gives Dask a healthy margin, without having tasks that are too small.

### 3. Avoid Very Large Graphs

- Dask workloads are composed of `tasks`.
- A task is a Python function, like np.sum applied onto a Python object, like a pandas DataFrame or NumPy array.
- If you are working with Dask collections with many partitions, then every operation you do, like x + 1 likely generates many tasks, at least as many as partitions in your collection.

- You can build smaller graphs by:
  - Larger chunks: Increase chunk size in your Dask collections to create fewer tasks (requires sufficient worker memory).
  - Fuse operations: Combine multiple operations into single functions using `da.map_blocks` or `dd.map_partitions`.
  - Break up computations: Submit very large workloads in smaller chunks sequentially.

### 4. Learn Techniques For Customization

- The high level Dask collections (array, DataFrame, bag) include common operations that follow standard Python APIs from NumPy and pandas.
- However, many Python workloads are complex and may require operations that are not included in these high level APIs.

### 5. Stop Using Dask When No Longer Needed

- In many workloads, it is common to use Dask to read in a large amount of data, reduce it down, and then iterate on a much smaller amount of data.
- For this latter stage on smaller data it may make sense to stop using Dask, and start using normal Python again.

```py
df = dd.read_parquet("lots-of-data-*.parquet")
df = df.groupby('name').mean()  # reduce data significantly
df = df.compute()               # continue on with pandas/NumPy
```

### 6. Persist When You Can

- Accessing data from RAM is often much faster than accessing it from disk.
- Once you have your dataset in a clean state that both:
  - Fits in memory
  - Is clean enough that you will want to try many different analyses

- Then it is a good time to persist your data in RAM.

```py
df = dd.read_parquet("lots-of-data-*.parquet")
df = df.fillna(...)  # clean up things lazily
df = df[df.name == 'Alice']  # get down to a more reasonable size

df = df.persist()  # trigger computation, persist in distributed RAM
```

### 7. Store Data Efficiently

> Faster computers mean data access (I/O) becomes a bottleneck, especially for parallel processing. To optimize, consider how you store your data.

- Use newer compression formats (lz4, snappy, Z-Standard) for better performance and random access.
- Switch to storage formats like Parquet, ORC, Zarr, for random access, metadata, and binary data efficiency.
- Consider cloud compatibility and chunk data for optimized access patterns.

### 8. Processes and Threads

- Threads for numbers: Use threads for numerical libraries (NumPy, pandas, etc.) that benefit from relaxed GIL.
- Processes for text: Use processes for text data and non-numerical tasks.
- Processes for large machines: Consider using some processes even for numerical tasks on machines with many cores.

For more information on threads, processes, and how to configure them in Dask, see the scheduler documentation.

### 9. Load Data with Dask

- Don't create large Python objects yourself for Dask. Let Dask handle it!  This avoids unnecessary data movement within Dask.
- Check here for [examples](https://docs.dask.org/en/stable/best-practices.html#load-data-with-dask).

### 10. Avoid calling compute repeatedly

- Compute related results with shared computations in a single dask.compute() call.

```py
# Don't repeatedly call compute

df = dd.read_csv("...")
xmin = df.x.min().compute()
xmax = df.x.max().compute()


# Do compute multiple results at the same time

df = dd.read_csv("...")
xmin, xmax = dask.compute(df.x.min(), df.x.max())
```
