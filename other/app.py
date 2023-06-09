"""This module contains an API endpoint connected to a WWW."""
import logging
import os
from typing import Any

import requests
from fastapi import FastAPI, status
from get_database import DB
from schema import Output, UserInput

app = FastAPI()
CONTAINER_NAME, OTHER_PORT = "cool_app", 8000
OTHER_URL = os.getenv("OTHER_URL", f"http://{CONTAINER_NAME}:{OTHER_PORT}/users")

VERSION = "1.1"


@app.get(path='/', status_code=status.HTTP_200_OK)
def index() -> Any:
    """This is the homepage."""
    return {"message": "This API is working!", "api_version": VERSION}


@app.post(path='/predict', status_code=status.HTTP_200_OK, response_model=Output)
def predict_gender(name: UserInput) -> Output:
    """This is used to predict a person's gender based on the name."""

    URL = f"https://api.genderize.io?name={name.name}"
    response = requests.get(url=URL)

    # Add collection
    users_collection = DB["users"]
    # Save data
    users_collection.insert_one(response.json())

    return response.json()


@app.get(path='/users', status_code=status.HTTP_200_OK)
def get_users() -> list[str]:
    """This returns the data in the database."""
    documents = DB["users"].find()

    # Convert documents to a list of dicts
    user_data = [str(doc) for doc in documents]

    return user_data


@app.get(path='/other_users', status_code=status.HTTP_200_OK)
def get_other_users() -> Any:
    """This returns the data in the database. This is connected to a server
    running on another container."""
    response = requests.get(url=OTHER_URL)
    return response.json()


if __name__ == '__main__':
    import uvicorn

    HOST, PORT = "0.0.0.0", int(os.getenv("PORT", 6060))  # pylint:disable=invalid-envvar-default

    # Use this for debugging purposes only
    logging.warning("Running in development mode. Do not run like this in production.")

    # Run the server
    uvicorn.run("app:app", host=HOST, port=PORT, log_level="info", reload=True)
