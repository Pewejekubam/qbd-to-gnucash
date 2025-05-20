<!-- filepath: c:\git-root\qbd-to-gnucash\prd\core-prd-v3.0.0.md -->
# Core PRD: QuickBooks Desktop to GnuCash Conversion Tool
**Version:** 3.4.0
**Date:** 2025-05-19  
**State:** Agentic AI Compatibility Enhancement

## 1. Compatibility Matrix

Compatibility Matrix  
| Module Name         | PRD Version | Compatible With Core PRD |
|---------------------|-------------|--------------------------|
| Chart of Accounts   | v1.0.5      | v3.4.0                   |
| Sales Tax Code List | (TBD)       | v3.4.0                   |
| Item List           | (TBD)       | v3.4.0                   |
| Customer List       | (TBD)       | v3.4.0                   |
| Vendor List         | (TBD)       | v3.4.0                   |
| (roadmap modules)   | (see roadmap list) | (future)          |

## 2. History

History  
v2.7.3: Final monolithic PRD before modularization.  
v3.0.0: Core PRD established as the root of a modular PRD system. All module-specific logic to be extracted into versioned standalone files in `./prd/{module}/`.  
v3.0.1: Minor clarifications and error handling improvements.  
v3.1.0: Mandated explicit function signatures and interface contracts for all module boundaries.
v3.3.1: Standardized terminology for mapping diff file, output file path, and accounts.csv. Added Terminology section for clarity and future consistency.
v3.4.0: Added explicit JSON Schema and Python typing examples for all major data structures. Updated interface contracts and example calls for public functions/classes.

## 3. Introduction

### 3.1 Project Overview

This project delivers a command-line conversion tool for migrating financial data from QuickBooks Desktop (QBD) into GnuCash using structured `.csv` files. The initial focus is on the QBD Chart of Accounts (`!ACCNT`), with support for parsing IIF exports, mapping account types, reconstructing hierarchies, and generating GnuCash-compatible output. 

The core framework applies a consistent processing pipeline — input ingestion, parsing, mapping, and output generation — which is reused across all modules. The first implemented module, the "Accounts" module, converts QBD account data to GnuCash-compatible format. Other modules will build upon this core logic, but the present scope remains limited to account migration.

This project is CLI-only; no graphical user interface will be developed or supported.

---

### 3.2 Scope

**In-Scope**
- Input: QBD Chart of Accounts (`!ACCNT`) IIF export
- Output: GnuCash-compatible `accounts.csv`
- Core engine to handle:
  - Parsing of IIF data
  - Generation of structured GnuCash import format
- Modular design for reusability across future conversion types

**Out-of-Scope**
- All QBD exports **other than** Chart of Accounts are excluded in this phase:
  - Customers, Vendors, Employees, Items, Transactions, etc.
- QIF import workflows and GUI support are excluded
- No roadmap implementation is assumed; future module integration will reuse the core engine but is not defined here

---

### 3.3 Target Audience

This tool is intended for technical users — accountants, bookkeepers, or developers — performing structured financial data migration from QBD to GnuCash. Familiarity with the principles of double-entry accounting and GnuCash's account-type model is strongly recommended.

---

### 3.4 Background Context

QuickBooks Desktop is a proprietary platform, and many users are migrating to open-source accounting systems for reasons including cost, longevity, and transparency. However, the lack of compatible conversion tooling presents a serious barrier. This project exists to fill that gap, enabling clean migration of core data without data loss or manual recreation.

---

## 4. Objectives & Goals

### 4.1 Primary Objective
Enable seamless and accurate conversion of QuickBooks Desktop (QBD) financial data—beginning with the Chart of Accounts—into a GnuCash-compatible format, using a modular, configuration-driven command-line tool suitable for agentic AI implementation.

