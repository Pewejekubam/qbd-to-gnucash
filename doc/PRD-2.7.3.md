# PRD: QuickBooks Desktop to GnuCash Conversion Tool
**Version:** 2.7.3
**Date:** 2025-05-14  
**State:** Under Review

## 1. Introduction

### 1.1 Project Overview

This project delivers a command-line conversion tool for migrating financial data from QuickBooks Desktop (QBD) into GnuCash using structured `.csv` files. The initial focus is on the QBD Chart of Accounts (`!ACCNT`), with support for parsing IIF exports, mapping account types, reconstructing hierarchies, and generating GnuCash-compatible output. 

The core framework applies a consistent processing pipeline — input ingestion, parsing, mapping, and output generation — which is reused across all modules. The first implemented module, the "Accounts" module, converts QBD account data to GnuCash-compatible format. Other modules will build upon this core logic, but the present scope remains limited to account migration.

This project is CLI-only; no graphical user interface will be developed or supported.

---

### 1.2 Scope

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

### 1.3 Target Audience

This tool is intended for technical users — accountants, bookkeepers, or developers — performing structured financial data migration from QBD to GnuCash. Familiarity with the principles of double-entry accounting and GnuCash's account-type model is strongly recommended.

---

### 1.4 Background Context

QuickBooks Desktop is a proprietary platform, and many users are migrating to open-source accounting systems for reasons including cost, longevity, and transparency. However, the lack of compatible conversion tooling presents a serious barrier. This project exists to fill that gap, enabling clean migration of core data without data loss or manual recreation.

---

## 2. Objectives & Goals

### 2.1 Primary Objective
Enable seamless and accurate conversion of QuickBooks Desktop (QBD) financial data—beginning with the Chart of Accounts—into a GnuCash-compatible format, using a modular, configuration-driven command-line tool suitable for agentic AI implementation.

### 2.2 Success Criteria
- ✅ **Correctness**: Generated `accounts.csv` file imports cleanly into GnuCash with all account types mapped correctly and hierarchical structure preserved.
- ✅ **Validation**: Import passes GnuCash's CSV importer validation with no structural errors or account-type mismatches.
- ✅ **Resilience**: Conversion tool tolerates minor input inconsistencies (e.g., naming anomalies, empty fields) and logs them as structured issues.
- ✅ **Iteration Support**: Tool supports a configurable workflow including generation of both "specific" and "diff" JSON mapping files, enabling iterative correction and reprocessing.
- ✅ **Traceability**: Every transformation step (parsing, mapping, output) is logged with structured detail to support debugging and auditing.
- ✅ **Agentic Compatibility**: All logic is modular and declarative enough to support AI-based code generation with minimal human intervention.

### 2.3 Background Context
The ability to migrate financial records from QBD into GnuCash is essential for users transitioning to open-source or non-proprietary systems. GnuCash relies on strict double-entry accounting principles and requires precise data structuring during import. A conversion tool that meets these standards will allow users to retain control of their data while escaping licensing or platform lock-in. A clean, modular tool also provides the foundation for future modules (e.g., Transactions, Vendors, Customers), each using the same logic framework to extend the system.

---

## 3. User Stories & Use Cases

#### 3.1 User Stories

- **As a finance team member**, I want to convert a QBD account list into a GnuCash-compatible format so I can continue managing finances without proprietary software.
- **As a technical operator**, I want to validate the CSV structure before importing into GnuCash so I can avoid errors during the migration.
- **As a developer**, I want the tool to be modular and scriptable so I can integrate it into an automated migration pipeline.
- **As a business stakeholder**, I want to see clear logs and diffs so I can trust the data integrity of the migrated output.
- **As a contributor**, I want the architecture to be transparent and well-documented so I can extend it to other QBD data types in the future.

> **Creator's User Story:**  
> As a technical team lead, I'm responsible for migrating our company's financial records from QuickBooks Desktop after Intuit's repeated subscription hikes — most recently from $142 to $163 *per seat*. With multiple users across departments, this translates into thousands of dollars per month. This tool is being developed to eliminate that recurring cost, free us from vendor lock-in, and preserve full access to our historical financial data in a stable, open-source system.

---

#### 3.2 Use Cases

