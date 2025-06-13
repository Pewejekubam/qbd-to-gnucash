# Product Requirements Document — accounts.py  

**Document Version:** v1.3.0
**Module Identifier:** module-prd-accounts-v1.3.0.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam (Development Engineer)  
**Last Updated:** 2025-06-10  
**Compatible Core PRD:** core-prd-main-v3.9.1.md  
**Governance Model:** prd-governance-model-v2.7.0.md  

---

## 1. Purpose
This module manages the conversion and validation of account data exported from QuickBooks Desktop (QBD) into an import format compatible with GnuCash CSV import. It handles account mapping, hierarchy construction, and enforces typing rules critical for correct financial data import. This module's interface contracts comply with Core PRD v3.9.1 Section 11.5 Interface Authority Precedence Rules.

## 2. Scope
- Covers mapping and validating `!ACCNT` records as dispatched by the core dispatcher.
- Produces CSV outputs compatible with GnuCash's import formats.  
- Enforces strict rules on account typing, placeholder accounts, and AR/AP account special handling.  
- Integrates text-based mapping workflow for unmapped account types requiring user input.
- Does not process transaction data or other QBD list types beyond accounts.  
- Does not modify source QBD files or handle QIF imports.

---

## 3. Inputs and Outputs  

### 3.1 Inputs

- Dispatched payloads containing `!ACCNT` section data, as provided by the central dispatcher conforming to the `core_dispatch_payload_v1` schema.  
  > ⚠️ **Note:** This module no longer performs `.IIF` file parsing. All parsing and section routing is performed upstream by the central dispatcher. Direct consumption of `.IIF` files is deprecated as of v1.0.9.

- Core dispatch payload conforming to core_dispatch_payload_v1 schema:
  - `section` (str): Section identifier (e.g., `!ACCNT`)
  - `records` (list): Parsed records within the section
  - `output_dir` (str): Target directory for output files
  - `extra_config` (dict, optional): Additional configuration overrides or agent directives

- Mapping configuration files (`.json`) specifying:
  - Account type mappings (QBD to GnuCash),
  - Default type rules for unmapped entries,
  - Optional fallback configurations for placeholder detection and root account typing.

