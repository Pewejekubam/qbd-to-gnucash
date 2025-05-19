````markdown
# Module PRD: Validation

## Version
v1.0.4

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

## Data Structure Definitions (Agentic AI Compatibility)

### Account Record (Python Typing)
```python
from typing import TypedDict, Optional
class AccountRecord(TypedDict):
    NAME: str
    ACCNTTYPE: str
    DESC: Optional[str]
    PARENT: Optional[str]
    # ...other QBD fields as needed
```
