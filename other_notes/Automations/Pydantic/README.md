# Pydantic

## Table of Content

- [Pydantic](#pydantic)
  - [Table of Content](#table-of-content)
  - [Pydantic Models](#pydantic-models)
  - [Pydantic Settings](#pydantic-settings)

## Pydantic Models

```py
from datetime import datetime
from typing import Annotated, Any, Literal
from uuid import uuid4

from pydantic import BaseModel, BeforeValidator, ConfigDict, Field, field_serializer  # type: ignore
from pydantic.alias_generators import to_camel


def round_probability(value: float) -> float:
    """Round a float value to two decimal places.

    Returns:
        float: Rounded value.
    """
    if isinstance(value, float):
        return round(value, 2)
    return value


class BaseSchema(BaseModel):
    """Base schema class that inherits from Pydantic BaseModel.

    This class provides common configuration for all schema classes including
    camelCase alias generation, population by field name, and attribute mapping.
    """

    model_config: ConfigDict = ConfigDict(  # type: ignore
        alias_generator=to_camel,
        populate_by_name=True,
        from_attributes=True,
        arbitrary_types_allowed=True,
    )


Float = Annotated[float, BeforeValidator(round_probability)]


class PersonSchema(BaseSchema):
    """Schema for a person."""

    id: str | None = Field(default=None, description="Unique identifier for the person.")
    sex: Literal["male", "female"] = Field(description="Sex of the passenger.")
    age: Float = Field(description="Age of the passenger.")
    pclass: int = Field(description="Passenger class.")
    sibsp: int = Field(description="Number of siblings/spouses aboard.")
    parch: int = Field(description="Number of parents/children aboard.")
    fare: Float = Field(description="Fare paid for the ticket.")
    embarked: Literal["s", "c", "q"] = Field(description="Port of embarkation.")
    survived: int = Field(default=0, description="Survival status of the passenger.")
    timestamp: datetime = Field(default_factory=datetime.now, description="Timestamp of the entry.")

    @field_serializer("timestamp")
    def serialize_datetimes(self, v: datetime) -> str:
        """Serializes datetime fields to ISO format."""
        return v.isoformat()


class MultiPersonsSchema(BaseSchema):
    """Schema for multiple people."""

    persons: list[PersonSchema] = Field(description="List of people.")

```

## Pydantic Settings

```py
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    """
    Settings class for managing application configuration.
    """

    model_config = SettingsConfigDict(env_file=".env")

    # RabbitMQ settings
    RABBITMQ_HOST: str
    RABBITMQ_PORT: int
    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: SecretStr
    RABBITMQ_EXPIRATION_MS: int
    RABBITMQ_FANOUT_EXCHANGE: str
    RABBITMQ_DIRECT_EXCHANGE: str
    RABBITMQ_PRESENCE_EXCHANGE: str

    # Database settings
    DATABASE_PREFIX: str
    DATABASE_HOST: str
    DATABASE_PORT: int
    DATABASE_USER: str
    DATABASE_PASSWORD: SecretStr
    DATABASE_NAME: str

    # JWT settings
    JWT_SECRET_KEY: SecretStr
    JWT_ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int

    # WebSocket settings
    WS_HEARTBEAT_INTERVAL: int

    @property
    def database_url(self) -> str:
        return (
            f"{self.DATABASE_PREFIX}{self.DATABASE_USER}:{self.DATABASE_PASSWORD.get_secret_value()}"
            f"@{self.DATABASE_HOST}:{self.DATABASE_PORT}/{self.DATABASE_NAME}"
        )

    @property
    def rabbitmq_url(self) -> str:
        """
        Constructs the RabbitMQ connection URL.

        Returns
        -------
        str
            Complete RabbitMQ connection URL in the format:
            amqp://user:password@host:port/
        """
        return (
            f"amqp://{self.RABBITMQ_USER}:{self.RABBITMQ_PASSWORD.get_secret_value()}"
            f"@{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/"
        )

def refresh_settings() -> Settings:
    """Refresh environment variables and return new Settings instance.

    This function reloads environment variables from .env file and creates
    a new Settings instance with the updated values.

    Returns
    -------
    Settings
        A new Settings instance with refreshed environment variables
    """
    load_dotenv(override=True)
    return Settings()

settings: Settings = refresh_settings()
```
