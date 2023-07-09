# PySpark

## Table of Content

- [PySpark](#pyspark)
  - [Table of Content](#table-of-content)
  - [Install Java](#install-java)
  - [Basic Operations](#basic-operations)
    - [Create Spark Session](#create-spark-session)
    - [Load Data](#load-data)
    - [Drop Columns](#drop-columns)
    - [Add A New Column](#add-a-new-column)
    - [Regex](#regex)
    - [User Defined Functions (UDFs)](#user-defined-functions-udfs)
    - [Select Unique Items In A Column](#select-unique-items-in-a-column)
    - [Check For Null/NaN Values](#check-for-nullnan-values)
    - [Filter Keyword](#filter-keyword)
    - [When Keyword](#when-keyword)

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
fp = "../data/path/to/data.csv"
raw_data = spark.read.option("header", "true").option("inferSchema", "true").csv(fp)

raw_data.printSchema()
```

### Drop Columns

```python
# Drop irrelevant columns
data = raw_data.drop("_c14", "_c15", "_c16", "_c17")
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
# Create a copy of the DataFrame
df = data.alias("df")

df = df.select("reviews").filter(~((df["reviews"].isNull()) | (df["reviews"] == r"")))
df.show()
```

### Filter Keyword

```python
# Create a copy of the DataFrame
df = data.alias("df")

df = df.select("reviews").filter(~((df["reviews"].isNull()) | (df["reviews"] == r"")))
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