### 4.2 Success Criteria
- ✅ **Correctness**: Generated `accounts.csv` file imports cleanly into GnuCash with all account types mapped correctly and hierarchical structure preserved.
- ✅ **Validation**: Import passes GnuCash's CSV importer validation with no structural errors or account-type mismatches.
- ✅ **Resilience**: Conversion tool tolerates minor input inconsistencies (e.g., naming anomalies, empty fields) and logs them as structured issues.
- ✅ **Iteration Support**: Tool supports a configurable workflow including generation of both "specific" and "diff" JSON mapping files, enabling iterative correction and reprocessing.
- ✅ **Traceability**: Every transformation step (parsing, mapping, output) is logged with structured detail to support debugging and auditing.
- ✅ **Agentic Compatibility**: All logic is modular and declarative enough to support AI-based code generation with minimal human intervention.

### 4.3 Background Context
The ability to migrate financial records from QBD into GnuCash is essential for users transitioning to open-source or non-proprietary systems. GnuCash relies on strict double-entry accounting principles and requires precise data structuring during import. A conversion tool that meets these standards will allow users to retain control of their data while escaping licensing or platform lock-in. A clean, modular tool also provides the foundation for future modules (e.g., Transactions, Vendors, Customers), each using the same logic framework to extend the system.

---

## 5. User Stories & Use Cases

### 5.1 User Stories

- **As a finance team member**, I want to convert a QBD account list into a GnuCash-compatible format so I can continue managing finances without proprietary software.
- **As a technical operator**, I want to validate the CSV structure before importing into GnuCash so I can avoid errors during the migration.
- **As a developer**, I want the tool to be modular and scriptable so I can integrate it into an automated migration pipeline.
- **As a business stakeholder**, I want to see clear logs and diffs so I can trust the data integrity of the migrated output.
- **As a contributor**, I want the architecture to be transparent and well-documented so I can extend it to other QBD data types in the future.

> **Creator's User Story:**  
> As a technical team lead, I'm responsible for migrating our company's financial records from QuickBooks Desktop after Intuit's repeated subscription hikes — most recently from $142 to $163 *per seat*. With multiple users across departments, this translates into thousands of dollars per month. This tool is being developed to eliminate that recurring cost, free us from vendor lock-in, and preserve full access to our historical financial data in a stable, open-source system.

---

### 5.2 Use Cases

- A user runs the CLI tool against a QBD `.IIF` file containing the Chart of Accounts. The tool maps types, constructs hierarchies, and emits a valid `accounts.csv` for GnuCash.
- A user modifies the mapping configuration and re-runs the tool to adjust output structure based on GnuCash's import requirements.
- A user runs the tool in verbose mode to inspect how each QBD account was interpreted, including unmapped or ambiguous cases.
- A technical user integrates the tool into a shell script to batch-convert QBD files during a scheduled system migration.

---

### 5.3 Background Context

These user stories and use cases reflect real-world pressures faced by organizations using QBD — primarily the rising cost of licensing and the limitations of proprietary formats. By designing the tool to operate via the command line and to support detailed inspection, mapping flexibility, and configuration diffs, it solves not only the technical challenge of migration but also addresses auditability, extensibility, and maintainability. This allows both end users and system owners to move toward GnuCash with confidence and control.

---

## 6. System Architecture and Workflow

### 6.1 Terminology

- **Mapping diff file**: The file `accounts_mapping_diff.json` written to `output/`, containing unmapped QBD account types for user review and correction.
- **Output file path**: The file path for the final GnuCash-compatible output, typically `output/accounts.csv`.
- **accounts.csv**: The canonical CSV output file for GnuCash import, generated by the tool.
- All references to mapping differences, output targets, and CSV paths in this document and all module PRDs must use these terms.

---

### 6.2 Directory Layout

