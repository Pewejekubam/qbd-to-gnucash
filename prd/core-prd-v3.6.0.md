<!-- filepath: c:\git-root\qbd-to-gnucash\prd\core-prd-v3.5.0.md -->
# Core PRD: QuickBooks Desktop to GnuCash Conversion Tool

**Document Version:** 3.6.0
**State:** Under Review / Workflow Discrepancy
**Author:** Pewe Jekubam

---

## 1.0 Compatibility Matrix

| Module Name         | PRD Version | Compatible With Core PRD |
|---------------------|-------------|--------------------------|
| Chart of Accounts   | v1.0.9      | v3.6.0                   |
| Sales Tax Code List | (TBD)       |                          |
| Item List           | (TBD)       |                          |
| Customer List       | (TBD)       |                          |
| Vendor List         | (TBD)       |                          |

---

## 2.0 Revision History
- v3.6.0 – Corrected domain module naming
- v3.5.1 – Remediated governance audit violations (compatibility matrix, history format, duplicate section, user story subsections)
- v3.5.0 – Finalized full extraction and compliance with separation of concerns and compartmentalization of domain-specific content.
- v3.4.1 – Split module logic into dedicated files and updated user story mappings.
- v3.4.0 – Added explicit JSON Schema and Python typing examples for all major data structures. Updated interface contracts and example calls for public functions/classes.
- v3.3.1 – Standardized terminology for mapping diff file, output file path, and accounts.csv. Added Terminology section for clarity and future consistency.
- v3.1.0 – Mandated explicit function signatures and interface contracts for all module boundaries.
- v3.0.1 – Minor clarifications and error handling improvements.  
- v3.0.0 – Core PRD established as the root of a modular PRD system. All module-specific logic to be extracted into versioned standalone files in `./prd/{module}/`.  
- v2.7.3 – Final monolithic PRD before modularization.

---

## 3. Introduction

### 3.1 Project Overview

This project delivers a modular, command-line conversion tool for migrating financial data from QuickBooks Desktop (QBD) into GnuCash using structured import files. The core framework applies a consistent, extensible processing pipeline—centralized input ingestion and parsing, followed by dispatching well-defined payloads to domain modules for mapping and output generation—which is reused across all modules. Each domain module (e.g., Accounts, Vendors, Transactions, and others) is responsible for converting its respective QBD data as received from the dispatcher into GnuCash-compatible formats, as defined in its own PRD. The core PRD defines the shared architecture, orchestration, and extension points for all modules.

This project is CLI-only; no graphical user interface or CLI arguments will be developed or supported.

### 3.2 Scope

**In-Scope**  
- Core engine functionality for parsing input files, dispatching section payloads, mapping, and generating output files compatible with GnuCash import formats.  
- Modular design to enable extension for additional financial data domains.  
- Command-line interface for invoking conversion pipelines and managing configuration.

**Out-of-Scope**  
- Domain-specific business rules, data formats, and export types, which are managed in respective domain PRDs.  
- User interface (GUI), workflow orchestration beyond the core engine, and user interaction layers.  
- Integration with external systems or live data sources.

Domain modules (e.g., Accounts, Vendors, Transactions) maintain their own scoped responsibilities and define detailed data handling and format processing within their respective PRDs.

### 3.3 Target Audience

This tool is intended for technical users — accountants, bookkeepers, or developers — performing structured financial data migration from QBD to GnuCash. Familiarity with the principles of double-entry accounting and GnuCash's account-type model is strongly recommended.

### 3.4 Background Context

QuickBooks Desktop is a proprietary platform, and many users are migrating to open-source accounting systems for reasons including cost, longevity, and transparency. However, the lack of compatible conversion tooling presents a serious barrier. This project exists to fill that gap, enabling clean migration of core data without data loss or manual recreation.

---

## 4. Objectives & Goals

### 4.1 Primary Objective
Enable seamless and accurate conversion of QuickBooks Desktop (QBD) financial data—beginning with the Chart of Accounts—into a GnuCash-compatible format, using a modular, configuration-driven command-line tool suitable for agentic AI implementation.

