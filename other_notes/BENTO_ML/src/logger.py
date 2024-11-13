"""
This module is contains the logger.

author: Chinedu Ezeofor
"""

import logging

from rich.logging import RichHandler
from typeguard import typechecked


@typechecked
def get_rich_logger(name: str | None = "richLogger") -> logging.Logger:
    """This is used to create a logger object with RichHandler."""

    # Create logger if it doesn't exist
    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.DEBUG)

        # Create console handler with formatting
        console_handler = RichHandler(
            rich_tracebacks=True,
            level=logging.DEBUG,
            log_time_format="%y-%m-%d %H:%M:%S",
        )
        console_handler.setLevel(logging.DEBUG)
        formatter = logging.Formatter("%(message)s")
        console_handler.setFormatter(formatter)

        # Add console handler to the logger
        logger.addHandler(console_handler)

    return logger


logger = get_rich_logger()
