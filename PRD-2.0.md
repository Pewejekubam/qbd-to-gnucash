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

This tool is intended for technical users — accountants, bookkeepers, or developers — performing structured financial data migration from QBD to GnuCash. Familiarity with the principles of double-entry accounting and GnuCash’s account-type model is strongly recommended.

---

### 1.4 Background Context

QuickBooks Desktop is a proprietary platform, and many users are migrating to open-source accounting systems for reasons including cost, longevity, and transparency. However, the lack of compatible conversion tooling presents a serious barrier. This project exists to fill that gap, enabling clean migration of core data without data loss or manual recreation.

## 2. Objectives & Goals

### 2.1 Primary Objective
Enable seamless and accurate conversion of QuickBooks Desktop (QBD) financial data—beginning with the Chart of Accounts—into a GnuCash-compatible format, using a modular, configuration-driven command-line tool suitable for agentic AI implementation.

### 2.2 Success Criteria
- ✅ **Correctness**: Generated `accounts.csv` file imports cleanly into GnuCash with all account types mapped correctly and hierarchical structure preserved.
- ✅ **Validation**: Import passes GnuCash’s CSV importer validation with no structural errors or account-type mismatches.
- ✅ **Resilience**: Conversion tool tolerates minor input inconsistencies (e.g., naming anomalies, empty fields) and logs them as structured issues.
- ✅ **Iteration Support**: Tool supports a configurable workflow including generation of both “specific” and “diff” JSON mapping files, enabling iterative correction and reprocessing.
- ✅ **Traceability**: Every transformation step (parsing, mapping, output) is logged with structured detail to support debugging and auditing.
- ✅ **Agentic Compatibility**: All logic is modular and declarative enough to support AI-based code generation with minimal human intervention.

### 2.3 Background Context
The ability to migrate financial records from QBD into GnuCash is essential for users transitioning to open-source or non-proprietary systems. GnuCash relies on strict double-entry accounting principles and requires precise data structuring during import. A conversion tool that meets these standards will allow users to retain control of their data while escaping licensing or platform lock-in. A clean, modular tool also provides the foundation for future modules (e.g., Transactions, Vendors, Customers), each using the same logic framework to extend the syste

### 3. User Stories & Use Cases

#### 3.1 User Stories

- **As a finance team member**, I want to convert a QBD account list into a GnuCash-compatible format so I can continue managing finances without proprietary software.
- **As a technical operator**, I want to validate the CSV structure before importing into GnuCash so I can avoid errors during the migration.
- **As a developer**, I want the tool to be modular and scriptable so I can integrate it into an automated migration pipeline.
- **As a business stakeholder**, I want to see clear logs and diffs so I can trust the data integrity of the migrated output.
- **As a contributor**, I want the architecture to be transparent and well-documented so I can extend it to other QBD data types in the future.

> **Creator’s User Story:**  
> As a technical team lead, I’m responsible for migrating our company's financial records from QuickBooks Desktop after Intuit’s repeated subscription hikes — most recently from $142 to $163 *per seat*. With multiple users across departments, this translates into thousands of dollars per month. This tool is being developed to eliminate that recurring cost, free us from vendor lock-in, and preserve full access to our historical financial data in a stable, open-source system.

---

#### 3.2 Use Cases

- A user runs the CLI tool against a QBD `.IIF` file containing the Chart of Accounts. The tool maps types, constructs hierarchies, and emits a valid `accounts.csv` for GnuCash.
- A user modifies the mapping configuration and re-runs the tool to adjust output structure based on GnuCash’s import requirements.
- A user runs the tool in verbose mode to inspect how each QBD account was interpreted, including unmapped or ambiguous cases.
- A technical user integrates the tool into a shell script to batch-convert QBD files during a scheduled system migration.

---

#### 3.3 Background Context

