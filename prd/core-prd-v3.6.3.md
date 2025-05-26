# Core PRD: QuickBooks Desktop to GnuCash Conversion Tool

**Document Version:** v3.6.3  
**Module Identifier:** core-prd-v3.6.3.md  
**State:** Finalized for Governance Compliance
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-05-25  
**Governance Model:** prd-governance-model-v2.3.10.md  

---

## 1. Scope
This project delivers a modular, command-line conversion tool for migrating financial data from QuickBooks Desktop (QBD) into GnuCash using structured import files. The core framework applies a consistent, extensible processing pipeline—centralized input ingestion and parsing, followed by dispatching well-defined payloads to domain modules for mapping and output generation—which is reused across all modules. Each domain module (e.g., Accounts, Vendors, Transactions, and others) is responsible for converting its respective QBD data as received from the dispatcher into GnuCash-compatible formats, as defined in its own PRD. The core PRD defines the shared architecture, orchestration, and extension points for all modules.

This project is CLI-only; no graphical user interface or CLI arguments will be developed or supported.

### 1.1 Target Audience
This tool is intended for technical users — accountants, bookkeepers, or developers — performing structured financial data migration from QBD to GnuCash. Familiarity with the principles of double-entry accounting and GnuCash's account-type model is strongly recommended.

---

## 2. Structural Rules
All section numbering and headers must be strictly sequential and hierarchical, following the format `## <n>. <Title>`, with subsections as `### <n>.<m> <Title>`. No numbering jumps, omissions, or renumbering inconsistencies are permitted. All major sections must be delimited by a horizontal rule (`---`). Section headers are immutable; no renaming or paraphrasing is allowed. Documents failing to conform to these requirements must be rejected or corrected before further processing.

---

## 3. Background Context
QuickBooks Desktop is a proprietary platform, and many users are migrating to open-source accounting systems for reasons including cost, longevity, and transparency. However, the lack of compatible conversion tooling presents a serious barrier. This project exists to fill that gap, enabling clean migration of core data without data loss and with minimal manual recreation.

---

## 4. Formatting Protocols
Only Markdown is permitted. No embedded HTML, LaTeX, or rich text formatting is allowed. All code blocks, lists, and indentation must remain in canonical syntax without modification. No summaries, examples, or commentary may be introduced unless explicitly required by protocol.

---

## 5. Versioning Enforcement
### 5.1 Revision History

| Version | Date       | Author | Summary                                                
|---------|------------|--------|--------------------------------------------------------
| 3.6.3   | 2025-05-25 | PJ     | Finalized authoritative revision history, ensured full compliance, and validated content integrity from v3.6.0
| 3.6.2   | 2025-05-25 | PJ     | Fully integrated, restored missing content, finalized for full governance compliance 
| 3.6.1   | 2025-05-25 | PJ     | Reorganized for full compliance with governance v2.3.10 
| 3.6.0   | 2025-05-24 | PJ     | Corrected domain module naming                         
| 3.5.1   | 2025-05-23 | PJ     | Remediated governance audit violations (compatibility matrix, history format, duplicate sections, user story subsections) 
| 3.5.0   | 2025-05-22 | PJ     | Finalized full extraction and compliance with separation of concerns and compartmentalization of domain-specific content 
| 3.4.1   | 2025-05-21 | PJ     | Split module logic into dedicated files and updated user story mappings 
| 3.4.0   | 2025-05-20 | PJ     | Added explicit JSON Schema and Python typing examples for all major data structures. Updated interface contracts and example calls for public functions/classes 
| 3.3.1   | 2025-05-19 | PJ     | Standardized terminology for mapping diff file, output file path, and accounts.csv. Added Terminology section for clarity and future consistency 
| 3.1.0   | 2025-05-18 | PJ     | Mandated explicit function signatures and interface contracts for all module boundaries |
| 3.0.1   | 2025-05-17 | PJ     | Minor clarifications and error handling improvements   
| 3.0.0   | 2025-05-16 | PJ     | Core PRD established as root of a modular PRD system. All module-specific logic to be extracted into versioned standalone files in `./prd/{module}/` 
| 2.7.3   | 2025-05-15 | PJ     | Final monolithic PRD before modularization  

---

