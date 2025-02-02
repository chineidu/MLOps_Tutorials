import requests  # type: ignore
from . import constants

from dagster import asset


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
    taxi_zones: requests.Response = requests.get(
        "https://data.cityofnewyork.us/api/views/755u-8jsi/rows.csv?accessType=DOWNLOAD"
    )

    with open(constants.TAXI_ZONES_FILE_PATH, "wb") as f:
        f.write(taxi_zones.content)
