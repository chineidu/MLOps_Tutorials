"""This module contains simple API endpoints."""
from typing import Any

from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from src.utilities import logger

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


@app.get(path='/message', status_code=status.HTTP_200_OK)
def home() -> dict[str, str]:
    """This is the homepage."""
    return {"message": "The API is functional!"}


if __name__ == '__main__':
    import uvicorn

    host, port = "0.0.0.0", 8000

    # Use this for debugging purposes only
    logger.warning("Running in development mode. Do not run like this in production.")

    # Run the server
    uvicorn.run("main:app", host=host, port=port, log_level="info", reload=True)