## 6. Update Discipline
Edits must strictly modify the targeted logic. Collateral adjustments are prohibited. Insertions must occur at precisely the correct semantic location. Renumbering must occur coherently across all affected sections in a single correction pass.

---

## 7. Modular PRD Definition
### 7.1 Module Ownership and Directory Boundaries
Each domain module owns its **full functional implementation**, including all subcomponents necessary for its logic, construction, and validation.

#### 7.1.1 Domain Module Naming and Containment Rules
To ensure maintainability, prevent cross-domain collisions, and support governance enforcement:
- All domain-specific modules must:
  - Use a domain prefix in their filename (e.g., `accounts_`, `customers_`).
  - Reside within their respective domain directory (e.g., `src/modules/accounts/`).
  - Avoid placement in `src/utils/` or any unrelated folder.
- Only domain-agnostic modules may be placed in `src/utils/` (e.g., `iif_parser.py`, `error_handler.py`, `logging.py`).

##### 7.1.1.1 Examples (Correct vs Incorrect)
✅ `src/modules/accounts/accounts_validation.py`  
❌ `src/utils/validation.py` *(violates naming and containment rules)*

##### 7.1.1.2 Developer Checklist
Before creating or moving any file:
- ✅ Prefix domain logic with its module name.
- ✅ Place it under `src/modules/<domain>/`.
- ❌ Never place domain logic in `utils/`.

> This rule is mandatory for all current and future modules. Violations are considered governance failures and must be corrected before codegen or commit.

---

## 8. Inter-PRD Dependencies
All module references must use relative paths and canonical anchor links (e.g., `[Section 7.1.1](#711-domain-module-naming-and-containment-rules)`). Invalid references must trigger rejection—no silent failures. Cross-version references require explicit version-lock enforcement. All referenced PRDs must exist in the repository and be version-locked in the reference (e.g., `[Logging Framework PRD v1.0.4](./logging/module-prd-logging-v1.0.4.md)`).

---

## 9. AI Agent Compliance
PRDs must be executable by autonomous agents without transformation. Acceptable interface formats: TypedDict, JSON Schema, strict enumerations. Exception types, exit codes, and validation suites must be explicitly defined. Logging must be deterministic and flush-safe. No heuristic assumptions are allowed.

---

## 10. Governance Authority
This protocol overrides all prior formatting practices, inline notes, and AI model heuristics. Precedence follows: governance > core PRD > module PRD. No agent or human may override governance without a formally published revision.

---

## 11. Compliance Enforcement
AI agents must affirm this governance before making structural edits. Human contributors must pass protocol validation before submitting or merging changes. All violations trigger PRD invalidation. Affected versions must not be processed.

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
  - core-prd-v3.6.0.md
  - prd-module-template-v3.6.2.md
  - README-core.md
  - accounts/
    - module-prd-accounts-v1.1.1.md
    - module-prd-accounts_mapping-v1.0.6.md
    - module-prd-accounts_validation-v1.0.1.md
    - README-accounts.md
    - README-accounts_mapping.md
    - README-accounts_validation.md
  - logging/
    - module-prd-logging-v1.0.4.md
    - README-logging.md
- src/
  - main.py
  - modules/
    - accounts/
      - accounts.py
      - accounts_mapping.py
      - accounts_mapping_baseline.json
      - accounts_tree.py
      - accounts_validation.py
  - utils/
    - error_handler.py
    - iif_parser.py
    - logging.py

