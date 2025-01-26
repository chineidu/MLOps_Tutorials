import requests  # type: ignore
from . import constants

from dagster import asset


@asset
def taxi_trips_file() -> None:
    month_to_fetch: str = "2023-03"
    raw_trips = requests.get(
        (
            f"https://d37ci6vzurychx.cloudfront.net/"
            f"trip-data/yellow_tripdata_{month_to_fetch}.parquet"
        )
    )

    with open(constants.TAXI_TRIPS_TEMPLATE_FILE_PATH.format(month_to_fetch), "wb") as f:
        f.write(raw_trips.content)
