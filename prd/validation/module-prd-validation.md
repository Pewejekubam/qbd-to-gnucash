````markdown
# Module PRD: Validation

[core-prd-v3.0.0.md](../core-prd-v3.0.0.md)

## Compatibility
Compatible with: core-prd-v3.0.0.md

## Module Contract: validation.py

**Purpose:**
Implements a validation suite for parsed records. Enforces structure, field presence, and mapping integrity before output generation.

**Inputs:**
- Parsed record list (from the IIF parser, typically `!ACCNT`)
- Mapping dictionary (baseline + overrides) for account type resolution
- Optional context metadata for logging/debugging

**Outputs:**
- Logs structured validation warnings and errors
- Raises exceptions if fatal structural violations are detected

**Invariants:**
- All field names must match the original QBD `.IIF` headers exactly (e.g., `NAME`, `ACCNTTYPE`)
- No inferred or lowercase aliases may be used (e.g., `name`, `type`)
- All required fields must be present and non-empty
- All types must either map cleanly or trigger the diff capture

**Failure Modes:**
- Logs validation issues with record number and offending key/value
- Fails pipeline early if required fields or mappings are missing
- Returns structured validation report (if used programmatically)
````
