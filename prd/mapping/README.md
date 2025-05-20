# Mapping Module

**Version:** 1.0.4  
**Date:** 2025-05-19  

---

## 1. Overview

This module provides the mapping logic for the QBD-to-GnuCash conversion tool. It manages the mapping of QBD account types to GnuCash types and hierarchies, supports baseline and specific mapping overlays, and generates diff files for unmapped types. The module is fully agentic AI-compatible and supports modular extension.

---

## 2. Features

- Manages mapping of QBD account types to GnuCash types and hierarchies
- Supports baseline and user-specific mapping overlays
- Generates diff files for unmapped QBD types
- Agentic AI-compatible PRD and interface contracts

---

## 3. Usage

- Used automatically by the main tool during mapping and diff generation
- Mapping files are located in `registry/mapping/` and `output/`
- See `module-prd-mapping-v1.0.4.md` for interface contracts and example calls

---

## 4. Data Structures

- See `module-prd-mapping-v1.0.4.md` for explicit JSON Schema and Python typing for all major data structures (mapping files, mapping diff, etc.)

---

## 5. Example Calls

See the "Example Calls for Public Functions/Classes" section in `module-prd-mapping-v1.0.4.md` for realistic usage and edge cases.

---

## 6. Version History

- v1.0.0 (2025-05-19): Initial release, extracted and modularized from core PRD.
- v1.0.4 (2025-05-19): Align with PRD-base v3.4.0, update interface contracts and data structure definitions for agentic AI compatibility.

---

## 7. References

- [module-prd-mapping-v1.0.4.md](module-prd-mapping-v1.0.4.md): Canonical contract and requirements for the mapping module.
- [../core-prd-v3.4.0.md](../core-prd-v3.4.0.md): Core PRD for the modular system.
- [GnuCash CSV Import Guide](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)
- [GnuCash CSV Import Source (C implementation)](https://github.com/Gnucash/gnucash/blob/stable/gnucash/import-export/csv-imp/assistant-csv-account-import.c)
