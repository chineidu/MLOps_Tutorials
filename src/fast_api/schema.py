"""This module contains the schema for the data."""
from typing import Optional

from pydantic import BaseModel


class UserInput(BaseModel):
    """This model contains the schema for the user input."""

    name: str
    role: str
    experience: Optional[float]
    department: str

    class Config:
        """Sample Payload."""

        schema_extra = {
            "example": {
                "name": "Neidu",
                "role": "ML Engineer",
                "department": "Data",
                "experience": 3,
            }
        }


class Output(BaseModel):
    """This model contains the schema for the ML model output."""

    name: Optional[str]
    role: Optional[str]
    department: str
    experience: Optional[int]
    predicted_salary: Optional[float]


class DBOutput(BaseModel):
    """This model contains the schema for the DB output."""

    data: list[Output]
