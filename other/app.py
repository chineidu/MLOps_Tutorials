"""This module contains an API endpoint connected to a WWW."""
import os
from typing import Any

import requests
from fastapi import FastAPI, status

from other.schema import Output, UserInput
from src.utilities import logger

app = FastAPI()
API_NAME = 'Sample API'


@app.get(path='/', status_code=status.HTTP_200_OK)
def index() -> Any:
    """This is the homepage."""
    return {"message": "This API is working!"}


@app.post(path='/predict', status_code=status.HTTP_200_OK)
def predict_gender(name: UserInput) -> Output:
    """This is used to predict a person's gender based on the name."""

    URL = f"https://api.genderize.io?name={name.name}"
    response = requests.get(url=URL)

    return response.json()


if __name__ == '__main__':
    import uvicorn

    HOST, PORT = "0.0.0.0", int(os.getenv("PORT", 6060))  # pylint:disable=invalid-envvar-default

    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")

    # Run the server
    uvicorn.run("app:app", host=HOST, port=PORT, log_level="info", reload=True)
