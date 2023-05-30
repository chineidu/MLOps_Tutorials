"""This module contains the schema for the data."""
from pydantic import BaseModel


class UserInput(BaseModel):
    """This model contains the schema for the user input."""

    name: str

    class Config:
        """Sample Payload."""

        schema_extra = {
            "example": {
                "name": "Chukwudi",
            }
        }


class Output(BaseModel):
    """This model contains the schema for the API output."""

    count: int
    gender: str
    name: str
    probability: float
