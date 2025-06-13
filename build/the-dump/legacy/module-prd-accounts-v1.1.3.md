# Product Requirements Document — accounts.py  

**Document Version:** v1.1.3
**Module Identifier:** accounts-prd-v1.1.3.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam (Development Engineer)  
**Last Updated:** 2025-06-03  
**Governance Model:** prd-governance-model-v2.3.10.md  

---

## 1. Purpose
This module manages the conversion and validation of account data exported from QuickBooks Desktop (QBD) into an import format compatible with GnuCash CSV import. It handles account mapping, hierarchy construction, and enforces typing rules critical for correct financial data import.

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

> 💡 See [Core PRD v3.6.5, Section 13.4: Input File Discovery and Processing Model](../core-prd-main-v3.6.5.md#134-input-file-discovery-and-processing-model) for the canonical definition of `core_dispatch_payload_v1`.

### 3.2 Outputs  
- `accounts.csv` formatted for GnuCash import containing converted accounts.  
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

| Module Name           | Import Path                                                                                      | Purpose                                   
|-----------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------
| `accounts_export.py`  | `from modules.accounts.accounts_export import export_accounts_to_gnucash_csv`                    | Handles GnuCash CSV export for mapped and validated accounts    
| `accounts_mapping.py` | `from modules.accounts.accounts_mapping import load_and_merge_mappings`                          | Loading and merging JSON mapping files    
| `accounts_tree.py`    | `from modules.accounts.accounts_tree import build_accounts_tree`                                 | Building and validating account hierarchy 
| `error_handler.py`    | `from utils.error_handler import IIFParseError, MappingLoadError, AccountsTreeError, OutputError`| Standardized exception classes            
| `iif_parser.py`       | `from utils.iif_parser import parse_iif_file`                                                    | Used only by the dispatcher; not called directly by this module as of v1.0.9+ 
| `logger.py`           | `from utils.logger import setup_logging`                                                         | Centralized logging configuration         

### External Requirements

- Python 3.8+ as specified in [Core PRD v3.6.4, Section 9](../core-prd-main-v3.6.4.md#9-ai-agent-compliance)  
- Conforms to logging/error handling policies as defined in [Core PRD v3.6.4, Sections 7.2, 7.3, and 7.10](../core-prd-main-v3.6.4.md#7-modular-prd-definition)  
- The mapping file structure defined here adheres to the conventions established in [Core PRD v3.6.4, Section 11.2](../core-prd-main-v3.6.4.md#112-human-validation), which requires mapping files to be in JSON format and referenced via configuration. This module's mapping schema specifically supports account type conversions while maintaining the broader architectural pattern defined in the core requirements.
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
- The error classes and exit codes for this module are defined in the authoritative registry in [Core PRD Section 16: Authoritative Error Classes & Error Code Table](../../core-prd-main-v3.6.4.md#16-authoritative-error-classes--error-code-table). All errors must be raised and logged in compliance with the centralized logging module requirements. No ad-hoc or undocumented error classes are permitted.

---

## 8. Logging & Observability
- This module complies with the centralized logging module requirements as defined in [Logging Framework module PRD v1.0.4](../../logging/module-prd-logging-v1.0.4.md) and [Core PRD Section 7.3: Logging Strategy](../../core-prd-main-v3.6.4.md#73-logging-strategy). All logging and error handling must reference the authoritative error classes, codes, and severity levels as defined in [Core PRD Section 16](../../core-prd-main-v3.6.4.md#16-authoritative-error-classes--error-code-table). Logging must be structured, deterministic, and flush-safe, and must capture all error events, validation failures, and key processing steps with sufficient metadata for downstream auditing and debugging.

---

## 9. Versioning & Change Control  

### 9.1 Revision History  
| Version | Date       | Author | Summary                           
|---------|------------|--------|--------------------------------- 
| v1.0.0  | 2025-05-21 | PJ     | Initial governance-compliant PRD 
| v1.0.8  | 2025-05-21 | PJ     | Full processing through PRD template v3.5.1
| v1.0.9  | 2025-05-21 | PJ     | Full processing through PRD template v3.5.2 (which broke it!)
| v1.0.10 | 2025-05-23 | PJ     | Editorial and semantic cleanup; clarified parsing vs dispatch validation
| v1.1.1  | 2025-05-23 | PJ     | module and core PRD document naming and location restructure
| v1.1.2  | 2025-06-03 | PJ     | Added `accounts_export.py` to the "Dependencies" table (Section 6.3)
| v1.1.3  | 2025-06-03 | PJ     | Standardized Error Classes & Exit Codes and Logging & Observability sections to reference authoritative error code table and logging PRD; removed local error code/category definitions for PRD compliance.

### 9.2 Upstream/Downstream Impacts  
- Changes to mapping schema or account typing rules require coordination with config management modules.  
- Downstream modules consuming account CSVs depend on this module for data correctness.  
- Validation logic updates affect overall pipeline reliability.

---

## 10. Example Calls for Public Functions/Classes  

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

---

## 11. Appendix (Optional)  
### 11.1 Data Schemas or Additional References  
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

## 12. Domain Module Naming and Containment Rules

To ensure maintainability, prevent cross-domain collisions, and support governance enforcement:

- All domain-specific modules must:
  - Use a domain prefix in their filename (e.g., `accounts_`, `customers_`).
  - Reside within their respective domain directory (e.g., `src/modules/accounts/`).
  - Avoid placement in `src/utils/` or any unrelated folder.

- Only domain-agnostic modules may be placed in `src/utils/` (e.g., `iif_parser.py`, `error_handler.py`, `logging.py`).

### Examples
✅ `src/modules/accounts/accounts_validation.py`  
❌ `src/utils/validation.py` *(violates naming and containment rules)*

### Developer Checklist
Before creating or moving any file:
- ✅ Prefix domain logic with its module name.
- ✅ Place it under `src/modules/<domain>/`.
- ❌ Never place domain logic in `utils/`.

> This rule is mandatory for all current and future modules. Violations are considered governance failures and must be corrected before codegen or commit.

### Glossary
- **Domain Validation Module:** Validation logic specific to a business domain, named with the domain prefix and located in the domain's module directory.
- **Generic Validation Module:** Validation logic that is reusable across domains, permitted in `src/utils/` only if it contains no domain-specific logic.
