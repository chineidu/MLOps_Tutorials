# Transformation Using Spark

- Transform ~70GB Data Using Spark.

## Table of Content

- [Transformation Using Spark](#transformation-using-spark)
  - [Table of Content](#table-of-content)
  - [Transformations Using Spark](#transformations-using-spark)
    - [PySpark Modules](#pyspark-modules)
    - [Create Spark Session](#create-spark-session)
    - [Load Data](#load-data)
    - [Drop NULLs And Duplicates](#drop-nulls-and-duplicates)
    - [Create New Columns](#create-new-columns)
    - [Delete Variables (To Save Memory)](#delete-variables-to-save-memory)
    - [Save The Data](#save-the-data)

## Transformations Using Spark

### PySpark Modules

```py
# PySpark Modules
from pyspark.sql import SparkSession
import pyspark.sql.functions as F
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    TimestampType,
    DoubleType)
from pyspark.sql.functions import year, month, concat_ws, countDistinct, col, when

```

### Create Spark Session

```py

# Create Spark Session
spark = SparkSession.builder.appName("fidelity").getOrCreate()
```

### Load Data

```py

# Define the structure for the data frame
schema = StructType([
    StructField('acid',
                StringType(), True),
    StructField('tran_date',
                TimestampType(), False),
    StructField('tran_type',
                StringType(), True),
    StructField('amount',
                DoubleType(), True),
    StructField('tran_desc',
                StringType(), True)
])

# Load all the parquet data in each sub-directory
fp: str = "s3://your/input/path/**/*.parquet"

# Applying custom schema to data frame
df = spark.read.format("parquet").schema(schema).option("header", True).load(fp)

# OR: Without applying the schema (auto-infer schema)
df = spark.read.format("parquet").option("header", True).load(fp)

```

### Drop NULLs And Duplicates

```py
## Preproessing
df_not_null = df.filter(df["tran_date"].isNotNull())
df_null = df.filter(df["tran_date"].isNull())

# Get the counts
df_not_null.count()
df_null.count()

# Drop Duplicates
df_not_null = df_not_null.distinct()

```

### Create New Columns

- Perform feature engineerng.

```py
# Add 2 new columns (year and month)
df_with_year_month = (
                        df_not_null
                        .withColumn("year", year("tran_date"))
                        .withColumn("month", month("tran_date"))
                    )

# Add a new column by concatenating (year-month)
df_with_year_month = (
                        df_with_year_month
                        .withColumn("year_month", concat_ws("-", "year", "month"))
                    )

# Group by 'acid' and count distinct 'year_month' values
grouped_df = (
              df_with_year_month
              .groupBy("acid")
              .agg(countDistinct("year_month")
              .alias("distinct_month_count"))
            )

# Filter groups having more than 6 distinct 'year_month' values
THRESH: int = 6
filtered_df = grouped_df.filter(col("distinct_month_count") >= THRESH)

# Join the data (select ONLY rows that satisfy the threshold)
result_df = df_with_year_month.join(filtered_df, "acid")

# Map tran_type to "debit", "credit"
result_df = (
                result_df
                .withColumn("tran_type", when(col("tran_type") == "D", "debit")
                .otherwise(when(col("tran_type") == "C", "credit")
                .otherwise("debit")))
            )
# Rename columns acid: customer_id, tran_date: date, tran_desc: narration
# You can also use `alias`
result_df = (
                result_df.withColumnRenamed("acid", "customer_id")
                .withColumnRenamed("tran_date", "date")
                .withColumnRenamed("tran_desc", "narration")
            )
# Drop the columns 'year', 'month', and 'year_month'
updated_df = result_df.drop(["year", "month", "distinct_month_count"])
```

### Delete Variables (To Save Memory)

```py
# Delete these variables to save data
del result_df
del df_with_year_month
del df_not_null
del df
del grouped_df
del filtered_df
```

### Save The Data

- Write to disk.

```py
# Cache the data
updated_dfx = updated_df.cache()

# Write the data to S3
s3_bucket_path: str = "s3://your/output/path/"

(
  updated_dfx.write.format("parquet")
 .partitionBy("year_month")
 .mode("overwrite")
 .save(s3_bucket_path)
)
```
