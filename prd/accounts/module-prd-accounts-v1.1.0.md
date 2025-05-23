# Product Requirements Document — accounts.py  
**Document Version:** v1.1.0
**Module Identifier:** accounts.py  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam (Development Engineer)  
**Last Updated:** 2025-05-21  

---

## 1. Purpose  
This module manages the conversion and validation of account data exported from QuickBooks Desktop (QBD) into a format compatible with GnuCash CSV import. It handles account mapping, hierarchy construction, and enforces typing rules critical for correct financial data import.

---

## 2. Scope  
- Covers mapping and validating `!ACCNT` records as dispatched by the core dispatcher.
- Produces CSV outputs compatible with GnuCash’s import formats.  
- Enforces strict rules on account typing, placeholder accounts, and AR/AP account special handling.  
- Does not process transaction data or other QBD list types beyond accounts.  
- Does not modify source QBD files or handle QIF imports.

---

## 3. Inputs and Outputs  

### 3.1 Inputs

- Dispatched payloads containing `!ACCNT` section data, as provided by the central dispatcher conforming to the `core_dispatch_payload_v1` schema.  
  > ⚠️ **Note:** This module no longer performs `.IIF` file parsing. All parsing and section routing is performed upstream by the central dispatcher. Direct consumption of `.IIF` files is deprecated as of v1.0.9.

- Mapping configuration files (`.json`) specifying:
  - Account type mappings (QBD to GnuCash),
  - Default type rules for unmapped entries,
  - Optional fallback configurations for placeholder detection and root account typing.

- Dispatcher context metadata:
  - `input_path`: Original source file (for traceability).
  - `output_dir`: Directory for generated files.
  - `log_path`: Central log output for all dispatch-related activity.
  - `extra_config` (optional): Reserved for future agentic directives or overrides.

> 💡 See Section 6.5.1 of the Core PRD for the canonical definition of `core_dispatch_payload_v1`.

### 3.2 Outputs  
- CSV files formatted for GnuCash import containing converted accounts.  
- Internal data structures representing the account tree and mappings.  
- Validation error logs and exit codes on failure conditions.

---

## 4. Functional Requirements  

### 4.1 Overview  
The module converts QBD accounts into a GnuCash-compatible hierarchy, applying type mappings, enforcing parent-child relationships, and validating compliance with required account types and placeholders.

### 4.2 Detailed Behavior  
- Process `!ACCNT` records as received from the dispatcher; do not parse raw files directly.  
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

- **Input:**  
  - A dispatched section payload object conforming to the `core_dispatch_payload_v1` schema, representing the `!ACCNT` section extracted and parsed from the original `.IIF` file.  
    This object includes:  
    - `section` (str): Section identifier, e.g., `!ACCNT`  
    - `records` (list): List of parsed records within the section  
    - `input_path` (str): Original source file path for traceability  
    - `output_dir` (str): Target directory for output files  
    - `log_path` (str): Log file path for recording processing information  
    - `mapping_config` (dict): Account mapping configuration details  
    - `extra_config` (dict, optional): Additional configuration overrides or agent directives

- **Output:**  
  - Processed account data structured for GnuCash CSV export  
  - Validation results, logs, and exit codes as per the module specification

> ⚠️ **Note:** Direct acceptance of `.IIF` file paths is deprecated as of module v1.0.9.  
> Modules must exclusively accept centrally dispatched section payloads to maintain consistency with the core dispatch workflow and enable modular, agentic processing.

### 6.2 Interface Contracts  

#### Public Interface: `run_accounts_pipeline`
- **Arguments:**  
  - `payload: dict` (conforming to `core_dispatch_payload_v1` schema; see Section 6.1)  
- **Return Type:** `None`
- **Exceptions:**  
  - `IIFParseError`  
  - `MappingLoadError`  
  - `AccountsTreeError`
- **Description:** Entry point for processing QBD `!ACCNT` list. Ensures full pipeline execution from dispatched payload to validated GnuCash CSV generation.
- **Example Call:**  
  ```python
  # Example agentic/dispatch-based call:
  run_accounts_pipeline(payload={
      'section': '!ACCNT',
      'records': [...],
      'input_path': 'input/sample-qbd-accounts.IIF',
      'output_dir': 'output/',
      'log_path': 'output/qbd-to-gnucash.log',
      'mapping_config': {...},
      'extra_config': {...}
  })
  ```

> **Legacy interface using direct file paths is deprecated as of v1.0.9. Modules must accept only centrally dispatched section payloads.**

**Data Structures:**
- Input: `payload` (dict) conforming to `core_dispatch_payload_v1` (see Section 6.1)
- Output: Processed account data for GnuCash CSV, validation logs, and exit codes
- Example mapping structure: `Dict[str, Any]` as loaded from JSON

- Mapping File Schema (accounts_mapping_specific.json, accounts_mapping_baseline.json):
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

### 6.3 Dependencies  

