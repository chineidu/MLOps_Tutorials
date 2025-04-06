# Pydantic

## Table of Content

- [Pydantic](#pydantic)
  - [Table of Content](#table-of-content)
  - [Pydantic Settings](#pydantic-settings)

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
