class IIFParseError(Exception):
    """Raised when the IIF file is malformed or unreadable."""
    pass

class MappingLoadError(Exception):
    """Raised when mapping files fail to load or are invalid."""
    pass

class AccountTreeError(Exception):
    """Raised when account tree construction or flattening fails."""
    pass

class RegistryKeyConflictError(Exception):
    """Raised when two modules register the same IIF key."""
    pass

class UnregisteredKeyError(Exception):
    """Raised when no module is registered to handle a given IIF key."""
    pass
