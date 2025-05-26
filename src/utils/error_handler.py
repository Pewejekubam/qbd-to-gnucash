# Agentic affirmation: This script is compliant with PRD v3.6.3 and Governance Document v2.3.10.

class IIFParseError(Exception):
    """Raised when an IIF file cannot be parsed as expected."""
    pass

class MappingLoadError(Exception):
    """Raised when mapping files are missing, unreadable, or invalid."""
    pass

class AccountsTreeError(Exception):
    """Raised when the account hierarchy is invalid or contains cycles/orphans."""
    pass

class ValidationError(Exception):
    """Raised when validation of processed data fails."""
    pass

class OutputError(Exception):
    """Raised when output file generation fails."""
    pass