| Module Name        | Import Path                                                                                       | Purpose                                   |
|--------------------|---------------------------------------------------------------------------------------------------|-------------------------------------------|
| `mapping.py`       | `from list_converters.mapping import load_and_merge_mappings`                                     | Loading and merging JSON mapping files    |
| `accounts_tree.py` | `from modules.accounts.accounts_tree import build_accounts_tree`                                  | Building and validating account hierarchy |
| `error_handler.py` | `from utils.error_handler import IIFParseError, MappingLoadError, AccountsTreeError, OutputError`  | Standardized exception classes            |
| `iif_parser.py`    | `from utils.iif_parser import parse_iif_file`                                                     | Used only by the dispatcher; not called directly by this module as of v1.0.9+ |
| `logger.py`        | `from utils.logger import setup_logging`                                                          | Centralized logging configuration         |- **External Requirements:**

#### External Requirements
- Python 3.8+ as specified in Core PRD section 9
- No external package dependencies beyond Python standard library
- Conforms to logging/error handling policies as defined in Core PRD sections 7.2, 7.3, and 7.10
    

- **External Data Format Contracts:**  
  - JSON mapping schema (for `accounts_mapping_specific.json`, `accounts_mapping_baseline.json`)  
  - GnuCash CSV import format for accounts
  - The mapping file structure defined here adheres to the conventions established in Core PRD section 11.2, which requires mapping files to be in JSON format and referenced via configuration. This module's mapping schema specifically supports account type conversions while maintaining the broader architectural pattern defined in the core requirements.

---

## 7. Validation & Error Handling  

### 7.1 Validation Rules  
- Input accounts must have valid QuickBooks account types.  
- Enforce one AR and one AP root account; duplicates trigger errors.  
- Placeholder accounts must be inserted if mapping is missing.  
  - **Fallback logic:** If an account type is not mapped, a placeholder account is created using the default rules specified in the mapping file (e.g., mapped to 'Uncategorized:ASSET' or as defined in `mapping["default_rules"]`). All such events are logged with context, and the placeholder is clearly marked in the output.  
- Account type promotion under “1-child” rule must not violate type constraints.  
- Hierarchy must not contain cycles or invalid parent references.

### 7.2 Error Classes & Exit Codes
- **Error Code Reference:** All error codes are defined as constants in `utils/error_handler.py`, following the format `E###` (e.g., `E001`, `E002`, `E003`).

- **Module-Specific Error Categories:**
  - **Dispatch Validation (formerly "Parsing"):** Errors originating from invalid or malformed payloads passed by the dispatcher—such as corrupted section structures, missing headers, or encoding issues detected during upstream `.IIF` preprocessing.
  - **Mapping:** Unknown account types, missing hierarchy definitions, mapping load failures.
  - **Tree Construction:** Missing parents, circular references, 1-child promotion violations.
  - **Output:** CSV generation failures, file permission issues.

- **Exception Classes:** Referenced from centralized `utils/error_handler.py`:
  - `IIFParseError`: Raised by the dispatcher for `.IIF` parsing or extraction failures; logged by modules when surfaced through upstream diagnostics or payload metadata.
  - `MappingLoadError`: Mapping-related failures.
  - `AccountsTreeError`: Hierarchy and construction-related failures.
  - `OutputError`: Failures during output generation.

- **ValidationError Structure:**
  - The `ValidationError` `TypedDict` is used for structured logging of validation issues. It is not raised as an exception but is included in logs and error reports for agentic inspection and debugging.

- **Exit Codes:** As per core PRD specification:
  - `0`: Success
  - `1`: Critical failure (e.g., dispatch validation, mapping load failure)
  - `2`: Validation errors (e.g., tree construction, unresolved references)

- **Usage:** All exceptions and error codes must reference centralized constants from `utils/error_handler.py`.

- **Logging:** Conforms to logging framework and structure defined in Core PRD §7.10.

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
| v1.0.9  | 2025-05-21 | PJ     | Full processing through PRD template v3.5.2 (which broke it!)
| v1.0.10 | 2025-05-23 | PJ     | Editorial and semantic cleanup; clarified parsing vs dispatch validation | 

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

```python
# Agentic/dispatch-based example (current, v1.0.9+):
run_accounts_pipeline(payload={
    'section': '!ACCNT',
    'records': [...],
    'input_path': 'input/sample-qbd-accounts.IIF',
    'output_dir': 'output/',
    'log_path': 'output/qbd-to-gnucash.log',
    'mapping_config': {...},
    'extra_config': {...}
})
```

> **Legacy Example (deprecated as of v1.0.9):**
> ```python
> run_accounts_pipeline(
>     iif_path='input/sample-qbd-accounts.IIF',
>     mapping_path='output/accounts_mapping_specific.json',
>     csv_path='output/accounts.csv',
>     log_path='output/qbd-to-gnucash.log',
>     mapping_diff_path='output/accounts_mapping_diff.json'
> )
> ```

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