These user stories and use cases reflect real-world pressures faced by organizations using QBD — primarily the rising cost of licensing and the limitations of proprietary formats. By designing the tool to operate via the command line and to support detailed inspection, mapping flexibility, and configuration diffs, it solves not only the technical challenge of migration but also addresses auditability, extensibility, and maintainability. This allows both end users and system owners to move toward GnuCash with confidence and control.


### 4. **System Architecture and Workflow**

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
| **Docs**           | README must declare data dependencies (e.g., “Customers require Accounts and Terms”). |

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
    def validate_iif_record(self, record: dict) -> bool:
        ...

    def validate_mapping(self, qb_type: str, mapping: dict) -> bool:
        ...

    def validate_account_tree(self, tree: dict) -> bool:
        ...

    def validate_flattened_tree(self, tree: dict) -> bool:
        ...

    def validate_csv_row(self, row: dict) -> bool:
        ...

    def run_all(self, records, mapping, tree, csv_rows):
        ...
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



## 5. **Non-Functional Requirements**

### **Performance & Scalability**

- Must scale to at least thousands of account entries per file.
- Should process large `.IIF` files efficiently without excessive memory or CPU usage.

### **Error Handling**

- Must not crash on partial or malformed input files.
- Should gracefully skip or log malformed records and continue processing.
- Stops execution if unmapped account types are detected and a new mapping file is generated.
- Raises clear exceptions for critical errors (e.g., missing required files, invalid data structures).

### **Logging Strategy**

- Should generate logging output for:
  - Unmapped account types.
  - Missing files.
  - Structural anomalies in input data.
  - Key processing steps (e.g., account tree construction, CSV writing).
- Uses Python’s `logging` module with a standard log format and configurable log level.
- Logs both warnings and errors, and provides info/debug logs for traceability.

### **File I/O Assumptions**

- Input files are unmodified QuickBooks `.IIF` exports.
- Output files include:
  - `accounts.csv` (GnuCash-compatible, with full hierarchy).
  - HTML files for sales tax codes and payment terms.
  - Optionally, a `specific_mapping.json` for unmapped types.
- Reads and writes files using UTF-8 encoding.
- Assumes the working directory or configured paths are writable and accessible.

### **Working Directory & Config Handling**

- Loads configuration (input/output directories, mapping file paths) from environment variables or a config file.
- Ensures the project root is in `PYTHONPATH` for module imports.
- Supports `.env` or config file for cross-platform path management (future enhancement).

### **Hierarchy Construction**

- GnuCash hierarchy is determined by colon-delimited account paths (e.g., `Expenses:Travel:Airfare`).
- Each account's **full path** determines its position in the hierarchy, but its `Account Name` field (used for display/reference) includes **only the final segment** (e.g., `Airfare`), not the full path.
- This separation ensures GnuCash properly resolves the account tree without duplicating path information in display names.
- Placeholder parents are inserted when intermediate levels are missing from the input.
- During flattening, placeholder accounts with only one real child are removed, and their child is promoted to preserve a clean hierarchy.
- Hierarchy integrity and naming rules are validated against GnuCash import rules ([GnuCash Guide: Accounts](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)).

### **Security Concerns**

- Does not process executable code or macros from input files.
- Only reads and writes plain text files (CSV, JSON, HTML).
- No explicit handling of sensitive data, but assumes input files do not contain confidential information.

### **User Experience & Automation**

- Provides clear instructions and error messages for manual steps (e.g., editing mapping files, post-import GnuCash actions).
- Generates HTML files for easier manual entry of sales tax codes and payment terms.
- Supports iterative workflow: user can refine mappings and re-run the script.
- Output files are formatted for easy import into GnuCash and for human readability.

### **Automation & Extensibility**

- Modular design allows for future automation (e.g., batch processing, dry-run mode, preview/report mode).
- Designed for easy extension to other QuickBooks list types or additional output formats.

### **Assumptions**

- Only the `!ACCNT` list type is handled by the accounts module.
- Account names are consistently delimited by `:` for hierarchy.
- Input files are expected to be well-formed QuickBooks exports unless otherwise noted.

### **External References & Compatibility**

