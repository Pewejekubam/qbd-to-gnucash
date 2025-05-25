# Product Requirements Document — Mapping Module  

**Document Version:** v1.0.7  
**Module Identifier:** mapping-prd-v1.0.7.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-05-23  
**Governance Model:** prd-governance-model-v2.3.10.md  
---

## 1. Scope
Loads, merges, and validates account type mapping files. Provides lookup services for resolving QBD types to GnuCash account types and hierarchy paths.

---

## 2. Inputs and Outputs

### 2.1 Inputs
- Baseline mapping JSON (required)
- Specific mapping JSON (optional override)

### 2.2 Outputs
- Combined dictionary of `account_types` and `default_rules`
- Optional mapping diff file for unmapped types (`accounts_mapping_diff.json`)

---

## 3. Functional Requirements  

### 3.1 Overview  
- Load and merge mapping files  
- Provide lookup services for QBD to GnuCash account types  
- Handle unmapped types and logging  

### 3.2 Detailed Behavior  

#### 3.2.1 Loading Mapping Files  
- Loads baseline and specific mapping JSON files  
- Merges the two files into a single dictionary  

#### 3.2.2 Lookup Services  
- Provides exact QBD key lookups (e.g., `BANK`, `OCASSET`, `AR`)  
- Fallback behavior is defined by `default_rules`  

#### 3.2.3 Unmapped Types  
- Returns a list of unmapped QBD account types  
- Logs all key loads, fallbacks, and mapping mismatches  

#### 3.2.4 Version-Locked Core PRD Reference  
- Aligns with [Core PRD v3.6.3 Section 6.5.1](../core-prd-v3.6.3.md#651-processing-rules)  

---

## 4. Configuration & Environment

### 4.1 Config Schema
No specific config options are required.

### 4.2 Environment Constraints
- Input mapping files must follow expected schema
- Module-specific logging/error handling requirements are handled by the centralized logging module

---

## 5. Interface & Integration  

### 5.1 Interface Contracts  

#### load_mapping  
- Arguments: `user_mapping_path: Optional[str]`  
- Return type: `Dict[str, Any]`  
- Exceptions raised: `MappingLoadError`  
- Description: Loads and merges mapping files for QBD to GnuCash account types.  

#### find_unmapped_types  
- Arguments: `records: List[Dict[str, Any]]`, `mapping: Dict[str, Any]`  
- Return type: `List[str]`  
- Exceptions raised: None  
- Description: Returns a list of unmapped QBD account types.  

### 5.2 Dependencies  
- [Logging Framework module PRD v1.0.4](../logging/module-prd-logging-v1.0.4.md)  
- [Core PRD v3.6.3 Section 7.3: Logging Strategy](../core-prd-v3.6.3.md#73-logging-strategy)  

---

## 6. Validation & Error Handling

### 6.1 Validation Rules
- Input mapping files must follow expected schema
- All lookups must use exact QBD keys

### 6.2 Error Classes & Exit Codes
- `MappingLoadError` is raised if required files are missing or unreadable

---

## 7. Logging & Observability
- This module complies with the centralized logging module requirements.

---

## 8. Versioning & Change Control

### 8.1 Revision History
| Version | Date       | Author     | Summary                  
|---------|------------|------------|--------------------------
| v1.0.0  | 2025-05-19 | PJ         | Initial release          
| v1.0.2  | 2025-05-19 | PJ         | Add explicit JSON Schema 
| v1.0.4  | 2025-05-19 | PJ         | Align with PRD-base v3.4.0
| v1.0.5  | 2025-05-21 | PJ         | Full processing through PRD template v3.5.1
| v1.0.6  | 2025-05-23 | PJ         | Updated logging and core PRD references for governance compliance
| v1.0.7  | 2025-05-23 | PJ         | module and core PRD document naming and location restructure

### 8.2 Upstream/Downstream Impacts
Changes to this module may affect other modules that rely on the mapping functionality.

---

## 9. Non-Functional Requirements
No specific non-functional requirements are noted.

---

## 10. Example Calls for Public Functions/Classes

### 11.1 load_mapping

```python
# Normal case
mapping = load_mapping('output/accounts_mapping_specific.json')
# Edge case: missing file
try:
    mapping = load_mapping('output/missing.json')
except MappingLoadError as e:
    print(e)
```

---

## 11. Appendix (Optional)
### 12.1. Mapping File Schema

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
