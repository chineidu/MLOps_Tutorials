import os
import requests  # type: ignore

from dagster import asset
from dagster._utils.backoff import backoff
import duckdb
from . import constants


@asset
def taxi_trips_file() -> None:
    """Download taxi trip data from NYC Open Data and save to local file."""
    month_to_fetch: str = "2023-03"
    raw_trips: requests.Response = requests.get(
        (
            f"https://d37ci6vzurychx.cloudfront.net/"
            f"trip-data/yellow_tripdata_{month_to_fetch}.parquet"
        )
    )

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb") as f:
        f.write(raw_trips.content)


@asset
def taxi_zones_file() -> None:
    """Download NYC taxi zones data rom NYC Open Data Portal and save to local file."""
    # taxi_zones: requests.Response = requests.get(
    #     "https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD"
    # )

    # with open(constants.TAXI_ZONES_FILE_PATH, "wb") as f:
    #     f.write(taxi_zones.content)
    with open(constants.TAXI_ZONES_FILE_PATH, "rb") as f:
        raw_zones = f.read()


@asset(deps=["taxi_trips_file"])
def taxi_trips() -> None:
    """Create a table 'trips' in DuckDB from taxi trip data.

    This function loads taxi trip data from a Parquet file into a DuckDB table,
    transforming and renaming columns for analysis.

    Returns
    -------
    None
    """
    query: str = """
        CREATE OR REPLACE TABLE trips AS (
            SELECT
                VendorID as vendor_id,
                PULocationID as pickup_location_id,
                RateCodeID as rate_code_id,
                payment_type as payment_type,
                tpep_dropoff_datetime as dropoff_datetime,
                tpep_pickup_datetime as pickup_datetime,
                trip_distance as trip_distance,
                passenger_count as passenger_count,
                total_amount as total_amount,

            from 'data/raw/taxi_trips_2023-03.parquet'
        );
    """
    conn: duckdb.DuckDBPyConnection = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={
            "database": os.getenv("DUCKDB_DATABASE"),
        },
        max_retries=10,
    )
    conn.execute(query)


@asset(deps=["taxi_zones_file"])
def taxi_zones() -> None:
    """Create a table 'zones' in DuckDB from taxi zone data.

    This function loads NYC taxi zone data from a CSV file into a DuckDB table,
    transforming and renaming columns for analysis.

    Returns
    -------
    None
    """
    query: str = f"""
        CREATE OR REPLACE TABLE zones AS (
            SELECT
                LocationID as zone_id,
                Borough as borough,
                Zone as zone,
                the_geom as geometry,
            from '{constants.TAXI_ZONES_FILE_PATH}'
        );
    """
    conn: duckdb.DuckDBPyConnection = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={
            "database": os.getenv("DUCKDB_DATABASE"),
        },
        max_retries=10,
    )
    conn.execute(query)