```plaintext
.
├── input/                # User-provided IIF files  
├── output/               # Final GnuCash files (accounts.csv, customers.csv, etc.)  
│   └── accounts_mapping_specific.json   # User-managed override mappings  
│   └── accounts_mapping_diff.json       # Auto-generated unmapped entries  
├── intermediate/         # Debug JSON/HTML outputs, tree visualizations  
├── registry/             # Dispatcher logic and key-based config hooks  
│   └── mapping/          # JSON mapping files (baseline only) 
├── modules/              # Conversion modules by domain  
│   ├── accounts.py  
│   ├── customers.py  
│   ├── vendors.py  
│   ├── transactions.py  
│   └── ...  
├── utils/                # Shared utilities (parsing, diagnostics, output writers)  
└── main.py               # Entrypoint: orchestrates dispatch and phase flow  
```

---

### 6.3 Data Mapping Flow

- Convert QBD data structures (e.g., `ACCNT` lines) into normalized internal dictionaries.
- Normalize all incoming fields to lowercase with underscores.
- Validate IIF structure and mapping status before further transformation.
- Use a registry-dispatched orchestrator to delegate per-key transformations based on configuration.
- Merge `accounts_mapping_specific.json` on top of `accounts_mapping_baseline.json`.
- Emit GnuCash-compatible `accounts.csv` output after path resolution and flattening.
- Additional modules like `customers`, `vendors`, and `transactions` are modularized and follow the same dispatch+config pipeline, but are not yet implemented in the MVP.

---

### 6.4 Config Merge & Diff Workflow

- On first run, only the `accounts_mapping_baseline.json` file is present.
- If unmapped types or accounts are detected, a `accounts_mapping_diff.json` file is written to `output/`, capturing problematic entries for review.
- Users must edit the `diff` file, copy relevant entries into `accounts_mapping_specific.json`, and rerun the tool.
- On each run, the system will:
  1. Load the baseline config.
  2. Merge the specific config (if present).
  3. Write a new `diff` if unresolved mappings remain.
- This process allows incremental refinement of account mappings.
- This pattern generalizes to other future modules.
> The presence of all three stages (baseline load, specific overlay, diff write) must be enforced in the pipeline with log assertions or debug-mode checkpoints.

---

### 6.5 Special Handling: Accounts Receivable / Payable

GnuCash uses `RECEIVABLE` and `PAYABLE` as internal account types for its business modules.

To avoid import issues and GUI bugs:

- This tool maps:
  - QBD `AR` accounts to `ASSET`
  - QBD `AP` accounts to `LIABILITY`
- Names and hierarchy are preserved (e.g., `Assets:Accounts Receivable`).

After import:

1. Open your GnuCash file.
2. Enable business features via the *Business* menu.
3. Manually edit the `Accounts Receivable` and `Accounts Payable` accounts.
4. Set their types to `RECEIVABLE` and `PAYABLE` respectively.

---

### 6.6 Extensibility Guidelines

| Domain             | Guideline                                                                             |
| ------------------|----------------------------------------------------------------------------------------|
| **Registry**       | Dispatches behavior per `key`, not filename. Extensible via config.                   |
| **Parsers**        | Output `List[Dict]`; header normalization must occur at parse-time.                   |
| **Tree Builders**  | Must be path-aware (e.g., `Assets:Bank:Checking`) and placeholder-safe.               |
| **Writers**        | Accept normalized data; must understand output modality (e.g., CSV, QIF).             |
| **Error Handling** | Prefer structured exceptions and path-aware diagnostics.                              |
| **Mapping**        | Separate `baseline` from `specific`; support hot-swappable overrides.                 |
| **CLI**            | Should inspect intermediate artifacts (tree size, unmapped types, etc.).              |
| **Docs**           | README must declare data dependencies (e.g., "Customers require Accounts and Terms"). |

---

### 6.7 Error Handling Strategy

**Error Classifications**