- A user runs the CLI tool against a QBD `.IIF` file containing the Chart of Accounts. The tool maps types, constructs hierarchies, and emits a valid `accounts.csv` for GnuCash.
- A user modifies the mapping configuration and re-runs the tool to adjust output structure based on GnuCash's import requirements.
- A user runs the tool in verbose mode to inspect how each QBD account was interpreted, including unmapped or ambiguous cases.
- A technical user integrates the tool into a shell script to batch-convert QBD files during a scheduled system migration.

---

#### 3.3 Background Context

These user stories and use cases reflect real-world pressures faced by organizations using QBD — primarily the rising cost of licensing and the limitations of proprietary formats. By designing the tool to operate via the command line and to support detailed inspection, mapping flexibility, and configuration diffs, it solves not only the technical challenge of migration but also addresses auditability, extensibility, and maintainability. This allows both end users and system owners to move toward GnuCash with confidence and control.

---

## 4. System Architecture and Workflow

---

#### 📁 Directory Layout

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

#### 🧩 Data Mapping Flow

- Convert QBD data structures (e.g., `ACCNT` lines) into normalized internal dictionaries.
- Normalize all incoming fields to lowercase with underscores.
- Validate IIF structure and mapping status before further transformation.
- Use a registry-dispatched orchestrator to delegate per-key transformations based on configuration.
- Merge `accounts_mapping_specific.json` on top of `accounts_mapping_baseline.json`.
- Emit GnuCash-compatible `accounts.csv` output after path resolution and flattening.
- Additional modules like `customers`, `vendors`, and `transactions` are modularized and follow the same dispatch+config pipeline, but are not yet implemented in the MVP.

---

#### 🔄 Config Merge & Diff Workflow

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

#### 💼 Special Handling: Accounts Receivable / Payable

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

#### 🔌 Extensibility Guidelines

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

#### 🚨 Error Handling Strategy

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

#### 🧪 Factored Validation Suite

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

**Summary Table: Stage vs. Validator**

| Stage                | Validator Method            |
|----------------------|-----------------------------|
| IIF Parsing          | `validate_iif_record`       |
| Mapping              | `validate_mapping`          |
| Tree Construction    | `validate_account_tree`     |
| Parent Existence     | `validate_account_tree`     |
| Flattening           | `validate_flattened_tree`   |
| CSV Output           | `validate_csv_row`          |

---

## 5. Non-Functional Requirements

### Performance & Scalability

- Must scale to at least thousands of account entries per file.
- Should process large `.IIF` files efficiently without excessive memory or CPU usage.

### Error Handling

- Must not crash on partial or malformed input files.
- Should gracefully skip or log malformed records and continue processing.
- Stops execution if unmapped account types are detected and a new mapping file is generated.
- Raises clear exceptions for critical errors (e.g., missing required files, invalid data structures).

### Logging Strategy

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

### File I/O Assumptions

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

### Working Directory & Config Handling

- Loads configuration (input/output directories, mapping file paths) from environment variables or a config file.
- Ensures the project root is in `PYTHONPATH` for module imports.
- Supports `.env` or config file for cross-platform path management (future enhancement).

### Hierarchy Construction

- GnuCash hierarchy is determined by colon-delimited account paths (e.g., `Expenses:Travel:Airfare`).
- Each account's **full path** determines its position in the hierarchy, but its `Account Name` field (used for display/reference) includes **only the final segment** (e.g., `Airfare`), not the full path.
- This separation ensures GnuCash properly resolves the account tree without duplicating path information in display names.
- Placeholder parents are inserted when intermediate levels are missing from the input.
- During flattening, placeholder accounts with only one real child are removed, and their child is promoted to preserve a clean hierarchy.
- Hierarchy integrity and naming rules are validated against GnuCash import rules ([GnuCash Guide: Accounts](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)).

### Security Concerns

- Does not process executable code or macros from input files.
- Only reads and writes plain text files (CSV, JSON, HTML).
- No explicit handling of sensitive data, but assumes input files may contain confidential information.

### User Experience & Automation

- Provides clear instructions and error messages for manual steps (e.g., editing mapping files, post-import GnuCash actions).
- Supports iterative workflow: user can refine mappings and re-run the script.
- Output files are formatted for easy import into GnuCash and for human readability.

