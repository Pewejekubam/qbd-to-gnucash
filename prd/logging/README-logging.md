# Logging Framework Module

## Overview
This module defines the centralized logging framework for all modules in the QBD-to-GnuCash conversion tool. It standardizes log formats, error categories, log flushing, and error handling requirements to ensure consistency, traceability, and agentic AI compatibility across the system. The module is fully compliant with the latest governance and core PRD standards, and follows the logging and error handling model described in the authoritative PRD.

## File Structure
- `module-prd-logging-v1.0.5.md` — Authoritative PRD for the logging module
- `logging.py` — Logging implementation
- `README-logging.md` — This file

## Design Reference
This module is governed by [Logging Framework PRD v1.0.5 Section 1: Scope](./module-prd-logging-v1.0.5.md#1-scope) and follows the [Governance Model PRD v2.7.0 Section 2](../prd-governance-model-v2.7.0.md#2-structural-rules-and-document-standards). All interface contracts, error handling, and logging are aligned with [Core PRD v3.9.1 Section 7.3: Logging Strategy](../core-prd-main-v3.9.1.md#73-logging-strategy).

## Key Responsibilities
- Provide a consistent and centralized logging mechanism for all modules
- Enforce uniform log format, error category tagging, and directory management
- Prevent log loss during crashes by ensuring all handlers are flushed before process exit
- Auto-create log files and directories if missing
- All log categories must conform to predefined ERROR_CATEGORIES
- Support agentic AI traceability and structured logs
- Ensure all validation and error handling is compliant with the authoritative error code table

## Exceptions & Logging
- Exceptions: `OSError` (directory creation or log flush failures), logging errors (see [Logging Framework PRD v1.0.5 Section 6.2: Error Classes & Exit Codes](./module-prd-logging-v1.0.5.md#62-error-classes--exit-codes))
- Logging: All modules must call `setup_logging()` before logging; all errors and process exits are logged per [Logging Framework PRD v1.0.5 Section 6](./module-prd-logging-v1.0.5.md#6-validation--error-handling) and [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table)

## Revision History
| Version | Date       | Author | Summary                           |
|---------|------------|--------|-----------------------------------|
| v1.0.5  | 2025-06-10 | PJ     | README updated to match PRD v1.0.5|
| v1.0.5a | 2025-06-11 | PJ     | README fully aligned with PRD v1.0.5, clarified compliance and responsibilities |
