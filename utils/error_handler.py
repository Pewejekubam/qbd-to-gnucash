"""
Custom Exception Classes for QBD to GnuCash Conversion
"""
class IIFParseError(Exception):
    """Raised when IIF parsing fails."""
    exit_code = 10

class MappingLoadError(Exception):
    """Raised when mapping file loading or merging fails."""
    exit_code = 11

class AccountTreeError(Exception):
    """Raised when account tree construction or flattening fails."""
    exit_code = 12

class ValidationError(Exception):
    """Raised for validation failures."""
    exit_code = 13
