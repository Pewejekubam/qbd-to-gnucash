"""Improved logging facility for QBD to GnuCash conversion with domain tagging.

This module provides user-focused console logging with technical details in file logs.
Updated to remove 'root:' logger names and 'AUDIT:' prefixes per logging specification.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Optional

from .error_handler import ConversionError

def setup_logging(log_file: Optional[str] = None) -> None:
    """Initialize the logging system with user-focused console and detailed file logging.
    
    Args:
        log_file: Optional path to the log file. If not provided, defaults to 'output/qbd-to-gnucash.log'
    """
    if not log_file:
        log_file = os.path.join('output', 'qbd-to-gnucash.log')
    
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    
    # Configure root logger to capture everything
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    
    # Clear any existing handlers
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Console handler - INFO level only, user-focused messages
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    # Remove 'root:' from console format - just show the message
    console_formatter = logging.Formatter('%(message)s')
    console_handler.setFormatter(console_formatter)
    
    # File handler - DEBUG level, technical details with UTF-8 encoding
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.DEBUG)
    # Remove 'root:' from file format - show timestamp, level, and message only
    file_formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(message)s')
    file_handler.setFormatter(file_formatter)
    
    # Add handlers to root logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    
    # Log startup message to console (user-focused) with domain tag
    logging.info("[CORE] QBD to GnuCash Conversion Tool - Started")
    
    # Log detailed startup to file only with domain tag
    logging.debug("[CORE] Detailed logging initialized: " + log_file)
    logging.debug("[CORE] Console logging: INFO level (user-focused)")
    logging.debug("[CORE] File logging: DEBUG level (technical details)")

def log_user_info(message: str) -> None:
    """Log user-focused information to console and file."""
    logging.info(message)

def log_user_success(message: str) -> None:
    """Log user success message to console and file."""
    # Use ASCII 'SUCCESS:' instead of unicode checkmark
    logging.info(f"SUCCESS: {message}")

def log_user_error(message: str, log_reference: str = None) -> None:
    """Log user error with guidance to console and detailed info to file.
    
    Args:
        message: User-friendly error message
        log_reference: Optional reference to log section for details
    """
    # Use ASCII 'ERROR:' instead of unicode X mark
    error_msg = f"ERROR: {message}"
    if log_reference:
        error_msg += f" (see logs: {log_reference})"
    logging.error(error_msg)

def log_technical_detail(message: str) -> None:
    """Log technical details to file only (DEBUG level) - removed AUDIT prefix."""
    # Remove AUDIT: prefix per logging specification
    logging.debug(message)

def log_module_registration(module_key: str) -> None:
    """Log module registration - file only with domain tag."""
    logging.debug(f"[CORE] Module registered - {module_key} module key -> processing function")

def log_unregistered_module_key(module_key: str, record_count: int) -> None:
    """Log unregistered module key - file only with domain tag."""
    logging.debug(f"[CORE] Module key not registered - {module_key} ({record_count} module key records) - no processing module available")
    logging.debug(f"[CORE] To process {module_key} module keys, register a module with: register_global_module('{module_key}', module_function)")

def log_field_mismatch(line_number: int, section: str, expected: int, got: int) -> None:
    """Log field count mismatch - file only with domain tag."""
    logging.debug(f"[IIF-PARSER] Field count mismatch at line {line_number} in section {section}. Expected {expected}, got {got}")

def log_config_mapping(account_name: str, qbd_type: str, gnucash_type: str, hierarchy: str) -> None:
    """Log detailed config mapping - file only."""
    logging.debug(f"[ACCOUNTS-MAPPING] Mapped account '{account_name}' ({qbd_type}) -> {gnucash_type} at {hierarchy}")

def log_config_placement(account_name: str, hierarchy: str, gnucash_type: str) -> None:
    """Log account placement - file only."""
    logging.debug(f"[ACCOUNTS-TREE] Placed account '{account_name}' under '{hierarchy}' as {gnucash_type}")

def log_file_processing_start(file_path: str) -> None:
    """Log start of file processing - user focused."""
    filename = os.path.basename(file_path)
    log_technical_detail(f"[CORE] Begin content-based processing - {file_path}")
    # Console shows filename only for cleaner output
    
def log_file_processing_result(file_path: str, module_keys_found: int, total_records: int, processed_modules: list = None) -> None:
    """Log file processing results - user focused.
    
    Args:
        file_path: Path to the processed file
        module_keys_found: Number of module keys discovered
        total_records: Total module key records processed
        processed_modules: List of successfully processed modules with results
    """
    filename = os.path.basename(file_path)
    
    if processed_modules:
        for module_result in processed_modules:
            module_name = module_result.get('module', 'unknown')
            output_file = module_result.get('output', 'unknown')
            account_count = module_result.get('count', 'unknown')
            log_user_success(f"[CORE] Processing {filename} -> {module_name} module -> {output_file} ({account_count} accounts)")
    else:
        # File processed but no modules handled the content
        log_user_info(f"[CORE] Processing {filename}: {module_keys_found} module keys found, {total_records} module key records processed")
        log_user_info(f"[CORE] No registered modules for discovered module keys")

def log_pipeline_summary(total_files: int, processed_sections: int) -> None:
    """Log final pipeline summary - user focused."""
    if processed_sections > 0:
        log_user_success(f"[CORE] Conversion completed: {processed_sections} modules processed from {total_files} files")
    else:
        log_user_info(f"[CORE] Conversion completed: {total_files} files processed, no module key records handled")
        log_user_info("[CORE] To process additional data types, register modules for the discovered module keys")

def log_file_discovery(file_list: list) -> None:
    """Log discovered files - user focused."""
    log_user_info(f"[CORE] Discovered {len(file_list)} IIF files for processing:")
    for file_path in file_list:
        filename = os.path.basename(file_path)
        log_user_info(f"[CORE]   * {filename}")

def log_iif_parsing_summary(file_path: str, sections_found: int, lines_processed: int) -> None:
    """Log IIF parsing completion - technical detail only."""
    log_technical_detail(f"[CORE] IIF parsing completed - {file_path} -> {sections_found} module keys discovered, {lines_processed} lines processed")

def log_module_dispatch(module_key: str, record_count: int) -> None:
    """Log module dispatch - technical detail only."""
    log_technical_detail(f"[CORE] Module dispatch - {record_count} {module_key} module key records -> registered module")

def log_module_success(module_key: str, result: str = None) -> None:
    """Log module completion - technical detail only."""
    if result:
        log_technical_detail(f"[CORE] Module completed successfully - {module_key} -> {result}")
    else:
        log_technical_detail(f"[CORE] Module completed successfully - {module_key}")

def log_sections_found(sections: list) -> None:
    """Log discovered sections - technical detail only."""
    log_technical_detail(f"[CORE] Module keys found: {sections}")

def flush_logs() -> None:
    """Flush all log handlers to ensure data is written."""
    for handler in logging.getLogger().handlers:
        handler.flush()