| Stage                 | Example Errors                                             |
|----------------------|------------------------------------------------------------|
| **Parsing**           | Missing header in IIF, tab mismatch, invalid UTF-8         |
| **Mapping**           | Unknown QBD account type, no destination hierarchy defined |
| **Tree Construction** | Missing parent, failed 1-child promotion, circular paths   |
| **Output**            | File write permission denied, CSV malformed                |
| **Registry**          | Unregistered key, key conflict, fallback loop              |

**Metadata Required**

- **File or Key**: e.g., `sample-qbd-accounts.IIF`, `!ACCNT`
- **Line/Record Ref**: e.g., `Row 24`, `Account Name: Other Expenses`
- **Processing Step**: Parsing → Mapping → Tree → Output
- **Expected vs Actual**: Clear diff
- **Registry Context**: If applicable
- **Structured JSON log**: Optional for agent inspection

**Fallback Rules**

| Condition                | Action                            |
|-------------------------|-----------------------------------|
| Unmapped QBD type        | Fallback to `Uncategorized:ASSET` |
| Missing parent path      | Insert placeholder dynamically    |
| Registry key not defined | Fail with structured error        |
| IIF file unreadable      | Abort with detailed notice        |

**Feedback Format**

- Console output: Human-readable
- Log file: Trace with file, function, chain
- Optional debug: Intermediate decisions and chain
- Agent-compatible phrasing and structure

---

### 6.8 Factored Validation Suite

A **validation suite** is a set of reusable, composable methods that inspect integrity at each stage of the pipeline. These support error raising, structured logging, and optional halting.

**Structure**

```python
class AccountValidationSuite:
    def validate_iif_record(self, record: dict) -> bool: ...
    def validate_mapping(self, qb_type: str, mapping: dict) -> bool: ...
    def validate_account_tree(self, tree: dict) -> bool: ...
    def validate_flattened_tree(self, tree: dict) -> bool: ...
    def validate_csv_row(self, row: dict) -> bool: ...
    def run_all(self, records, mapping, tree, csv_rows): ...
```

**Integration Points**

- **After parsing**: validate each IIF record.
- **After mapping**: ensure every QBD type maps to a known GnuCash path.
- **After tree build**: detect missing parents, circular paths.
- **After flattening**: validate placeholder promotion and 1-child rule.
- **Before CSV write**: confirm final row integrity.

**Pipeline Usage**

```python
validator = AccountValidationSuite()

for record in records:
    validator.validate_iif_record(record)

for qb_type in qb_account_types:
    validator.validate_mapping(qb_type, combined_map)

validator.validate_account_tree(tree)
validator.validate_flattened_tree(tree)

for row in csv_rows:
    validator.validate_csv_row(row)
```

**Benefits**

- Centralizes logic for integrity enforcement
- Improves error logging and testability
- Supports automation and agent-aware validation
- Makes dry-run/test modes possible

---

#### 6.8.1 Summary Table: Stage vs. Validator

| Stage                | Validator Method            |
|----------------------|-----------------------------|
| IIF Parsing          | `validate_iif_record`       |
| Mapping              | `validate_mapping`          |
| Tree Construction    | `validate_account_tree`     |
| Parent Existence     | `validate_account_tree`     |
| Flattening           | `validate_flattened_tree`   |
| CSV Output           | `validate_csv_row`          |

---

### 6.9 Interface Contracts and Function Signatures

- All module boundaries must have clearly documented function signatures in the PRD.
  - This includes function name, argument names and types (using Python typing), return type, exceptions raised, and a 1-2 line docstring/description.
  - Example format:
    ```python
    def parse_iif_accounts(iif_path: str) -> List[Dict[str, Any]]
        """Parse an IIF file and return a list of account records."""
    Raises: IIFParseError
    Example: records = parse_iif_accounts('input/sample.iif')
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

---

## 7. Data Structure Definitions (Agentic AI Compatibility)

### 7.1 Mapping Diff File (accounts_mapping_diff.json)
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "type": "object",
  "properties": {
    "unmapped_accounts": {
      "type": "array",
      "items": {
        "type": "object",
        "properties": {
          "qbd_type": {"type": "string"},
          "account_name": {"type": "string"},
          "suggested_gnucash_type": {"type": ["string", "null"]}
        },
        "required": ["qbd_type", "account_name"]
      }
    }
  },
  "required": ["unmapped_accounts"]
}
```

