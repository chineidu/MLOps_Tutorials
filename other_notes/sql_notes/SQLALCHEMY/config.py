import logging
import sys
from contextlib import contextmanager
from pathlib import Path
from typing import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import QueuePool
from src.config.settings import refresh_settings

settings = refresh_settings()
PACKAGE_PATH = Path(__file__).parent.parent.absolute()


def create_logger(
    name: str = "logger",
    log_level: int = logging.INFO,
    log_file: str | None = None,
) -> logging.Logger:
    """
    Create a configured logger with custom date formatting.

    Parameters:
    -----------
    name : str, optional
        Name of the logger, by default 'logger'
    log_level : int, optional
        Logging level, by default logging.INFO
    log_file : str, optional
        Path to log file. If None, logs to console, by default None

    Returns:
    --------
    logging.Logger
        Configured logger instance
    """
    # Create logger
    logger = logging.getLogger(name)
    logger.setLevel(log_level)
    logger.propagate = False  # Don't propagate to parent loggers

    # Clear any existing handlers
    logger.handlers.clear()

    # Create formatter with YYYY-MM-DD HH:MM:SS format
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - [%(levelname)s] - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(log_level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger

logger = create_logger(name="database_utils")

class DatabasePool:
    """Database connection pool with automatic reconnection."""

    def __init__(self, database_url: str) -> None:
        """Initialize"""
        self.database_url: str = database_url
        self._engine: Engine | None = None
        self._session_factory: sessionmaker[Session] | None = None
        self._setup_engine()

    def _setup_engine(self) -> None:
        """Set up the database engine and session factory."""
        self._engine = create_engine(
            self.database_url,
            poolclass=QueuePool,
            pool_size=10,  # Keep 10 connections in pool
            max_overflow=5,  # Allow N extra connections
            pool_timeout=10,  # Wait N seconds for connection
            pool_recycle=1_800,  # Recycle connections after 30 minutes
            pool_pre_ping=True,  # Test connections before use
            echo=False,
        )

        self._session_factory = sessionmaker(bind=self._engine, expire_on_commit=True)
        logger.info("Database connection pool initialized")

    @contextmanager
    def get_session(self) -> Generator[Session, None, None]:
        """Get a database session with automatic commit/rollback."""
        if not self._session_factory:
            raise RuntimeError("Session factory not initialized")

        session: Session = self._session_factory()
        try:
            yield session
            session.commit()

        except Exception:
            session.rollback()
            raise

        finally:
            session.close()

    def health_check(self) -> bool:
        """Check if database is healthy."""
        try:
            with self.get_session() as session:
                session.execute(text("SELECT 1"))
            return True
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def close(self) -> None:
        """Close connection pool."""
        if self._engine:
            self._engine.dispose()
            logger.info("Database pool closed")

    @property
    def engine(self) -> Engine:
        """Get database engine."""
        if self._engine is None:
            raise RuntimeError("Database engine is not initialized.")
        return self._engine


__all__: list[str] = ["PACKAGE_PATH", "create_logger"]
