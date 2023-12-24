# PySpark

## Table of Content

- [PySpark](#pyspark)
  - [Table of Content](#table-of-content)
  - [Install Java](#install-java)
  - [Basic Operations](#basic-operations)
    - [Create Spark Session](#create-spark-session)
    - [Load Data](#load-data)
    - [Load Data With Schema And Delimiter](#load-data-with-schema-and-delimiter)
    - [Create A Copy](#create-a-copy)
    - [Select Column(s) And Return A DataFrame](#select-columns-and-return-a-dataframe)
    - [Drop Columns](#drop-columns)
    - [Add A New Column](#add-a-new-column)
    - [Regex](#regex)
    - [User Defined Functions (UDFs)](#user-defined-functions-udfs)
    - [Select Unique Items In A Column](#select-unique-items-in-a-column)
    - [Check For Null/NaN Values](#check-for-nullnan-values)
    - [Filter Keyword](#filter-keyword)
    - [When Keyword](#when-keyword)
    - [Casting](#casting)
    - [Summary Stats](#summary-stats)
    - [Group By](#group-by)
    - [Split Large Data](#split-large-data)

## Install Java

- It requires Java8
- Visit this [link](https://www.java.com/en/download/) to download and install Java8.

## Basic Operations

### Create Spark Session

```python
# Built-in libraries
import re
from typing import Any
import pandas as pd


# PySpark Modules
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import (
    ArrayType,
    DoubleType,
    StringType,
    IntegerType,
    FloatType,
    StructType,
    StructField,
    LongType,
)

# Create Spark Session
spark = SparkSession.builder.appName("enterYourAppName").getOrCreate()
```

### Load Data

```python
# Load data
fp = "./path/to/data.csv"
raw_data = spark.read.option("header", "true").option("inferSchema", "true").csv(fp)

raw_data.printSchema()
```

### Load Data With Schema And Delimiter

```python
FILEPATH = "path/to/file.csv"
DELIMITER = "|"
SCHEMA = StructType(
    [
        StructField("trans_date", StringType(), nullable=True),
        StructField("cust_id", IntegerType(), nullable=True),
        StructField("brand_name", StringType(), nullable=True),
        StructField("description", StringType(), nullable=True),
        StructField("amount", FloatType(), nullable=True),
    ]
)
data = spark.read.schema(SCHEMA).option("delimiter", DELIMITER).format("csv").load(FILEPATH)
```

### Create A Copy

```python
# Create a copy of the DataFrame
df = data.alias("df")
```

### Select Column(s) And Return A DataFrame

```python
# Drop irrelevant columns
data = data.select("_c14", "_c15", "_c16", "_c17")
```

### Drop Columns

```python
raw_data = raw_data.drop("course_name", "reviews_avg", "course_duration", "price_after_discount")
```

### Add A New Column

```python
# Drop irrelevant columns
raw_data = raw_data.withColumn("new_column_name", F.col("column") + 15)
```

### Regex

```python
# Clean the reviews_avg
REVIEWS_PATTERN_1 = r"\d{1}\.\d{1}"

data = data.withColumn(
    "reviews",
    F.regexp_extract(F.col("reviews_avg"), pattern=REVIEWS_PATTERN_1, idx=0),
)


data.show(5, truncate=60)
```

### User Defined Functions (UDFs)

```python
@F.udf(returnType=StringType())
def extract_prog_language(input_: str, pattern: str) -> Any:
    """This returns a list containing the matched pattern."""
    result = re.compile(pattern=pattern, flags=re.I).findall(string=str(input_))
    result = [var.strip() for var in set(result)]
    return "|".join(result)

# Apply the udf
data = data.withColumn(
    "prog_languages_n_tools",
    extract_prog_language(F.lower(F.col("course_name")), F.lit(PATTERN)),
)

data.show(10, truncate=50)
```

### Select Unique Items In A Column

```python
# Replace null/invalid values
data.select("reviews").distinct().show(50)

# Convert to Pandas
print(data.select("reviews").distinct().toPandas()["reviews"].values)
```

### Check For Null/NaN Values

```python
df = df.select("reviews").filter(~((df["reviews"].isNull()) | (df["reviews"] == r"")))
df.show()
```

### Filter Keyword

```python
# Create a copy of the DataFrame
df = data.alias("df")

# Verify!
df.select("num_reviews").filter(df["num_reviews].isNull()).show()
df.show()
```

### When Keyword

```python
# Replace null/invalid values
data = data.withColumn(
    "reviews",
    F.when(F.col("reviews").isNull(), REPL_VALUE)
    .when(F.col("reviews") == "", REPL_VALUE)
    .otherwise(F.col("reviews"))
    .cast("double"),
)

data.show()
```

### Casting

```text
- Convert the column to a different data type.
```

```python
# Course duration and lectures count
DURATION_THRESH = 100  # hours
DURATION_REPL_VALUE = 15  # hours
LECTURES_COUNT_VALUE = 20

# Extract the patterns and replace invalid values
DURATION_PATTERN = r"\d{1,3}\.?\d{1,2}"

data = data.withColumn(
    "course_duration_hrs",
    F.regexp_extract(F.col("course_duration"), pattern=DURATION_PATTERN, idx=0),
).withColumn(
    "course_duration_hrs",
    F.when(F.col("course_duration_hrs") > DURATION_THRESH, DURATION_REPL_VALUE)
    .otherwise(F.col("course_duration_hrs"))
    .cast("double"),
)

data.show()
```

### Summary Stats

```python
# Summary stats of course rating
data.agg(
    F.min("reviews").alias("min_review"), # min
    F.max("reviews").alias("max_review"), # max
    F.round(F.avg("reviews"), 2).alias("avg_review"), # mean
    F.expr("percentile(reviews, 0.5)").alias("median_review"), # median (50% percentile)
    F.round(F.stddev("reviews"), 2).alias("std_review"), # std
).show()
```

### Group By

```python
(
  data.groupBy("course_flag")
  .agg(F.count("course_flag")
  .alias("count"))
  .show(truncate=False)
)
```

### Split Large Data

```python
# filename: split_into_parts.py

from argparse import ArgumentParser

# PySpark Modules
from pyspark.sql import SparkSession

# Create a SparkSession
spark = SparkSession.builder.getOrCreate()


def split_data() -> None:
    """This is used to split the transaction data."""
    parser = ArgumentParser()
    parser.add_argument("--input-path", help="This is the input filepath", type=str)
    parser.add_argument("--output-path", help="This is the output filepath", type=str)

    args = parser.parse_args()
    input_path, output_path = args.input_path, args.output_path

    # Load the dataset as a DataFrame
    df = spark.read.csv(input_path, header=True, inferSchema=True)
    print("================== Data has been loaded!!! ==================\n")

    # Specify the number of chunks
    NUM_CHUNKS = 3

    # Generate an array of equal weights
    WEIGHTS = [1.0 / NUM_CHUNKS] * NUM_CHUNKS

    # Split the dataset into n-chunks
    CHUNKS = df.randomSplit(WEIGHTS, seed=123)

    # Split the data into chunks
    for idx, chunk in enumerate(CHUNKS):
        # Save the chunked data
        chunk.write.csv(f"{output_path}_{idx+1}.csv", header=True)
        print(f"Chunk {idx} has been saved.")

    print("\n\t================== Done!!! ==================\n")


if __name__ == "__main__":
    split_data()

# To execute on the CLI run:
# python split_into_parts.py --input-path "data/file/path" --output-path "data/file/path"
# OR
# spark-submit split_into_parts.py --input-path "data/file/path" --output-path "data/file/path"
```
