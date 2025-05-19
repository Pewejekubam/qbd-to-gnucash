````markdown
# Module PRD: Validation

## Version
v1.0.1

[core-prd-v3.2.0.md](../core-prd-v3.2.0.md)

## Compatibility
Compatible with: core-prd-v3.2.0.md

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

## 4. Interface Contract

### 4.1 Public Functions/Classes
- Name: AccountValidationSuite
  - Arguments (constructor):
    - mapping: dict
  - Methods:
    - validate_iif_record(record: dict) -> bool
    - validate_mapping(record: dict) -> bool
    - validate_account_tree(tree: object) -> bool
    - validate_flattened_tree(flat: list) -> bool
    - validate_csv_row(row: dict) -> bool
    - run_all(iif_records: list, tree: object, flat: list, csv_rows: list) -> bool
  - Exceptions raised: None (errors are collected in self.errors)
  - Example call:
    ```python
    validator = AccountValidationSuite(mapping)
    ok = validator.run_all(records, tree, flat, csv_rows)
    ```

### 4.2 Data Structures
- Input: records (list of dict), mapping (dict), tree (object), flat (list), csv_rows (list)
- Output: validation result (bool), errors (list)

## 5. Error Logging and Graceful Exit
- This module must comply with all requirements in [Logging Framework module PRD v1.0.0](../logging/module-prd-logging-v1.0.0.md) and [core PRD section 7.12](../core-prd-v3.2.0.md#712-logging-and-error-handling).
- Remove all module-specific logging/error handling requirements from this document; see the centralized logging module for details.
````
