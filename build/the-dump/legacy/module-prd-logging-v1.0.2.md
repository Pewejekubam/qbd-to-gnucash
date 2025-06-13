# Logging Framework Module PRD: QuickBooks Desktop to GnuCash Conversion Tool
**Version:** 1.0.2  
**Date:** 2025-05-19  
**State:** Initial Release

## 1. Purpose

This module defines the centralized logging framework for all modules in the QBD-to-GnuCash conversion tool. It standardizes log formats, error categories, log flushing, and error handling requirements to ensure consistency, traceability, and agentic AI compatibility across the system.

## 2. Scope

- Applies to all core and extension modules (accounts, mapping, validation, etc.).
- Governs all logging output, error reporting, and log file management.
- Supersedes any module-specific logging requirements.

## 3. Logging Requirements

### 3.1 Log Format
- All logs must use Python's `logging` module.
- Log format:
  ```python
  logging.basicConfig(
      level=logging.INFO,
      format='%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s',
      datefmt='%Y-%m-%d %H:%M:%S'
  )
  ```
- Log entries must include:
  - Timestamp
  - Log level (INFO, WARNING, ERROR, etc.)
  - Module and function name
  - Message

### 3.2 Log File Location
- Default log file: `output/qbd-to-gnucash.log`.
- Log file path must be configurable via environment variable or config file.
- The logging directory must be created automatically if it does not exist.

### 3.3 Log Flushing and Process Exit
- All log handlers must be flushed to disk before any process exit (including `os._exit`, `sys.exit`, or unhandled exceptions).
- Fatal errors must be logged synchronously before exit.
- Modules must avoid abrupt termination without logging.

### 3.4 Error Categories
- All errors must be classified according to the following categories:
  - Parsing
  - Mapping
  - Tree Construction
  - Output
  - Registry
- Example error category structure:
  ```python
  ERROR_CATEGORIES = {
      "Parsing": ["Missing header", "Tab mismatch", "Invalid UTF-8"],
      "Mapping": ["Unknown account type", "No destination hierarchy defined"],
      "Tree Construction": ["Missing parent", "Failed 1-child promotion", "Circular paths"],
      "Output": ["File write permission denied", "CSV malformed"],
      "Registry": ["Unregistered key", "Key conflict", "Fallback loop"]
  }
  ```
- Error codes/messages must be defined as constants in `utils/error_handler.py`.

### 3.5 Logging Events
- Log the following events at minimum:
  - Unmapped account types
  - Missing files
  - Structural anomalies in input data
  - Key processing steps (e.g., account tree construction, CSV writing)
  - Unicode normalization/stripping events (with file name and line number)
  - All errors and exceptions

### 3.6 Log Levels
- Use appropriate log levels:
  - `INFO` for normal operations and key steps
  - `WARNING` for recoverable issues
  - `ERROR` for critical failures
  - `DEBUG` for detailed traceability (optional, configurable)

### 3.7 Agentic AI Compatibility
- Log messages must be structured and explicit to support agentic AI inspection and debugging.
- Where possible, include contextual information (file, function, input parameters) in log entries.

## 4. Interface Contract

- The logging framework must expose a setup function:
  ```python
  def setup_logging(log_path: Optional[str] = None, log_level: str = "INFO") -> None
      """Initializes logging with the specified path and level. Ensures log directory exists and applies the standard format."""
  ```
  - Arguments:
      - log_path: Optional[str] — Path to the log file (default: None, uses config/env or default path)
      - log_level: str — Logging level (default: "INFO")
  - Return type: None
  - Exceptions raised: OSError (if log directory cannot be created)
  - Example call:
    ```python
    setup_logging(log_path='output/qbd-to-gnucash.log', log_level='DEBUG')
    ```
- All modules must call `setup_logging()` before any logging occurs.
- All error logging must use the centralized logger.

## 5. Data Structure Definitions (Agentic AI Compatibility)

### Log Event Structure (Python Typing)
```python
from typing import TypedDict, Optional
class LogEvent(TypedDict):
    timestamp: str
    level: str
    module: str
    function: str
    message: str
    context: Optional[dict]
```
### Error Category Structure (Python Typing)
```python
from typing import Dict, List
ErrorCategories = Dict[str, List[str]]
```

## 6. Example Calls for Public Functions/Classes

### setup_logging
```python
# Normal case
setup_logging(log_path='output/qbd-to-gnucash.log', log_level='DEBUG')
# Edge case: log directory does not exist (should be created automatically)
setup_logging(log_path='output/nonexistent-dir/qbd-to-gnucash.log', log_level='INFO')
```

## 7. Summary Table: Functions, Data Structures, Schemas, and Example Calls

| Function/Class   | Data Structure/Schema         | Example Call Location         |
|-----------------|-------------------------------|------------------------------|
| setup_logging   | LogEvent (Python Typing)      | Example Calls section         |
| ErrorCategories | ErrorCategories (Python Typing)| Data Structure Definitions    |

## 8. Error Handling and Logging Checklist

- [x] All errors and exceptions are logged before process exit.
- [x] Log handlers are flushed before exit.
- [x] Log format and file location conform to this module.
- [x] Error categories and codes are used consistently.
- [x] Logging is agent-compatible and includes context.

## 9. References

- [Core PRD v3.4.0, Section 10.12](../core-prd-v3.4.0.md#1012-logging-and-error-handling)
- [Python logging documentation](https://docs.python.org/3/library/logging.html)

## 10. Version History

- v1.0.0 (2025-05-19): Initial release, extracted and centralized all logging requirements from core and module PRDs.
- v1.0.1 (2025-05-19): Normalize function signature documentation in Interface Contract, refine data structure typing, and clarify example call.
- v1.0.2 (2025-05-19): Add explicit Python typing for log event structure and error category structure. Add comprehensive example calls for setup_logging, including edge cases. Reference schemas and examples in the interface contract. Add a summary table mapping functions/data structures to their schema and example call location.
