from typing import Literal
from urllib.parse import quote

from dotenv import load_dotenv
from pydantic import SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Settings class for managing application configuration.
    """

    model_config = SettingsConfigDict(env_file=".env")

    # ======= OpenRouter =======
    OPENROUTER_API_KEY: SecretStr = SecretStr("your_api_key_here")
    OPENROUTER_URL: str = "https://openrouter.ai/api/v1"

    # ======= Groq =======
    GROQ_API_KEY: SecretStr = SecretStr("your_groq_api_key_here")
    GROQ_URL: str = "https://api.groq.ai/openai/v1"

    # @field_validator("RABBITMQ_PORT", "MYSQL_PORT", mode="before")
    # @classmethod
    # def parse_port_fields(cls, v: str | int) -> int:
    #     """Parses port fields to ensure they are integers."""
    #     if isinstance(v, str):
    #         try:
    #             return int(v.strip())
    #         except ValueError:
    #             raise ValueError(f"Invalid port value: {v}") from None

    #     if isinstance(v, int) and not (1 <= v <= 65535):
    #         raise ValueError(f"Port must be between 1 and 65535, got {v}")

    #     return v

    # @property
    # def rabbitmq_url(self) -> str:
    #     """Constructs the RabbitMQ connection URL."""
    #     passwd: str = quote(self.RABBITMQ_DEFAULT_PASS.get_secret_value(), safe="")
    #     raw_vhost: str = (self.VIRTUAL_HOST or "").strip()

    #     # Normalize vhost to ensure it starts with a slash
    #     if not raw_vhost:
    #         normalized_vhost: str = "/"
    #     else:
    #         normalized_vhost = raw_vhost if raw_vhost.startswith("/") else f"/{raw_vhost}"
    #     encoded_vhost: str = quote(normalized_vhost, safe="")

    #     return (
    #         f"amqp://{self.RABBITMQ_DEFAULT_USER}:{passwd}@"
    #         f"{self.RABBITMQ_HOST}:{self.RABBITMQ_PORT}/{encoded_vhost}"
    #         f"?heartbeat={self.RABBITMQ_HEARTBEAT}"
    #     )

    # @property
    # def celery_database_url(self) -> str:
    #     """
    #     Constructs the PostgreSQL connection URL.

    #     Returns
    #     -------
    #     str
    #         Complete PostgreSQL connection URL in the format:
    #         - db+postgresql://user:password@host:port/dbname
    #         - db+mysql://user:password@host:port/dbname
    #     """

    #     password: str = quote(self.MYSQL_PASSWORD.get_secret_value(), safe="")
    #     url: str = (
    #         f"db+mysql+pymysql://{self.MYSQL_USER}:{password}"
    #         f"@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}?charset=utf8mb4"
    #     )

    #     return url

    # @property
    # def database_url(self) -> str:
    #     """
    #     Constructs the database connection URL.

    #     Returns
    #     -------
    #     str
    #         Complete database connection URL in the format:
    #         - postgresql+psycopg2://user:password@host:port/dbname
    #         - mysql+pymysql://user:password@host:port/dbname
    #     """
    #     password: str = quote(self.MYSQL_PASSWORD.get_secret_value(), safe="")
    #     url: str = f"mysql+pymysql://{self.MYSQL_USER}:{password}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"

    #     return url


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

    return Settings()  # type: ignore


app_settings: Settings = refresh_settings()
