# Module PRD: Mapping

## Version
v1.0.4

[core-prd-v3.2.0.md](../core-prd-v3.2.0.md)

## Compatibility
Compatible with: core-prd-v3.2.0.md

## Module Contract: mapping.py

**Purpose:**
Loads, merges, and validates account type mapping files. Provides lookup services for resolving QBD types to GnuCash account types and hierarchy paths.

**Inputs:**
- Baseline mapping JSON (required)
- Specific mapping JSON (optional override)

**Outputs:**
- Combined dictionary of `account_types` and `default_rules`
- Optional mapping diff file for unmapped types (`accounts_mapping_diff.json`)

**Invariants:**
- Input mapping files must follow expected schema
- All lookups must use exact QBD keys (e.g., `BANK`, `OCASSET`, `AR`)
- Fallback behavior is defined by `default_rules`

**Failure Modes:**
- Raises `MappingLoadError` if required files are missing or unreadable
- Logs all key loads, fallbacks, and mapping mismatches

## 4. Interface Contract
### 4.1 Public Functions/Classes
- Name: load_mapping
  - Arguments:
      - user_mapping_path: Optional[str]
  - Return type: Dict[str, Any]
  - Exceptions raised: MappingLoadError
  - Description: Loads and merges mapping files for QBD to GnuCash account types.
  - Example call:
    ```python
    mapping = load_mapping('output/accounts_mapping_specific.json')
    ```
- Name: find_unmapped_types
  - Arguments:
      - records: List[Dict[str, Any]]
      - mapping: Dict[str, Any]
  - Return type: List[str]
  - Exceptions raised: None
  - Description: Returns a list of unmapped QBD account types.
  - Example call:
    ```python
    unmapped = find_unmapped_types(records, mapping)
    ```

### 4.2 Data Structures
- Input: records (List[Dict[str, Any]]), mapping (Dict[str, Any])
- Output: mapping (Dict[str, Any]), unmapped types (List[str])
- Example mapping structure:
  ```python
  {
      'account_types': Dict[str, Dict[str, Any]],
      'default_rules': Dict[str, Any]
  }
  ```

## Data Structure Definitions (Agentic AI Compatibility)

### Mapping File (accounts_mapping_specific.json, account_mapping_baseline.json)
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

### Mapping Structure (Python Typing)
```python
from typing import Dict, Any
MappingType = Dict[str, Any]
```

## Example Calls for Public Functions/Classes

### load_mapping
```python
# Normal case
mapping = load_mapping('output/accounts_mapping_specific.json')
# Edge case: missing file
try:
    mapping = load_mapping('output/missing.json')
except MappingLoadError as e:
    print(e)
```

### find_unmapped_types
```python
# Normal case
unmapped = find_unmapped_types(records, mapping)
# Edge case: empty records
unmapped = find_unmapped_types([], mapping)
assert unmapped == []
```

## Summary Table: Functions, Data Structures, Schemas, and Example Calls

| Function/Class       | Data Structure/Schema                | Example Call Location         |
|---------------------|---------------------------------------|-------------------------------|
| load_mapping        | Mapping File (JSON Schema)            | Example Calls section         |
| find_unmapped_types | Mapping Structure (Python Typing)     | Example Calls section         |
| Mapping Files       | Mapping File (JSON Schema)            | Data Structure Definitions    |

## 5. Error Logging and Graceful Exit
- This module must comply with all requirements in [Logging Framework module PRD v1.0.0](../logging/module-prd-logging-v1.0.0.md) and [core PRD section 7.12](../core-prd-v3.2.0.md#712-logging-and-error-handling).
- Remove all module-specific logging/error handling requirements from this document; see the centralized logging module for details.

## Version History

- v1.0.0 (2025-05-19): Initial release, extracted and centralized all mapping module requirements from core PRD.
- v1.0.2 (2025-05-19): Add explicit JSON Schema and Python typing for all major data structures. Add comprehensive example calls for public functions/classes, including edge cases. Reference schemas and examples in the interface contract. Add a summary table mapping functions/data structures to their schema and example call location.
- v1.0.4 (2025-05-19): Align with PRD-base v3.4.0, update interface contracts and data structure definitions for agentic AI compatibility.
