# Core PRD: QuickBooks Desktop to GnuCash Conversion Tool

**Document Version:** v3.6.9 
**Module Identifier:** core-prd-main-v3.6.9.md  
**State:** CR-001 Implementation Complete - All Requirements Addressed
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-06-10  
**Governance Model:** prd-governance-model-v2.5.0.md  

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
| 3.6.5   | 2025-06-03 | PJ     | Standardized Error Classes & Exit Codes and Logging & Observability sections to reference  |
| 3.6.4   | 2025-05-30 | PJ     | Full, flat, standalone core PRD. All references, metadata, and section anchors updated to v3.6.4. Supersedes v3.6.3. |
| 3.6.3   | 2025-05-25 | PJ     | Finalized authoritative revision history, ensured full compliance, and validated content integrity from v3.6.0 |
| 3.6.2   | 2025-05-25 | PJ     | Fully integrated, restored missing content, finalized for full governance compliance |
| 3.6.1   | 2025-05-25 | PJ     | Reorganized for full compliance with governance v2.3.10 |
| 3.6.0   | 2025-05-24 | PJ     | Corrected domain module naming                         |
| 3.5.1   | 2025-05-23 | PJ     | Remediated governance audit violations (compatibility matrix, history format, duplicate sections, user story subsections) |
| 3.5.0   | 2025-05-22 | PJ     | Finalized full extraction and compliance with separation of concerns and compartmentalization of domain-specific content |
| 3.4.1   | 2025-05-21 | PJ     | Split module logic into dedicated files and updated user story mappings |
| 3.4.0   | 2025-05-20 | PJ     | Added explicit JSON Schema and Python typing examples for all major data structures. Updated interface contracts and example calls for public functions/classes |
| 3.3.1   | 2025-05-19 | PJ     | Standardized terminology for mapping diff file, output file path, and accounts.csv. Added Terminology section for clarity and future consistency |
| 3.1.0   | 2025-05-18 | PJ     | Mandated explicit function signatures and interface contracts for all module boundaries |
| 3.0.1   | 2025-05-17 | PJ     | Minor clarifications and error handling improvements   |
| 3.0.0   | 2025-05-16 | PJ     | Core PRD established as root of a modular PRD system. All module-specific logic to be extracted into versioned standalone files in `./prd/{module}/` |
| 2.7.3   | 2025-05-15 | PJ     | Final monolithic PRD before modularization  |
| 3.6.6   | 2025-06-10 | PJ     | Governance compliance pass: standardized "shall" language, updated governance model reference to v2.5.0 |
| 3.7.0   | 2025-06-10 | PJ     | Implemented CR-001: corrected payload schema, fixed section identifiers, added interface definitions, exception contracts, logging constraints, module entry point requirements, boolean return type standardization, and module boundary enhancement matrices |

---

## 6. Update Discipline
Edits shall strictly modify the targeted logic. Collateral adjustments are prohibited. Insertions shall occur at precisely the correct semantic location. Renumbering shall occur coherently across all affected sections in a single correction pass.

---

### 7.1 Module Ownership and Directory Boundaries
Each domain module owns its **full functional implementation**, including all subcomponents necessary for its logic, construction, and validation.

#### 7.1.1 Domain Module Naming and Containment Rules
To ensure maintainability, prevent cross-domain collisions, and support governance enforcement:
- All domain-specific modules shall:
  - Use a domain prefix in their filename (e.g., `accounts_`, `customers_`).
  - Reside within their respective domain directory (e.g., `src/modules/accounts/`).
  - Avoid placement in `src/utils/` or any unrelated folder.
- Only domain-agnostic modules may be placed in `src/utils/` (e.g., `iif_parser.py`, `error_handler.py`, `logging.py`).

##### 7.1.1.1 Examples (Correct vs Incorrect)
Correct: `src/modules/accounts/accounts_validation.py`  
Incorrect: `src/utils/validation.py` *(violates naming and containment rules)*

##### 7.1.1.2 Developer Checklist
Before creating or moving any file:
- Correct: Prefix domain logic with its module name.
- Correct: Place it under `src/modules/<domain>/`.
- Incorrect: Never place domain logic in `utils/`.

> This rule is mandatory for all current and future modules. Violations are considered governance failures and shall be corrected before codegen or commit.

---