### Automation & Extensibility

- Modular design allows for future automation (e.g., batch processing, dry-run mode, preview/report mode).
- Designed for easy extension to other QuickBooks list types or additional output formats.

### Assumptions

- Only the `!ACCNT` list type is handled by the accounts module.
- Account names are consistently delimited by `:` for hierarchy.
- Input files are expected to be well-formed QuickBooks exports unless otherwise noted.

### External References & Compatibility

- Aligns with GnuCash CSV import logic and requirements.
- Ensures output matches GnuCash's expectations for commodity, namespace, and account hierarchy.

---

## 6. Explicit Inputs/Outputs & File Contracts

### 6.1 Sample Input/Output Files

- **Sample Input:** See `input/sample-qbd-accounts.IIF` for a real QuickBooks Chart of Accounts export. This file contains lines like:

  ```
  !ACCNT	NAME	ACCNTTYPE	DESC	ACCNUM	HIDDEN
  ACCNT	Checking	BANK	Main checking account	1000	N
  ACCNT	Savings	BANK	Savings account	1001	N
  ACCNT	Accounts Receivable	AR		1100	N
  ACCNT	Accounts Payable	AP		2000	N
  ```

- **Sample Output:** See `output/accounts.csv` for a GnuCash-compatible output. Example row:

  ```csv
  Type,Full Account Name,Account Name,Account Code,Description,Account Color,Notes,Symbol,Namespace,Hidden,Tax Info,Placeholder
  ```

- **File Naming Conventions:**
  - Input: Any files with the `.IIF` extension in the `input/` directory.
  - Mapping: `mappings/account_mapping_baseline.json`, `output/accounts_mapping_specific.json`, `output/accounts_mapping_diff.json`

- **CSV Field Order:**
  - Required: `Type,Full Account Name,Account Name,Account Code,Description,Account Color,Notes,Symbol,Namespace,Hidden,Tax Info,Placeholder`
  - Optional fields may be left blank but must be present in the header.
> A test must validate that the output CSV includes all expected headers, even if the data is blank.

---

## 7. API/Function Contracts

For each module, the main functions/classes, signatures, and exceptions are as follows:

### 7.1 `utils/iif_parser.py`
```python
def parse_iif(filepath: str) -> List[Dict[str, str]]:
    """Parses IIF file and returns list of account records. Raises IIFParseError on malformed input."""
```
---

### 7.2 Validation Rules for Parsed Records

Validation logic must operate on field names exactly as exported from QuickBooks Desktop. These are **case-sensitive** and must not be inferred or transformed.

---

#### ✅ Validation Rule: Required Fields

Each parsed record must contain the following fields with non-empty values:

- `NAME` — must not be blank
- `ACCNTTYPE` — must be present and must match a supported QBD → GnuCash type mapping

If either is missing or blank, the parser must raise `IIFParseError`.

---

#### ✅ Validation Rule: Field Count Match

The number of fields in each `ACCNT` record must match the number of fields in the detected `!ACCNT` header. This must be enforced as follows:

- If a line has **fewer fields** than the header: raise `IIFParseError`
- If a line has **more fields** than the header: raise `IIFParseError`

Each record must be zipped with the header to create a `Dict[str, str]` map of values.

---

#### ✅ Validation Rule: Type Mapping Must Resolve

Every `ACCNTTYPE` value must map to a GnuCash account type as defined in the combined mapping file (`baseline` + `specific`). If a mapping is missing:

- The unmapped `ACCNTTYPE` must be added to the `diff` dictionary
- The program must terminate with exit code `2`
- A complete mapping diff must be written to `output/accounts_mapping_diff.json`

---

#### ✅ Validation Rule: Record Line Prefix Enforcement (Added in PRD v2.7.3)

After detecting a `!ACCNT` section header, the parser must validate that all subsequent records intended for processing begin with the literal prefix `ACCNT`.

If a line does not start with `ACCNT`:
- It must be skipped without raising an error
- It must not be parsed, validated, or included in the output
- It may be logged at debug level for traceability

This rule prevents malformed or non-record lines (e.g., junk footer rows, misformatted data) from triggering `IIFParseError` exceptions.

