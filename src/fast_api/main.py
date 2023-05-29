"""This module contains simple API endpoints."""
from typing import Any

from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse

from src.fast_api.schema import DBOutput, Output, UserInput
from src.utilities import DB, _make_prediction, _save_json_data, logger

app = FastAPI()
API_NAME = 'Sample API'


@app.get(path='/', status_code=status.HTTP_200_OK)
def index() -> Any:
    """This is the index. It returns a basic HTML response."""
    body = f"""
            <html>
                <body style='padding: 15px;'>
                    <h1>Welcome to the {API_NAME}</h1>
                    <div>
                    Check the docs: <a href='/docs'>here</a>
                    </div>
                </body>
            </html>
    """
    return HTMLResponse(content=body)


@app.post(path='/predict', status_code=status.HTTP_200_OK)
def predict_income(user_input: UserInput) -> Output:
    """This is used to predict the user's income."""

    # Parse the input
    name, role = user_input.name, user_input.role
    result = _make_prediction(name=name, role=role)
    # Save data to a file
    _save_json_data(data=result)
    # Update the database
    DB["data"].append(result)

    return result  # type: ignore


@app.get(path="/users", status_code=status.HTTP_200_OK)
def get_results() -> DBOutput:
    """This returns the data stored in the database."""
    return DB  # type: ignore


if __name__ == '__main__':
    import uvicorn

    host, port = "0.0.0.0", 8000

    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")

    # Run the server
    uvicorn.run("main:app", host=host, port=port, log_level="info", reload=True)