### 4.2 Success Criteria
- ✅ **Correctness**: Inputs sourced directly from QuickBooks Desktop exports are parsed and registered by the core engine, which dispatches them to the appropriate domain modules. Each module is responsible for generating importable output files that conform to GnuCash’s requirements.
- ✅ **Validation**: Import processes validate output data against GnuCash’s schema and structural rules, ensuring no errors or mismatches occur during import.
- ✅ **Resilience**: The system tolerates minor input inconsistencies (e.g., naming anomalies, empty fields) and logs them as structured issues for review.
- ✅ **Iteration Support**: Supports configurable workflows including generation of both specific and diff JSON mapping files, enabling iterative correction and reprocessing.
- ✅ **Traceability**: All transformation steps (parsing, mapping, output) are logged with structured detail to support debugging and auditing.
- ✅ **Agentic Compatibility**: Logic is modular and declarative to facilitate AI-based code generation and automation with minimal human intervention.

### 4.3 Strategic Considerations
The ability to migrate financial records from QBD into GnuCash is essential for users transitioning to open-source or non-proprietary systems. GnuCash relies on strict double-entry accounting principles and requires precise data structuring during import. A conversion tool that meets these standards will allow users to retain control of their data while escaping licensing or platform lock-in. A clean, modular tool also provides the foundation for future modules (e.g., Transactions, Vendors, Customers), each using the same logic framework to extend the system.

### 4.4 Module Ownership and Directory Boundaries

Each domain module owns its **full functional implementation**, including all subcomponents necessary for its logic, construction, and validation

### 4.5 Domain Module Naming and Containment Rules

To ensure maintainability, prevent cross-domain collisions, and support governance enforcement:

- All domain-specific modules must:
  - Use a domain prefix in their filename (e.g., `accounts_`, `customers_`).
  - Reside within their respective domain directory (e.g., `src/modules/accounts/`).
  - Avoid placement in `src/utils/` or any unrelated folder.

- Only domain-agnostic modules may be placed in `src/utils/` (e.g., `iif_parser.py`, `error_handler.py`, `logging.py`).

#### 4.5.1 Examples (Correct vs Incorrect)

✅ `src/modules/accounts/accounts_validation.py`  
❌ `src/utils/validation.py` *(violates naming and containment rules)*

#### 4.5.2 Developer Checklist

Before creating or moving any file:
- ✅ Prefix domain logic with its module name.
- ✅ Place it under `src/modules/<domain>/`.
- ❌ Never place domain logic in `utils/`.

> This rule is mandatory for all current and future modules. Violations are considered governance failures and must be corrected before codegen or commit.

---

## 5. User Stories & Use Cases

### 5.1 Actors
- **Finance team member**: Converts a QBD account list into a GnuCash-compatible format.
- **Technical operator**: Validates CSV structure before importing into GnuCash.
- **Developer**: Integrates the tool into an automated migration pipeline.
- **Business stakeholder**: Reviews logs and diffs for data integrity.
- **Contributor**: Extends the architecture to other QBD data types.

### 5.2 Usage Flow
- The core engine parses input files and dispatches data to the configured domain modules for processing.
- The core engine loads and validates mapping configuration files to ensure consistent domain module behavior.
- The core engine logs processing steps and errors in a structured format for downstream auditing and debugging.
- The system supports dynamic module integration via configuration to extend supported data domains.

### 5.3 User Stories
- As a finance team member, I want to convert a QBD account list into a GnuCash-compatible format so I can continue managing finances without proprietary software.
- As a technical operator, I want to validate the CSV structure before importing into GnuCash so I can avoid errors during the migration.
- As a developer, I want the tool to be modular and scriptable so I can integrate it into an automated migration pipeline.
- As a business stakeholder, I want to see clear logs and diffs so I can trust the data integrity of the migrated output.
- As a contributor, I want the architecture to be transparent and well-documented so I can extend it to other QBD data types in the future.

> **Creator's User Story:**  
> As a technical team lead, I'm responsible for migrating our company's financial records from QuickBooks Desktop after Intuit's repeated subscription hikes — most recently from $142 to $163 *per seat*. With multiple users across departments, this translates into thousands of dollars per month. This tool is being developed to eliminate that recurring cost, free us from vendor lock-in, and preserve full access to our historical financial data in a stable, open-source system.

