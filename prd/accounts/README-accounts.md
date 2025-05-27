# Accounts Module

## Overview
This module manages the conversion and validation of account data exported from QuickBooks Desktop (QBD) into a format compatible with GnuCash CSV import. It handles account mapping, hierarchy construction, and enforces typing rules critical for correct financial data import.

## File Structure
- `src/modules/accounts/accounts.py` — Main accounts module logic
- `src/modules/accounts/accounts_mapping.py` — Account mapping loader and merger
- `src/modules/accounts/accounts_mapping_baseline.json` — Baseline mapping JSON file
- `src/modules/accounts/accounts_tree.py` — Account tree builder and validator
- `src/modules/accounts/accounts_validation.py` — Account validation logic
- `prd/accounts/README-accounts.md` — This file
- Output: 
    - `output/accounts.csv` - Fully converted, GNUCash compatible import file
    - `output/accounts_mapping_diff.json` - Accounts that had no match to the baseline during mapping

## Design Reference
This module is governed by [module-prd-accounts-v1.1.1.md](./module-prd-accounts-v1.1.1.md) and follows the PRD governance model.

## Key Responsibilities
- Process dispatched `!ACCNT` records from the central dispatcher (no direct IIF parsing)
- Apply mapping and hierarchy rules to produce GnuCash-compatible CSV output
- Enforce strict account typing, placeholder handling, and AR/AP account rules
- Construct and validate the account tree structure
- Log all processing phases for traceability

## Exceptions & Logging
- Exceptions: `MappingLoadError`, `AccountsTreeError`, validation exceptions (see PRD §7)
- Logging: All errors and processing steps are logged to `output/qbd-to-gnucash.log` per [logging/module-prd-logging-v1.0.4.md](../logging/module-prd-logging-v1.0.4.md)

## Revision History
| Version | Date       | Author | Summary                           |
|---------|------------|--------|-----------------------------------|
| v1.1.1  | 2025-05-25 | PJ     | README updated to match PRD v1.1.1|
| v1.1.0  | 2025-05-23 | PJ     | README updated for accounts module governance and naming conventions|
| v1.0.9  | 2025-05-21 | PJ     | README aligned with PRD and governance model|
