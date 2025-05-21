# Product Requirements Document — accounts.py  
**Document Version:** v1.0.9
**Module Identifier:** accounts.py  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam (Development Engineer)  
**Last Updated:** 2025-05-21  

---

## 1. Purpose  
This module manages the conversion and validation of account data exported from QuickBooks Desktop (QBD) into a format compatible with GnuCash CSV import. It handles account mapping, hierarchy construction, and enforces typing rules critical for correct financial data import.

---

## 2. Scope  
- Covers parsing, mapping, and validating QBD account list exports (`!ACCNT` records).  
- Produces CSV outputs compatible with GnuCash’s import formats.  
- Enforces strict rules on account typing, placeholder accounts, and AR/AP account special handling.  
- Does not process transaction data or other QBD list types beyond accounts.  
- Does not modify source QBD files or handle QIF imports.

---

## 3. Inputs and Outputs  

### 3.1 Inputs  
- QBD list export CSV files with `!ACCNT` records, including account fields as per QuickBooks schema.  
- Mapping configuration files (YAML/JSON) specifying account type mappings and default rules.

### 3.2 Outputs  
- CSV files formatted for GnuCash import containing converted accounts.  
- Internal data structures representing the account tree and mappings.  
- Validation error logs and exit codes on failure conditions.

---

## 4. Functional Requirements  

### 4.1 Overview  
The module converts QBD accounts into a GnuCash-compatible hierarchy, applying type mappings, enforcing parent-child relationships, and validating compliance with required account types and placeholders.

### 4.2 Detailed Behavior  
- Parse `!ACCNT` records from QBD exports.  
- Apply account type mappings based on config; fallback to placeholders where mappings are missing.  
- Enforce the “1-child” rule: accounts with a single child may have their type promoted to match the child.  
- Handle AR/AP account typing strictly, ensuring only one AR and one AP root account exist.  
- Construct a hierarchical account tree to preserve parent-child relationships.  
- Validate account structure and type consistency; raise errors on violations.  
- Output converted accounts to CSV, ensuring GnuCash compatibility.

---

## 5. Configuration & Environment  

### 5.1 Config Schema  
- Mapping files specifying:  
  - Account type mappings (`mapping["account_types"]`)  
  - Default placeholder rules (`mapping["default_rules"]`)  
- Validation rule flags for strict AR/AP enforcement and placeholder behavior.

### 5.2 Environment Constraints  
- Python 3.8+ runtime assumed.  
- Input files must conform to QBD export specifications; no source file alterations allowed.  
- Outputs must meet GnuCash CSV import requirements.  
- Logging follows centralized policies unless exceptional handling is required.

---

## 6. Interface & Integration  

### 6.1 Module Contract: accounts.py

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

**Public Functions/Classes:**
- Name: `run_accounts_pipeline`
  - **Arguments:**
    - `iif_path: str`
    - `mapping_path: str`
    - `csv_path: str`
    - `log_path: str`
    - `mapping_diff_path: str`
  - **Return type:** `None`
  - **Exceptions raised:** `IIFParseError`, `MappingLoadError`, `AccountTreeError`
  - **Description:** Orchestrates the full pipeline for QBD account conversion to GnuCash CSV.
  - **Example call:**
    ```python
    run_accounts_pipeline(
        iif_path='input/sample-qbd-accounts.IIF',
        mapping_path='output/accounts_mapping_specific.json',
        csv_path='output/accounts.csv',
        log_path='output/qbd-to-gnucash.log',
        mapping_diff_path='output/accounts_mapping_diff.json'
    )
    ```
> **Note on log_path parameter:** The `log_path` parameter provides flexibility for specifying a custom log file location. When not specified or set to None, the system will default to using `output/qbd-to-gnucash.log` as defined in the core PRD section 7.10. This parameter allows for module-specific logging while maintaining compatibility with centralized logging strategies.

### 6.2 Interface Contracts  

#### Public Interface: `run_accounts_pipeline`
- **Arguments:**  
  - `iif_path: str`  
  - `mapping_path: str`  
  - `csv_path: str`  
  - `log_path: str`  
  - `mapping_diff_path: str`
- **Return Type:** `None`
- **Exceptions:**  
  - `IIFParseError`  
  - `MappingLoadError`  
  - `AccountTreeError`
