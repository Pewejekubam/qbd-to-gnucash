# Core PRD: QuickBooks Desktop to GnuCash Conversion Tool

**Document Version:** v3.9.1
**Module Identifier:** core-prd-main-v3.9.1.md  
**Compatible Core PRD:** core-prd-main-v3.9.1.md  
**Governance Model:** prd-governance-model-v2.7.0.md  
**State:** CR-002 Phase 2 Complete  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-06-10  

---

## 1. Scope
This project delivers a modular, command-line conversion tool for migrating financial data from QuickBooks Desktop (QBD) into GnuCash using structured import files. The core framework applies a consistent, extensible processing pipeline—centralized input ingestion and parsing, followed by dispatching well-defined payloads to domain modules for mapping and output generation—which is reused across all modules. Each domain module (e.g., Accounts, Vendors, Transactions, and others) is responsible for converting its respective QBD data as received from the dispatcher into GnuCash-compatible formats, as defined in its own PRD. The core PRD defines the shared architecture, orchestration, and extension points for all modules.

This project is CLI-only; no graphical user interface or CLI arguments will be developed or supported.

### 1.1 Target Audience
This tool is intended for technical users — accountants, bookkeepers, or developers — performing structured financial data migration from QBD to GnuCash. Familiarity with the principles of double-entry accounting and GnuCash's account-type model is strongly recommended.

---

## 2. Structural Rules
All section numbering and headers shall be strictly sequential and hierarchical, following the format `## <n>. <Title>`, with subsections as `### <n>.<m> <Title>`. No numbering jumps, omissions, or renumbering inconsistencies are permitted. All major sections shall be delimited by a horizontal rule (`---`). Section headers are immutable; no renaming or paraphrasing is allowed. Documents failing to conform to these requirements shall be rejected or corrected before further processing.

---

## 3. Background Context
QuickBooks Desktop is a proprietary platform, and many users are migrating to open-source accounting systems for reasons including cost, longevity, and transparency. However, the lack of compatible conversion tooling presents a serious barrier. This project exists to fill that gap, enabling clean migration of core data without data loss and with minimal manual recreation.

---

## 4. Formatting Protocols
Only Markdown is permitted. No embedded HTML, LaTeX, or rich text formatting is allowed. All code blocks, lists, and indentation shall remain in canonical syntax without modification. No summaries, examples, or commentary may be introduced unless explicitly required by protocol.

---

## 5. Versioning Enforcement
### 5.1 Revision History

| Version | Date       | Author | Summary                                                |
|---------|------------|--------|--------------------------------------------------------|
| 2.7.3   | 2025-05-15 | PJ     | Final monolithic PRD before modularization            |
| 3.0.0   | 2025-05-16 | PJ     | Core PRD established as root of a modular PRD system. All module-specific logic to be extracted into versioned standalone files in `./prd/{module}/` |
| 3.0.1   | 2025-05-17 | PJ     | Minor clarifications and error handling improvements   |
| 3.1.0   | 2025-05-18 | PJ     | Mandated explicit function signatures and interface contracts for all module boundaries |
| 3.3.1   | 2025-05-19 | PJ     | Standardized terminology for mapping diff file, output file path, and accounts.csv. Added Terminology section for clarity and future consistency |
| 3.4.0   | 2025-05-20 | PJ     | Added explicit JSON Schema and Python typing examples for all major data structures. Updated interface contracts and example calls for public functions/classes |
| 3.4.1   | 2025-05-21 | PJ     | Split module logic into dedicated files and updated user story mappings |
| 3.5.0   | 2025-05-22 | PJ     | Finalized full extraction and compliance with separation of concerns and compartmentalization of domain-specific content |
| 3.5.1   | 2025-05-23 | PJ     | Remediated governance audit violations (compatibility matrix, history format, duplicate sections, user story subsections) |
| 3.6.0   | 2025-05-24 | PJ     | Corrected domain module naming                         |
| 3.6.1   | 2025-05-25 | PJ     | Reorganized for full compliance with governance v2.3.10 |
| 3.6.2   | 2025-05-25 | PJ     | Fully integrated, restored missing content, finalized for full governance compliance |
| 3.6.3   | 2025-05-25 | PJ     | Finalized authoritative revision history, ensured full compliance, and validated content integrity from v3.6.0 |
| 3.6.4   | 2025-05-30 | PJ     | Full, flat, standalone core PRD. All references, metadata, and section anchors updated to v3.6.4. Supersedes v3.6.3. |
| 3.6.5   | 2025-06-03 | PJ     | Standardized Error Classes & Exit Codes and Logging & Observability sections to reference  |
| 3.6.6   | 2025-06-10 | PJ     | Governance compliance pass: standardized "shall" language, updated governance model reference to v2.5.0 |
| 3.7.0   | 2025-06-10 | PJ     | Corrected payload schema to 4-field working implementation per CR-001 |
| 3.8.0   | 2025-06-10 | PJ     | Phase 1 governance compliance cleanup: reordered revision history, removed redundant sections, added dependency declarations per Governance v2.7.0 |
| 3.9.0   | 2025-06-10 | PJ     | Phase 2 CR-002 implementation: added interface authority precedence rules, module entry point standards, enhanced module boundary specification matrix |

