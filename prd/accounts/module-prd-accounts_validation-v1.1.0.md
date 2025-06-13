# Product Requirements Document — Validation  

**Document Version:** v1.1.0
**Module Identifier:** module-prd-accounts_validation-prd-v1.1.0.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-06-11  
**Compatible Core PRD:** core-prd-main-v3.9.1.md  
**Governance Model:** prd-governance-model-v2.7.0.md  
---

## 1. Scope  

The `validation` module performs final-stage cross-domain verification of all parsed and transformed data before output is emitted. It ensures data consistency, mapping completeness, hierarchy integrity, and conformance with GnuCash import requirements. All validation errors are raised in structured form and logged in compliance with centralized logging policy.  

---

## 2. Inputs and Outputs  

### 2.1 Inputs  
- Post-mapping in-memory data structures from domain modules
- Configuration and registry data from core dispatcher
- Mapping baseline and diff files (read-only validation)
- Output-ready CSV data for structural scanning

### 2.2 Outputs  
- **Boolean return value:** Validation success (True) or failure (False)
- **Log entries:** Validation results, error conditions, constraint violations
- **Structured validation errors:** Raised exceptions with error codes and context
- **Process exit coordination:** Signals to core for appropriate exit code determination (`0`, `1`, or `2`)  

---

## 3. Functional Requirements  

### 3.1 Overview  
The validation module enforces global correctness constraints after individual domain modules complete processing. It identifies fatal mismatches, referential gaps, and mapping inconsistencies that would break GnuCash import through comprehensive cross-domain validation checks.

### 3.2 Detailed Behavior  

#### 3.2.1 Account Tree Validation
- Scans account hierarchy for orphaned nodes and missing parent references
- Detects circular parent-child relationships across account structure
- Validates account type assignments and placeholder promotion rules
- Enforces unique account path requirements

#### 3.2.2 Mapping Consistency Validation
- Verifies all account types resolve to valid GnuCash mappings
- Validates mapping configuration completeness against processed data
- Checks for conflicting or ambiguous mapping rules
- Ensures required AR/AP account type compliance

#### 3.2.3 Data Integrity Validation
- Validates CSV output structure for GnuCash import compatibility
- Checks for null or empty values in required fields
- Verifies encoding normalization and UTF-8 conformance
- Ensures data consistency across domain module outputs

#### 3.2.4 Error Collection and Reporting
- Collects validation errors with structured context information
- Categorizes violations by severity and domain impact
- Provides actionable error messages for resolution guidance
- Coordinates with logging framework for audit trail capture

#### 3.2.5 Exit Coordination
- Signals validation results to core orchestrator for exit code determination
- Ensures all validation errors are logged and flushed before process termination
- Provides clear success/failure indication for pipeline continuation decisions  

---

## 4. Configuration & Environment  

### 4.1 Config Schema  
- Validation configuration parameters:
  - `validation.enabled: bool` — master toggle for validation execution
  - `validation.strict_mode: bool` — enforce strict validation without fallback rules
  - `validation.check_hierarchy: bool` — enable account hierarchy validation
  - `validation.check_mappings: bool` — enable mapping consistency validation
- Configuration loaded from central config file managed by core dispatcher

### 4.2 Environment Constraints  
- Python 3.8+ runtime environment assumed
- UTF-8 encoding enforcement for all text processing
- Output directory shall be accessible for log file writing
- Input data structures shall conform to domain module output specifications
- Logging shall use centralized framework exclusively as defined in [Logging Framework PRD v1.0.4](../logging/module-prd-logging-v1.0.4.md)  

---

## 5. Interface & Integration  

### 5.1 Module Contract: validation  
- **Purpose:** Final validation of all domain outputs  
- **Inputs:** In-memory output from modules, config, mapping files  
- **Outputs:** Raised exceptions, flushed logs  
- **Invariants:** No unhandled errors may exit the pipeline  
- **Failure Modes:** Raises `ValidationError`, returns code 2  

### 5.2 Interface Contracts: run_validation_pass()