### 5.4 Use Cases
- These user stories and use cases reflect real-world pressures faced by organizations using QBD — primarily the rising cost of licensing and the limitations of proprietary formats. By designing the tool to operate via the command line and to support detailed inspection, mapping flexibility, and configuration diffs, it solves not only the technical challenge of migration but also addresses auditability, extensibility, and maintainability. This allows both end users and system owners to move toward GnuCash with confidence and control.

---

## 6. System Architecture and Workflow


.                                  # Project root
├── input/                         # User-provided IIF files
│   ├── sample-qbd-accounts.IIF
│   ├── sample-qbd-customers.IIF
│   ├── sample-qbd-items.IIF
│   ├── sample-qbd-payment-terms.IIF
│   └── sample-qbd-sales-tax-codes.IIF
├── output/                        # Generated output files and logs
│   └── qbd-to-gnucash.log
├── prd/                           # Product Requirements Documents (PRDs)
│   ├── core-prd-v3.6.0.md         # Core PRD
│   ├── prd-module-template-v3.5.1.md # PRD template
│   ├── README-core.md             # Core PRD README
│   ├── accounts/                  # Accounts module PRDs
│   │   ├── module-prd-accounts-v1.1.1.md
│   │   ├── module-prd-accounts_mapping-v1.0.6.md
│   │   ├── module-prd-accounts_validation-v1.0.1.md
│   │   ├── README-accounts.md
│   │   ├── README-accounts_mapping.md
│   │   └── README-accounts_validation.md
│   └── logging/
│       ├── module-prd-logging-v1.0.4.md
│       └── README-logging.md
├── src/                           # Source code for conversion tool
│   ├── main.py                    # Entrypoint script
│   ├── modules/
│   │   └── accounts/
│   │       ├── accounts.py                # Main logic for account conversion
│   │       ├── accounts_mapping.py        # Mapping logic loader/merger
│   │       ├── accounts_mapping_baseline.json # Mapping config
│   │       ├── accounts_tree.py           # Account tree builder
│   │       └── accounts_validation.py     # Validation logic
│   └── utils/
│       ├── error_handler.py       # Standardized error classes
│       ├── iif_parser.py          # IIF format parser
│       └── logging.py             # Logging setup and utilities
> For rules about domain ownership and why `accounts_tree.py` lives inside the `accounts` module, see Section 4.4.

### 6.2 Error Handling Strategy

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

### 6.3 Interface Contracts and Function Signatures

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

### 6.4 Core Interface Contracts

This section documents the public interface contracts for core orchestration functions that modules interact with. All signatures, docstrings, exception handling, and example usages follow the standards established in Section 6.3. These contracts ensure reliable integration, governance compliance, and agentic compatibility across the codebase.

#### 6.4.1 Core Orchestration Functions

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

#### 6.4.2 Exception Classes

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

### 6.5 Input File Discovery and Processing Model

The tool supports dynamic discovery and structured dispatch of user-provided `.IIF` files placed in the `input/` directory. This section defines the complete file ingestion lifecycle.

#### 6.5.1 File Discovery

- All `.IIF` files (case-insensitive) located in the `input/` directory will be discovered.
- Filenames are not interpreted for routing or validation. Discovery is content-based.
- Subdirectories inside `input/` are ignored.

#### 6.5.2 Section Header Parsing

- Each `.IIF` file is scanned line-by-line to detect top-level QuickBooks headers (e.g., `!ACCNT`, `!TRNS`, `!CUST`, etc.).
- Header lines may occur in any order and may be interleaved with data or other headers.
- A single `.IIF` file may contain multiple section types. All are independently extracted.
- Unsupported or unrecognized headers will be logged and ignored with a warning.

#### 6.5.3 Module Dispatch

- For each detected section, a normalized dispatch event is constructed and routed to the appropriate processing module (e.g., `accounts`, `transactions`, `customers`, etc.).
- Each section is processed independently, even if originating from the same `.IIF` file.
- Processing modules are responsible for validation, mapping, transformation, and output generation for their assigned sections.