---

## 6. Inter-PRD Dependencies
All module references shall use relative paths and canonical anchor links (e.g., `[Section 7.1.1: Domain Module Naming](#711-domain-module-naming-and-containment-rules)`). Invalid references shall trigger rejection—no silent failures. Cross-version references require explicit version-lock enforcement. All referenced PRDs shall exist in the repository and be version-locked in the reference (e.g., `[Logging Framework PRD v1.0.4: Interface Section](./logging/module-prd-logging-v1.0.4.md#5-interface--integration)`).

---

## 7. AI Agent Compliance
PRDs shall be executable by autonomous agents without transformation. Acceptable interface formats: TypedDict, JSON Schema, strict enumerations. Exception types, exit codes, and validation suites shall be explicitly defined. Logging shall be deterministic and flush-safe. No heuristic assumptions are allowed.

---

## 8. Governance Authority
This protocol overrides all prior formatting practices, inline notes, and AI model heuristics. Precedence follows: governance > core PRD > module PRD. No agent or human may override governance without a formally published revision.

---

## 9. Compliance Enforcement
AI agents shall affirm this governance before making structural edits. Human contributors shall pass protocol validation before submitting or merging changes. All violations trigger PRD invalidation. Affected versions shall not be processed.

---

## 10. User Stories & Use Cases
### 10.1 Actors
- **Finance team member**: Converts a QBD account list into a GnuCash-compatible format.
- **Technical operator**: Validates CSV structure before importing into GnuCash.
- **Developer**: Integrates the tool into an automated migration pipeline.
- **Business stakeholder**: Reviews logs and diffs for data integrity.
- **Contributor**: Extends the architecture to other QBD data types.

### 10.2 Usage Flow
- The core engine parses input files and dispatches data to the configured domain modules for processing.
- The core engine loads and validates mapping configuration files to ensure consistent domain module behavior.
- The core engine logs processing steps and errors in a structured format for downstream auditing and debugging.
- The system supports dynamic module integration via configuration to extend supported data domains.

### 10.3 User Stories
- As a finance team member, I want to convert a QBD account list into a GnuCash-compatible format so I can continue managing finances without proprietary software.
- As a technical operator, I want to validate the CSV structure before importing into GnuCash so I can avoid errors during the migration.
- As a developer, I want the tool to be modular and scriptable so I can integrate it into an automated migration pipeline.
- As a business stakeholder, I want to see clear logs and diffs so I can trust the data integrity of the migrated output.
- As a contributor, I want the architecture to be transparent and well-documented so I can extend it to other QBD data types in the future.

> **Creator's User Story:**  
> As a technical team lead, I'm responsible for migrating our company's financial records from QuickBooks Desktop after Intuit's repeated subscription hikes — most recently from $142 to $163 *per seat*. With multiple users across departments, this translates into thousands of dollars per month. This tool is being developed to eliminate that recurring cost, free us from vendor lock-in, and preserve full access to our historical financial data in a stable, open-source system.

### 10.4 Use Cases
- These user stories and use cases reflect real-world pressures faced by organizations using QBD — primarily the rising cost of licensing and the limitations of proprietary formats. By designing the tool to operate via the command line and to support detailed inspection, mapping flexibility, and configuration diffs, it solves not only the technical challenge of migration but also addresses auditability, extensibility, and maintainability. This allows both end users and system owners to move toward GnuCash with confidence and control.