- Aligns with GnuCash CSV import logic and requirements.
- Ensures output matches GnuCash’s expectations for commodity, namespace, and account hierarchy.


### 6. **Technical Requirements**

- **Technology Stack:**
  - Python 3.x is used for the entire conversion pipeline.
  - No third-party libraries are required; the project relies solely on the standard library (`csv`, `json`, `os`, `logging`).

- **Code Architecture:**
  - The codebase is modular, divided by function:
    - `main.py`: Entry point; handles config loading and dispatch.
    - `accounts.py`: Orchestrates the account conversion pipeline.
    - `iif_parser.py`: Parses QuickBooks IIF files into structured records.
    - `mapping.py`: Loads and merges baseline and user-defined mappings.
    - `account_tree.py`: Builds and manipulates the account hierarchy tree.
    - `csv_writer.py`: Outputs the final CSV file in GnuCash-compatible format.
  - Data flows through: config loading → IIF parsing → mapping → tree construction → validation → flattening → CSV writing.

- **External Libraries/Dependencies:**
  - None beyond Python’s standard library.

- **Logging and Config Handling:**
  - Logging is implemented using Python’s `logging` module in all major modules.
    - Logs malformed lines, unmapped types, structural anomalies, and key events.
  - Configuration paths are loaded from environment variables or a config object in `main.py`.
    - Future improvements may include `.env` support or a centralized config loader.

- **Background Context:**
  - Python was chosen for its readability, ecosystem support, and compatibility with GnuCash’s CSV schema.
  - The current architecture emphasizes separation of concerns and extensibility, with a focus on modularity and pure data transformation.
  - The primary architectural pain point is complexity and duplication in the account tree logic across modules, presenting opportunities for simplification:
    - Refactor tree/placeholder logic into a single class.
    - Normalize logging and validation across modules.

- **Account Type Resolution**
  - QuickBooks account types are normalized (uppercased and stripped) before mapping.
  - Type mapping prefers specific user-defined mappings, falls back to baseline, and uses a default rule if none found.
  - AR/AP handling is deferred to manual fix post-import, mapped temporarily to ASSET/LIABILITY to avoid GnuCash import errors.

- **Placeholder and Hierarchy Construction**
  - Missing intermediate parents in a colon-delimited account path are injected as `"Placeholder": "T"` accounts with minimal required fields.
  - Duplicate placeholders are upgraded in-place if real account info arrives later in the data stream.

- **Flattening and Promotion**
  - Placeholder accounts with exactly one child are removed to minimize tree depth ("1-child rule"), and the child is promoted up the tree.
  - Ensures clean hierarchy and avoids GnuCash warnings about redundant levels.

- **Output Strategy**
  - `Full Account Name` is derived from the colon path key, never from input field.
  - Sorting: accounts are sorted to ensure parents precede children using colon-count and lexical order.
  - All required and optional fields are output with default values to maintain GnuCash compatibility.


### 7. **Assumptions & Constraints**

- **Assumptions:**
  - Users have access to exported QuickBooks Desktop `.IIF` files.
  - Users possess basic familiarity with accounting principles and GnuCash.
  - The provided mapping files (`account_mapping_baseline.json` and optional user-specific mapping) will cover all relevant account types.
  - Users are targeting the GnuCash CSV importer, not QIF or SQL-based ingestion.
  - File and directory structures follow expected naming conventions and paths defined in the configuration.

- **Constraints:**
  - The tool supports QuickBooks Desktop `.IIF` exports only; QB Online formats are not compatible.
  - Supported QuickBooks versions are 2017 and newer (tested against known IIF structures from these versions).
  - GnuCash import behavior may differ slightly across versions; the tool aligns with GnuCash 5.x CSV importer specifications.
  - Only account, customer/vendor, price, and transaction conversions are supported—no payroll, inventory, or job costing modules are handled.
  - Placeholder and "1-child" rule logic is optimized for cleaner GnuCash hierarchies, but may occasionally alter the original QuickBooks structure.