### 7.2 Mapping Baseline File (account_mapping_baseline.json)
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

### 7.3 Account Record (Python Typing)
```python
from typing import TypedDict, Optional
class AccountRecord(TypedDict):
    NAME: str
    ACCNTTYPE: str
    DESC: Optional[str]
    PARENT: Optional[str]
    # ...other QBD fields as needed
```

### 7.4 Validation Error Structure (Python Typing)
```python
class ValidationError(TypedDict):
    record: dict
    error: str
    stage: str
```

## 8. Example Calls for Public Functions/Classes

### 8.1 parse_iif_accounts
```python
# Normal case
records = parse_iif_accounts('input/sample-qbd-accounts.IIF')
assert isinstance(records, list)
assert 'NAME' in records[0]

# Edge case: empty file
try:
    parse_iif_accounts('input/empty.iif')
except IIFParseError as e:
    print(e)
```

### 8.2 run_accounts_pipeline
```python
# Normal case
run_accounts_pipeline(
    iif_path='input/sample-qbd-accounts.IIF',
    mapping_path='output/accounts_mapping_specific.json',
    csv_path='output/accounts.csv',
    log_path='output/qbd-to-gnucash.log',
    mapping_diff_path='output/accounts_mapping_diff.json'
)
# Edge case: missing mapping file
try:
    run_accounts_pipeline(
        iif_path='input/sample-qbd-accounts.IIF',
        mapping_path='output/missing.json',
        csv_path='output/accounts.csv',
        log_path='output/qbd-to-gnucash.log',
        mapping_diff_path='output/accounts_mapping_diff.json'
    )
except MappingLoadError as e:
    print(e)
```

### 8.3 AccountValidationSuite
```python
validator = AccountValidationSuite(mapping)
# Normal case
ok = validator.run_all(records, tree, flat, csv_rows)
# Edge case: missing required field
bad_record = {"ACCNTTYPE": "BANK"}  # Missing NAME
assert not validator.validate_iif_record(bad_record)
```

## 9. Summary Table: Functions, Data Structures, Schemas, and Example Calls

| Function/Class           | Data Structure/Schema                | Example Call Location         |
|-------------------------|--------------------------------------|------------------------------|
| parse_iif_accounts      | AccountRecord (Python Typing)        | Example Calls section         |
| run_accounts_pipeline   | See Interface Contract, Mapping JSON | Example Calls section         |
| AccountValidationSuite  | ValidationError (Python Typing)      | Example Calls section         |
| Mapping Files           | Mapping Baseline/Diff (JSON Schema)  | Data Structure Definitions    |

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

- Input files are **immutable exports from QuickBooks Desktop (.IIF)**.
- No part of the pipeline may modify, clean, preprocess, or restructure these files.
- The tool must adapt to the raw input format exactly as exported.
- The parser must:
  - Skip any irrelevant list headers (`!HDR`, `!TRNS`, etc.) before reaching `!ACCNT`.
  - Activate only when the relevant section (`!ACCNT`) is encountered.
  - Raise `IIFParseError` if relevant data (e.g., `ACCNT` lines) appear before the matching header.
  - Ignore unrelated headers and sections without failure.
- Output files include:
  - `accounts.csv` (GnuCash-compatible, with full hierarchy)
  - Optionally, `accounts_mapping_diff.json` for unmapped types
- Reads and writes files using UTF-8 encoding.
- Non UTF-8 characters in input files are stripped and not replaced (lossy decode).
- The tool must ensure all necessary output subdirectories (`output/`, `intermediate/`) exist at runtime.
- These directories should be created automatically (`os.makedirs(..., exist_ok=True)`) before any file I/O occurs.
- Logging must not assume the prior existence of the log path — directory creation is the tool’s responsibility.

