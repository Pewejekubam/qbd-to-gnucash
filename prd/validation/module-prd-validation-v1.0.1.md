# Product Requirements Document — Validation  
**Document Version:** v1.0.1
**Module Identifier:** validation.py  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-05-21  

---

## 1. Purpose  
The `validation` module performs final-stage cross-domain verification of all parsed and transformed data before output is emitted. It ensures data consistency, mapping completeness, hierarchy integrity, and conformance with GnuCash import requirements. All validation errors are raised in structured form and logged in compliance with centralized logging policy.

---

## 2. Scope  

### In-Scope  
- Global data integrity checks (duplicate paths, missing parents)  
- Domain interdependency validation (e.g., mapping vs. hierarchy)  
- Structured error collection and exit signaling  
- Enforcement of error codes and logging contracts

### Out-of-Scope  
- Parsing of `.IIF` input files  
- Mapping logic or tree construction  
- Output file generation  

---

## 3. Inputs and Outputs  

### 3.1 Inputs  
- Post-mapping in-memory data structures from domain modules  
- Configuration and registry data  
- Mapping baseline and diff files (read-only)  
- Output-ready CSV data (for structural scanning)

### 3.2 Outputs  
- Structured validation errors (raised and logged)  
- `output/qbd-to-gnucash.log`  
- Process exit code: `0`, `1`, or `2` depending on result  

---

## 4. Functional Requirements  

### 4.1 Overview  
The validation module enforces global correctness constraints after individual modules finish processing. It identifies fatal mismatches, referential gaps, and mapping inconsistencies that would break GnuCash import.

### 4.2 Detailed Behavior  
- Scans account tree for orphaned nodes, invalid types, and unpromoted placeholders  
- Ensures all required mappings exist and are valid  
- Checks for duplicate paths and conflicting identifiers  
- Verifies encoding normalization and UTF-8 conformance (if applicable)  
- All exceptions must be logged and flushed before termination  

---

## 5. Configuration & Environment  

### 5.1 Config Schema  
- `validation.enabled: bool` — master toggle  
- `validation.strict_mode: bool` — if True, no fallbacks permitted  
- Uses central config file loaded by core  

### 5.2 Environment Constraints  
- UTF-8 decoding enforcement  
- Output directory must be writable  
- `PYTHONPATH` must include project root  

---

## 6. Interface & Integration  

### 6.1 Module Contract: validation  
- **Purpose:** Final validation of all domain outputs  
- **Inputs:** In-memory output from modules, config, mapping files  
- **Outputs:** Raised exceptions, flushed logs  
- **Invariants:** No unhandled errors may exit the pipeline  
- **Failure Modes:** Raises `ValidationError`, returns code 2  

### 6.2 Interface Contracts: run_validation_pass()

```python
def run_validation_pass(data: Dict[str, Any]) -> None:
    """
    Perform global validation checks on processed module data.

    Args:
        data (Dict[str, Any]): A dictionary of all processed domain data keyed by module. Each key should be the module name (e.g., 'accounts', 'mapping'), and each value should be the validated output structure from that module, as defined in its respective PRD. Example structure:

        data = {
            'accounts': {
                # ...accounts module output structure...
            },
            'mapping': {
                # ...mapping module output structure...
            },
            # ...other modules...
        }

    Raises:
        ValidationError: If structural or logical issues are detected. See Appendix for schema.
        HierarchyViolationError: For invalid parent-child relations. See Appendix for schema.
        MappingInconsistencyError: For missing or invalid mapping references. See Appendix for schema.
    """

# Example call:
run_validation_pass({
    'accounts': {...},
    'mapping': {...},
    # ...other modules...
})
```

### 6.3 Dependencies
- utils/error_handler.py (see [../utils/error_handler.py](../../utils/error_handler.py))
- mapping registry
- All domain modules (transitively)

### 6.4 Data Structure Definitions
- **Internal Modules:**
  - validation_checks.py: rule-level assertions
  - validator.py: main entrypoint, logging + exit logic
- **External Requirements:**
  - Logging policy: [Logging Framework PRD v1.0.2](../logging/module-prd-logging-v1.0.2.md)
  - Error constants: [Core PRD v3.5.0](../core-prd-v3.5.0.md)
- **External Data Format Contracts:**
  - Must conform to GnuCash CSV import format
  - Uses resolved mapping output and account tree structure

---

## 7. Validation & Error Handling

### 7.1 Validation Rules
- All account paths must be unique
- No orphaned children or circular hierarchies
- Mapping keys must resolve to known GnuCash types
- Placeholder accounts must be promoted or flagged
- Must not emit CSV with null or empty required fields

### 7.2 Error Classes & Exit Codes
- ValidationError (base class, see Appendix for schema)
- HierarchyViolationError (see Appendix for schema)
- MappingInconsistencyError (see Appendix for schema)
- E001: Invalid IIF structure
- E002: Unknown account type
- E003: Missing parent

**Exit Codes:**
- 0: Success (no errors raised)
- 1: Critical failure (unexpected exception or system error)
- 2: Validation failure (one or more validation errors detected)

---

## 8. Logging & Error Handling
- All logging behavior is governed by centralized policy:
  - See: module-prd-logging-v1.0.2.md
  - Log to output/qbd-to-gnucash.log
  - All exceptions must be flushed before sys.exit()
  - Strict conformance to UTF-8 and error code contracts

---

## 9. Versioning & Change Control

### 9.1 Revision History
| Version | Date       | Author        | Summary                         
|---------|------------|---------------|---------------------------------
| v1.0.0  | 2025-05-21 | Pewe Jekubam  | Initial scaffold and contract spec 
| v1.0.1  | 2025-05-21 | Pewe Jekubam  | Codegen-ready: clarified input structure, added example call, explicit error schemas, and updated references for agentic compatibility 

### 9.2 Upstream/Downstream Impacts
- Upstream: mapping, accounts, customers, vendors
- Downstream: logging, exit strategy, CLI test harness

---

## 10. Non-Functional Requirements
- Deterministic pass/fail output
- Fast fail on fatal violations
- Must not mutate input or write files (other than logging)
- Compatible with headless, agent-driven runs

---

## 11. Open Questions / TODOs
- Should validation support partial modes for incremental dev testing?
- Should this module emit a JSON report for downstream diffing?
- When future modules (e.g., vendors) are added, should validation become plugin-aware?

---

## 12. Appendix (Optional)
### 12.1 Data Schemas or Additional References
```json
{
  "ValidationError": {
    "type": "object",
    "properties": {
      "code": { "type": "string" },
      "message": { "type": "string" },
      "context": { "type": "object" }
    },
    "required": ["code", "message"]
  },
  "HierarchyViolationError": {
    "type": "object",
    "properties": {
      "code": { "type": "string" },
      "message": { "type": "string" },
      "context": { "type": "object" }
    },
    "required": ["code", "message"]
  },
  "MappingInconsistencyError": {
    "type": "object",
    "properties": {
      "code": { "type": "string" },
      "message": { "type": "string" },
      "context": { "type": "object" }
    },
    "required": ["code", "message"]
  }
}
```
