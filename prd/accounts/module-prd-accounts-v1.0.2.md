````markdown
# Module PRD: Accounts

## Version
v1.0.2

[core-prd-v3.2.0.md](../core-prd-v3.2.0.md)

## Compatibility
Compatible with: core-prd-v3.2.0.md

## Module Contract: accounts.py

**Purpose:**
Orchestrates the full processing pipeline for the `!ACCNT` list type:
- Parsing → Mapping → Tree Construction → Validation → CSV Output

**Inputs:**
- `.IIF` filepath containing a `!ACCNT` section
- Mapping files:
  - `account_mapping_baseline.json` (required)
  - `accounts_mapping_specific.json` (optional override)
- Output target path (e.g., `output/accounts.csv`)

**Outputs:**
- GnuCash-compatible CSV (`accounts.csv`)
- Optional diff file for unmapped types (`accounts_mapping_diff.json`)
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
- **Note:** The `mapping` returned by `load_and_merge_mappings()` must be unpacked before being used. Callers must extract the mapping dictionary and diff as follows:
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
- Example call:
  ```python
  run_accounts_pipeline('input/sample-qbd-accounts.IIF', 'output/accounts_mapping_specific.json', 'output/accounts.csv', 'output/qbd-to-gnucash.log', 'output/accounts_mapping_diff.json')
  ```

### 4.2 Data Structures
- Input: IIF file path (str), mapping file path (str)
- Output: CSV file path (str), log file path (str), mapping diff file path (str)

## 5. Error Logging and Graceful Exit
- This module must comply with all requirements in [Logging Framework module PRD v1.0.0](../logging/module-prd-logging-v1.0.0.md) and [core PRD section 7.12](../core-prd-v3.2.0.md#712-logging-and-error-handling).
- Remove all module-specific logging/error handling requirements from this document; see the centralized logging module for details.
````