```python
def run_validation_pass(data: Dict[str, Any]) -> None:
    """
    Perform global validation checks on processed module data.

    Args:
        data (Dict[str, Any): A dictionary of all processed domain data keyed by module. Each key should be the module name (e.g., 'accounts', 'mapping'), and each value should be the validated output structure from that module, as defined in its respective PRD. Example structure:

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

### 5.3 Dependencies
- The error classes and exit codes for this module are defined in the authoritative registry in [Core PRD v3.9.1 Section 14: Authoritative Error Classes & Error Code Table](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table). All errors shall be raised and logged in compliance with the centralized logging module requirements.

| Module Name           | Import Path                                                                                      | Purpose                                   
|-----------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------
| `typing`              | `from typing import Dict, List, Any, Optional, Bool`                                            | Type annotations for interface contracts |
| `error_handler.py`    | `from utils.error_handler import ValidationError, HierarchyViolationError, MappingInconsistencyError` | Standardized exception classes            
| `logging.py`          | `from utils.logging import setup_logging`                                                        | Centralized logging configuration

### 5.4 Data Structure Definitions
- **Validation Input Structure:**
  ```python
  ValidationInput = Dict[str, Any]  # Domain module outputs keyed by module name
  ValidationResult = Bool           # Success/failure indication
  ```
- **Error Context Structure:**
  ```python
  ErrorContext = Dict[str, Any]     # Structured error metadata for debugging
  ```

### 5.5 External Requirements
- Python 3.8+ as specified in [Core PRD v3.9.1 Section 9](../core-prd-main-v3.9.1.md#9-ai-agent-compliance)
- Conforms to logging/error handling policies as defined in [Core PRD v3.9.1 Section 7.3](../core-prd-main-v3.9.1.md#73-logging-strategy)
- Validation logic shall enforce GnuCash CSV import format requirements
- All domain module outputs shall conform to their respective PRD specifications for successful validation

### 5.4 Data Structure Definitions
- **Internal Modules:**
  - accounts_validation.py: rule-level assertions, main entrypoint, logging + exit logic
- **External Requirements:**
  - Logging policy: [Logging Framework PRD v1.0.4](../logging/module-prd-logging-v1.0.4.md)
  - Error constants: [Core PRD v3.9.1](../core-prd-main-v3.9.1.md)
- **External Data Format Contracts:**
  - Shall conform to GnuCash CSV import format
  - Uses resolved mapping output and account tree structure
- **Upstream Dependencies:**
  - Coordinates with [accounts PRD v1.3.1 Section 4.2](../accounts/module-prd-accounts-v1.3.1.md#42-core-module-behavior-accountspy) for validation orchestration
  - Integrates with [accounts_mapping PRD v1.1.0](../accounts/module-prd-accounts_mapping-v1.1.0.md) for mapping validation requirements

---

## 6. Validation & Error Handling

### 6.1 Validation Rules
- All account paths shall be unique across the complete account hierarchy
- Account parent-child relationships shall form a valid tree structure without cycles
- All account types shall resolve to valid GnuCash mapping configurations
- Required fields in CSV output shall contain valid, non-null values
- Placeholder accounts shall be properly promoted according to GnuCash requirements
- AR/AP account types shall conform to special handling requirements
- UTF-8 encoding shall be validated across all text data
- Data consistency shall be maintained across all domain module outputs

### 6.2 Error Classes & Exit Codes
Error classes and exit codes shall be implemented per [Core PRD v3.9.1 Section 11.3.2: Error Implementation Protocol](../core-prd-main-v3.9.1.md#1132-error-implementation-protocol). All error handling shall reference the authoritative registry in [Core PRD v3.9.1 Section 14: Authoritative Error Classes & Error Code Table](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table).

### 6.3 Error Context and Recovery
- Validation errors shall include structured context information identifying the specific data element and validation rule that failed
- Error messages shall provide actionable guidance for resolving validation failures
- Failed validation shall result in immediate pipeline termination with appropriate exit code signaling
- All validation errors shall be logged with sufficient detail for debugging and audit purposes

---

## 7. Logging & Observability
- This module complies with the centralized logging module requirements as defined in [Logging Framework module PRD v1.0.4](../logging/module-prd-logging-v1.0.4.md) and [Core PRD v3.9.1 Section 7.3: Logging Strategy](../core-prd-main-v3.9.1.md#73-logging-strategy). All logging and error handling shall reference the authoritative error classes, codes, and severity levels as defined in [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table). Logging shall be structured, deterministic, and flush-safe, and shall capture all error events, validation failures, and key processing steps with sufficient metadata for downstream auditing and debugging.

---

## 8. Versioning & Change Control

### 8.1 Revision History
| Version | Date       | Author        | Summary                         
|---------|------------|---------------|---------------------------------
| v1.0.0  | 2025-05-21 | Pewe Jekubam  | Initial scaffold and contract spec 
| v1.0.1  | 2025-05-21 | Pewe Jekubam  | Codegen-ready: clarified input structure, added example call, explicit error schemas, and updated references for agentic compatibility 
| v1.0.2  | 2025-05-23 | PJ            | module and core PRD document naming and location restructure
| v1.0.3  | 2025-06-03 | PJ            | Standardized Error Classes & Exit Codes and Logging & Observability sections to reference authoritative error code table
| v1.1.0r1| 2025-06-11 | PJ            | Governance compliance update: updated Core PRD reference to v3.9.1, Governance Model to v2.7.0, enforced deterministic language, aligned error handling with current standards
| v1.1.0  | 2025-06-11 | PJ            | Production release: removed window dressing from non-functional requirements, finalized for adoption

### 8.2 Upstream/Downstream Impacts
- Upstream: mapping, accounts, customers, vendors
- Downstream: logging, exit strategy, CLI test harness

---

## 9. Non-Functional Requirements
- **Memory Efficiency:** Validation shall process data in-memory without requiring intermediate file storage
- **Data Integrity:** Validation shall preserve input data without modification during processing

---

## 10. Appendix (Optional)
### 10.1 Data Schemas or Additional References
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