> For rules about domain ownership and why `accounts_tree.py` lives inside the `accounts` module, see [Section 7.1.1](#711-domain-module-naming-and-containment-rules).

### 13.1 Error Handling Strategy

**Error Classifications**

| Stage                 | Example Errors                                             |
|-----------------------|------------------------------------------------------------|
| **Parsing**           | Missing header in input file, tab mismatch, invalid UTF-8  |
| **Mapping**           | Unknown domain type, no destination hierarchy defined      |
| **Tree Construction** | Missing parent, failed 1-child promotion, circular paths   |
| **Output**            | File write permission denied, output file malformed        |
| **Registry**          | Unregistered key, key conflict, fallback loop              |

*Note: Each module PRD must define any additional error types and examples relevant to its domain. The above are illustrative and may be extended by modules.*

**Metadata Required**
- **File or Key**: e.g., `input file`, `domain key`
- **Line/Record Ref**: e.g., `Row 24`, `Record Name: ...`
- **Processing Step**: Parsing → Mapping → Tree → Output
- **Expected vs Actual**: Clear diff
- **Registry Context**: If applicable
- **Structured JSON log**: Optional for agent inspection

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

*Module PRDs must specify any additional feedback or logging requirements unique to their domain.*

### 13.2 Interface Contracts and Function Signatures

- All module boundaries must have clearly documented function signatures in the PRD.
  - This includes function name, argument names and types (using Python typing), return type, exceptions raised, and a 1-2 line docstring/description.
  - Example format:
    ```python
    def parse_iif_accounts(iif_path: str) -> List[Dict[str, Any]]:
        """Parse an IIF file and return a list of account records."""
        # ...function implementation...
        
    Raises: IIFParseError
    
    # Example usage:
    records = parse_iif_accounts('input/sample.iif')
    ```
- For each module, the PRD must include an "Interface Contract" section that specifies:
  - All public functions/classes intended for use by other modules.
  - Expected input and output types (using Python typing).
  - Error/exception handling expectations.
  - A realistic example call for every public function/class, matching the documented signature and reflecting a real use case.
- Any change to a shared interface must be reflected in the PRD and communicated to all dependent modules.
- The PRD requires a review process for interface changes, including updating all relevant documentation and test cases.
- Code reviews must check for conformance to the documented contracts.
- Example calls and test cases should be included in the PRD to clarify correct usage.

### 13.3 Core Interface Contracts

This section documents the public interface contracts for core orchestration functions that modules interact with. All signatures, docstrings, exception handling, and example usages follow the standards established in Section 13.2. These contracts ensure reliable integration, governance compliance, and agentic compatibility across the codebase.

#### 13.3.1 Core Orchestration Functions

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
        key (str): The unique section key (e.g., '!ACCNT').
        module (Any): The module object implementing the required interface.
    Raises:
        RegistryKeyConflictError: If the key is already registered.
    """
    # ...function implementation...

# Example usage:
register_module(registry, '!ACCNT', accounts_module)
```

##### `dispatch_to_module`
```python
def dispatch_to_module(registry: Dict[str, Any], section_key: str, records: List[Dict[str, Any]]) -> Any:
    """Dispatch parsed records to the appropriate domain module for processing.
    Args:
        registry (Dict[str, Any]): The central registry mapping section keys to modules.
        section_key (str): The section key identifying the domain (e.g., '!ACCNT').
        records (List[Dict[str, Any]]): Parsed records for the section.
    Returns:
        Any: Module-specific result (e.g., processed data, output file path).
    Raises:
        KeyError: If the section_key is not registered.
        Exception: For module-specific processing errors.
    """
    # ...function implementation...

# Example usage:
result = dispatch_to_module(registry, '!ACCNT', account_records)
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

#### 13.3.2 Exception Classes

All custom exceptions raised by core functions are defined in `utils/error_handler.py` and must be referenced by all modules and core logic for consistency.

```python
class RegistryKeyConflictError(Exception):
    """Raised when two modules attempt to register the same section key."""
    pass

class ValidationError(Exception):
    """Raised when validation of input or output data fails."""
    pass

# Example usage:
try:
    register_module(registry, '!ACCNT', accounts_module)
except RegistryKeyConflictError as e:
    log_and_exit(str(e), code=1)
```

### 13.4 Input File Discovery and Processing Model

The tool supports dynamic discovery and structured dispatch of user-provided `.IIF` files placed in the `input/` directory. This section defines the complete file ingestion lifecycle.

#### 13.4.1 File Discovery
- All `.IIF` files (case-insensitive) located in the `input/` directory will be discovered.
- Filenames are not interpreted for routing or validation. Discovery is content-based.
- Subdirectories inside `input/` are ignored.

#### 13.4.2 Section Header Parsing
- Each `.IIF` file is scanned line-by-line to detect top-level QuickBooks headers (e.g., `!ACCNT`, `!TRNS`, `!CUST`, etc.).
- Header lines may occur in any order and may be interleaved with data or other headers.
- A single `.IIF` file may contain multiple section types. All are independently extracted.
- Unsupported or unrecognized headers will be logged and ignored with a warning.

#### 13.4.3 Module Dispatch
- For each detected section, a normalized dispatch event is constructed and routed to the appropriate processing module (e.g., `accounts`, `transactions`, `customers`, etc.).
- Each section is processed independently, even if originating from the same `.IIF` file.
- Processing modules are responsible for validation, mapping, transformation, and output generation for their assigned sections.

#### 13.4.4 Dispatch Payload Schema

All section data is passed between components using a canonical dispatch schema:

**`core_dispatch_payload_v1`**

| Key              | Type     | Description                                         |
|------------------|----------|-----------------------------------------------------|
| `section`        | `str`    | QuickBooks header name (e.g., `!ACCNT`)            |
| `records`        | `list`   | Parsed records under the section header            |
| `input_path`     | `str`    | Absolute path to the source `.IIF` file            |
| `output_dir`     | `str`    | Destination directory for processed output         |
| `log_path`       | `str`    | File path for logging messages related to this dispatch |
| `mapping_config` | `dict`   | Resolved mapping configuration for this section    |
| `extra_config`   | `dict`   | Optional: Additional runtime parameters (may be empty) |

All module contracts must conform to this schema. Future schema versions must be versioned separately and gated by config or CLI flags.

### Governance Note
This section is **immutable** under PRD Governance v2.3.10. All changes must go through formal versioning review. Referencing module PRDs must treat this schema as canonical.

---

## 14. Module Ownership and Directory Boundaries

Each domain module owns its **full functional implementation**, including all subcomponents necessary for its logic, construction, and validation.

### 14.1 Domain Module Naming and Containment Rules

To ensure maintainability, prevent cross-domain collisions, and support governance enforcement:

- All domain-specific modules must:
  - Use a domain prefix in their filename (e.g., `accounts_`, `customers_`).
  - Avoid placement in `src/utils/` or any unrelated folder.

- Only domain-agnostic modules may be placed in `src/utils/` (e.g., `iif_parser.py`, `error_handler.py`, `logging.py`)

#### 14.1.1 Examples (Correct vs Incorrect)

✅ `src/modules/accounts/accounts_validation.py`  
❌ `src/utils/validation.py` *(violates naming and containment rules)*

#### 14.1.2 Developer Checklist

Before creating or moving any file:
- ✅ Prefix domain logic with its module name.
- ✅ Place it under `src/modules/<domain>/`.
- ❌ Never place domain logic in `utils/`.

> This rule is mandatory for all current and future modules. Violations are considered governance failures and must be corrected before codegen or commit.

---

## 15. Non-Functional Requirements, Testing, Onboarding, and Extensibility

### 15.1 Non-Functional Requirements
- **Performance:** The tool must process typical QBD exports (up to 10,000 records per section) in under 60 seconds on commodity hardware.
- **Reliability:** All critical errors must be logged and surfaced to the user. The tool must fail fast on unrecoverable errors and provide actionable diagnostics.
- **Portability:** The tool must run on Windows, macOS, and Linux with no code changes, requiring only Python 3.8+ and standard libraries.
- **Maintainability:** All modules and core logic must be documented and follow the interface contract and directory rules.

### 15.2 Testing and Validation
- **Unit Tests:** Each module must provide unit tests for all public functions, covering normal and edge cases.
- **Integration Tests:** The core pipeline must be tested end-to-end using sample `.IIF` files and mapping configurations.
- **Validation:** Output files must be validated against GnuCash import requirements. Validation errors must be logged and surfaced.
- **Test Artifacts:** Sample input and output files must be maintained in a dedicated test directory.

### 15.3 Onboarding and Contributor Guidance
- **Getting Started:** New contributors should review the core PRD, module PRDs, and governance model before making changes.
- **Setup:** Clone the repository, install Python 3.8+, and run `python src/main.py` to execute the tool.
- **Contribution:** All changes must be accompanied by PRD updates and tests. Code reviews must check for governance compliance.

### 15.4 Extensibility
- **Adding Modules:** New domains can be added by creating a new module PRD and implementing the required interface contract. The core registry must be updated to recognize the new section key.
- **Configuration:** Mapping and validation logic must be externalized to configuration files where possible to support future changes without code edits.
- **Agentic Compatibility:** All logic must be modular and declarative to support future AI-driven automation and code generation.

---

<!-- End of core-prd-v3.6.3.md -->