> 💡 See [Core PRD v3.9.1 Section 11.4: Input File Discovery and Processing Model](../core-prd-main-v3.9.1.md#114-input-file-discovery-and-processing-model) for the canonical definition of `core_dispatch_payload_v1`.

### 3.2 Outputs  
- `accounts.csv` formatted for GnuCash import containing converted accounts.
- Text-based questions file (`accounts_mapping_questions.txt`) when unmapped account types are detected.
- Generational archive files (`accounts_mapping_questions_v{number}.txt`) for processed questions.
- Internal data structures representing the account tree and mappings.  
- Validation error logs and exit codes on failure conditions.

---

## 4. Functional Requirements  

### 4.1 Overview  
The module converts QBD accounts into a GnuCash-compatible hierarchy, applying type mappings, enforcing parent-child relationships, and validating compliance with required account types and placeholders. It includes autonomous text-based workflow management for handling unmapped account types requiring user input.

### 4.2 Detailed Behavior  
- Process `!ACCNT` records as received from the dispatcher; do not parse raw files directly.  
- Apply account type mappings based on config; fallback to placeholders where mappings are missing.  
- Enforce the "1-child" rule: accounts with a single child may have their type promoted to match the child.  
- Handle AR/AP account typing strictly, ensuring only one AR and one AP root account exist.  
- Construct a hierarchical account tree to preserve parent-child relationships.  
- Validate account structure and type consistency; raise errors on violations.  
- Handle unmapped account types through text-based workflow integration.
- Generate user-friendly questions file when mapping gaps detected.
- HALT pipeline processing to await user input on unmapped accounts.
- Process completed mapping questions and integrate results into pipeline.
- Archive processed questions files using generational naming pattern.
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
    - `output_dir` (str): Target directory for output files  
    - `extra_config` (dict, optional): Additional configuration overrides or agent directives

- **Output:**  
  - Processed account data structured for GnuCash CSV export  
  - Text-based questions file for unmapped accounts (when applicable)
  - Validation results, logs, and exit codes as per the module specification

> ⚠️ **Note:** Direct acceptance of `.IIF` file paths is deprecated as of module v1.0.9.  
> Modules must exclusively accept centrally dispatched section payloads to maintain consistency with the core dispatch workflow and enable modular, agentic processing.

### 6.2 Interface Contracts  

#### Public Interface: `run_accounts_pipeline`
- **Arguments:**  
  - `payload: Dict[str, Any]` (conforming to `core_dispatch_payload_v1` schema; see Section 6.1)  
- **Return Type:** `bool`
- **Exceptions:**  
  - `IIFParseError`  
  - `MappingLoadError`  
  - `AccountsTreeError`
- **Description:** Entry point for processing QBD `!ACCNT` list with text-based mapping workflow support. Ensures full pipeline execution from dispatched payload to validated GnuCash CSV generation. Returns False when HALT condition reached (user action required for unmapped accounts).

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
| `accounts_mapping.py` | `from modules.accounts.accounts_mapping import load_mapping, find_unmapped_types, generate_text_mapping_questions, parse_text_mapping_file` | Loading and merging JSON mapping files with text-based workflow support
| `accounts_tree.py`    | `from modules.accounts.accounts_tree import build_accounts_tree`                                 | Building and validating account hierarchy 
| `accounts_validation.py` | `from modules.accounts.accounts_validation import run_validation_pipeline`                       | Final validation
| `error_handler.py`    | `from utils.error_handler import IIFParseError, MappingLoadError, AccountsTreeError, OutputError`| Standardized exception classes            
| `iif_parser.py`       | `from utils.iif_parser import parse_iif_file`                                                    | Used only by the dispatcher; not called directly by this module as of v1.0.9+ 
| `logger.py`           | `from utils.logger import setup_logging`                                                         | Centralized logging configuration         

### External Requirements

- Python 3.8+ as specified in [Core PRD v3.9.1 Section 9](../core-prd-main-v3.9.1.md#9-ai-agent-compliance)  
- Conforms to logging/error handling policies as defined in [Core PRD v3.9.1 Sections 7.2, 7.3, and 7.10](../core-prd-main-v3.9.1.md#7-modular-prd-definition)  
- The mapping file structure defined here adheres to the conventions established in [Core PRD v3.9.1 Section 11.2](../core-prd-main-v3.9.1.md#112-human-validation), which requires mapping files to be in JSON format and referenced via configuration. This module's mapping schema specifically supports account type conversions while maintaining the broader architectural pattern defined in the core requirements.

---

## 7. Validation & Error Handling  

### 7.1 Validation Rules  
- Input accounts must have valid QuickBooks account types.  
- Enforce one AR and one AP root account; duplicates trigger errors.  
- Placeholder accounts must be inserted if mapping is missing.  
  - **Fallback logic:** If an account type is not mapped, a placeholder account is created using the default rules specified in the mapping file (e.g., mapped to 'Uncategorized:ASSET' or as defined in `mapping["default_rules"]`). All such events are logged with context, and the placeholder is clearly marked in the output.  
- Account type promotion under "1-child" rule must not violate type constraints.  
- Hierarchy must not contain cycles or invalid parent references.
- Text-based questions file must be properly formatted for successful parsing.

### 7.2 Error Classes & Exit Codes
All error classes and exit codes are automatically implemented per Core PRD v3.9.1 Section 11.3.2 Error Implementation Protocol. The authoritative registry is defined in [Core PRD v3.9.1 Section 14: Authoritative Error Classes & Error Code Table](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table). No ad-hoc or undocumented error classes are permitted.

---

## 8. Logging & Observability
This module complies with the centralized logging module requirements as defined in [Logging Framework module PRD v1.0.5](../logging/module-prd-logging-v1.0.5.md) and [Core PRD v3.9.1 Section 7.3: Logging Strategy](../core-prd-main-v3.9.1.md#73-logging-strategy). All logging and error handling must reference the authoritative error classes, codes, and severity levels as defined in [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table). Logging must be structured, deterministic, and flush-safe, and must capture all error events, validation failures, and key processing steps with sufficient metadata for downstream auditing and debugging.

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
| v1.2.0  | 2025-06-10 | PJ     | Module PRD alignment: Core PRD v3.9.1 compatibility, prd-governance-model-v2.7.0.md compliance, major interface changes with payload schema correction, interface authority compliance, dependency declarations
| v1.3.0  | 2025-06-10 | PJ     | Text-based mapping workflow integration: HALT conditions, user interaction support, mapping questions processing, generational file management, autonomous workflow control

### 9.2 Upstream/Downstream Impacts  
- Changes to mapping schema or account typing rules require coordination with config management modules.  
- Downstream modules consuming account CSVs depend on this module for data correctness.  
- Validation logic updates affect overall pipeline reliability.
- Text-based workflow introduces user interaction points that may affect pipeline automation.

---

## 10. Example Calls for Public Functions/Classes  

```python
from modules.accounts.accounts import run_accounts_pipeline

# Text-based mapping workflow integration
payload = {
    'section': '!ACCNT',
    'records': [
        {'NAME': 'Cash', 'ACCNTTYPE': 'BANK', 'DESC': 'Primary checking account'},
        {'NAME': 'Equipment', 'ACCNTTYPE': 'UNMAPPED_ASSET_TYPE', 'DESC': 'Office equipment'}
    ],
    'output_dir': 'output/',
    'extra_config': {'strict_validation': True}
}

success = run_accounts_pipeline(payload)
if not success:
    print("Pipeline halted: User action required for unmapped accounts")
    print("Edit output/accounts_mapping_questions.txt and restart pipeline")
else:
    print("Accounts processing completed successfully")

# HALT condition example - when unmapped types detected:
# [WARN] [MAPPING] Found 1 unmapped account types requiring user input:
# [WARN] [MAPPING]   - UNMAPPED_ASSET_TYPE
# [INFO] [MAPPING] Generated questions file: accounts_mapping_questions.txt
# [INFO] [MAPPING] Edit the file and restart pipeline to continue
# [HALT] User action required
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