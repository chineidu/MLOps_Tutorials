"""This is used to configure the database."""
import os
from typing import Any, Optional

from pymongo import MongoClient

USERNAME, PASSWORD, HOST_NAME = (
    os.getenv("USERNAME"),
    os.getenv("PASSWORD"),
    os.getenv("HOSTNAME"),
)


def get_database(
    *, username: Optional[str], password: Optional[str], host_name: Optional[str]
) -> Any:
    """This is used to create a MongoDB connection."""
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    PORT, DB_NAME = 27017, "names"

    CONNECTION_STRING = (
        f"mongodb://{username}:{password}@{host_name}:{PORT}/{DB_NAME}?authSource=admin"
    )

    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)

    # Create the database
    return client["user_details"]


DB = get_database(username=USERNAME, password=PASSWORD, host_name=HOST_NAME)
