from datetime import datetime, timedelta
import os
from dagster import asset
from dagster._utils.backoff import backoff
import duckdb
import geopandas as gpd
import matplotlib.pyplot as plt
import pandas as pd
import polars as pl

pl.Config.set_tbl_cols(n=1_000)

from . import constants


@asset(deps=["taxi_trips", "taxi_zones"])
def manhattan_stats() -> None:
    query = """
        select
            zones.zone,
            zones.borough,
            zones.geometry,
            count(1) as num_trips,
        from trips
        left join zones on trips.pickup_location_id = zones.zone_id
        where borough = 'Manhattan' and geometry is not null
        group by zone, borough, geometry
    """

    conn = duckdb.connect(os.getenv("DUCKDB_DATABASE"))
    trips_by_zone = conn.execute(query).fetch_df()

    trips_by_zone["geometry"] = gpd.GeoSeries.from_wkt(trips_by_zone["geometry"])
    trips_by_zone = gpd.GeoDataFrame(trips_by_zone)

    with open(constants.MANHATTAN_STATS_FILE_PATH, "w") as output_file:
        output_file.write(trips_by_zone.to_json())


@asset(deps=["manhattan_stats"])
def manhattan_map() -> None:
    trips_by_zone = gpd.read_file(constants.MANHATTAN_STATS_FILE_PATH)

    fig, ax = plt.subplots(figsize=(10, 10))
    trips_by_zone.plot(column="num_trips", cmap="plasma", legend=True, ax=ax, edgecolor="black")
    ax.set_title("Number of Trips per Taxi Zone in Manhattan")

    ax.set_xlim([-74.05, -73.90])  # Adjust longitude range
    ax.set_ylim([40.70, 40.82])  # Adjust latitude range

    # Save the image
    plt.savefig(constants.MANHATTAN_MAP_FILE_PATH, format="png", bbox_inches="tight")
    plt.close(fig)


# @asset(deps=["taxi_trips"])
# def trips_by_week() -> None:
#     """Aggregate taxi trip data by week and save to CSV.

#     This function processes taxi trip data, aggregating metrics like number of trips,
#     total amount, trip distance, and passenger count on a weekly basis from March to
#     April 2023. Results are saved to a CSV file.

#     Returns
#     -------
#     None
#         Writes results to a CSV file specified by TRIPS_BY_WEEK_FILE_PATH.
#     """
#     fp: str = constants.TRIPS_BY_WEEK_FILE_PATH
#     conn: duckdb.DuckDBPyConnection = backoff(
#         fn=duckdb.connect,
#         retry_on=(RuntimeError, duckdb.IOException),
#         kwargs={"database": os.getenv("DUCKDB_DATABASE")},
#         max_retries=10,
#     )
#     current_date: datetime = datetime.strptime("2023-03-01", constants.DATE_FORMAT)
#     end_date: datetime = datetime.strptime("2023-04-01", constants.DATE_FORMAT)
#     result: pl.DataFrame = pl.DataFrame()

#     while current_date < end_date:
#         current_date_str: str = current_date.strftime(constants.DATE_FORMAT)
#         query: str = """
#         SELECT
#             vendor_id, total_amount, trip_distance, passenger_count
#         FROM trips
#         WHERE date_trunc('week', pickup_datetime) = date_trunc('week', '{current_date_str}'::date)
#         """
#         data_for_week: pl.DataFrame = conn.execute(query).pl()
#         aggregated_df: pl.DataFrame = data_for_week.select(
#             pl.col("vendor_id").count().cast(pl.Int64).alias("num_trips"),
#             pl.col("total_amount").sum().count().cast(pl.Float32).round(2),
#             pl.col("trip_distance").sum().count().cast(pl.Float32).round(2),
#             pl.col("passenger_count").sum().count().cast(pl.Int64),
#             pl.lit(current_date).alias("period"),
#         )
#         result = pl.concat([result, aggregated_df], how="vertical")
#         current_date = current_date + timedelta(days=7)
#     aggregated_df = aggregated_df.sort("period")
#     aggregated_df.write_csv(fp)


@asset(deps=["taxi_trips"])
def trips_by_week() -> None:
    conn = backoff(
        fn=duckdb.connect,
        retry_on=(RuntimeError, duckdb.IOException),
        kwargs={
            "database": os.getenv("DUCKDB_DATABASE"),
        },
        max_retries=10,
    )

    current_date = datetime.strptime("2023-03-01", constants.DATE_FORMAT)
    end_date = datetime.strptime("2023-04-01", constants.DATE_FORMAT)

    result = pd.DataFrame()

    while current_date < end_date:
        current_date_str = current_date.strftime(constants.DATE_FORMAT)
        query = f"""
            select
                vendor_id, total_amount, trip_distance, passenger_count
            from trips
            where date_trunc('week', pickup_datetime) = date_trunc('week', '{current_date_str}'::date)
        """

        data_for_week = conn.execute(query).fetch_df()

        aggregate = (
            data_for_week.agg(
                {
                    "vendor_id": "count",
                    "total_amount": "sum",
                    "trip_distance": "sum",
                    "passenger_count": "sum",
                }
            )
            .rename({"vendor_id": "num_trips"})
            .to_frame()
            .T
        )  # type: ignore

        aggregate["period"] = current_date

        result = pd.concat([result, aggregate])

        current_date += timedelta(days=7)

    # clean up the formatting of the dataframe
    result["num_trips"] = result["num_trips"].astype(int)
    result["passenger_count"] = result["passenger_count"].astype(int)
    result["total_amount"] = result["total_amount"].round(2).astype(float)
    result["trip_distance"] = result["trip_distance"].round(2).astype(float)
    result = result[["period", "num_trips", "total_amount", "trip_distance", "passenger_count"]]
    result = result.sort_values(by="period")

    result.to_csv(constants.TRIPS_BY_WEEK_FILE_PATH, index=False)


def func_for_debugging():
    query: str = """
        SELECT
            *
        FROM trips
        LIMIT 100;
    """
    conn = duckdb.connect(database="data/staging/data.duckdb")
    df: pl.DataFrame = conn.execute(query).pl()
    current_date: datetime = datetime.strptime("2023-03-01", constants.DATE_FORMAT)
    # print(df)
    aggregated_df: pl.DataFrame = df.select(
        pl.col("vendor_id").count().alias("num_trips"),
        pl.col("total_amount").sum(),
        pl.col("trip_distance").sum(),
        pl.col("passenger_count").sum(),
        period=pl.lit(current_date),
    )
    print(aggregated_df)
    print(df.head(5))


if __name__ == "__main__":
    # func_for_debugging()
    pass
