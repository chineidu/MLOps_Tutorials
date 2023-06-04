"""This is used to configure the database."""
import os
from typing import Optional

from pymongo import MongoClient

USERNAME, PASSWORD = os.getenv("USERNAME"), os.getenv("PASSWORD")


def get_database(*, username: Optional[str], password: Optional[str]):
    """This is used to create a MongoDB connection."""
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    HOST_NAME, PORT, DB_NAME = "mongodb", 27017, "names"

    CONNECTION_STRING = (
        f"mongodb://{username}:{password}@{HOST_NAME}:{PORT}/{DB_NAME}?authSource=admin"
    )

    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)

    # Create the database
    return client["user_details"]


DB = get_database(username=USERNAME, password=PASSWORD)
