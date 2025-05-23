# Mapping Module

## Overview
This module manages the mapping of QBD account types to GnuCash types and hierarchies. It loads, merges, and validates mapping files, provides lookup services, and generates diff files for unmapped types. The module is fully agentic AI-compatible and supports modular extension.

## File Structure
- `module-prd-mapping-v1.0.6.md` — PRD for the mapping module
- `mapping.py` — Mapping logic
- `README.md` — This file
- Mapping files: `registry/mapping/account_mapping_baseline.json`, `output/accounts_mapping_diff.json`

## Design Reference
This module is governed by [module-prd-mapping-v1.0.6.md](./module-prd-mapping-v1.0.6.md)

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
Changelog: v1.0.6 — README aligned with PRD and governance model (2025-05-23)
