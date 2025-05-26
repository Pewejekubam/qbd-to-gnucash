# Agentic affirmation: This script is compliant with PRD v3.6.3 and Governance Document v2.3.10.

import logging
from logging import Logger
from typing import Optional


def get_logger(log_path: str) -> Logger:
    """
    Set up and return a structured logger writing to the specified log file.
    Args:
        log_path (str): Path to the log file.
    Returns:
        Logger: Configured logger instance.
    """
    logger = logging.getLogger("qbd-to-gnucash")
    logger.setLevel(logging.INFO)
    # Remove all handlers if re-initializing
    if logger.hasHandlers():
        logger.handlers.clear()
    handler = logging.FileHandler(log_path, encoding="utf-8")
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


def flush_logs(logger: Logger) -> None:
    """
    Flush all handlers for the given logger (ensures logs are written to disk).
    Args:
        logger (Logger): Logger instance to flush.
    """
    for handler in logger.handlers:
        handler.flush()