**Rationale:**
QuickBooks `.IIF` files may contain footer rows, comments, or misaligned data after `!ACCNT`. These should be explicitly excluded from structured parsing.

---

#### 🔒 Field Name Enforcement Across Pipeline

All downstream modules must reference parsed IIF records using the **original QBD-exported field names only**. This includes (but is not limited to):

- Account tree construction
- Type mapping and hierarchy flattening
- CSV row composition
- Logging and debugging tools

The following rules apply:
- No inferred or lowercase versions (`name`, `accnttype`, `type`) may be used once records are parsed
- Field access must use exact keys: `NAME`, `ACCNTTYPE`, `DESC`, `ACCNUM`, etc.
- If intermediate fields (e.g., `full_account_name`) are computed, they must be derived explicitly from QBD-native fields and documented in the corresponding module

---

### 7.3 `list_converters/account_tree.py`
```python
class AccountTree:
    def __init__(self, records: List[Dict[str, str]], mapping: Dict): ...
    def validate(self) -> List[str]: ...
```

### 7.4 `exporters/account_csv.py`

```python
def write_accounts_csv(rows: List[Dict[str, str]], output_path: str) -> None:
    """
    """
```

**Purpose:**  
Handles CSV output for GnuCash Accounts import. Responsible for formatting, field ordering, and consistent encoding across all account exports.

**Inputs:**  
- `rows`: List of dictionaries with normalized GnuCash-ready keys.
- `output_path`: Target filepath for `accounts.csv`.

**Field Requirements:**  
Each row must include the following fields, in this order:
```
Type  
Full Account Name  
Account Name  
Account Code  
Description  
Account Color  
Notes  
Symbol  
Namespace  
Hidden  
Tax Info  
Placeholder
```

**Encoding and Format:**  
- Output must be UTF-8 encoded (without BOM).
- CSV quoting must be enabled for **all fields** (`csv.QUOTE_ALL`).
- A header row must be written explicitly, in the field order listed above.

**Failure Modes:**  
- Raises `CSVExportError` on any failure to write the CSV file.
- Logs the number of rows written and the output path.
- Logs a warning if zero rows are passed in.

### 7.5 Error Handling

All modules must raise custom exceptions defined in `utils/error_handler.py`. This ensures consistent, structured error management across the tool and supports automated logging, debugging, and exit-code handling.

#### 📌 Required Exception Classes

The following exception classes must be **explicitly implemented** in `utils/error_handler.py`:

```python
class IIFParseError(Exception):
    """Raised when the IIF file is malformed or unreadable."""
    pass

class MappingLoadError(Exception):
    """Raised when mapping files fail to load or are invalid."""
    pass

class AccountTreeError(Exception):
    """Raised when account tree construction or flattening fails."""
    pass

class RegistryKeyConflictError(Exception):
    """Raised when two modules register the same IIF key."""
    pass

class UnregisteredKeyError(Exception):
    """Raised when no module is registered to handle a given IIF key."""
    pass
```

These classes are referenced in `main.py`, `accounts.py`, and validation routines. Their presence should be verified before orchestration logic is implemented. This prevents missing-import runtime errors and ensures consistent fallback behavior.

#### 🔁 Usage Guidelines

- Each exception should be caught and logged with full context (`file`, `line`, `key`, `step`)
- Critical errors (e.g., unreadable input, unresolvable mappings) must trigger exit with code 1
- Validation-triggered errors (e.g., unmapped account types) must trigger exit with code 2
- Structured error messages should support both console output and machine-readable logs

#### 🧪 Optional Unit Test

To enforce the presence of required exceptions, a test case may be added:

```python
# tests/test_error_handler.py

import utils.error_handler as eh

def test_defined_exceptions():
    assert hasattr(eh, 'IIFParseError')
    assert hasattr(eh, 'MappingLoadError')
    assert hasattr(eh, 'AccountTreeError')
    assert hasattr(eh, 'RegistryKeyConflictError')
    assert hasattr(eh, 'UnregisteredKeyError')
```

This ensures alignment between declared usage and actual implementation.

---

> All listed exceptions must be physically present in `utils/error_handler.py`. Their presence should be **verifiable by static test** (e.g., via `hasattr()` or `importlib`). No exception should be referenced without definition.

### 7.6 Module Contracts

