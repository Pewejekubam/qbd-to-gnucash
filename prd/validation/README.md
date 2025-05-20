# Validation Module

**Version:** 1.0.4  
**Date:** 2025-05-19  

---

## 1. Overview

This module provides the validation logic for the QBD-to-GnuCash conversion tool. It implements staged validators for IIF parsing, mapping, tree construction, flattening, and CSV output, ensuring data integrity and agentic AI compatibility throughout the pipeline.

---

## 2. Features

- Validates QBD IIF records, mapping, account tree, and CSV output
- Centralizes integrity enforcement for all pipeline stages
- Supports error raising, structured logging, and optional halting
- Agentic AI-compatible validation suite and interface contracts

---

## 3. Usage

- Used automatically by the main tool during each processing phase
- All errors and exceptions are logged to `output/qbd-to-gnucash.log`
- See `module-prd-validation-v1.0.4.md` for interface contracts and example calls

---

## 4. Data Structures

- See `module-prd-validation-v1.0.4.md` for explicit Python typing for all major data structures (validation error, account record, etc.)

---

## 5. Example Calls

See the "Example Calls for Public Functions/Classes" section in `module-prd-validation-v1.0.4.md` for realistic usage and edge cases.

---

## 6. Version History

- v1.0.0 (2025-05-19): Initial release, extracted and modularized from core PRD.
- v1.0.4 (2025-05-19): Align with PRD-base v3.4.0, update interface contracts and data structure definitions for agentic AI compatibility.

---

## 7. References

- [module-prd-validation-v1.0.4.md](module-prd-validation-v1.0.4.md): Canonical contract and requirements for the validation module.
- [../core-prd-v3.4.0.md](../core-prd-v3.4.0.md): Core PRD for the modular system.
- [GnuCash CSV Import Guide](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)
- [GnuCash CSV Import Source (C implementation)](https://github.com/Gnucash/gnucash/blob/stable/gnucash/import-export/csv-imp/assistant-csv-account-import.c)
