"""Module with logging configuration."""

import logging
import sys


def setup_logging(log_level: str = 'info'):
    """Configure application logging.

    :param log_level: Logging level string.
    """
    level = getattr(logging, log_level.upper(), logging.INFO)

    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    root_logger.handlers.clear()

    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )
    handler.setFormatter(formatter)

    root_logger.addHandler(handler)

    return logging.getLogger(__name__)