#### Module: accounts.py

**Purpose:**  
Orchestrates the full processing pipeline for the `!ACCNT` list type:
- Parsing → Mapping → Tree Construction → Validation → CSV Output

**Inputs:**  
- `.IIF` filepath containing a `!ACCNT` section
- Mapping files:
  - `account_mapping_baseline.json` (required)
  - `accounts_mapping_specific.json` (optional override)
- Output target path (e.g., `output/accounts.csv`)

**Outputs:**  
- GnuCash-compatible CSV (`accounts.csv`)
- Optional diff file for unmapped types (`accounts_mapping_diff.json`)
- Logs for all key pipeline steps

**Invariants:**  
- All input records must be parsed using original QBD field names (e.g., `NAME`, `ACCNTTYPE`) — case-sensitive
- Intermediate fields (e.g., `full_account_name`) must be derived explicitly and consistently
- Account records must pass validation before CSV generation
- Logging must track pipeline stages and critical error points

**Failure Modes:**  
- Raises `MappingLoadError`, `AccountTreeError`, or validation exceptions on failure
- Logs structured messages for all validation issues
- Halts pipeline if critical steps fail (e.g., mapping or tree invalid)
- **Note:** The `mapping` returned by `load_and_merge_mappings()` must be unpacked before being used. Callers must extract the mapping dictionary and diff as follows:
  ```python
  mapping, diff = load_and_merge_mappings(...)
  ```

#### Module: validation.py

**Purpose:**  
Implements a validation suite for parsed records. Enforces structure, field presence, and mapping integrity before output generation.

**Inputs:**  
- Parsed record list (from the IIF parser, typically `!ACCNT`)
- Mapping dictionary (baseline + overrides) for account type resolution
- Optional context metadata for logging/debugging

**Outputs:**  
- Logs structured validation warnings and errors
- Raises exceptions if fatal structural violations are detected

**Invariants:**  
- All field names must match the original QBD `.IIF` headers exactly (e.g., `NAME`, `ACCNTTYPE`)
- No inferred or lowercase aliases may be used (e.g., `name`, `type`)
- All required fields must be present and non-empty
- All types must either map cleanly or trigger the diff capture

**Failure Modes:**  
- Logs validation issues with record number and offending key/value
- Fails pipeline early if required fields or mappings are missing
- Returns structured validation report (if used programmatically)

#### Module: iif_parser.py

**Purpose:**  
Parses `.IIF` files exported from QuickBooks Desktop, extracting structured records from the requested list section (e.g., `!ACCNT`) only.

**Inputs:**  
- Filepath to `.IIF` file
- Target key (e.g., `!ACCNT`, `!VEND`, etc.)

**Outputs:**  
- List of normalized records (one `dict` per line, using field names from the corresponding `!<KEY>` header)

**Invariants:**  
- Ignores all other headers (`!HDR`, `!TRNS`, etc.) until the specified `!KEY` is found
- Extracts only data rows matching that key (e.g., `ACCNT`)
- Retains original QuickBooks field names (case-sensitive)
- Raises `IIFParseError` if data lines appear before a matching header or if no data lines are found

**Failure Modes:**  
- Structured exception with file name and line number
- Logs parsing state transitions (header found, records counted, errors)

#### Module: account_tree.py

**Purpose:**  
Builds and flattens the account hierarchy for GnuCash import, including placeholder insertion and 1-child pruning.

**Inputs:**  
- Parsed list of account records (from `!ACCNT`)
- Mapping dictionary to resolve account type and hierarchy path

**Outputs:**  
- Flat list of normalized GnuCash-ready accounts
- Optional derived fields (e.g., `full_account_name`, placeholder flags)

**Invariants:**  
- Operates on QBD field names only (e.g., `NAME`, `ACCNTTYPE`)
- Constructs full paths using colon-delimited names
- Ensures all parent accounts exist (inserts placeholders as needed)
- Removes placeholder-only branches with a single child (1-child promotion)
- All inserted placeholder accounts must include valid `NAME`, `Full Account Name`, and `ACCNTTYPE` fields

**Failure Modes:**  
- Raises `AccountTreeError` if the hierarchy cannot be resolved
- Logs tree depth, placeholder insertions, and flattening results

