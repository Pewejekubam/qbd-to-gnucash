````markdown
# Module PRD: Mapping

## Version
v1.0.1

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
- Optional diff map of unmapped types (for export)

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
  - Return type: dict
  - Exceptions raised: MappingLoadError
  - Example call:
    ```python
    mapping = load_mapping('output/accounts_mapping_specific.json')
    ```

- Name: find_unmapped_types
  - Arguments:
    - records: List[dict]
    - mapping: dict
  - Return type: List[str]
  - Exceptions raised: None
  - Example call:
    ```python
    unmapped = find_unmapped_types(records, mapping)
    ```

### 4.2 Data Structures
- Input: records (List[dict]), mapping (dict)
- Output: mapping (dict), unmapped types (List[str])

## 5. Error Logging and Graceful Exit
- This module must comply with all requirements in [Logging Framework module PRD v1.0.0](../logging/module-prd-logging-v1.0.0.md) and [core PRD section 7.12](../core-prd-v3.2.0.md#712-logging-and-error-handling).
- Remove all module-specific logging/error handling requirements from this document; see the centralized logging module for details.
````
