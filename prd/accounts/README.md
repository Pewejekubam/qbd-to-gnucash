# Accounts Module

## 1. Version
1.0.5  
**Date:** 2025-05-19  

---

## 2. Overview

This module implements the QBD Chart of Accounts to GnuCash conversion logic. It parses QBD IIF `!ACCNT` records, applies mapping and hierarchy rules, and generates a GnuCash-compatible `accounts.csv` file. The module enforces strict validation, logging, and deterministic account type inheritance, and is fully agentic AI-compatible.

---

## 3. Features

- Parses QBD Chart of Accounts (`!ACCNT`) from IIF files
- Applies mapping and hierarchy rules to produce GnuCash-compatible output
- Generates diff files for unmapped QBD types
- Logs all processing phases for traceability
- Strict enforcement of field names and type inheritance
- All placeholder accounts are structurally complete and validated
- Agentic AI-compatible PRD and interface contracts

---

## 4. Usage

- Place your `.IIF` file in `input/`
- Run the main tool (see project root README)
- Output will be written to `output/accounts.csv` and `output/accounts_mapping_diff.json` (if unmapped types found)
- All errors and exceptions are logged to `output/qbd-to-gnucash.log`

---

## 5. Data Structures

- See `module-prd-accounts-v1.0.5.md` for explicit JSON Schema and Python typing for all major data structures (account record, mapping files, validation errors).

---

## 6. Example Calls

See the "Example Calls for Public Functions/Classes" section in `module-prd-accounts-v1.0.5.md` for realistic usage and edge cases.

---

## 7. Version History

- v1.0.0 (2025-05-19): Initial release, extracted and modularized from core PRD.
- v1.0.5 (2025-05-19): Align with PRD-base v3.4.0, update interface contracts and data structure definitions for agentic AI compatibility.

---

## 8. References

- [module-prd-accounts-v1.0.5.md](module-prd-accounts-v1.0.5.md): Canonical contract and requirements for the accounts module.
- [../core-prd-v3.4.0.md](../core-prd-v3.4.0.md): Core PRD for the modular system.
- [GnuCash CSV Import Guide](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)
- [GnuCash CSV Import Source (C implementation)](https://github.com/Gnucash/gnucash/blob/stable/gnucash/import-export/csv-imp/assistant-csv-account-import.c)