#### Module: `exporters/account_csv.py`

**Purpose:**
Handles CSV output of flattened GnuCash-ready account records. Converts normalized dictionaries into a standards-compliant GnuCash `accounts.csv` file.

**Inputs:**
- `rows`: List of dictionaries, each representing a GnuCash account row. All dictionaries must contain the full field set expected by GnuCash.
- `output_path`: Filepath to which the CSV should be written (e.g., `output/accounts.csv`).

**Outputs:**
- UTF-8 encoded CSV file at the specified path, with the correct field headers and format for GnuCash import.

**Invariants:**
- CSV must include **exactly these fields**, in this order:
  - `Type`
  - `Full Account Name`
  - `Account Name`
  - `Account Code`
  - `Description`
  - `Account Color`
  - `Notes`
  - `Symbol`
  - `Namespace`
  - `Hidden`
  - `Tax Info`
  - `Placeholder`

**All Rows:**
- All rows must use consistent quoting (`csv.QUOTE_ALL`)

**Output Encoding:**
- Must create written using UTF-8 encoding (without BOM)

**Directory Handling:**
- Must create parent directories for `output_path` if they do not exist

**Failure Modes:**
- Raises `CSVExportError` (defined in `utils/error_handler.py`) on:
  - File write errors (e.g., permissions, disk full)
  - Incomplete row data (missing required columns)
  - Any unhandled I/O exception during export

**Logging:**
- Logs all export attempts, file size, and row count
- Logs full stack trace on exception

#### Placeholder Construction Requirements

Placeholder accounts are inserted during hierarchy construction when intermediate path segments are missing from the original QuickBooks export.

Each placeholder **must be a structurally complete account record** and must meet the following requirements:

- `NAME`: The **final segment** of the account path (e.g., `Travel` from `Expenses:Travel`)
- `Full Account Name`: The **entire colon-delimited path** to that placeholder (e.g., `Expenses:Travel`)
- `ACCNTTYPE`: Inherited from the nearest real child account, or logically derived by tracing upward to the closest known valid type (must map to a valid GnuCash type)
- `placeholder`: Optional field with value `'T'` to mark synthetic records (for traceability only)

These fields must be present on all placeholder accounts so that they:
- Pass validation with no exceptions
- Are written cleanly to the GnuCash-compatible CSV
- Can be used to resolve hierarchy rollups in GnuCash post-import

Placeholder accounts are **not exempt from any structural rules** applied to real accounts.

#### Module: mapping.py

**Purpose:**  
Loads, merges, and validates account type mapping files. Provides lookup services for resolving QBD types to GnuCash account types and hierarchy paths.

**Inputs:**  
- Baseline mapping JSON (required)
- Specific mapping JSON (optional override)

**Outputs:**  
- Combined dictionary of `account_types` and `default_rules`
- Optional diff map of unmapped types (for export)

**Invariants:**  
- Input mapping files must follow expected schema
- All lookups must use exact QBD keys (e.g., `BANK`, `OCASSET`, `AR`)
- Fallback behavior is defined by `default_rules`

**Failure Modes:**  
- Raises `MappingLoadError` if required files are missing or unreadable
- Logs all key loads, fallbacks, and mapping mismatches

#### Module: main.py

**Purpose:**  
Entry point for the CLI tool. Loads configuration, initializes logging, and dispatches processing to the correct module based on IIF section key.

**Inputs:**  
- CLI arguments or config (input file paths, keys)
- Registry of handlers for each list type (e.g., `!ACCNT` → `accounts.py`)

**Outputs:**  
- Runs the selected processing pipeline and logs output
- Exits with structured return codes (0 = success, 1 = critical error, 2 = diff triggered)

**Invariants:**  
- Must create `output/` and other directories if missing
- Must configure logging before pipeline begins
- Must catch and route all structured exceptions to appropriate exit codes

**Failure Modes:**  
- Raises `UnregisteredKeyError` for unhandled keys
- Handles all structured errors via `error_handler.py`
- Writes full run log to file and stderr stream

#### Module: `list_converters/mapping.py`

This module provides mapping services to resolve QBD `ACCNTTYPE` values and hierarchical category overrides based on one or more mapping files. It must be reusable across all list types that support mapping input.

---

