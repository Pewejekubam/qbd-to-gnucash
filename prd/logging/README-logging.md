# Logging Framework Module

## Overview
This module provides the centralized logging framework for the QBD-to-GnuCash conversion tool. It standardizes log formats, error categories, log flushing, and error handling requirements to ensure consistency, traceability, and agentic AI compatibility across the system.

## File Structure
- `module-prd-logging-v1.0.4.md` — PRD for the logging module
- `logging.py` — Logging implementation
- `README.md` — This file

## Design Reference
This module is governed by [module-prd-logging-v1.0.4.md](./module-prd-logging-v1.0.4.md)

## Key Contracts or Responsibilities
- Provide a consistent and centralized logging mechanism for all modules
- Enforce uniform log format, error category tagging, and directory management
- Ensure all handlers are flushed before process exit
- Auto-create log files and directories if missing
- Support agentic AI traceability and structured logs

## Exceptions & Logging
- Exceptions: `OSError` (directory creation), logging errors (see PRD §7)
- Logging: All modules must call `setup_logging()` before logging; all errors and process exits are logged per PRD


## Revision History  
| Version | Date       | Author | Summary                           
|---------|------------|--------|--------------------------------- 
| v1.0.4  | 2025-05-23 | PJ     | README aligned with PRD and governance model