## 8. Inter-PRD Dependencies
All module references shall use relative paths and canonical anchor links (e.g., `[Section 7.1.1: Domain Module Naming](#711-domain-module-naming-and-containment-rules)`). Invalid references shall trigger rejection—no silent failures. Cross-version references require explicit version-lock enforcement. All referenced PRDs shall exist in the repository and be version-locked in the reference (e.g., `[Logging Framework PRD v1.0.4: Interface Section](./logging/module-prd-logging-v1.0.4.md#5-interface--integration)`).

---

## 9. AI Agent Compliance
PRDs shall be executable by autonomous agents without transformation. All interface definitions, exception contracts, and logging constraints are specified in Section 13 to ensure deterministic agentic code generation.

---

## 10. Governance Authority
This protocol overrides all prior formatting practices, inline notes, and AI model heuristics. Precedence follows: governance > core PRD > module PRD. No agent or human may override governance without a formally published revision.

---

## 11. Compliance Enforcement
AI agents shall affirm this governance before making structural edits. Human contributors shall pass protocol validation before submitting or merging changes. All violations trigger PRD invalidation. Affected versions shall not be processed.

---

## 12. User Stories & Use Cases
### 12.1 Actors
- **Finance team member**: Converts a QBD account list into a GnuCash-compatible format.
- **Technical operator**: Validates CSV structure before importing into GnuCash.
- **Developer**: Integrates the tool into an automated migration pipeline.
- **Business stakeholder**: Reviews logs and diffs for data integrity.
- **Contributor**: Extends the architecture to other QBD data types.

### 12.2 Usage Flow
- The core engine parses input files and dispatches data to the configured domain modules for processing.
- The core engine loads and validates mapping configuration files to ensure consistent domain module behavior.
- The core engine logs processing steps and errors in a structured format for downstream auditing and debugging.
- The system supports dynamic module integration via configuration to extend supported data domains.

### 12.3 User Stories
- As a finance team member, I want to convert a QBD account list into a GnuCash-compatible format so I can continue managing finances without proprietary software.
- As a technical operator, I want to validate the CSV structure before importing into GnuCash so I can avoid errors during the migration.
- As a developer, I want the tool to be modular and scriptable so I can integrate it into an automated migration pipeline.
- As a business stakeholder, I want to see clear logs and diffs so I can trust the data integrity of the migrated output.
- As a contributor, I want the architecture to be transparent and well-documented so I can extend it to other QBD data types in the future.

> **Creator's User Story:**  
> As a technical team lead, I'm responsible for migrating our company's financial records from QuickBooks Desktop after Intuit's repeated subscription hikes — most recently from $142 to $163 *per seat*. With multiple users across departments, this translates into thousands of dollars per month. This tool is being developed to eliminate that recurring cost, free us from vendor lock-in, and preserve full access to our historical financial data in a stable, open-source system.

### 12.4 Use Cases
- These user stories and use cases reflect real-world pressures faced by organizations using QBD — primarily the rising cost of licensing and the limitations of proprietary formats. By designing the tool to operate via the command line and to support detailed inspection, mapping flexibility, and configuration diffs, it solves not only the technical challenge of migration but also addresses auditability, extensibility, and maintainability. This allows both end users and system owners to move toward GnuCash with confidence and control.

---

## 13. System Architecture and Workflow

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
  - core-prd-v3.7.0.md
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

