# Module PRD: Validation

## 1. Version
v1.0.4

[core-prd-v3.2.0.md](../core-prd-v3.2.0.md)

## 2. Compatibility
Compatible with: core-prd-v3.2.0.md

## 3. Module Contract: validation.py

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
- All types must either map cleanly or trigger the mapping diff file

**Failure Modes:**
- Logs validation issues with record number and offending key/value
- Fails pipeline early if required fields or mappings are missing
- Returns structured validation report (if used programmatically)

## 4. Interface Contract

### 4.1 Public Functions/Classes
- Name: AccountValidationSuite
  - Arguments (constructor):
      - mapping: Dict[str, Any]
  - Methods:
      - validate_iif_record(record: Dict[str, Any]) -> bool
      - validate_mapping(qb_type: str, mapping: Dict[str, Any]) -> bool
      - validate_account_tree(tree: Dict[str, Any]) -> bool
      - validate_flattened_tree(flat: List[Dict[str, Any]]) -> bool
      - validate_csv_row(row: Dict[str, Any]) -> bool
      - run_all(iif_records: List[Dict[str, Any]], tree: Dict[str, Any], flat: List[Dict[str, Any]], csv_rows: List[Dict[str, Any]]) -> bool
  - Exceptions raised: None (errors are collected in self.errors)
  - Description: Provides validation methods for each stage of the QBD-to-GnuCash pipeline.
  - Example call:
    ```python
    validator = AccountValidationSuite(mapping)
    ok = validator.run_all(records, tree, flat, csv_rows)
    ```

### 4.2 Data Structures
- Input: records (List[Dict[str, Any]]), mapping (Dict[str, Any]), tree (Dict[str, Any]), flat (List[Dict[str, Any]]), csv_rows (List[Dict[str, Any]])
- Output: validation result (bool), errors (List[str])
- Example validation error structure:
  ```python
  {
      'record': Dict[str, Any],
      'error': str,
      'stage': str
  }
  ```

## 5. Data Structure Definitions (Agentic AI Compatibility)

### 5.1 Account Record (Python Typing)
```python
from typing import TypedDict, Optional
class AccountRecord(TypedDict):
    NAME: str
    ACCNTTYPE: str
    DESC: Optional[str]
    PARENT: Optional[str]
    # ...other QBD fields as needed
```

## 6. Example Calls for Public Functions/Classes

### 6.1 AccountValidationSuite
```python
validator = AccountValidationSuite(mapping)
# Normal case
ok = validator.run_all(records, tree, flat, csv_rows)
# Edge case: missing required field
bad_record = {"ACCNTTYPE": "BANK"}  # Missing NAME
assert not validator.validate_iif_record(bad_record)
```

## 7. Summary Table: Functions, Data Structures, Schemas, and Example Calls

| Function/Class         | Data Structure/Schema                | Example Call Location         |
|-----------------------|--------------------------------------|------------------------------|
| AccountValidationSuite | AccountRecord, ValidationError       | Example Calls section         |
| AccountRecord         | AccountRecord (Python Typing)        | Data Structure Definitions    |
| ValidationError       | ValidationError (Python Typing)      | Data Structure Definitions    |

## 8. Error Logging and Graceful Exit
- This module must comply with all requirements in [Logging Framework module PRD v1.0.2](../logging/module-prd-logging-v1.0.2.md) and [core PRD section 10.12](../core-prd-v3.4.0.md#1012-logging-and-error-handling).
- Remove all module-specific logging/error handling requirements from this document; see the centralized logging module for details.

## 9. Version History

- v1.0.0 (2025-05-19): Initial release, extracted and centralized all validation module requirements from core PRD.
- v1.0.4 (2025-05-19): Align with PRD-base v3.4.0, update interface contracts and data structure definitions for agentic AI compatibility.