### ✅ Required Function: `load_and_merge_mappings`

**Signature:**
`def load_and_merge_mappings(baseline_path: str, specific_path: Optional[str]) -> Tuple[Dict, Dict]`

**Description:**
- Loads the baseline and specific mapping JSON files.
- Merges them into a single mapping dictionary.
- Computes a `diff` of unmapped `ACCNTTYPE` values based on parsed input.

**Return Value:**
A tuple containing:
1. `mapping: Dict` — merged mapping dictionary in the format:
   `{ "account_types": { "BANK": { "type": "ASSET", "gnc_type": "BANK" }, ... } }`
2. `diff: Dict` — unmapped QBD types to be written to `accounts_mapping_diff.json` if non-empty.

**Contract Enforcement:**
- Callers **must unpack** the return value using:
  `mapping, diff = load_and_merge_mappings(...)`
- Passing the full tuple downstream is a contract violation.

**Failure Modes:**
- Raises `MappingLoadError` if files are missing or invalid.
- Logs duplicate keys or conflicts during merge.

---

### 7.7 Placeholder Typing Phase

**Purpose:**  
This phase ensures that all placeholder accounts inserted during hierarchy construction are assigned a valid `ACCNTTYPE` and GnuCash `Type`. It is executed *after* tree construction and *before* flattening. Placeholder accounts must meet all structural and semantic requirements for CSV export and validation. No placeholder may proceed untyped.

**Context:**  
GnuCash account hierarchies require each account — including inserted placeholders — to have a valid `Type`. Since placeholder accounts are not present in the original IIF export, their type must be derived in a deterministic, rule-driven way. This phase implements that logic.

---

#### Step 1: Detect Mapping-Declared Paths

Before placeholder type inheritance is applied, each node in the account tree must be checked against the declared `destination_hierarchy` values in the merged account type mapping.

If a node’s `Full Account Name` exactly matches one of these declared paths:

- It must be treated as a real, declared account — not a placeholder.
- Its `ACCNTTYPE` and `Type` must be assigned using the mapping entry associated with that path.
- It must be marked:
  - `placeholder = 'F'`
  - `type_resolution = 'mapping'`
  - `inferred_from = <mapping key>` (e.g., `'BANK'`)

This override takes precedence over any upward inheritance or synthetic typing logic.

**Validation Constraint:**  
If multiple mapping entries reference the same `destination_hierarchy` but resolve to **different GnuCash types**, this constitutes a configuration error. It must be detected during mapping load and halt the pipeline with a structured validation failure.

---

#### Step 2: Inherit Type from Parent

For any remaining placeholder nodes not matched by a declared path:

- Traverse upward to the nearest ancestor with a valid `ACCNTTYPE`.
- Inherit the ancestor’s `ACCNTTYPE`, and resolve the GnuCash `Type` using the mapping.
- Set:
  - `type_resolution = 'inherited'`
  - `inferred_from = <ancestor path>`

**Validation Rule:**  
If no typed ancestor can be found (e.g., the entire lineage is synthetic or incomplete), this violates the PRD’s structural guarantee that all trees originate from a known top-level type. The pipeline must:

- Raise a structured validation error:  
  `"Unresolved placeholder type — no valid ancestor."`
- Halt execution with exit code 2.
- Log the affected placeholder path and all inspected ancestors.

Fallback to `default_rules` is explicitly disallowed under this model.

---

#### Step 3: Record Type Resolution Metadata

Each placeholder account, after typing, must include the following diagnostic metadata fields:

- `type_resolution`: One of:
  - `'mapping'` (if declared path match)
  - `'inherited'` (if type was inherited upward)
  - `'error'` (if resolution failed; this is terminal)
- `inferred_from`: The mapping key or parent path that supplied the type

These fields are retained in intermediate outputs and logs to support debugging, auditing, and agent-based diagnostics.

---

**Outcome:**  
After this phase completes, all nodes in the account tree (real and placeholder) have valid, validated type assignments. The tree is now safe to flatten and export to `accounts.csv`.

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
4. Run the conversion:
   ```pwsh
   python main.py
   ```
5. Review `output/accounts.csv` and logs in `output/qbd-to-gnucash.log`.

### 12.2 References
- [GnuCash CSV Import Guide](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)
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
