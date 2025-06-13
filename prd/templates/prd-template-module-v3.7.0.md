# Product Requirements Document — [Module Name]

**Document Version:** v[version]  
**Module Identifier:** [module_name-prd-v[version].md]  
**Compatible Core PRD:** core-prd-main-v3.9.1.md  
**Governance Model:** prd-governance-model-v2.7.0.md  
**Domain:** [domain_name]  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** [YYYY-MM-DD]  

---

**Dependency Metadata Block (MANDATORY)**
```markdown
**Compatible Core PRD:** core-prd-main-v3.9.1.md
**Governance Model:** prd-governance-model-v2.7.0.md
```
> All module PRDs must include this block immediately after the header. All versions must be explicit and version-locked (no wildcards or ranges). See [Governance Model PRD v2.7.0 Section 4.4: Dependency Declaration Requirements](../prd-governance-model-v2.7.0.md#44-dependency-declaration-requirements).

#### **Metadata Enforcement Clause**
PRDs missing any required metadata fields **must be rejected without processing** per governance validation rules. All placeholders (e.g., [Describe ...]) must be replaced before PRD acceptance.

---

## 1. Purpose
[Concise description of the module's responsibility and intent within the QBD to GnuCash conversion system. Focus on what this domain module converts and its role in the overall pipeline.]

---

## 2. Scope
[Define the boundaries of the module, what it covers and what it explicitly does not. Reference [Core PRD v3.9.1 Section 12.1: Enhanced Module Boundary Specification Matrix](../core-prd-main-v3.9.1.md#121-enhanced-module-boundary-specification-matrix) for placement decisions. Explicitly state domain ownership and separation from other domains.]

> **Domain Index Reminder:** The domain name must match a valid entry in the [Governance Model PRD v2.7.0 Section 3.2: Authoritative Domain Index](../prd-governance-model-v2.7.0.md#32-authoritative-domain-index).

---

## 3. Inputs and Outputs

### 3.1 Inputs
[Modules must receive dispatched payloads conforming to `core_dispatch_payload_v1` schema as defined in [Core PRD v3.9.1 Section 11.4.4: Dispatch Payload Schema](../core-prd-main-v3.9.1.md#1144-dispatch-payload-schema). Direct file processing is not permitted. Specify the exact section key this module handles (e.g., 'ACCNT', 'CUST', etc.).]

### 3.2 Outputs
[List all output files, data structures, and processing results. All outputs must be directed to the `output/` directory structure. Specify exact output file names and formats (e.g., `accounts.csv`, `customers.csv` for GnuCash import).]

---

## 4. Functional Requirements

### 4.1 Overview
[High-level summary of key functions and responsibilities within domain boundaries. Must align with domain-specific processing requirements while maintaining interface compliance.]

### 4.2 Detailed Behavior
[Step-by-step or feature-specific descriptions of module behavior. Must not contradict [Core PRD v3.9.1 Section 11.5: Interface Authority Precedence Rules](../core-prd-main-v3.9.1.md#115-interface-authority-precedence-rules). Focus on domain-specific transformation logic from QBD format to GnuCash-compatible output.]

---

## 5. Configuration & Environment

### 5.1 Config Schema
[Describe any configuration options or parameters the module uses. Configuration must be provided via payload `extra_config` field or external configuration files. No CLI argument processing permitted.]

### 5.2 Environment Constraints
[Specify environment dependencies, payload format requirements, or runtime constraints. Must support Python 3.8+ and follow [Core PRD v3.9.1 Section 13.1: Non-Functional Requirements](../core-prd-main-v3.9.1.md#131-non-functional-requirements).]

---

## 6. Interface & Integration

### 6.1 Module Contract: [module_name]
[Define Purpose, Inputs, Outputs, Invariants, Failure Modes following [Core PRD v3.9.1 Section 11.5: Interface Authority Precedence Rules](../core-prd-main-v3.9.1.md#115-interface-authority-precedence-rules). This contract must specify how the module integrates with the core dispatch system.]

### 6.2 Interface Contracts

#### Primary Entry Point (MANDATORY)
**Function Name:** `run_<domain>_pipeline`  
**Signature:** `run_<domain>_pipeline(payload: Dict[str, Any]) -> bool`  
**Parameter:** `payload` conforming to `core_dispatch_payload_v1` schema  
**Return Type:** `bool` (True=success, False=failure with appropriate logging)  
**Schema Compliance:** Must accept `core_dispatch_payload_v1` as defined in [Core PRD v3.9.1 Section 11.4.4: Dispatch Payload Schema](../core-prd-main-v3.9.1.md#1144-dispatch-payload-schema)  

**Exceptions:** [List domain-specific exceptions that may be raised, must reference error codes from Section 7.2]

**Example Call:**
```python
success = run_<domain>_pipeline({
    'section': '<SECTION_KEY>',
    'records': [...],
    'output_dir': 'output/',
    'extra_config': {}
})
```

[Additional interface contracts for internal functions with complete signatures, arguments, return types, exceptions, descriptions. Must comply with [Core PRD v3.9.1 Section 11.3.1: Core Orchestration Functions](../core-prd-main-v3.9.1.md#1131-core-orchestration-functions) patterns.]

### 6.3 Dependencies
[List module dependencies and references to other PRDs. Required dependencies include:
- [Logging Framework PRD v1.0.5 Section 5: Interface & Integration](../logging/module-prd-logging-v1.0.5.md#5-interface--integration) for centralized logging
- [Core PRD v3.9.1 Section 7.3: Logging Strategy](../core-prd-main-v3.9.1.md#73-logging-strategy) for error codes and interface patterns
- Any domain-specific mapping or configuration files]

> **Dependency Declaration Guidance:** All dependencies must be version-locked and referenced with compliant links. See [Governance Model PRD v2.7.0 Section 4.4](../prd-governance-model-v2.7.0.md#44-dependency-declaration-requirements).

### 6.4 Data Structure Definitions
- **Internal Modules:** [List all domain-specific modules with naming prefix (e.g., `accounts_mapping.py`, `accounts_tree.py`, `accounts_export.py`)]
- **External Requirements:** [Reference to payload schema, error handling framework, logging requirements]
- **External Data Format Contracts:** [GnuCash CSV import format specifications, JSON mapping file schemas]

---

## 7. Validation & Error Handling

### 7.1 Validation Rules
[Define input validation, data integrity rules, and required checks. Include explicit schema validation against `core_dispatch_payload_v1`. Specify domain-specific validation requirements (e.g., account type validation, hierarchy checks, etc.).]

### 7.2 Error Classes & Exit Codes
The error classes and exit codes for this module are defined in the authoritative registry in [Core PRD v3.9.1 Section 14: Authoritative Error Classes & Error Code Table](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table). 

**Error Implementation Protocol:** Functions containing logical patterns that correspond to error code descriptions in [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table) shall implement those error codes automatically per the deterministic mapping protocol defined in [Core PRD v3.9.1 Section 11.3.2: Exception Classes](../core-prd-main-v3.9.1.md#1132-exception-classes). No implementation discretion exists.

**Domain-Specific Error Code Range:** [Specify the assigned error code range for this domain, e.g., E11xx for accounts domain]

**Implementation Mapping:**
- File operations → File-related error codes (E0101, E0106, E0108, etc.)
- Data validation → Validation error codes (E0102, E0107, E1190, etc.)  
- Parsing operations → Parse error codes (E0105, E0109, E0110, etc.)
- Export operations → Output error codes (E0104, E0111, E0112, etc.)
- Domain-specific operations → Domain error codes ([specify range])

All errors must be raised and logged in compliance with centralized logging requirements. No ad-hoc or undocumented error classes are permitted.

---

## 8. Logging & Observability

This module complies with centralized logging requirements as defined in [Logging Framework PRD v1.0.5 Section 5: Interface & Integration](../logging/module-prd-logging-v1.0.5.md#5-interface--integration) and [Core PRD v3.9.1 Section 7.3: Logging Strategy](../core-prd-main-v3.9.1.md#73-logging-strategy).

### 8.1 Console Logging Requirements

#### Tagging Standards
- **Domain tag format:** `[<DOMAIN>-<CONTEXT>]` where `<DOMAIN>` is uppercase domain name
- **Required contexts:** `PIPELINE` (main processing), domain-specific contexts as needed
- **ASCII only:** No unicode characters permitted in any console output
- **All lines tagged:** Every console message must include appropriate domain tag

#### Required Console Messages
- **Pipeline initiation:** `[<DOMAIN>-PIPELINE] Starting <domain> processing with X records`
- **Success completion:** `[<DOMAIN>-PIPELINE] <Domain> processing completed successfully`
- **HALT conditions:** `[<DOMAIN>-PIPELINE] Pipeline HALT: [specific reason with user guidance]`
- **Output confirmation:** `[<DOMAIN>-PIPELINE] Generated output file: [filename] ([size] bytes)`

#### Console Message Guidelines
- **User-centric:** Focus on data flow progression and user guidance
- **Minimal but helpful:** Each message serves specific user understanding
- **Error guidance:** Reference debug logs with searchable error codes
- **No technical noise:** Avoid verbose progress updates

### 8.2 Debug Logging Requirements

#### Domain Tagging
- **Primary tag:** `[<DOMAIN>-<COMPONENT>]` format for all debug messages
- **Component examples:** `MAPPING`, `VALIDATION`, `EXPORT`, `ORCHESTRATION`
- **Cross-references:** Use specific error codes for console log coordination
- **No prefixes:** No `AUDIT:` or similar prefixes permitted

#### Debug Content Standards
- **Technical detail focus:** Comprehensive processing steps and decision points
- **Error context:** Complete error information with file paths and validation details
- **Processing metrics:** Record counts, timing, and resource usage where relevant
- **Decision logging:** Document configuration choices and fallback logic

### 8.3 Logging Implementation Patterns

#### Function Call Examples
```python
# Console logging (user-focused)
log_user_info(f"[{DOMAIN}-PIPELINE] Starting {domain} processing with {len(records)} records")
log_user_error(f"[{DOMAIN}-PIPELINE] Module reports HALT. User action required. See debug log \"E{code}\" around {timestamp}")

# Debug logging (technical detail)
log_technical_detail(f"[{DOMAIN}-MAPPING] Loading configuration from: {config_path}")
log_technical_detail(f"[{DOMAIN}-VALIDATION] Validated {count} records against schema")
```

#### Error Code Coordination
- **HALT conditions:** Include millisecond timestamp for debug log searching
- **Error references:** Format `"E{code}" around {HH:MM:SS.mmm}` for precise navigation
- **Searchable patterns:** Ensure debug logs include referenced error codes

**Domain-Specific Logging:** [Specify any additional logging requirements unique to this domain, such as mapping statistics, conversion metrics, etc.]

All logging must reference authoritative error classes, codes, and severity levels from [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table).

---

## 9. Versioning & Change Control

### 9.1 Revision History
| Version | Date       | Author     | Summary |
|---------|------------|------------|---------|
| v1.0.0  | YYYY-MM-DD | [Author]   | Initial release |

> **Revision History Guidance:** All entries must be append-only, strictly chronological, and never deleted or overwritten. See [Governance Model PRD v2.7.0 Section 4.3: Revision History Requirements](../prd-governance-model-v2.7.0.md#43-revision-history-requirements).

### 9.2 Upstream/Downstream Impacts
[Describe effects on other modules or system components. Consider impacts on:
- Core dispatch system if interface changes
- Output consumers (GnuCash import process)
- Other domain modules if shared utilities are affected
- Configuration file formats]

---

## 10. Non-Functional Requirements
[Performance, security, scalability, maintainability requirements specific to this domain. Reference [Core PRD v3.9.1 Section 13.1: Non-Functional Requirements](../core-prd-main-v3.9.1.md#131-non-functional-requirements) for baseline requirements. No unit testing requirements - testing handled by post-processing workflows.]

---

## 11. Open Questions / TODOs
[List any unresolved issues, decisions, or items needing follow-up. Remove this section when all items are resolved.]

---

## 12. Appendix (Optional)
### 12.1 Data Schemas or Additional References
```json
{
  "domain_record_example": {
    "field1": "value_type",
    "field2": "value_type"
  },
  "mapping_file_schema": {
    "domain_types": {
      "qbd_type": {
        "gnucash_type": "string",
        "hierarchy_path": "string"
      }
    },
    "default_rules": {
      "fallback_type": "string"
    }
  }
}
```
> All schemas and data structures must be referenced from the main text and use canonical formats.

---

## 13. Domain Module Naming and Containment Rules

To ensure maintainability, prevent cross-domain collisions, and support governance enforcement:

- All domain-specific modules must:
  - Use a domain prefix in their filename (e.g., `accounts_`, `customers_`)
  - Reside within their respective domain directory (e.g., `src/modules/accounts/`)
  - Avoid placement in `src/utils/` or any unrelated folder

- Only domain-agnostic modules may be placed in `src/utils/` (e.g., `iif_parser.py`, `error_handler.py`, `logging.py`)

### Examples
✅ `src/modules/accounts/accounts_validation.py`  
❌ `src/utils/validation.py` *(violates naming and containment rules)*

### Developer Checklist
Before creating or moving any file:
- ✅ Prefix domain logic with its module name
- ✅ Place it under `src/modules/<domain>/`
- ❌ Never place domain logic in `utils/`

> This rule is mandatory for all current and future modules. Violations are considered governance failures and must be corrected before codegen or commit.

---

## 14. Governance & Compliance Checklist
- [ ] PRD file is located in the correct directory (`prd/<domain>/`)
- [ ] PRD filename matches governance rules (`module-prd-[domain]_[tag]-v[version].md`)
- [ ] All section headers are immutable and not paraphrased
- [ ] All major sections are delimited by `---` (horizontal rule only before/after major sections)
- [ ] All section numbers are strictly sequential with no gaps
- [ ] All placeholders have been replaced with actual content
- [ ] Compatible Core PRD and Governance Model versions specified
- [ ] Dependency metadata block present and version-locked
- [ ] Revision history table matches governance format and is append-only
- [ ] Entry point follows `run_<domain>_pipeline()` standard from [Core PRD v3.9.1 Section 11.6: Module Entry Point Standards](../core-prd-main-v3.9.1.md#116-module-entry-point-standards)
- [ ] All error codes reference [Core PRD v3.9.1 Section 14: Authoritative Error Classes & Error Code Table](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table)
- [ ] Interface contracts comply with [Core PRD v3.9.1 Section 11.5: Interface Authority Precedence Rules](../core-prd-main-v3.9.1.md#115-interface-authority-precedence-rules)
- [ ] Module boundary placement follows [Core PRD v3.9.1 Section 12.1: Enhanced Module Boundary Specification Matrix](../core-prd-main-v3.9.1.md#121-enhanced-module-boundary-specification-matrix)
- [ ] All inter-PRD and intra-PRD references use compliant linking format per [Governance v2.7.0 Section 5: PRD Reference and Linking Standards](../prd-governance-model-v2.7.0.md#5-prd-reference-and-linking-standards) (see below for examples)
- [ ] Payload input/output schemas validated against `core_dispatch_payload_v1`
- [ ] No CLI argument processing included
- [ ] All outputs directed to `output/` directory structure
- [ ] Domain-specific error code range assigned and documented
- [ ] Domain name matches authoritative domain index
- [ ] Console and debug logging patterns implemented per Section 8 requirements
- [ ] Domain tagging follows `[<DOMAIN>-<CONTEXT>]` format with ASCII compliance
- [ ] README and documentation artifacts updated to reflect all PRD changes (PRD-to-README alignment required)

> **Compliant Inter-PRD Link Example:**
> [Core PRD v3.9.1 Section 7.3: Logging Strategy](../core-prd-main-v3.9.1.md#73-logging-strategy)
> **Compliant Intra-PRD Link Example:**
> [Section 7.2: Error Classes & Exit Codes](#72-error-classes--exit-codes)

---

> **Note:** All section headers are immutable per [Governance v2.7.0 Section 2.2: Semantic Stability](../prd-governance-model-v2.7.0.md#22-semantic-stability). No renaming or paraphrasing is permitted. All placeholders must be replaced before PRD acceptance. This template incorporates all CR-2025-002 governance precision enhancements for conflict-free LFC artifact generation and horizontal scaling to roadmap domains.