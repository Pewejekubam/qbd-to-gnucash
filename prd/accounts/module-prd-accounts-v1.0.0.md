````markdown
# Module PRD: Accounts

[core-prd-v3.0.0.md](../core-prd-v3.0.0.md)

## Compatibility
Compatible with: core-prd-v3.0.0.md

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
````