- **Description:** Entry point for processing QBD `!ACCNT` list. Ensures full pipeline execution from input parsing to validated GnuCash CSV generation.
- **Example Call:**  
  ```python
  run_accounts_pipeline(
      iif_path='input/sample-qbd-accounts.IIF',
      mapping_path='output/accounts_mapping_specific.json',
      csv_path='output/accounts.csv',
      log_path='output/qbd-to-gnucash.log',
      mapping_diff_path='output/accounts_mapping_diff.json'
  )
  ```

 **Data Structures:**
 - Input: iif_path (str), mapping_path (str)
 - Output: csv_path (str), log_path (str), mapping_diff_path (str)
 - All file paths are of type str.
 - Example mapping structure: Dict[str, Any] as loaded from JSON.
 
 - Mapping File Schema (accounts_mapping_specific.json, account_mapping_baseline.json):
  ```JSON
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
 - Account Record (Python Typing):
 ```Python
 from typing import TypedDict, Optional
 class AccountRecord(TypedDict):
    NAME: str
    ACCNTTYPE: str
    DESC: Optional[str]
    PARENT: Optional[str]
    # ...other QBD fields as needed
 ```
 - Validation Error Structure (Python Typing):
 ```Python
 class ValidationError(TypedDict):
     record: dict
     error: str
     stage: str
 ```

### 6.3 Dependencies  

- **Internal Modules:**  
| Module Name        | Import Path                                                      | Purpose                                   |
|--------------------|------------------------------------------------------------------|-------------------------------------------|
| `mapping.py`       | `from list_converters.mapping import load_and_merge_mappings`    | Loading and merging JSON mapping files    |
| `accounts_tree.py` | `from modules.accounts.accounts_tree import build_account_tree`  | Building and validating account hierarchy |
| `error_handler.py` | `from utils.error_handler import IIFParseError, MappingLoadError`| Standardized exception classes            |
| `iif_parser.py`    | `from utils.iif_parser import parse_iif_file`                    | Parsing the QBD IIF file                  |
| `logger.py`        | `from utils.logger import setup_logging`                         | Centralized logging configuration         |

- **External Requirements:**

#### External Requirements
- Python 3.8+ as specified in Core PRD section 9
- No external package dependencies beyond Python standard library
- Conforms to logging/error handling policies as defined in Core PRD sections 7.2, 7.3, and 7.10
    

- **External Data Format Contracts:**  
  - JSON mapping schema (for `accounts_mapping_specific.json`, `account_mapping_baseline.json`)  
  - GnuCash CSV import format for accounts
  - The mapping file structure defined here adheres to the conventions established in Core PRD section 11.2, which requires mapping files to be in JSON format and referenced via configuration. This module's mapping schema specifically supports account type conversions while maintaining the broader architectural pattern defined in the core requirements.

---

## 7. Validation & Error Handling  

### 7.1 Validation Rules  
- Input accounts must have valid QuickBooks account types.  
- Enforce one AR and one AP root account; duplicates trigger errors.  
- Placeholder accounts must be inserted if mapping is missing.  
- Account type promotion under “1-child” rule must not violate type constraints.  
- Hierarchy must not contain cycles or invalid parent references.

### 7.2 Error Classes & Exit Codes
- `MappingError` (E010): Missing or invalid mapping entries (exit code 10).
- `ValidationError` (E020): Structural violations or type inconsistencies (exit code 20).
- `PlaceholderError` (E030): Placeholder account handling failures (exit code 30).
- All errors logged per centralized logging standards.


---

## 8. Logging & Error Handling  

- Defers to centralized logging and error handling policies as defined in `module-prd-logging-v1.0.2.md` and `utils/error_handler.py`.  
- Unique validation errors include detailed context to aid debugging.  
- No local overrides of logging behavior unless critical errors warrant special attention.

---

## 9. Versioning & Change Control  

### 9.1 Revision History  
| Version | Date       | Author | Summary                           
|---------|------------|--------|--------------------------------- 
| v1.0.0  | 2025-05-21 | PJ     | Initial governance-compliant PRD 
| v1.0.8  | 2025-05-21 | PJ     | Full processing through PRD template v3.5.1
| v1.0.9  | 2025-05-21 | PJ     | Full processing through PRD template v3.5.0
 

### 9.2 Upstream/Downstream Impacts  
- Changes to mapping schema or account typing rules require coordination with config management modules.  
- Downstream modules consuming account CSVs depend on this module for data correctness.  
- Validation logic updates affect overall pipeline reliability.

---

## 10. Non-Functional Requirements  
- Performance optimized to handle large QBD account exports with minimal latency.  
- Strict maintainability to allow future extension for additional QBD list types.  
- Security: No sensitive data exposure; input files treated as read-only.  
- Scalability: Designed to integrate with larger ETL workflows.

---

## 11. Open Questions / TODOs  
- Determine support strategy for future QBD list types beyond accounts.  
- Define automated testing coverage thresholds for complex validation rules.  
- Assess potential for supporting QIF imports in future releases.  

---

## 12. Example Calls for Public Functions/Classes  

### 12.1 `build_gnucash_accounts`  
```python
# Example usage  
from accounts import build_gnucash_accounts  
mapping_config = load_mapping_config("account_mapping.yaml")  
account_list = parse_qbd_export("qbd_accounts.csv")  
gnucash_accounts = build_gnucash_accounts(account_list, mapping_config)  
export_to_csv(gnucash_accounts, "gnucash_accounts.csv")  
```

---

## 13. Appendix (Optional)  
### 13.1 Data Schemas or Additional References  
```json
{
  "account_record": {
    "name": "string",
    "type": "string",
    "parent": "string|null",
    "placeholder": "boolean",
    "mapping_key": "string"
  }
}
```

---
