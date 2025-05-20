# Logging Framework Module

**Version:** 1.0.2  
**Date:** 2025-05-19  

---

## 1. Overview

This module provides the logging framework for the QBD-to-GnuCash conversion tool. It standardizes log formats, error categories, log flushing, and error handling requirements to ensure consistency, traceability, and agentic AI compatibility across the system.

---

## 2. Features

- Centralized logging setup for all modules
- Standard log format and log file location
- Error category and code definitions
- Automatic log directory creation
- Synchronous log flushing before process exit
- Agentic AI-compatible, structured log messages

---

## 3. Usage

- Import and call `setup_logging()` before any logging occurs in your module:

```python
from logging_module import setup_logging
setup_logging(log_path='output/qbd-to-gnucash.log', log_level='INFO')
```

- All errors and exceptions must be logged before process exit.
- Log handlers are flushed before exit.
- Log format and file location conform to this module's requirements.

---

## 4. Data Structures

- LogEvent (Python Typing):
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
- ErrorCategories (Python Typing):
```python
from typing import Dict, List
ErrorCategories = Dict[str, List[str]]
```

---

## 5. Example Calls

```python
# Normal case
setup_logging(log_path='output/qbd-to-gnucash.log', log_level='DEBUG')
# Edge case: log directory does not exist (should be created automatically)
setup_logging(log_path='output/nonexistent-dir/qbd-to-gnucash.log', log_level='INFO')
```

---

## 6. Version History

- v1.0.0 (2025-05-19): Initial release, extracted and centralized all logging requirements from core and module PRDs.
- v1.0.1 (2025-05-19): Normalize function signature documentation in Interface Contract, refine data structure typing, and clarify example call.
- v1.0.2 (2025-05-19): Add explicit Python typing for log event structure and error category structure. Add comprehensive example calls for setup_logging, including edge cases. Reference schemas and examples in the interface contract. Add a summary table mapping functions/data structures to their schema and example call location.

---

## 7. References

- [module-prd-logging-v1.0.2.md](module-prd-logging-v1.0.2.md): Canonical contract and requirements for the logging module.
- [../core-prd-v3.4.0.md](../core-prd-v3.4.0.md): Core PRD for the modular system.
- [Python logging documentation](https://docs.python.org/3/library/logging.html)
