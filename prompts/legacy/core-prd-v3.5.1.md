<!-- filepath: c:\git-root\qbd-to-gnucash\prd\core-prd-v3.5.0.md -->
# Core PRD: QuickBooks Desktop to GnuCash Conversion Tool

**Document Version:** 3.5.1  
**State:** Fully Governed & Codegen-Ready
**Author:** Pewe Jekubam

---

## 1.0 Compatibility Matrix

| Module Name         | PRD Version | Compatible With Core PRD |
|---------------------|-------------|--------------------------|
| Chart of Accounts   | v1.0.9      | v3.5.0                   |
| Sales Tax Code List | (TBD)       | v3.5.0                   |
| Item List           | (TBD)       | v3.5.0                   |
| Customer List       | (TBD)       | v3.5.0                   |
| Vendor List         | (TBD)       | v3.5.0                   |

---

## 2.0 History
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

This project delivers a modular, command-line conversion tool for migrating financial data from QuickBooks Desktop (QBD) into GnuCash using structured import files. The core framework applies a consistent, extensible processing pipeline—input ingestion, parsing, mapping, and output generation—which is reused across all modules. Each domain module (e.g., Accounts, Vendors, Transactions, and others) is responsible for converting its respective QBD data into GnuCash-compatible formats, as defined in its own PRD. The core PRD defines the shared architecture, orchestration, and extension points for all modules.

This project is CLI-only; no graphical user interface or CLI arguments will be developed or supported.

### 3.2 Scope

**In-Scope**  
- Core engine functionality for parsing, mapping, and generating output files compatible with GnuCash import formats.  
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

### 4.5 Domain Module Naming Requirements

- All submodules and files within a domain module must be named unambiguously to prevent cross-domain confusion and ensure clarity.
- File and submodule names should, wherever practical, include the parent domain as a prefix or otherwise clearly indicate their domain ownership.
- **Example:** Files in the `accounts` module should be named using the pattern `accounts_<submodule>.py` (e.g., `accounts_tree.py`, `accounts_utils.py`).
- This naming requirement applies to all current and future domain modules and their subcomponents.
- This rule is mandatory for governance compliance and supports extensibility, maintainability, and prevention of naming collisions across the codebase.

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


### 6.1 Directory Layout

```plaintext
.                                  # Project root
├── input/                        # User-provided IIF files
│   ├── sample-qbd-accounts.IIF   # Example Chart of Accounts export
│   ├── sample-qbd-customers.IIF  # Example Customers export
│   ├── sample-qbd-items.IIF      # Example Items export
│   ├── sample-qbd-payment-terms.IIF # Example Payment Terms export
│   └── sample-qbd-sales-tax-codes.IIF # Example Sales Tax Codes export
├── output/                       # Generated output files and logs
│   └── qbd-to-gnucash.log        # Main log file for conversion runs
├── prd/                          # Product Requirements Documents (PRDs)
│   ├── core-prd-vX.Y.Z.md        # Core PRD (this document)
│   ├── PRD-Module-Template-vX.Y.Z.md # PRD template for new modules
│   ├── accounts/                 # Accounts module PRD and docs
│   │   ├── module-prd-accounts-vX.Y.Z.md # Accounts module PRD
│   │   └── README.md             # Accounts module readme
│   ├── logging/                  # Logging module PRD and docs
│   │   ├── module-prd-logging-vX.Y.Z.md # Logging module PRD
│   │   └── README.md             # Logging module readme
│   └── mapping/                  # Mapping module PRD and docs
│       ├── module-prd-mapping-vX.Y.Z.md # Mapping module PRD
│       └── README.md             # Mapping module readme
├── src/                          # Source code for conversion tool
│   ├── modules/                  # Domain-specific modules
│   │   └── accounts/             # Accounts module implementation
│   │       ├── accounts.py       # Accounts conversion logic
│   │       └── accounts_tree.py   # Account tree builder (domain-owned)
│   ├── list_converters/          # Other list conversion logic (non-domain-specific)
│   │   └── mapping.py            # Mapping logic
│   ├── registry/                 # Registry and config hooks
│   │   └── mapping/              # Mapping registry
│   │       └── accounts_mapping_baseline.json # Baseline mapping config
│   ├── utils/                    # Shared utilities
│   │   ├── error_handler.py      # Error handling utilities
│   │   ├── iif_parser.py         # IIF file parser
│   │   ├── logging.py            # Logging utilities
│   │   └── validation.py         # Validation logic
│   └── validation/               # Validation module PRD and docs
│       ├── module-prd-validation-v1.0.4.md # Validation module PRD
│       └── README.md             # Validation module readme
├── main.py                       # Entrypoint: orchestrates dispatch and phase flow
└── README.md                     # Project overview and instructions
```
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
```

# Example usage:
try:
    register_module(registry, '!ACCNT', accounts_module)
except RegistryKeyConflictError as e:
    log_and_exit(str(e), code=1)
```

### 6.5 Global Dispatch Data Contract (Immutable)

> **Governance Note:**
> This section is IMMUTABLE and governed under PRD Governance Document v1.0.0. All module PRDs must cross-reference this section as the single source of truth for the core-to-module dispatch payload structure. Any changes require formal governance review and version increment.

#### 6.5.1 Canonical Payload Schema (`core_dispatch_payload_v1`)

The following schema defines the structured payload passed from the core dispatcher to each processing module. This contract is versioned and must be referenced by all modules for input validation and interface compliance.

```python
from typing import TypedDict, List, Dict, Any, Optional

class core_dispatch_payload_v1(TypedDict):
    """Canonical payload structure for core-to-module dispatch (v1)."""
    section_key: str  # Section identifier (e.g., '!ACCNT', '!VEND')
    records: List[Dict[str, Any]]  # List of parsed records for the section
    mapping: Dict[str, Any]  # Mapping configuration relevant to the module
    input_file: str  # Path to the source input file
    output_dir: str  # Directory for module output files
    log_path: str  # Path to the main log file
    config: Optional[Dict[str, Any]]  # Additional config (optional, module-specific)
```

#### 6.5.2 Example Payload

```python
example_payload: core_dispatch_payload_v1 = {
    "section_key": "!ACCNT",
    "records": [
        {"NAME": "Assets", "TYPE": "ASSET", "DESC": "Company assets"},
        {"NAME": "Bank", "TYPE": "BANK", "DESC": "Checking account"}
    ],
    "mapping": {
        "ASSET": "Asset",
        "BANK": "Bank"
    },
    "input_file": "input/sample-qbd-accounts.IIF",
    "output_dir": "output/",
    "log_path": "output/qbd-to-gnucash.log",
    "config": {
        "strict_mode": True,
        "module_version": "1.0.9"
    }
}
```

#### 6.5.3 Minimal Dispatch Function Signature

```python
def dispatch_to_module(module: Any, payload: core_dispatch_payload_v1) -> Any:
    """Dispatch the canonical payload to a processing module and return the result."""
    # ...function implementation...
```

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
| Condition                | Action                        |
|-------------------------|-------------------------------|
| Unregistered key         | Raise `KeyError`, log error   |
| Duplicate registration   | Raise `RegistryKeyConflictError` |
| Dispatch fails internally | Raise `DispatchError` or module-defined |
| Registry is empty        | Abort conversion with `E999` |

#### Example Usage (from main.py)

```python
registry = Registry()
registry.register('!ACCNT', accounts_module)
output = registry.dispatch('!ACCNT', account_records)
```

---

This interface should be honored across all modules using the registry dispatch pattern. Any deviation from this pattern must be justified in the relevant module PRD with test coverage and exception handling noted.
