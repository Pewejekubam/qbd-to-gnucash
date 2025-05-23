# Accounts Module

## Overview  
This module handles the conversion and validation of account data exported from QuickBooks Desktop (QBD) into a format compatible with GnuCash CSV import. It receives parsed `!ACCNT` records from the dispatcher, applies mapping and hierarchy rules, and generates a GnuCash-compatible `accounts.csv` file. The module enforces strict validation, logging, and deterministic account type inheritance.

## File Structure  
- `src/modules/accounts/accounts.py` — Main accounts module logic  
- `src/modules/accounts/accounts_mapping.py` — Account mapping loader and merger  
- `src/modules/accounts/accounts_mapping_baseline.json` — Baseline mapping JSON file  
- `src/modules/accounts/accounts_tree.py` — Account tree builder and validator  
- `src/modules/accounts/accounts_validation.py` — Account validation logic  
- `prd/accounts/README-accounts.md` — This file  
- Output: `output/accounts.csv`, `output/accounts_mapping_diff.json`  

## Design Reference  
This module is governed by [module-prd-accounts-v1.1.0.md](./module-prd-accounts-v1.1.0.md) and follows the PRD governance model.

## Key Responsibilities  
- Parse QBD Chart of Accounts (`!ACCNT`) from IIF files (via dispatched payload)  
- Apply mapping and hierarchy rules to produce GnuCash-compatible CSV output  
- Generate diff files for unmapped QBD account types  
- Enforce strict field names and deterministic account type inheritance  
- Validate all placeholder accounts and overall account tree structure  
- Log all processing phases for full traceability  

## Exceptions & Logging  
- Exceptions: `MappingLoadError`, `AccountsTreeError`, validation exceptions (see PRD §7)  
- Logging: All errors and processing steps are logged to `output/qbd-to-gnucash.log` per [logging/module-prd-logging-v1.0.4.md](../logging/module-prd-logging-v1.0.4.md)  

## Revision History  
| Version | Date       | Author | Summary                           
|---------|------------|--------|--------------------------------- 
| v1.1.0  | 2025-05-23 | PJ     | README updated for accounts module governance and naming conventions
| v1.0.9  | 2025-05-21 | PJ     | README aligned with PRD and governance model
