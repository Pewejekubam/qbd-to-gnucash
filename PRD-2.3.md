# PRD: QuickBooks Desktop to GnuCash Conversion Tool

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
  - Mapping of account types and hierarchy
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

- Input files are unmodified QuickBooks `.IIF` exports.
- Output files include:
  - `accounts.csv` (GnuCash-compatible, with full hierarchy).
  - HTML files for sales tax codes and payment terms (future roadmap).
  - Optionally, a `account_mapping_specific.json` for unmapped types.
- Reads and writes files using UTF-8 encoding.
- Non UTF-8 character in input files are stripped and not replaced.
- Assumes the working directory or configured paths are writable and accessible.

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
  ASSET,Assets:Current Assets:Bank:Checking,Checking,1000,Main checking account,,,,USD,CURRENCY,F,F,F
  ASSET,Assets:Current Assets:Bank:Savings,Savings,1001,Savings account,,,,USD,CURRENCY,F,F,F
  ASSET,Assets:Accounts Receivable,Accounts Receivable,1100,,,,USD,CURRENCY,F,F,F
  LIABILITY,Liabilities:Accounts Payable,Accounts Payable,2000,,,,USD,CURRENCY,F,F,F
  ```

- **File Naming Conventions:**
  - Input: Any files with the `.IIF` extension in the `input/` directory.
  - Output: `output/accounts.csv`
  - Mapping: `mappings/account_mapping_baseline.json`, `output/accounts_mapping_specific.json`, `output/accounts_mapping_diff.json`

- **CSV Field Order:**
  - Required: `Type,Full Account Name,Account Name,Account Code,Description,Account Color,Notes,Symbol,Namespace,Hidden,Tax Info,Placeholder`
  - Optional fields may be left blank but must be present in the header.

---

## 7. API/Function Contracts

For each module, the main functions/classes, signatures, and exceptions are as follows:

### 7.1 `utils/iif_parser.py`
```python
def parse_iif(filepath: str) -> List[Dict[str, str]]:
    """Parses IIF file and returns list of account records. Raises IIFParseError on malformed input."""
```

### 7.2 `list_converters/mapping.py`
```python
def load_mapping(baseline_path: str, specific_path: Optional[str] = None) -> Dict:
    """Loads and merges baseline and specific mapping files. Raises MappingLoadError on failure."""
```

### 7.3 `list_converters/account_tree.py`
```python
class AccountTree:
    def __init__(self, records: List[Dict[str, str]], mapping: Dict): ...
    def build_tree(self) -> Dict: ...
    def flatten_tree(self) -> List[Dict]: ...
    def ensure_all_parents_exist(self): ...
    def validate(self) -> List[str]: ...
```

### 7.4 `utils/csv_writer.py`
```python
def write_accounts_csv(rows: List[Dict], output_path: str) -> None:
    """Writes account rows to CSV in GnuCash format. Raises IOError on failure."""
```

### 7.5 Error Handling
- All modules should raise custom exceptions defined in `utils/error_handler.py` (e.g., `IIFParseError`, `MappingLoadError`, `AccountTreeError`).

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
          "destination_hierarchy": "Assets:Current Assets:Bank",
          "placeholder": false
        },
        "EQUITY": {
          "gnucash_type": "EQUITY",
          "destination_hierarchy": "Equity",
          "placeholder": false
        },
        "CCARD": {
          "gnucash_type": "LIABILITY",
          "destination_hierarchy": "Liabilities:Credit Cards",
          "placeholder": false
        },
        "AR": {
          "gnucash_type": "RECEIVABLE",
          "destination_hierarchy": "Assets:Accounts Receivable",
          "placeholder": false
        },
        "AP": {
          "gnucash_type": "PAYABLE",
          "destination_hierarchy": "Liabilities:Accounts Payable",
          "placeholder": false
        },
        "EXP": {
          "gnucash_type": "EXPENSE",
          "destination_hierarchy": "Expenses",
          "placeholder": false
        },
        "OEXP": {
          "gnucash_type": "EXPENSE",
          "destination_hierarchy": "Expenses:Other",
          "placeholder": false
        }
      },
      "default_rules": {
        "unmapped_accounts": {
          "gnucash_type": "ASSET",
          "destination_hierarchy": "Assets:Uncategorized",
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
