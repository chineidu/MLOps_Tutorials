"""This is used to configure the database."""

from pymongo import MongoClient


## TO DO: Create a mongodb connection and connect to api
def get_database():
    """This is used to create a MongoDB connection."""
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://mongodb:27017/names"

    # Create a connection using MongoClient.
    client = MongoClient(CONNECTION_STRING)

    # Create the database
    return client['user_details']


DB = get_database()
