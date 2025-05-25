# PRD Index: QBD to GnuCash Conversion Tool

## Overview
This directory contains the Product Requirements Documents (PRDs) governing the architecture, modules, and compliance of the QBD to GnuCash Conversion Tool. Each PRD is versioned, agentic-compatible, and maintained under the PRD Governance Model v2.3.10.

## File Structure
- `core-prd-v3.6.3.md` — Core product requirements and architecture
- `accounts/module-prd-accounts-v1.1.1.md` — Accounts module PRD
- `accounts/module-prd-accounts_mapping-v1.0.7.md` — Accounts Mapping module PRD
- `accounts/module-prd-accounts_validation-v1.0.2.md` — Accounts Validation module PRD
- `logging/module-prd-logging-v1.0.4.md` — Logging module PRD
- `prd-module-template-v3.6.2.md` — PRD template for new modules

## Design Reference
- All PRDs in this directory are governed by [PRD Governance Model v2.3.10](../prd/prd-governance-model-v2.3.10.md)
- Each module PRD references the core PRD and the logging PRD for shared contracts

## Key Contracts or Responsibilities
- Defines the authoritative requirements for each module and the core system
- Ensures strict separation of concerns and modularity
- Mandates explicit interface contracts, error handling, and logging
- Supports agentic AI compatibility and deterministic documentation
- Enforces sequential section numbering, Markdown-only formatting, and version-locked cross-references

## Exceptions & Logging
- Exception and logging requirements are formalized in each module PRD (see respective §7 or §8)
- Centralized logging and error handling are governed by [logging/module-prd-logging-v1.0.4.md](logging/module-prd-logging-v1.0.4.md)

## Revision History  
| Version | Date       | Author | Summary                          
|---------|------------|--------|-----------------------------------|
| v3.6.3  | 2025-05-25 | PJ     | README updated to match core PRD v3.6.3 |
| v3.6.0  | 2025-05-23 | PJ     | README aligned with PRD and governance model |