#### 6.5.4 Dispatch Payload Schema

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

This section is **immutable** under PRD Governance v1.0.0. All changes must go through formal versioning review. Referencing module PRDs must treat this schema as canonical.

### Example Payload

```python
example_payload = {
    "section": "!ACCNT",
    "records": [...],
    "input_path": "input/sample-qbd-accounts.IIF",
    "output_dir": "output/",
    "log_path": "output/qbd-to-gnucash.log",
    "mapping_config": {...},
    "extra_config": {}
}
```

> **Governance Note:**  
> This section is governed under **PRD Governance Document v1.0.0**.  
> - It defines `core_dispatch_payload_v1`, a canonical schema for module communication.  
> - All downstream module PRDs must treat this schema as the single source of truth.  
> - Any modifications require a formal version increment (e.g., `core_dispatch_payload_v2`) and a PRD governance review.

---

## 7. Non-Functional Requirements

### 7.1 Performance & Scalability

- Must scale to at least thousands of account entries per file.
- Should process large `.IIF` files efficiently without excessive memory or CPU usage.

### 7.2 Error Handling

- Must not crash on partial or malformed input files.
- Should gracefully skip or log malformed records and continue processing.
- Stops execution if unmapped account types are detected and a new mapping file is generated.
- Raises clear exceptions for critical errors (e.g., missing required files, invalid data structures).

### 7.3 Logging Strategy

- Should generate logging output for:
  - Unmapped account types.
  - Missing files.
  - Structural anomalies in input data.
  - Key processing steps (e.g., account tree construction, CSV writing).
- Uses Python's `logging` module with a standard log format and configurable log level.
- Logs both warnings and errors, and provides info/debug logs for traceability.

```python
# Logging format example
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
```

### 7.4 File I/O Assumptions

- All input files are treated as **immutable exports** from the source system (e.g., QuickBooks Desktop `.IIF` format).
- The pipeline must not modify, clean, restructure, or preprocess input files in any way.
- Parsing logic must:
  - Activate only when a relevant section header is encountered, as defined by each module.
  - Skip unrelated headers and sections without raising errors.
  - Raise a structured exception if domain-relevant data is encountered before the expected header.
  - Decode using UTF-8 and **strip** invalid characters (lossy decode, no substitution).
- Output files must:
  - Be written using UTF-8 encoding.
  - Follow module-defined format, structure, and naming conventions.
- The tool must:
  - Automatically create required output and intermediate directories using `os.makedirs(..., exist_ok=True)`.
  - Ensure that any paths required for logging also exist at runtime; directory creation is the tool's responsibility.
- File paths and naming conventions should be fully configurable per module or documented in the respective module PRD.

> **Note:**  
> Each module PRD must define:
> - The specific input section(s) it activates on (e.g., `!ACCNT`, `!VEND`).
> - The expected file naming conventions for outputs (e.g., `accounts.csv`).
> - Any module-specific error types for input file structure violations (e.g., `IIFParseError`).

### 7.5 Working Directory & Config Handling

- Loads configuration (input/output directories, mapping file paths) from environment variables or a config file.
- Ensures the project root is in `PYTHONPATH` for module imports.
- Supports `.env` or config file for cross-platform path management (future enhancement).


### 7.6 Security Concerns

- Does not process executable code or macros from input files.
- Only reads and writes plain text files (CSV, JSON, HTML).
- No explicit handling of sensitive data, but assumes input files may contain confidential information.

### 7.7 User Experience & Automation

- Provides clear instructions and error messages for manual steps (e.g., editing mapping files, post-import GnuCash actions).
- Supports iterative workflow: user can refine mappings and re-run the script.
- Output files are formatted for easy import into GnuCash and for human readability.

### 7.8 Automation & Extensibility

- Modular design allows for future automation (e.g., batch processing, dry-run mode, preview/report mode).
- Designed for easy extension to other QuickBooks list types or additional output formats.


### 7.9 External References & Compatibility

- Aligns with GnuCash CSV import logic and requirements.
- Ensures output matches GnuCash's expectations for commodity, namespace, and account hierarchy.

