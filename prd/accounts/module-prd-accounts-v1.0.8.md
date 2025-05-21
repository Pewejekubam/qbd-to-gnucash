# Product Requirements Document — accounts.py  
**Document Version:** v1.0.8
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

### 6.1 API Contracts  
- `build_gnucash_accounts(account_list, mapping_config) -> List[Account]`  
  - Parses and maps accounts; returns GnuCash-compatible accounts.  
  - Raises `MappingError` on missing mandatory mappings.  
- Validation functions raising defined exceptions on structural errors.

### 6.2 Dependencies  
- Depends on centralized logging and error handling modules (`utils/error_handler.py`).  
- Relies on external config parsers for mapping files.  
- Integrates downstream with CSV export modules for GnuCash import.

---

## 7. Validation & Error Handling  

### 7.1 Validation Rules  
- Input accounts must have valid QuickBooks account types.  
- Enforce one AR and one AP root account; duplicates trigger errors.  
- Placeholder accounts must be inserted if mapping is missing.  
- Account type promotion under “1-child” rule must not violate type constraints.  
- Hierarchy must not contain cycles or invalid parent references.

### 7.2 Error Classes & Exit Codes  
- `MappingError`: Missing or invalid mapping entries (exit code 10).  
- `ValidationError`: Structural violations or type inconsistencies (exit code 20).  
- `PlaceholderError`: Placeholder account handling failures (exit code 30).  
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