- **Background Context:**
  - These assumptions simplify the user workflow, reduce error surfaces, and allow for a focused, scriptable conversion process without requiring GUI interactions.
  - The version constraints align with typical lifecycle support from Intuit and GnuCash, reducing variability in exported formats.
  - Clearly stating scope and constraints ensures the project remains manageable and minimizes support for edge-case QuickBooks features or legacy data exports.


### 8. **Timeline & Milestones**

- **Milestones:**
  - ✅ Architecture Finalization: May 12, 2025  
  - 🚧 Core Refactor Begins (Accounts Pipeline): May 14, 2025  
  - 🧪 Internal POC Testing (Accounts Only): May 21, 2025  
  - 📦 End-to-End Conversion MVP (Accounts, Transactions, Prices): May 31, 2025  
  - 🧹 Cleanup, Logging, and Config Finalization: June 5, 2025  
  - 🧾 Full Documentation Draft Complete: June 10, 2025  
  - 🛠️ Freeze Codebase for External Review: June 14, 2025  
  - 📤 First Open Source Push (v0.1): June 15, 2025  

- **Background Context:**
  - This schedule aligns with internal planning for legacy QBD migration before Q3.
  - Dependencies on GnuCash CSV import behavior make early testing critical to avoid data fidelity issues.
  - A mid-June open source milestone supports internal adoption by finance teams and builds community feedback before broader expansion to customers or third-party tools.


### 9. **Risks & Mitigation**

- **Risk 1:**  
  Incomplete or incorrect mapping between QBD account types and GnuCash categories may result in data corruption or rejected imports.

  - **Risk Mitigation:**  
    Extensive validation testing using a wide range of QBD IIF exports.  
    Built-in logging to detect unmapped or miscategorized records early.  
    Configurable, testable mapping files to allow easy user overrides and corrections.

- **Risk 2:**  
  Misinterpretation of GnuCash’s CSV import rules could lead to invalid file formats or broken account hierarchies.

  - **Risk Mitigation:**  
    Implementation strictly aligned to the latest [GnuCash Guide on Accounts](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide) and the [CSV import specifications](https://github.com/Gnucash/gnucash/blob/stable/gnucash/import-export/csv-imp/assistant-csv-account-import.c).  
    Automated validation of CSV output structure pre-export.

- **Risk 3:**  
  Logic for placeholder promotion and tree flattening could introduce subtle structural issues in large or complex charts of accounts.

  - **Risk Mitigation:**  
    Isolate and modularize placeholder logic for unit testing.  
    Flag “promoted” accounts in logs for review.  
    Manual review checklist for unusually deep or flat hierarchies.

- **Background Context:**  
  Ensuring data integrity during migration is critical—both for financial correctness and user trust.  
  These risks are typical in financial data conversion tools but must be proactively managed to prevent reputational or compliance failures.

- **Risk: Mapping Errors or Omissions**
  - If an unmapped account type is encountered, the script generates a stub mapping file and halts with a clear error message.
  - Mitigation: Ensures mapping quality by forcing user input rather than silent failures.

- **Risk: Missing Hierarchy Parents**
  - GnuCash import fails if any parent is missing in the account tree.
  - Mitigation: Hierarchy construction guarantees all required parent placeholders are injected.

- **Risk: Misordered Output**
  - If child accounts are written before parents, GnuCash import can fail.
  - Mitigation: Tree is sorted to ensure top-down output based on colon-depth.


### Appendix A: Critical Implementation Patterns (from POC)

- `resolve_account_type(qb_type, mapping, default_rule)`  
  Normalize and resolve type via multi-tiered mapping system.

- `ensure_all_parents_exist(tree)`  
  Inject intermediate parent accounts with placeholder status.

- `flatten_account_tree(tree)`  
  Apply the 1-child rule to collapse unnecessary placeholder levels.

- `write_gnucash_csv(tree, output_path)`  
  Output accounts sorted by hierarchy depth with full and clean fields.


