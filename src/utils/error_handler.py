"""Error handling for QBD to GnuCash conversion tool.

This module defines all custom exceptions used throughout the application
to ensure consistent error handling and reporting.
"""

class QBDError(Exception):
    """Base class for all QBD conversion errors."""
    pass


class IIFParseError(QBDError):
    """Raised when parsing of IIF files fails."""
    pass


class MappingLoadError(QBDError):
    """Raised when loading or processing mapping files fails."""
    pass


class AccountsTreeError(QBDError):
    """Raised when building or processing the account hierarchy fails."""
    pass


class ValidationError(QBDError):
    """Raised when validation of data structures or rules fails."""
    pass


class OutputError(QBDError):
    """Raised when generating output files fails."""
    pass


# Error code constants
E001 = "E001"  # IIF Parse Error
E002 = "E002"  # Mapping Load Error
E003 = "E003"  # Account Tree Error
E004 = "E004"  # Validation Error
E005 = "E005"  # Output Generation Error

# Error code to exit code mapping
EXIT_CODES = {
    E001: 1,  # Critical failure
    E002: 1,  # Critical failure
    E003: 2,  # Validation error
    E004: 2,  # Validation error
    E005: 1,  # Critical failure
}

def get_exit_code(error: Exception) -> int:
    """Get the appropriate exit code for an error.
    
    Args:
        error: The exception that was raised
        
    Returns:
        Exit code (0=success, 1=critical failure, 2=validation error)
    """
    if isinstance(error, IIFParseError):
        return EXIT_CODES[E001]
    elif isinstance(error, MappingLoadError):
        return EXIT_CODES[E002]
    elif isinstance(error, AccountsTreeError):
        return EXIT_CODES[E003]
    elif isinstance(error, ValidationError):
        return EXIT_CODES[E004]
    elif isinstance(error, OutputError):
        return EXIT_CODES[E005]
    else:
        return 1  # Default to critical failure for unknown errors