### 7.10 Logging and Graceful Error Handling

- All modules must ensure that any error, exception, or abnormal termination is logged to the designated log file before the process exits.
- Logging must occur synchronously, and log handlers must be flushed to disk before any process termination (including `os._exit`, `sys.exit`, or unhandled exceptions).
- The log entry must include:
  - Timestamp
  - Error type and message
  - Contextual information (e.g., file, function, input parameters if relevant)
- This requirement applies to all current and future modules.
- Modules must avoid abrupt termination without logging.
- If a fatal error is encountered (e.g., unmapped types, validation failure), the error must be logged, and the log must be flushed before exiting.
- Where possible, modules should raise custom exceptions that are caught at the top level, ensuring logging and cleanup are performed.

### 7.11 Validation & Error Handling

- **Error Code Index:**  
  A centralized index of all error codes and their associated messages shall be maintained as constants in [`src/utils/error_handler.py`](../src/utils/error_handler.py). This module acts as the authoritative reference for error definitions, ensuring consistency and ease of maintenance. All error code constants (e.g., `E001`, `E002`, etc.) defined in this file act as a global, immutable registry and must be referenced by all modules.  
  See also: [Logging and Error Handling PRD](../prd/logging/module-prd-logging-v1.0.4.md)

- **Error Code Format:**  
  Codes should be short, unique strings prefixed with 'E' and followed by a numeric identifier (e.g., `E001`, `E002`). Each code maps to a descriptive error message.

- **Example error codes in `error_handler.py`:**  
  ```python
  E001 = 'Invalid IIF file structure'
  E002 = 'Unknown account type'
  E003 = 'Missing required field'
  # Additional error codes and messages as needed...
  ```

- **Usage:**
  All modules shall reference these constants when raising or logging errors, ensuring uniform error handling and reporting throughout the pipeline. The behaviors and exit codes described below are aligned with both the [Logging and Error Handling PRD](../prd/logging/module-prd-logging-v1.0.4.md) and the implementation in [`src/utils/error_handler.py`](../src/utils/error_handler.py).

- **Log File Location:** Default to `output/qbd-to-gnucash.log`. No rotation by default; recommend logrotate for production.
- **Exit Codes:**
  - 0: Success
  - 1: Critical failure (e.g., unreadable input, invalid mapping)
  - 2: Validation errors (e.g., unmapped types, missing parents)
  > All exit codes must be tested via CLI or subprocess-based test that verifies `sys.exit()` was called with the correct code.

  - On validation errors, tool writes details to log and exits with code 2.
  - On critical errors, tool logs and exits with code 1.

---

## 8. Testing & Acceptance

- **Minimal Test Cases:**
  - Empty input file
  - Duplicate account names or full paths
  - Missing parent accounts
  - Unmapped account types (triggers diff file)
  - Malformed IIF (e.g., missing header)
- **Validation Failure Surfacing:**
  - Errors and warnings are printed to stderr and logged to `output/qbd-to-gnucash.log`.
  - Exit code signals error type for automation.
  - **Missing `output/` directory**: Tool should auto-create it without crashing and initialize the log file.

### 8.1 Test Case Examples (Agentic Scaffolding)

> All test case examples below are declarative scaffolding for agentic validation. Each is traceable to a specific PRD requirement and is formatted for pytest compatibility. No new behaviors are introduced.

#### Example 1: Critical Failure (Exit Code 1)
```python
def test_unreadable_input_file(tmp_path):
    """Should exit with code 1 if input file is missing or unreadable.
    Ref: Section 7.11 - Exit code 1 (Critical failure)
    """
    # Simulate missing file scenario
    # ...invoke main.py with non-existent input file...
    # assert exit_code == 1
```

#### Example 2: Validation Error (Exit Code 2)
```python
def test_unmapped_account_type(tmp_path):
    """Should exit with code 2 if unmapped account type is encountered.
    Ref: Section 7.11 - Validation exit code 2
    """
    # Provide input with unmapped account type
    # ...invoke main.py with test input...
    # assert exit_code == 2
```