---

## 11. System Architecture and Workflow

Project root:
- input/
  - sample-qbd-accounts.IIF
  - sample-qbd-customers.IIF
  - sample-qbd-items.IIF
  - sample-qbd-payment-terms.IIF
  - sample-qbd-sales-tax-codes.IIF
- output/
  - qbd-to-gnucash.log
- prd/
  - core-prd-v3.9.0.md
  - prd-module-template-v3.6.2.md
  - README-core.md
  - accounts/
    - module-prd-accounts-v1.1.3.md
    - module-prd-accounts_mapping-v1.0.8.md
    - module-prd-accounts_validation-v1.0.2.md
    - module-prd-accounts_export-v1.0.1.md
    - README-accounts.md
    - README-accounts_mapping.md
    - README-accounts_validation.md
    - README-accounts_export.md
  - logging/
    - module-prd-logging-v1.0.4.md
    - README-logging.md
- src/
  - main.py
  - core.py
  - modules/
    - accounts/
      - accounts.py
      - accounts_export.py
      - accounts_mapping.py
      - accounts_mapping_baseline.json
      - accounts_tree.py
      - accounts_validation.py
  - utils/
    - error_handler.py
    - iif_parser.py
    - logging.py

> For rules about domain ownership and why `accounts_tree.py` lives inside the `accounts` module, see [Section 12.1.1: Domain Module Naming and Containment Rules](#1211-domain-module-naming-and-containment-rules).

### 11.1 Error Handling Strategy

**Error Classifications**

| Stage                 | Example Errors                                             |
|-----------------------|------------------------------------------------------------|
| **Parsing**           | Missing header in input file, tab mismatch, invalid UTF-8  |
| **Mapping**           | Unknown domain type, no destination hierarchy defined      |
| **Tree Construction** | Missing parent, failed 1-child promotion, circular paths   |
| **Output**            | File write permission denied, output file malformed        |
| **Registry**          | Unregistered key, key conflict, fallback loop              |

*Note: Each module PRD shall define any additional error types and examples relevant to its domain. The above are illustrative and may be extended by modules.*

**Metadata Required**
- **File or Key**: e.g., `input file`, `domain key`
- **Line/Record Ref**: e.g., `Row 24`, `Record Name: ...`
- **Processing Step**: Parsing → Mapping → Tree → Output
- **Expected vs Actual**: Clear diff
- **Registry Context**: If applicable

**Fallback Rules**

| Condition                | Action (Module-defined)                |
|-------------------------|----------------------------------------|
| Unmapped domain type     | Fallback to module-defined default     |
| Missing parent path      | Insert placeholder dynamically         |
| Registry key not defined | Fail with structured error             |
| Input file unreadable    | Abort with detailed notice             |

*Note: Fallback actions are defined by each module PRD. The above are architectural patterns; see module PRDs for specifics (e.g., Accounts module may fallback to `Uncategorized:ASSET`).*

**Feedback Format**
- Console output: Human-readable
- Log file: Trace with file, function, chain
- Optional debug: Intermediate decisions and chain
- Agent-compatible phrasing and structure

*Module PRDs shall specify any additional feedback or logging requirements unique to their domain.*

### 11.2 Interface Contracts and Function Signatures

- All module boundaries shall have clearly documented function signatures in the PRD.
  - This includes function name, argument names and types (using Python typing), return type, exceptions raised, and a 1-2 line docstring/description.
  - Example format:
    ```python
    def process_domain_payload(payload: Dict[str, Any]) -> bool:
        """Process dispatched payload through domain-specific pipeline."""
        # ...function implementation...
        
    Raises: DomainValidationError
    
    # Example usage:
    success = process_domain_payload(dispatch_payload)
    ```
- For each module, the PRD shall include an "Interface Contract" section that specifies:
  - All public functions/classes intended for use by other modules.
  - Expected input and output types (using Python typing).
  - Error/exception handling expectations.
  - A realistic example call for every public function/class, matching the documented signature and reflecting a real use case.
- Any change to a shared interface shall be reflected in the PRD and communicated to all dependent modules.
- The PRD requires a review process for interface changes, including updating all relevant documentation and test cases.
- Code reviews shall check for conformance to the documented contracts.
- Example calls and test cases should be included in the PRD to clarify correct usage.

### 11.3 Core Interface Contracts

This section documents the public interface contracts for core orchestration functions that modules interact with. All signatures, docstrings, exception handling, and example usages follow the standards established in Section 11.2. These contracts ensure reliable integration, governance compliance, and agentic compatibility across the codebase.

#### 11.3.1 Core Orchestration Functions

##### `run_conversion_pipeline`
```python
def run_conversion_pipeline(config: Dict[str, Any]) -> int:
    """Orchestrate the full conversion process: input parsing, mapping, tree construction, output generation, and logging.
    Args:
        config (Dict[str, Any]): Configuration dictionary specifying input/output paths, module registry, and mapping files.
    Returns:
        int: Exit code (0=success, 1=critical error, 2=validation error)
    Raises:
        FileNotFoundError: If required input files are missing.
        RegistryKeyConflictError: If two modules claim the same registry key.
        Exception: For any uncaught critical error.
    """
    # ...function implementation...

# Example usage:
from core import run_conversion_pipeline
exit_code = run_conversion_pipeline(config)
if exit_code != 0:
    sys.exit(exit_code)
```

##### `register_module`
```python
def register_module(registry: Dict[str, Any], key: str, entry_point: Callable[[Dict[str, Any]], bool]) -> None:
    """Register a domain module entry point with the core registry for dispatching input sections.
    Args:
        registry (Dict[str, Any]): The central registry mapping section keys to entry points.
        key (str): The unique section key (e.g., 'ACCNT').
        entry_point (Callable[[Dict[str, Any]], bool]): The module entry point function following Section 11.6 standards.
    Raises:
        RegistryKeyConflictError: If the key is already registered.
    """
    # ...function implementation...

# Example usage:
register_module(registry, 'ACCNT', accounts.run_accounts_pipeline)
```

##### `dispatch_to_module`
```python
def dispatch_to_module(registry: Dict[str, Any], section_key: str, payload: Dict[str, Any]) -> bool:
    """Dispatch complete payload to the appropriate domain module for processing.
    Args:
        registry (Dict[str, Any]): The central registry mapping section keys to entry points.
        section_key (str): The section key identifying the domain (e.g., 'ACCNT').
        payload (Dict[str, Any]): Complete dispatch payload conforming to core_dispatch_payload_v1 schema.
    Returns:
        bool: Success indication from module processing.
    Raises:
        KeyError: If the section_key is not registered.
        Exception: For module-specific processing errors.
    """
    # ...function implementation...

# Example usage:
success = dispatch_to_module(registry, 'ACCNT', dispatch_payload)
```

##### `log_and_exit`
```python
def log_and_exit(message: str, code: int = 1) -> None:
    """Log a critical error message and exit the process with the specified code.
    Args:
        message (str): The error message to log.
        code (int, optional): Exit code (default: 1).
    Raises:
        SystemExit: Always raised to terminate the process.
    """
    # ...function implementation...

# Example usage:
log_and_exit('Critical error: input file missing', code=1)
```

#### 11.3.2 Exception Classes

All custom exceptions raised by core functions and modules shall reference the authoritative error classes and error codes defined in [Section 14: Authoritative Error Classes & Error Code Table](#14-authoritative-error-classes--error-code-table). Each exception shall use its unique error code (e.g., `E0001`, `E0201`) and corresponding exit code as specified in the table.

The `utils/error_handler.py` module serves as the central registry for error management, ensuring all error classes and codes are version-locked, logically consistent, and compliant with this PRD. Any addition or modification of error classes or codes shall be reflected both in Section 14 and in `utils/error_handler.py`.

**Error Implementation Protocol:**

Error codes defined in Section 14 are mapped to function logic through deterministic pattern matching. Implementation is protocol-driven, not discretionary.

**Implementation Mapping:**
- File operations → File-related error codes (E0101, E0106, E0108, etc.)
- Data validation → Validation error codes (E0102, E0107, E1190, etc.)
- Parsing operations → Parse error codes (E0105, E0109, E0110, etc.)
- Export operations → Output error codes (E0104, E0111, E0112, etc.)

**Protocol Enforcement:** Functions containing logical patterns that correspond to error code descriptions in Section 14 shall implement those error codes automatically. No implementation discretion exists.

**Example usage:**

```python
from utils.error_handler import MappingLoadError

try:
    mapping = load_mapping('output/missing.json')
except MappingLoadError as e:
    # E1101: Mapping file missing, unreadable, or invalid schema (Exit Code: 2)
    log_and_exit(f"[E1101] {str(e)}", code=2)
```

- All raised exceptions shall include their error code in log output and follow the exit code discipline.
- All modules and the core shall use only the error classes and codes defined in Section 14.
- No ad-hoc or undocumented error classes are permitted.

### 11.4 Input File Discovery and Processing Model

The tool supports dynamic discovery and structured dispatch of user-provided `.IIF` files placed in the `input/` directory. This section defines the complete file ingestion lifecycle.

#### 11.4.1 File Discovery
- All `.IIF` files (case-insensitive) located in the `input/` directory will be discovered.
- Filenames are not interpreted for routing or validation. Discovery is content-based.
- Subdirectories inside `input/` are ignored.

#### 11.4.2 Section Header Parsing
- Each `.IIF` file is scanned line-by-line to detect top-level QuickBooks headers (e.g., `ACCNT`, `TRNS`, `CUST`, etc.).
- Header lines may occur in any order and may be interleaved with data or other headers.
- A single `.IIF` file may contain multiple section types. All are independently extracted.
- Unsupported or unrecognized headers will be logged and ignored with a warning.

#### 11.4.3 Module Dispatch
- For each detected section, a normalized dispatch event is constructed and routed to the appropriate processing module (e.g., `accounts`, `transactions`, `customers`, etc.).
- Each section is processed independently, even if originating from the same `.IIF` file.
- Processing modules receive dispatched section data and produce domain-appropriate output as defined in their respective module PRDs.

#### 11.4.4 Dispatch Payload Schema

All section data is passed between components using a canonical dispatch schema:

**`core_dispatch_payload_v1`**

| Key              | Type     | Description                                         |
|------------------|----------|-----------------------------------------------------|
| `section`        | `str`    | QuickBooks header name (e.g., `ACCNT`)            |
| `records`        | `list`   | Parsed records under the section header            |
| `output_dir`     | `str`    | Destination directory for processed output         |
| `extra_config`   | `dict`   | Optional: Additional runtime parameters (may be empty) |

All module contracts shall conform to this schema.

### 11.5 Interface Authority Precedence Rules

This section establishes the authoritative hierarchy for interface specifications to prevent conflicts between Core PRD and Module PRD interface definitions.

#### 11.5.1 Authority Hierarchy
- **[Section 11.3.1: Core Orchestration Functions](#1131-core-orchestration-functions)**: Cross-module interface patterns (authoritative)
- **Module PRD Section 6.2**: Domain-specific implementations (compliant)
- **Conflict Resolution**: Core PRD specifications supersede module PRD specifications for interface consistency

#### 11.5.2 Consistency Requirements
- All module interface contracts shall reference Core PRD patterns established in [Section 11.3.1: Core Orchestration Functions](#1131-core-orchestration-functions)
- Deviations from Core PRD interface patterns require explicit authorization documentation
- Interface changes shall propagate through the precedence hierarchy: Core → Module
- Module PRDs shall not contradict Core PRD interface specifications

#### 11.5.3 Implementation Standards
- Function signatures defined in [Section 11.3.1: Core Orchestration Functions](#1131-core-orchestration-functions) are binding for all modules
- Module-specific extensions shall follow Core PRD patterns and naming conventions
- Error handling contracts defined in [Section 11.3.2: Exception Classes](#1132-exception-classes) are mandatory across all modules
- Module PRDs shall document compliance with Core PRD interface authority

### 11.6 Module Entry Point Standards

Module entry points shall conform to standardized patterns for consistent dispatch integration.

#### 11.6.1 Entry Point Specification
- **Function Name Pattern:** `run_<domain>_pipeline`
- **Parameter:** Single payload parameter of type `Dict[str, Any]`
- **Return Type:** Boolean indicating processing success
- **Payload Schema:** Must accept `core_dispatch_payload_v1` as defined in Section 11.4.4

#### 11.6.2 Implementation Pattern
All domain modules implement the entry point specification identically. Function logic processes the payload according to domain-specific requirements defined in the respective module PRD.

---

## 12. Module Ownership and Directory Boundaries

### 12.1 Enhanced Module Boundary Specification Matrix

To ensure maintainability, prevent cross-domain collisions, and support governance enforcement, this section provides explicit decision matrices for module logic placement and boundary enforcement.

#### 12.1.1 Module Logic Placement Decision Matrix

**Domain-Specific Logic Placement:**

| Logic Type | Correct Location | Incorrect Location | Enforcement |
|------------|------------------|-------------------|-------------|
| Account validation | `src/modules/accounts/accounts_validation.py` | `src/utils/validation.py` | ❌ Governance violation |
| Customer mapping | `src/modules/customers/customers_mapping.py` | `src/utils/mapping.py` | ❌ Governance violation |
| Sales tax calculation | `src/modules/sales_tax/sales_tax_calculation.py` | `src/modules/accounts/` | ❌ Cross-domain violation |
| Generic IIF parsing | `src/utils/iif_parser.py` | `src/modules/accounts/` | ✅ Appropriate for utils |

**Decision Criteria:**
- **Domain-Specific**: Contains business logic specific to a QuickBooks data domain → Must use domain prefix and reside in `src/modules/<domain>/`
- **Cross-Domain Utility**: Reusable across multiple domains with no domain-specific logic → May reside in `src/utils/`
- **Hybrid Logic**: Contains both generic and domain-specific elements → Split into appropriate components

#### 12.1.2 Examples (Correct vs Incorrect)

**✅ Better Examples Using Existing Structure:**
- `src/modules/accounts/accounts_validation.py` - Real domain-specific validation logic
- `src/modules/accounts/accounts_mapping.py` - Real domain-specific mapping logic
- `src/utils/iif_parser.py` - Real cross-domain utility used by all domains
- `src/utils/error_handler.py` - Real cross-domain error management

**❌ Incorrect Examples:**
- `src/utils/validation.py` - Violates domain-specific logic placement rules
- `src/modules/accounts/other_domain_logic.py` - Violates cross-domain boundaries
- `src/modules/shared/common_mapping.py` - Creates ambiguous ownership

#### 12.1.3 Developer Checklist

Before creating or moving any file:
- ✅ Does this logic belong to a specific QuickBooks domain? → Use domain prefix and `src/modules/<domain>/`
- ✅ Is this logic truly reusable across all domains? → May use `src/utils/`  
- ✅ Does this create cross-domain dependencies? → Refactor or document authorized deviation
- ❌ Never place domain-specific logic in `src/utils/`
- ❌ Never create shared directories that blur domain ownership

> This rule is mandatory for all current and future modules. Violations are considered governance failures and shall be corrected before codegen or commit.

---

## 13. Non-Functional Requirements, Testing, Onboarding, and Extensibility

### 13.1 Non-Functional Requirements
- **Performance:** The tool shall process typical QBD exports (up to 10,000 records per section) in under 60 seconds on commodity hardware.
- **Reliability:** All critical errors shall be logged and surfaced to the user. The tool shall fail fast on unrecoverable errors and provide actionable diagnostics.
- **Portability:** The tool shall run on Windows, macOS, and Linux with no code changes, requiring only Python 3.8+ and standard libraries.
- **Maintainability:** All modules and core logic shall be documented and follow the interface contract and directory rules.

### 13.2 Testing and Validation
- **Integration Tests:** The core pipeline shall be tested end-to-end using sample `.IIF` files and mapping configurations.
- **Validation:** Output files shall be validated against GnuCash import requirements. Validation errors shall be logged and surfaced.
- **Test Artifacts:** Sample input and output files shall be maintained in a dedicated test directory.

### 13.3 Onboarding and Contributor Guidance
- **Getting Started:** New contributors should review the core PRD, module PRDs, and governance model before making changes.
- **Setup:** Clone the repository, install Python 3.8+, and run `python src/main.py` to execute the tool.
- **Contribution:** All changes shall be accompanied by PRD updates and tests. Code reviews shall check for governance compliance.

### 13.4 Extensibility
- **Adding Modules:** New domains can be added by creating a new module PRD and implementing the required interface contract. The core registry shall be updated to recognize the new section key.

---

## 14. Authoritative Error Classes & Error Code Table

All error codes are strictly numeric and follow a semantic numbering convention to ensure unique, easily referenced, and module-aligned identification. The first two digits indicate the associated module or domain, while the last two digits provide a unique identifier within that module's error class space. This structure enables rapid lookup, traceability, and governance enforcement.

- **E01xx** — Core and pipeline orchestration errors (input, config, registry, output, general validation)
- **E02xx** — Logging and observability subsystem errors
- **E11xx** — Accounts domain and submodules (mapping, tree, export, domain validation)
- **E91xx** — Governance and compliance violations
- **E99xx** — Reserved for unknown or unclassified errors

This numbering scheme is append-only and version-locked. Each module or domain PRD shall allocate new error codes within its assigned range, ensuring no overlap or ambiguity across the system.

| Error Class                  | Error Code | Description                                                      | Associated Module(s)      | Exit Code |
|------------------------------|------------|------------------------------------------------------------------|---------------------------|-----------|
| FileNotFoundError            | E0101      | Required input file is missing or unreadable                     | core, all                 | 1         |
| ValidationError              | E0102      | Input or output data fails schema or contract validation         | core, all                 | 2         |
| RegistryKeyConflictError     | E0103      | Duplicate registry key detected during module registration       | core                      | 1         |
| OutputWriteError             | E0104      | Output file cannot be written (permissions, disk full, etc.)     | core, all                 | 1         |
| IIFParseError                | E0105      | Raised when .IIF file parsing fails or input is malformed.       | core, all                 | 2         |
| ConfigFileNotFoundError      | E0106      | Required config file is missing or unreadable                    | core, all                 | 1         |
| ConfigValidationError        | E0107      | Config file fails schema or semantic validation                  | core, all                 | 2         |
| InputDirectoryNotFoundError  | E0108      | Input directory is missing or inaccessible                       | core                      | 1         |
| InputFileFormatError         | E0109      | Input file is not a valid IIF or expected format                 | core, all                 | 2         |
| SectionHeaderNotFoundError   | E0110      | No recognizable section headers found in input file              | core, all                 | 2         |
| OutputDirectoryNotFoundError | E0111      | Output directory missing or cannot be created                    | core, all                 | 1         |
| OutputFormatError            | E0112      | Output file fails post-write validation                          | core, all                 | 2         |
| PipelineHaltError            | E0113      | Unexpected halt not covered by other error classes               | core                      | 1         |
| LoggingError                 | E0201      | Logging subsystem failed to record a required event              | logging                   | 1         |
| LogFileWriteError            | E0202      | Log file cannot be written                                       | logging                   | 1         |
| LogFormatError               | E0203      | Log entry fails to serialize or is malformed                     | logging                   | 2         |
| MappingLoadError             | E1101      | Mapping file missing, unreadable, or invalid schema              | accounts_mapping          | 2         |
| UnmappedAccountTypeError     | E1102      | QBD account type not mapped and no default rule applies          | accounts_mapping          | 2         |
| MappingRuleError             | E1103      | Mapping config contains invalid or ambiguous rules               | accounts_mapping          | 2         |
| MappingAmbiguityError        | E1104      | Multiple mapping rules match a single input                      | accounts_mapping          | 2         |
| UnmappedFieldError           | E1105      | Required field in input has no mapping and no default            | accounts_mapping, all     | 2         |
| ExportOperationError         | E1106      | Failure during export logic                                      | accounts_export, all      | 2         |
| TreeConstructionError        | E1110      | Account tree cannot be constructed due to missing/circular refs  | accounts, accounts_tree   | 2         |
| AccountsTreeError            | E1111      | Raised when account hierarchy is invalid (e.g., cycles, orphan nodes, etc). | accounts_tree             | 2         |
| DomainValidationError        | E1190      | Domain-specific validation failed                                | all domain modules        | 2         |
| DomainDependencyError        | E1191      | Required domain dependency missing or failed to load             | all domain modules        | 1         |
| GovernanceViolationError     | E9101      | Detected violation of PRD/governance rules                       | core, all                 | 1         |
| UnknownError                 | E9999      | Unclassified error                                               | all                       | 1         |