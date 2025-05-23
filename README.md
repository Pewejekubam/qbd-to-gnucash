# QBD to GnuCash Conversion Tool

**Version:** 3.5.1  
**Date:** 2025-05-23  

---

## Overview
This project provides a modular, command-line tool for migrating financial data from QuickBooks Desktop (QBD) to GnuCash using structured import files. The system is governed by a set of agentic, versioned Product Requirements Documents (PRDs) and enforces strict modularity, validation, and logging. The initial focus is on the Chart of Accounts, with extensibility for additional QBD data domains.

---

## File Structure
```plaintext
.
├── input/                # QBD IIF exports
├── output/               # GnuCash CSVs, mapping diffs, logs
├── prd/                  # PRD-base and module PRDs
│   ├── core-prd-v3.5.1.md
│   ├── accounts/module-prd-accounts-v1.0.9.md
│   ├── logging/module-prd-logging-v1.0.4.md
│   ├── mapping/module-prd-mapping-v1.0.6.md
│   ├── validation/module-prd-validation-v1.0.1.md
│   └── prd-module-template-v3.5.2.md
├── modules/              # Per-domain converters (accounts, etc.)
├── utils/                # Shared logic: parsing, logging, validation
├── main.py               # Entrypoint CLI orchestrator
```

---

## Design Reference
- Governed by [core-prd-v3.5.1.md](prd/core-prd-v3.5.1.md) and module PRDs in `prd/`
- All requirements, contracts, and logging policies are defined in the PRDs
- PRD compliance is enforced by [PRD Governance Model v1.0.0](doc/prd-governance-model-v1.0.0.md)

---

## Key Contracts or Responsibilities
- Modular conversion of QBD data to GnuCash import formats
- Strict separation of concerns: core vs. module logic
- Explicit interface contracts, error handling, and logging
- Agentic AI compatibility and deterministic documentation
- All modules reference the centralized logging and error handling PRD

---

## Exceptions & Logging
- All exceptions and logging behaviors are governed by the module PRDs and [prd/logging/module-prd-logging-v1.0.4.md](prd/logging/module-prd-logging-v1.0.4.md)
- See each module PRD for specific exception classes and logging requirements (typically §7 or §8)

---
Changelog: v3.5.1 — README updated for PRD compliance and modular structure (2025-05-23)