#### Example 3: Success Path with Verifiable Output
```python
def test_successful_conversion_creates_csv_and_log(tmp_path):
    """Should produce accounts.csv and log file on successful run.
    Ref: Section 7.3, 7.11 - Logging and output file creation
    """
    # Provide valid input
    # ...invoke main.py with valid input...
    # assert output_dir.joinpath('accounts.csv').exists()
    # assert output_dir.joinpath('qbd-to-gnucash.log').exists()
```

---

## 9. Dependencies & Versioning

- **Python Version:** 3.8–3.12 supported. Use `python --version` to check.
- **No external dependencies** beyond the Python standard library.

---

## 10. Documentation & Onboarding

### 10.1 Getting Started
1. Clone the repository:
   ```pwsh
   git clone <repo-url>
   cd qbd-to-gnucash
   ```
2. Ensure Python 3.8+ is installed:
   ```pwsh
   python --version
   ```
3. Place your exported QBD IIF file in the `input/` directory.
4. Run the conversion (no arguments required or supported):
   ```pwsh
   python main.py
   ```
   **Note:**  
   Do not supply any command-line arguments or options. The tool is designed for maximum user-friendliness and will ignore any additional CLI input.
5. Review `output/accounts.csv` and logs in `output/qbd-to-gnucash.log`.

### 10.2 References
- [GnuCash CSV Import Guide](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)
- [GnuCash CSV Import Source (C implementation)](https://github.com/Gnucash/gnucash/blob/stable/gnucash/import-export/csv-imp/assistant-csv-account-import.c)
- [Sample Input/Output Files](input/sample-qbd-accounts.IIF, output/accounts.csv)

---

## 11. Clarify Extensibility Points

### 11.1 Extension Hooks

- To add a new module (e.g., Vendors), create a new file in `modules/` (e.g., `vendors.py`) following the pattern in `accounts.py`.
  - Register the module in `main.py` dispatch logic.

### 11.2 Mapping File Structure

- Each module PRD must define its own mapping file structure and conventions, as required by its domain.
- All mapping files must be in JSON format and referenced via configuration.
- The core PRD does not prescribe or exemplify domain-specific mapping structures; see the relevant module PRD for details.

### 11.3 Registry Dispatch and Interface Contract

The existing prose describes dispatch logic, but interface-level clarity is needed to guide agentic implementation.

#### Registry Contract

```python
class Registry:
    def __init__(self) -> None: ...
    
    def register(self, key: str, module: Any) -> None:
        """Register a domain module with a unique section key (e.g., '!ACCNT').
        Raises:
            RegistryKeyConflictError: If the key is already registered.
        """
    
    def dispatch(self, key: str, records: List[Dict[str, Any]]) -> Any:
        """Dispatches parsed records to the appropriate domain module.
        Raises:
            KeyError: If the key is not registered.
            Exception: If the target module raises an uncaught exception.
        """
```

#### Behavioral Notes
- Keys must be unique per module. Duplicates raise `RegistryKeyConflictError`.
- If a key is not registered, a structured error is raised (see `log_and_exit()` in core).
- On dispatch error, module-specific exceptions may propagate or be wrapped depending on `run_conversion_pipeline` error strategy.

#### Error Codes (from utils/error_handler.py)

```python
class RegistryKeyConflictError(Exception):
    """Raised when two modules attempt to register the same section key."""
    pass

class DispatchError(Exception):
    """Raised when dispatch fails due to an unknown or unreachable module."""
    pass
```

#### Fallback Rules (Reference)
| Condition                | Action                                   |
|---------------------------|-----------------------------------------|
| Unregistered key          | Raise `KeyError`, log error             |
| Duplicate registration    | Raise `RegistryKeyConflictError`        |
| Dispatch fails internally | Raise `DispatchError` or module-defined |
| Registry is empty         | Abort conversion with `E999`            |

#### Example Usage (from main.py)

```python
registry = Registry()
registry.register('!ACCNT', accounts_module)
output = registry.dispatch('!ACCNT', account_records)
```

---

This interface should be honored across all modules using the registry dispatch pattern. Any deviation from this pattern must be justified in the relevant module PRD with test coverage and exception handling noted.
