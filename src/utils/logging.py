"""Centralized logging framework for QBD to GnuCash conversion tool.
Version: 1.0.4

This module provides standardized logging setup and configuration
across all modules in the system.
"""
import logging
import os
from typing import Optional


def setup_logging(log_path: Optional[str] = None) -> logging.Logger:
    """Configure and return a logger instance.
    
    Args:
        log_path: Optional path to write log file. If not provided,
                 uses default path in output directory.
                 
    Returns:
        Configured logger instance
    """
    # Use default log path if none provided
    if not log_path:
        log_path = os.path.join('output', 'qbd-to-gnucash.log')
        
    # Create output directory if it doesn't exist
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    
    # Get logger for the calling module
    logger = logging.getLogger(os.path.basename(log_path))
    
    # Only add handlers if they haven't been added yet
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        
        # File handler
        fh = logging.FileHandler(log_path, encoding='utf-8')
        fh.setLevel(logging.INFO)
        
        # Console handler
        ch = logging.StreamHandler()
        ch.setLevel(logging.INFO)
        
        # Formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        fh.setFormatter(formatter)
        ch.setFormatter(formatter)
        
        # Add handlers
        logger.addHandler(fh)
        logger.addHandler(ch)
        
    return logger


def log_error(logger: logging.Logger, error: Exception, context: str = '') -> None:
    """Log an error with standard formatting.
    
    Args:
        logger: Logger instance to use
        error: Exception that was raised
        context: Optional context about where/why the error occurred
    """
    msg = f"{type(error).__name__}: {str(error)}"
    if context:
        msg = f"{context} - {msg}"
    logger.error(msg)