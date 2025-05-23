# Mapping Module

## Overview
This module manages the mapping of QBD account types to GnuCash types and hierarchies. It loads, merges, and validates mapping files, provides lookup services, and generates diff files for unmapped types. The module is fully agentic AI-compatible and supports modular extension.

## File Structure
- `prd/accounts/module-prd-accounts_mapping-v1.0.7.md` — PRD for the mapping module
- `src/modules/accounts/accounts_mapping.py` — Account mapping loader and merger  
- `prd/accounts/README-accounts_mapping.md` — This file
- `src/modules/accounts/accounts_mapping_baseline.json` — Baseline mapping JSON file 
- `output/accounts_mapping_diff.json` — Difference mapping from baseline JSON file 

## Design Reference
This module is governed by [module-prd-accounts_mapping-v1.0.7.md](./module-prd-accounts_mapping-v1.0.7.md)

## Key Contracts or Responsibilities
- Load and merge mapping files for QBD to GnuCash account types
- Provide lookup services for QBD to GnuCash account types
- Generate diff files for unmapped QBD types
- Enforce strict schema and validation rules for mapping files
- Log all key loads, fallbacks, and mapping mismatches

## Exceptions & Logging
- Exceptions: `MappingLoadError` (see PRD §7)
- Logging: All mapping and error events are logged per [logging/module-prd-logging-v1.0.4.md](../logging/module-prd-logging-v1.0.4.md)

---
## Revision History  
| Version | Date       | Author | Summary                           
|---------|------------|--------|--------------------------------- 
| v1.0.6  | 2025-05-23 | PJ     | README aligned with PRD and governance model
