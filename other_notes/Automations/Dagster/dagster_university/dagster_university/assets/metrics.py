import os
from dagster import asset
import matplotlib.pyplot as plt
import geopandas as gpd
import duckdb

from . import constants


@asset(
    deps=["taxi_trips", "taxi_zones"],
)
def manhattan_stats() -> None:
    query: str = """
        SELECT
            zones.zone,
            zones.borough,
            zones.geometry,
            COUNT(1) AS num_trips,
        FROM trips
            LEFT JOIN zones
            ON trips.pickup_location_id = zones.zone_id
        WHERE borough = 'Manhattan' AND geometry IS NOT NULL
        GROUP BY zone, borough, geometry
    """
    conn = duckdb.connect(os.getenv("DUCKDB_DATABASE"))
    trips_by_zone = conn.execute(query).fetch_df()
    trips_by_zone["geometry"] = gpd.GeoSeries.from_wkt(trips_by_zone["geometry"])
    trips_by_zone = gpd.GeoDataFrame(trips_by_zone)

    with open(constants.MANHATTAN_STATS_FILE_PATH, "w") as f:
        f.write(trips_by_zone.to_json())


@asset(deps=["manhattan_stats"])
def manhattan_map() -> None:
    trips_by_zone = gpd.read_file(constants.MANHATTAN_STATS_FILE_PATH)

    fig, ax = plt.subplots(figsize=(10, 10))
    trips_by_zone.plot(column="num_trips", cmap="plasma", legend=True, ax=ax, edgecolor="black")
    ax.set_title("Number of Trips per Taxi Zone in Manhattan")

    ax.set_xlim([-74.05, -73.90])  # Longitude
    ax.set_ylim([40.70, 40.82])  # Latitude

    plt.savefig(constants.MANHATTAN_MAP_FILE_PATH, format="png", bbox_inches="tight")
    plt.close(fig)


@asset(deps=["taxi_trips"])
def trips_by_week() -> None:
    fp: str = constants.TRIPS_BY_WEEK_FILE_PATH
    # period, num_trips, passenger_count, total_amount, trip_distance

    query: str = """
        SELECT
            pickup_datetime AS period,
            COUNT(1) AS num_trips,
            SUM(passenger_count) AS passenger_count,
            SUM(total_amount) AS total_amount,
            SUM(trip_distance) AS trip_distance
        FROM trips
        WHERE pickup_datetime BETWEEN '2023-01-01' AND '2023-01-07'
        GROUP BY period
    """
    conn = duckdb.connect(os.getenv("DUCKDB_DATABASE"))
    trips_by_week = conn.execute(query).fetch_df()
    trips_by_week.to_csv(fp, index=False)


# SELECT table_name
# FROM information_schema.tables
# WHERE table_schema = 'main';

# SELECT column_name, data_type
# FROM information_schema.columns
# WHERE table_name = 'your_table_name' AND table_schema = 'main';

# [
#     ("vendor_id", "INTEGER"),
#     ("pickup_location_id", "INTEGER"),
#     ("rate_code_id", "BIGINT"),
#     ("payment_type", "BIGINT"),
#     ("dropoff_datetime", "TIMESTAMP"),
#     ("pickup_datetime", "TIMESTAMP"),
#     ("trip_distance", "DOUBLE"),
#     ("passenger_count", "BIGINT"),
#     ("total_amount", "DOUBLE"),
# ]