### 7.5 Working Directory & Config Handling

- Loads configuration (input/output directories, mapping file paths) from environment variables or a config file.
- Ensures the project root is in `PYTHONPATH` for module imports.
- Supports `.env` or config file for cross-platform path management (future enhancement).

### 7.6 Hierarchy Construction

- GnuCash hierarchy is determined by colon-delimited account paths (e.g., `Expenses:Travel:Airfare`).
- Each account's **full path** determines its position in the hierarchy, but its `Account Name` field (used for display/reference) includes **only the final segment** (e.g., `Airfare`), not the full path.
- This separation ensures GnuCash properly resolves the account tree without duplicating path information in display names.
- Placeholder parents are inserted when intermediate levels are missing from the input.
- During flattening, placeholder accounts with only one real child are removed, and their child is promoted to preserve a clean hierarchy.
- Hierarchy integrity and naming rules are validated against GnuCash import rules ([GnuCash Guide: Accounts](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)).

### 7.7 Security Concerns

- Does not process executable code or macros from input files.
- Only reads and writes plain text files (CSV, JSON, HTML).
- No explicit handling of sensitive data, but assumes input files may contain confidential information.

### 7.8 User Experience & Automation

- Provides clear instructions and error messages for manual steps (e.g., editing mapping files, post-import GnuCash actions).
- Supports iterative workflow: user can refine mappings and re-run the script.
- Output files are formatted for easy import into GnuCash and for human readability.

### 7.9 Automation & Extensibility

- Modular design allows for future automation (e.g., batch processing, dry-run mode, preview/report mode).
- Designed for easy extension to other QuickBooks list types or additional output formats.

### 7.10 Assumptions

- Only the `!ACCNT` list type is handled by the accounts module.
- Account names are consistently delimited by `:` for hierarchy.
- Input files are expected to be well-formed QuickBooks exports unless otherwise noted.

### 7.11 External References & Compatibility

- Aligns with GnuCash CSV import logic and requirements.
- Ensures output matches GnuCash's expectations for commodity, namespace, and account hierarchy.

### 7.12 Logging and Graceful Error Handling

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

---

## 8. Configuration & Environment

- **Config Precedence:** If environment variables are set, they will be detected by the code and used. Otherwise, hard-coded paths will be used. This ensures that users can override defaults via environment variables, but the tool will always function with built-in fallback paths if none are set.
- **Config/Env Keys:**
  - `QBD_INPUT_PATH` (default: `input/sample-qbd-accounts.IIF`)
  - `GNC_OUTPUT_PATH` (default: `output/accounts.csv`)
  - `MAPPING_BASELINE_PATH` (default: `mappings/account_mapping_baseline.json`)
  - `MAPPING_SPECIFIC_PATH` (default: `output/accounts_mapping_specific.json`)
  - `MAPPING_DIFF_PATH` (default: `output/accounts_mapping_diff.json`)
- **Example config snippet:**
  ```python
  import os
  QBD_INPUT_PATH = os.getenv('QBD_INPUT_PATH', 'input/sample-qbd-accounts.IIF')
  GNC_OUTPUT_PATH = os.getenv('GNC_OUTPUT_PATH', 'output/accounts.csv')
  # ...
  ```

---

## 9. Validation & Error Handling

- **Error Codes/Messages:** Define as constants in `utils/error_handler.py`:
  ```python
  E001 = 'Invalid IIF file structure'
  E002 = 'Unknown account type'
  E003 = 'Missing required field'
  # ...
  ```
