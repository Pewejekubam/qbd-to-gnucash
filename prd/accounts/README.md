# Accounts Module

## Overview
This module manages the conversion and validation of account data exported from QuickBooks Desktop (QBD) into a format compatible with GnuCash CSV import. It parses QBD IIF `!ACCNT` records, applies mapping and hierarchy rules, and generates a GnuCash-compatible `accounts.csv` file. Strict validation, logging, and deterministic account type inheritance are enforced.

## File Structure
- `module-prd-accounts-v1.0.9.md` — PRD for the accounts module
- `accounts.py` — Main module logic
- `accounts_tree.py` — Account tree builder
- `README.md` — This file
- Output: `output/accounts.csv`, `output/accounts_mapping_diff.json`

## Design Reference
This module is governed by [module-prd-accounts-v1.0.9.md](./module-prd-accounts-v1.0.9.md)

## Key Contracts or Responsibilities
- Parse QBD Chart of Accounts (`!ACCNT`) from IIF files
- Apply mapping and hierarchy rules to produce GnuCash-compatible output
- Generate diff files for unmapped QBD types
- Enforce strict field names and type inheritance
- Validate all placeholder accounts and account tree structure
- Log all processing phases for traceability

## Exceptions & Logging
- Exceptions: `MappingLoadError`, `AccountTreeError`, validation exceptions (see PRD §7)
- Logging: All errors and processing steps are logged to `output/qbd-to-gnucash.log` per [logging/module-prd-logging-v1.0.4.md](../logging/module-prd-logging-v1.0.4.md)

---
Changelog: v1.0.9 — README aligned with PRD and governance model (2025-05-23)
