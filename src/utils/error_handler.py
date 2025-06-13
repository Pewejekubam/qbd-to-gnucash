"""Error handling utilities for QBD to GnuCash conversion.

This module provides centralized error handling functionality as specified in core-prd-main-v3.6.5.md.
All error codes follow the authoritative table in Core PRD Section 16.

UPDATED: Added E0104 OutputWriteError for file writing operations.
"""

class ConversionError(Exception):
    """Base class for conversion-specific exceptions."""
    def __init__(self, message: str, error_code: str, exit_code: int = 1):
        self.message = message
        self.error_code = error_code
        self.exit_code = exit_code
        # Include error code in exception message for logging
        super().__init__(f"[{error_code}] {message}")

class ValidationError(ConversionError):
    """Raised when data validation fails. Error Code: E0102"""
    def __init__(self, message: str):
        super().__init__(message, error_code="E0102", exit_code=2)

class IIFParseError(ConversionError):
    """Raised when .IIF file parsing fails. Error Code: E0105"""
    def __init__(self, message: str):
        super().__init__(message, error_code="E0105", exit_code=2)

class MappingLoadError(ConversionError):
    """Mapping file missing, unreadable, or invalid schema. Error Code: E1101"""
    def __init__(self, message: str):
        super().__init__(message, error_code="E1101", exit_code=2)

class AccountsTreeError(ConversionError):
    """Account hierarchy construction errors. Error Code: E1111"""
    def __init__(self, message: str):
        super().__init__(message, error_code="E1111", exit_code=2)

class ExportError(ConversionError):
    """Raised when data export fails. Error Code: E1106"""
    def __init__(self, message: str):
        super().__init__(message, error_code="E1106", exit_code=1)

class OutputWriteError(ConversionError):
    """Output file cannot be written. Error Code: E0104"""
    def __init__(self, message: str):
        super().__init__(message, error_code="E0104", exit_code=1)

class RegistryKeyConflictError(ConversionError):
    """Raised when duplicate registry key detected. Error Code: E0103"""
    def __init__(self, message: str):
        super().__init__(message, error_code="E0103", exit_code=1)

class FileNotFoundError(ConversionError):
    """Required input file missing or unreadable. Error Code: E0101"""
    def __init__(self, message: str):
        super().__init__(message, error_code="E0101", exit_code=1)

class LoggingError(ConversionError):
    """Logging subsystem failed. Error Code: E0201"""
    def __init__(self, message: str):
        super().__init__(message, error_code="E0201", exit_code=1)