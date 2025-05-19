````markdown
# Module PRD: Mapping

[core-prd-v3.0.0.md](../core-prd-v3.0.0.md)

## Compatibility
Compatible with: core-prd-v3.0.0.md

## Module Contract: mapping.py

**Purpose:**
Loads, merges, and validates account type mapping files. Provides lookup services for resolving QBD types to GnuCash account types and hierarchy paths.

**Inputs:**
- Baseline mapping JSON (required)
- Specific mapping JSON (optional override)

**Outputs:**
- Combined dictionary of `account_types` and `default_rules`
- Optional diff map of unmapped types (for export)

**Invariants:**
- Input mapping files must follow expected schema
- All lookups must use exact QBD keys (e.g., `BANK`, `OCASSET`, `AR`)
- Fallback behavior is defined by `default_rules`

**Failure Modes:**
- Raises `MappingLoadError` if required files are missing or unreadable
- Logs all key loads, fallbacks, and mapping mismatches
````
