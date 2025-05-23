# PRD Index: QBD to GnuCash Conversion Tool

## Overview
This directory contains the Product Requirements Documents (PRDs) governing the architecture, modules, and compliance of the QBD to GnuCash Conversion Tool. Each PRD is versioned, agentic-compatible, and maintained under the PRD Governance Model v1.0.0.

## File Structure
- `core-prd-v3.5.1.md` — Core product requirements and architecture
- `accounts/module-prd-accounts-v1.0.9.md` — Accounts module PRD
- `accounts/module-prd-accounts_mapping-v1.0.6.md` — Accounts Mapping module PRD
- `accounts/module-prd-accounts_validation-v1.0.1.md` — Accounts Validation module PRD
- `accounts/module-prd-accounts_tree-v1.0.1.md` — Accounts Validation module PRD
- `logging/module-prd-logging-v1.0.4.md` — Logging module PRD
- `prd-module-template-v3.5.2.md` — PRD template for new modules

## Design Reference
- All PRDs in this directory are governed by [PRD Governance Model v1.0.0](../doc/prd-governance-model-v1.0.0.md)
- Each module PRD references the core PRD and the logging PRD for shared contracts

## Key Contracts or Responsibilities
- Defines the authoritative requirements for each module and the core system
- Ensures strict separation of concerns and modularity
- Mandates explicit interface contracts, error handling, and logging
- Supports agentic AI compatibility and deterministic documentation

## Exceptions & Logging
- Exception and logging requirements are formalized in each module PRD (see respective §7 or §8)
- Centralized logging and error handling are governed by [logging/module-prd-logging-v1.0.4.md](logging/module-prd-logging-v1.0.4.md)


## Revision History  
| Version | Date       | Author | Summary                           
|---------|------------|--------|--------------------------------- 
| v3.6.0  | 2025-05-23 | PJ     | README aligned with PRD and governance model