> For rules about domain ownership and why `accounts_tree.py` lives inside the `accounts` module, see [Section 7.1.1: Domain Module Naming and Containment Rules](#711-domain-module-naming-and-containment-rules).

### 13.1 Error Handling Strategy and Logging Constraints

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

**Logging Constraints**
- All logging shall be deterministic and flush-safe
- No heuristic assumptions are permitted in logging logic
- Log entries shall include timestamp, level, module, function, and message
- Error conditions shall be logged before termination (normal or exceptional)
- Log context shall support traceability for AI agent inspection
- Log files and directories shall be auto-created if missing
- All modules shall call centralized logging setup prior to logging

*Module PRDs shall specify any additional feedback or logging requirements unique to their domain.*

### 13.2 Interface Contracts and Function Signatures

All module boundaries shall have clearly documented function signatures and exception contracts in the PRD to ensure agentic code generation compatibility.

**Interface Documentation Requirements**
- Function name, argument names and types (using Python typing), return type, exceptions raised, and docstring
- Example format:
  ```python
  def parse_iif_accounts(iif_path: str) -> List[Dict[str, Any]]:
      """Parse an IIF file and return a list of account records."""
      # ...function implementation...
      
  Raises: IIFParseError
  
  # Example usage:
  records = parse_iif_accounts('input/sample.iif')
  ```

**Module PRD Interface Contract Requirements**
- All public functions/classes intended for use by other modules
- Expected input and output types (using Python typing)
- Error/exception handling expectations
- Realistic example call for every public function/class

**Change Management Requirements**
- Any change to a shared interface shall be reflected in the PRD and communicated to all dependent modules
- PRD requires review process for interface changes, including updating all relevant documentation and test cases
- Code reviews shall check for conformance to documented contracts
- Example calls and test cases should be included in PRD to clarify correct usage

**Exception Contract Requirements**
- All custom exceptions shall reference the authoritative error classes defined in [Section 16: Authoritative Error Classes & Error Code Table](#16-authoritative-error-classes--error-code-table)
- Exception types, exit codes, and validation suites shall be explicitly defined
- Each exception shall use its unique error code and corresponding exit code as specified in Section 16
- No ad-hoc or undocumented exception classes are permitted
- All raised exceptions shall include their error code in log output and follow exit code discipline

### 13.3 Interface Definition Standards

All interface definitions shall conform to agentic-compatible formats to ensure deterministic code generation and autonomous implementation:

**Acceptable Interface Formats**
- **TypedDict**: For structured data with defined fields and types
- **JSON Schema**: For configuration files and data validation
- **Python typing**: For function signatures and return types
- **Strict enumerations**: For constrained value sets

**Interface Documentation Requirements**
- All public interfaces shall include complete type annotations
- Function signatures shall specify argument names, types, and return types
- Exception specifications shall reference Section 16 error codes
- Example usage shall be provided for all public interfaces

**Agentic Compatibility Standards**
- Interface specifications shall be executable by autonomous agents without transformation
- All type information shall be explicitly declared, not inferred
- Interface contracts shall be deterministic and unambiguous
- No heuristic assumptions are permitted in interface definitions

### 13.4 Module Entry Point Requirements

All domain modules shall implement standardized entry points to ensure consistent agentic code generation and horizontal scaling compatibility:

**Entry Point Naming Convention**
- Primary entry point: `run_<domain>_pipeline(payload: Dict[str, Any]) -> bool`
- Domain name shall match the authorized domain index from Governance Document
- Function name shall be lowercase with underscores

**Entry Point Signature Requirements**
- **Payload Parameter**: Shall conform to `core_dispatch_payload_v1` schema (Section 13.5.4)
- **Return Type**: Boolean success indication (True=success, False=failure)
- **Exception Handling**: Shall implement all applicable error codes from Section 16

**Documentation Requirements**
- Complete function signature in Module PRD Section 6.2
- Exception handling specification with error codes
- Realistic example call with payload structure

**Implementation Standards**
- Entry point shall handle all domain-specific processing autonomously
- No external dependencies beyond core utilities and domain configuration
- Logging shall comply with centralized logging requirements (Section 13.1)

**Example Entry Point Implementation**
```python
def run_accounts_pipeline(payload: Dict[str, Any]) -> bool:
    """Process accounts section data through mapping, validation, and export.
    
    Args:
        payload: Dispatch payload conforming to core_dispatch_payload_v1
        
    Returns:
        bool: True if processing succeeded, False if failed
        
    Raises:
        ValidationError: If payload schema validation fails (E0102)
        DomainValidationError: If domain-specific validation fails (E1190)
    """
    # Implementation details...
    return True

# Example usage:
success = run_accounts_pipeline({
    'section': 'ACCNT',
    'records': [...],
    'output_dir': 'output/',
    'extra_config': {}
})
```

### 13.5 Core Interface Contracts

This section documents the public interface contracts for core orchestration functions that modules interact with. All signatures, docstrings, exception handling, and example usages follow the standards established in Section 13.2. These contracts ensure reliable integration, governance compliance, and agentic compatibility across the codebase.

#### 13.5.1 Core Orchestration Functions

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
def register_module(registry: Dict[str, Any], key: str, module: Any) -> None:
    """Register a domain module with the core registry for dispatching input sections.
    Args:
        registry (Dict[str, Any]): The central registry mapping section keys to modules.
        key (str): The unique section key (e.g., 'ACCNT').
        module (Any): The module object implementing the required interface.
    Raises:
        RegistryKeyConflictError: If the key is already registered.
    """
    # ...function implementation...

# Example usage:
register_module(registry, 'ACCNT', accounts_module)
```

##### `dispatch_to_module`
```python
def dispatch_to_module(registry: Dict[str, Any], section_key: str, records: List[Dict[str, Any]]) -> bool:
    """Dispatch parsed records to the appropriate domain module for processing.
    Args:
        registry (Dict[str, Any]): The central registry mapping section keys to modules.
        section_key (str): The section key identifying the domain (e.g., 'ACCNT').
        records (List[Dict[str, Any]]): Parsed records for the section.
    Returns:
        bool: True if processing succeeded, False if failed.
    Raises:
        KeyError: If the section_key is not registered.
        Exception: For module-specific processing errors.
    """
    # ...function implementation...

# Example usage:
success = dispatch_to_module(registry, 'ACCNT', account_records)
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

#### 13.5.2 Exception Classes

All custom exceptions raised by core functions and modules shall reference the authoritative error classes and error codes defined in [Section 16: Authoritative Error Classes & Error Code Table](#16-authoritative-error-classes--error-code-table). Each exception shall use its unique error code (e.g., `E0001`, `E0201`) and corresponding exit code as specified in the table.

The `utils/error_handler.py` module serves as the central registry for error management, ensuring all error classes and codes are version-locked, logically consistent, and compliant with this PRD. Any addition or modification of error classes or codes shall be reflected both in Section 16 and in `utils/error_handler.py`.

**Example usage:**

```python
from utils.error_handler import MappingLoadError

try:
    mapping = load_mapping('output/missing.json')
except MappingLoadError as e:
    # E0201: Mapping file missing, unreadable, or invalid schema (Exit Code: 2)
    log_and_exit(f"[E0201] {str(e)}", code=2)
```

- All raised exceptions shall include their error code in log output and follow the exit code discipline.
- All modules and the core shall use only the error classes and codes defined in Section 16.
- No ad-hoc or undocumented error classes are permitted.

### 13.6 Input File Discovery and Processing Model

The tool supports dynamic discovery and structured dispatch of user-provided `.IIF` files placed in the `input/` directory. This section defines the complete file ingestion lifecycle.

#### 13.6.1 File Discovery
- All `.IIF` files (case-insensitive) located in the `input/` directory will be discovered.
- Filenames are not interpreted for routing or validation. Discovery is content-based.
- Subdirectories inside `input/` are ignored.

#### 13.6.2 Section Header Parsing
- Each `.IIF` file is scanned line-by-line to detect top-level QuickBooks headers (e.g., `ACCNT`, `TRNS`, `CUST`, etc.).
- Header lines may occur in any order and may be interleaved with data or other headers.
- A single `.IIF` file may contain multiple section types. All are independently extracted.
- Unsupported or unrecognized headers will be logged and ignored with a warning.

#### 13.6.3 Module Dispatch
- For each detected section, a normalized dispatch event is constructed and routed to the appropriate processing module (e.g., `accounts`, `transactions`, `customers`, etc.).
- Each section is processed independently, even if originating from the same `.IIF` file.
- Processing modules are responsible for validation, mapping, transformation, and output generation for their assigned sections.

#### 13.6.4 Dispatch Payload Schema

All section data is passed between components using a canonical dispatch schema:

**`core_dispatch_payload_v1`**

| Key              | Type     | Description                                         |
|------------------|----------|-----------------------------------------------------|
| `section`        | `str`    | QuickBooks header name (e.g., `ACCNT`)            |
| `records`        | `list`   | Parsed records under the section header            |
| `output_dir`     | `str`    | Destination directory for processed output         |
| `extra_config`   | `dict`   | Optional: Additional runtime parameters (may be empty) |

All module contracts shall conform to this schema. Future schema versions shall be versioned separately and gated by config or CLI flags.

### 13.7 Governance Note
This section is **immutable** under PRD Governance v2.5.0. All changes shall go through formal versioning review. Referencing module PRDs shall treat this schema as canonical.

---

## 14. Module Ownership and Directory Boundaries

Each domain module owns its **full functional implementation**, including all subcomponents necessary for its logic, construction, and validation.

### 14.1 Domain Module Naming and Containment Rules

To ensure maintainability, prevent cross-domain collisions, and support governance enforcement:

**Module Placement Matrix**

| Module Type | Belongs In | Does NOT Belong In | Examples |
|-------------|------------|-------------------|----------|
| **Domain-Specific Logic** | `src/modules/<domain>/` | `src/utils/` | ✅ `accounts_validation.py` → `src/modules/accounts/` |
| **Domain-Agnostic Utilities** | `src/utils/` | `src/modules/<domain>/` | ✅ `iif_parser.py` → `src/utils/` |
| **Cross-Domain Shared Code** | `src/utils/` | `src/modules/<domain>/` | ✅ `error_handler.py` → `src/utils/` |

**Enforcement Rules for Logic Placement Violations**
- All domain-specific modules shall use domain prefix in filename (e.g., `accounts_`, `customers_`)
- Violations of module placement shall trigger governance failure and require correction before codegen
- Code reviews shall verify module placement compliance using this matrix
- Any authorized deviations shall be explicitly documented with rationale in code comments

**Confirmed Roadmap Module Preparation**
The following domains are confirmed for horizontal scaling and shall follow these placement rules:

| Domain | Directory | Module Prefix | Entry Point |
|--------|-----------|---------------|-------------|
| **sales_tax** | `src/modules/sales_tax/` | `sales_tax_` | `run_sales_tax_pipeline()` |
| **items** | `src/modules/items/` | `items_` | `run_items_pipeline()` |
| **customers** | `src/modules/customers/` | `customers_` | `run_customers_pipeline()` |
| **vendors** | `src/modules/vendors/` | `vendors_` | `run_vendors_pipeline()` |

**Logic Placement Violation Examples**
- ❌ `src/utils/validation.py` containing accounts-specific logic
- ❌ `src/modules/accounts/parser.py` containing generic IIF parsing
- ❌ `src/modules/customers/error_handler.py` containing cross-domain error classes

#### 14.1.1 Examples (Correct vs Incorrect)

  Correct: `src/modules/accounts/accounts_validation.py`  
  Incorrect: `src/utils/validation.py` *(violates naming and containment rules)*

#### 14.1.2 Developer Checklist

Before creating or moving any file:
- Correct: Prefix domain logic with its module name.
- Correct: Place it under `src/modules/<domain>/`.
- Correct: Never place domain logic in `utils/`.

> This rule is mandatory for all current and future modules. Violations are considered governance failures and shall be corrected before codegen or commit.

---

## 15. Non-Functional Requirements, Testing, Onboarding, and Extensibility

### 15.1 Non-Functional Requirements
- **Performance:** The tool shall process typical QBD exports (up to 10,000 records per section) in under 60 seconds on commodity hardware.
- **Reliability:** All critical errors shall be logged and surfaced to the user. The tool shall fail fast on unrecoverable errors and provide actionable diagnostics.
- **Portability:** The tool shall run on Windows, macOS, and Linux with no code changes, requiring only Python 3.8+ and standard libraries.
- **Maintainability:** All modules and core logic shall be documented and follow the interface contract and directory rules.

### 15.2 Testing and Validation
- **Unit Tests:** Each module shall provide unit tests for all public functions, covering normal and edge cases.
- **Integration Tests:** The core pipeline shall be tested end-to-end using sample `.IIF` files and mapping configurations.
- **Validation:** Output files shall be validated against GnuCash import requirements. Validation errors shall be logged and surfaced.
- **Test Artifacts:** Sample input and output files shall be maintained in a dedicated test directory.

### 15.3 Onboarding and Contributor Guidance
- **Getting Started:** New contributors should review the core PRD, module PRDs, and governance model before making changes.
- **Setup:** Clone the repository, install Python 3.8+, and run `python src/main.py` to execute the tool.
- **Contribution:** All changes shall be accompanied by PRD updates and tests. Code reviews shall check for governance compliance.

### 15.4 Extensibility
- **Adding Modules:** New domains can be added by creating a new module PRD and implementing the required interface contract. The core registry shall be updated to recognize the new section key.
- **Configuration:** Mapping and validation logic shall be externalized to configuration files where possible to support future changes without code edits.
- **Agentic Compatibility:** All logic shall be modular and declarative to support future AI-driven automation and code generation.

---

## 16. Authoritative Error Classes & Error Code Table

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