- **Log File Location:** Default to `output/qbd-to-gnucash.log`. No rotation by default; recommend logrotate for production.
- **Exit Codes:**
  - 0: Success
  - 1: Critical failure (e.g., unreadable input, invalid mapping)
  - 2: Validation errors (e.g., unmapped types, missing parents)
  > All exit codes must be tested via CLI or subprocess-based test that verifies `sys.exit()` was called with the correct code.

- **Behavior:**
  - On validation errors, tool writes details to log and exits with code 2.
  - On critical errors, tool logs and exits with code 1.

---

## 10. Testing & Acceptance

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

---

## 11. Dependencies & Versioning

- **Python Version:** 3.8–3.12 supported. Use `python --version` to check.
- **No external dependencies** beyond the Python standard library.

---

## 12. Documentation & Onboarding

### 12.1 Getting Started

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

### 12.2 References
- [GnuCash CSV Import Guide](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)
- [GnuCash CSV Import Source (C implementation)](https://github.com/Gnucash/gnucash/blob/stable/gnucash/import-export/csv-imp/assistant-csv-account-import.c)
- [Sample Input/Output Files](input/sample-qbd-accounts.IIF, output/accounts.csv)

---

## 13. Clarify Extensibility Points

- **Extension Hooks:**
  - To add a new module (e.g., Vendors), create a new file in `modules/` (e.g., `vendors.py`) following the pattern in `accounts.py`.
  - Register the module in `main.py` dispatch logic.
- **Mapping File Structure:**
  - All mapping files are JSON, with the following structure:
    ```json
    {
      "account_types": {
        "BANK": {
          "gnucash_type": "ASSET",
          "placeholder": false
        },
        "EQUITY": {
          "gnucash_type": "EQUITY",
          "placeholder": false
        },
        "CCARD": {
          "gnucash_type": "LIABILITY",
          "placeholder": false
        },
        "AR": {
          "gnucash_type": "RECEIVABLE",
          "placeholder": false
        },
        "AP": {
          "gnucash_type": "PAYABLE",
          "placeholder": false
        },
        "EXP": {
          "gnucash_type": "EXPENSE",
          "placeholder": false
        },
        "OEXP": {
          "gnucash_type": "EXPENSE",
          "placeholder": false
        }
      },
      "default_rules": {
        "unmapped_accounts": {
          "gnucash_type": "ASSET",
          "placeholder": false
        }
      }
    }
    ```
  - New mapping files should be placed in `registry/mapping/` or `output/` as appropriate and referenced in config.

---

## 13.1 Registry Dispatch and Fallback Logic

- Registry dispatches per-key (e.g., `!ACCNT`, `!TRNS`).
- Keys must be unique per module.
- If two modules claim the same key, a `RegistryKeyConflictError` is raised.
- Module registration occurs in `main.py` via the `registry.dispatch()` call.
- If a key is not registered, a structured error is raised and logged.

---

## 13.2 Declarative Error Categories Table

A declarative error category structure is used for code generation, test scaffolding, and documentation:

```python
ERROR_CATEGORIES = {
    "Parsing": ["Missing header", "Tab mismatch", "Invalid UTF-8"],
    "Mapping": ["Unknown account type", "No destination hierarchy defined"],
    "Tree Construction": ["Missing parent", "Failed 1-child promotion", "Circular paths"],
    "Output": ["File write permission denied", "CSV malformed"],
    "Registry": ["Unregistered key", "Key conflict", "Fallback loop"]
}
```

---

## 13.3 Unicode Normalization and Logging

- All input files are read as UTF-8. If non-UTF-8 characters are encountered, they are stripped.
- To avoid silent data loss, the tool logs a warning each time a character is stripped or replaced during normalization.
- Example implementation:

```python
def safe_decode(line, file_path):
    try:
        return line.encode('utf-8').decode('utf-8')
    except UnicodeDecodeError as e:
        logging.warning(f"Unicode decode error in {file_path}: {e}. Stripping invalid characters.")
        return line.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
```

- All normalization and stripping events are logged with file name and line number for traceability.

---
