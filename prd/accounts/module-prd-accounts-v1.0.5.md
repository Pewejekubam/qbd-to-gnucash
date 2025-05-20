# Module PRD: Accounts

## 1. Version
v1.0.5

[core-prd-v3.2.0.md](../core-prd-v3.2.0.md)

## 2. Compatibility
Compatible with: core-prd-v3.2.0.md

## 3. Module Contract: accounts.py

**Purpose:**
Orchestrates the full processing pipeline for the `!ACCNT` list type:
- Parsing → Mapping → Tree Construction → Validation → CSV Output

**Inputs:**
- `.IIF` filepath containing a `!ACCNT` section
- Mapping files:
  - `account_mapping_baseline.json` (required)
  - `accounts_mapping_specific.json` (optional override)
- Output file path (e.g., `output/accounts.csv`)

**Outputs:**
- GnuCash-compatible CSV (`accounts.csv`)
- Optional mapping diff file for unmapped types (`accounts_mapping_diff.json`)
- Logs for all key pipeline steps

**Invariants:**
- All input records must be parsed using original QBD field names (e.g., `NAME`, `ACCNTTYPE`) — case-sensitive
- Intermediate fields (e.g., `full_account_name`) must be derived explicitly and consistently
- Account records must pass validation before CSV generation
- Logging must track pipeline stages and critical error points

**Failure Modes:**
- Raises `MappingLoadError`, `AccountTreeError`, or validation exceptions on failure
- Logs structured messages for all validation issues
- Halts pipeline if critical steps fail (e.g., mapping or tree invalid)
- **Note:** The `mapping` returned by `load_and_merge_mappings()` must be unpacked before being used. Callers must extract the mapping dictionary and mapping diff file as follows:
  ```python
  mapping, diff = load_and_merge_mappings(...)
  ```

## 4. Interface Contract

### 4.1 Public Functions/Classes
- Name: run_accounts_pipeline
  - Arguments:
      - iif_path: str
      - mapping_path: str
      - csv_path: str
      - log_path: str
      - mapping_diff_path: str
  - Return type: None
  - Exceptions raised: IIFParseError, MappingLoadError, AccountTreeError
  - Description: Orchestrates the full pipeline for QBD account conversion to GnuCash CSV.
  - Example call:
    ```python
    run_accounts_pipeline(
        iif_path='input/sample-qbd-accounts.IIF',
        mapping_path='output/accounts_mapping_specific.json',
        csv_path='output/accounts.csv',
        log_path='output/qbd-to-gnucash.log',
        mapping_diff_path='output/accounts_mapping_diff.json'
    )
    ```

### 4.2 Data Structures
- Input: iif_path (str), mapping_path (str)
- Output: csv_path (str), log_path (str), mapping_diff_path (str)
- All file paths are of type `str`.
- Example mapping structure: `Dict[str, Any]` as loaded from JSON.

## 5. Data Structure Definitions (Agentic AI Compatibility)

### 5.1 Mapping File (accounts_mapping_specific.json, account_mapping_baseline.json)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "account_types": {
      "type": "object",
      "additionalProperties": {
        "type": "object",
        "properties": {
          "gnucash_type": {"type": "string"},
          "hierarchy_path": {"type": "string"}
        },
        "required": ["gnucash_type", "hierarchy_path"]
      }
    },
    "default_rules": {
      "type": "object",
      "additionalProperties": {"type": "string"}
    }
  },
  "required": ["account_types", "default_rules"]
}
```

### 5.2 Account Record (Python Typing)
```python
from typing import TypedDict, Optional
class AccountRecord(TypedDict):
    NAME: str
    ACCNTTYPE: str
    DESC: Optional[str]
    PARENT: Optional[str]
    # ...other QBD fields as needed
```

### 5.3 Validation Error Structure (Python Typing)
```python
class ValidationError(TypedDict):
    record: dict
    error: str
    stage: str
```

## 6. Example Calls for Public Functions/Classes

### 6.1 run_accounts_pipeline
```python
# Normal case
run_accounts_pipeline(
    iif_path='input/sample-qbd-accounts.IIF',
    mapping_path='output/accounts_mapping_specific.json',
    csv_path='output/accounts.csv',
    log_path='output/qbd-to-gnucash.log',
    mapping_diff_path='output/accounts_mapping_diff.json'
)
# Edge case: missing mapping file
try:
    run_accounts_pipeline(
        iif_path='input/sample-qbd-accounts.IIF',
        mapping_path='output/missing.json',
        csv_path='output/accounts.csv',
        log_path='output/qbd-to-gnucash.log',
        mapping_diff_path='output/accounts_mapping_diff.json'
    )
except MappingLoadError as e:
    print(e)
```

## 7. Summary Table: Functions, Data Structures, Schemas, and Example Calls

| Function/Class         | Data Structure/Schema                | Example Call Location         |
|-----------------------|--------------------------------------|------------------------------|
| run_accounts_pipeline | See Interface Contract, Mapping JSON | Example Calls section         |
| Mapping Files         | Mapping Baseline/Specific (JSON Schema) | Data Structure Definitions    |
| AccountRecord         | AccountRecord (Python Typing)        | Data Structure Definitions    |
| ValidationError       | ValidationError (Python Typing)      | Data Structure Definitions    |

## 8. Error Handling and Logging
- This module must comply with all requirements in [Logging Framework module PRD v1.0.2](../logging/module-prd-logging-v1.0.2.md) and [core PRD section 10.12](../core-prd-v3.4.0.md#1012-logging-and-error-handling).
- Remove all module-specific logging/error handling requirements from this document; see the centralized logging module for details.

## 9. Version History

- v1.0.0 (2025-05-19): Initial release, extracted and centralized all accounts module requirements from core PRD.
- v1.0.1 (2025-05-19): Add explicit JSON Schema and Python typing for all major data structures. Add comprehensive example calls for public functions/classes, including edge cases. Reference schemas and examples in the interface contract. Add a summary table mapping functions/data structures to their schema and example call location.
- v1.0.5 (2025-05-19): Align with PRD-base v3.4.0, update interface contracts and data structure definitions for agentic AI compatibility.
