# QBD to GnuCash Conversion Tool

**Version:** 3.4.0  
**Date:** 2025-05-19  

---

## 🚀 Overview

This tool delivers a command-line utility for migrating financial data from QuickBooks Desktop (QBD) into GnuCash using structured `.csv` files. The initial focus is on the QBD Chart of Accounts (`!ACCNT`), with support for parsing IIF exports, mapping account types, reconstructing hierarchies, and generating GnuCash-compatible output. The tool enforces strict validation, logging, and deterministic behavior for account hierarchy construction, type inference, and placeholder promotion.

> **Architectural Constraint:**
> All account nodes — real or placeholder — exist beneath one of five canonical root types: ASSET, LIABILITY, INCOME, EXPENSE, or EQUITY. Account types are determined exclusively by tracing upward to the nearest typed ancestor. Sibling, child, or majority-based inference is forbidden. Fallbacks to mapping default rules are deprecated. This is a structural invariant.

---

## ✅ Features

- Converts QBD Chart of Accounts to GnuCash CSV format
- Preserves account hierarchy and type mapping
- Generates diff files for unmapped QBD types
- Logs each processing phase for traceability
- Modular design with clean CLI integration
- Strict enforcement of field names and type inheritance rules
- All placeholder accounts are structurally complete and validated
- Agentic AI-compatible PRD and module documentation
- Explicit JSON Schema and Python typing for all major data structures

---

## 📦 Directory Structure

```plaintext
.
├── input/                # QBD IIF exports
├── output/               # GnuCash CSVs and mapping diffs
├── intermediate/         # Debug/visualization artifacts
├── registry/             # Mapping logic and dispatch rules
├── modules/              # Per-domain converters (accounts, vendors, etc.)
├── utils/                # Shared logic: parsing, writing, validation
├── prd/                  # PRD-base and module PRDs
└── main.py               # Entrypoint CLI orchestrator
```

---

## 🧩 Supported Inputs & Outputs

- Input: QuickBooks Desktop `.IIF` files containing `!ACCNT` entries only
- Output: `accounts.csv` formatted for GnuCash import
- Mapping files:
  - `registry/mapping/account_mapping_baseline.json`
  - `output/accounts_mapping_specific.json` (user override)
  - `output/accounts_mapping_diff.json` (auto-generated)

---

## 🛠️ Getting Started

### Requirements

- Python 3.8–3.12
- No external dependencies (stdlib only)

### Installation

```pwsh
git clone <repo-url>
cd qbd-to-gnucash
```

### Running the Tool

1. Place your `.IIF` file in `input/`
2. Run the converter:
   ```pwsh
   python main.py
   ```
3. Inspect output:
   - `output/accounts.csv`
   - `output/accounts_mapping_diff.json` (if unmapped types found)
   - `output/qbd-to-gnucash.log` for diagnostics

---

## 🔁 Mapping Workflow

1. Tool reads the baseline mapping.
2. Applies specific overrides (if present).
3. Writes a diff file for any unmapped QBD account types.
4. User updates the specific mapping and reruns.

Mapping files use the following structure:

```json
{
  "account_types": {
    "BANK": {
      "gnucash_type": "ASSET",
      "destination_hierarchy": "Assets:Current Assets:Bank",
      "placeholder": false
    },
    ...
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

**Note:** Fallback to `default_rules` for placeholder typing is deprecated as of v3.4.0. All placeholder types must be resolved by upward inheritance only.

---

## 📁 Sample Input & Output

**Sample Input:**
```text
!ACCNT	NAME	ACCNTTYPE	DESC	ACCNUM	HIDDEN
ACCNT	Checking	BANK	Main checking account	1000	N
ACCNT	Accounts Receivable	AR		1100	N
ACCNT	Accounts Payable	AP		2000	N
```

**Sample Output (`accounts.csv`):**
```csv
Type,Full Account Name,Account Name,Account Code,Description,Account Color,Notes,Symbol,Namespace,Hidden,Tax Info,Placeholder
ASSET,Assets:Current Assets:Bank:Checking,Checking,1000,Main checking account,,,,USD,CURRENCY,F,F,F
ASSET,Assets:Accounts Receivable,Accounts Receivable,1100,,,,USD,CURRENCY,F,F,F
LIABILITY,Liabilities:Accounts Payable,Accounts Payable,2000,,,,USD,CURRENCY,F,F,F
```

---

## 🧪 Validation Suite

The system includes staged validators for:

| Stage              | Method                        |
|--------------------|-------------------------------|
| IIF Parsing        | `validate_iif_record()`       |
| Mapping            | `validate_mapping()`          |
| Tree Construction  | `validate_account_tree()`     |
| Flattening         | `validate_flattened_tree()`   |
| CSV Output         | `validate_csv_row()`          |

All field names are enforced as exported from QBD (`NAME`, `ACCNTTYPE`, etc.). No inferred or lowercase aliases are permitted.

---

## ⚙️ Configuration

The following environment variables can override default paths:

| Key                    | Default Path                         |
|------------------------|--------------------------------------|
| `QBD_INPUT_PATH`       | `input/sample-qbd-accounts.IIF`      |
| `GNC_OUTPUT_PATH`      | `output/accounts.csv`                |
| `MAPPING_BASELINE_PATH`| `registry/mapping/account_mapping_baseline.json` |
| `MAPPING_SPECIFIC_PATH`| `output/accounts_mapping_specific.json` |
| `MAPPING_DIFF_PATH`    | `output/accounts_mapping_diff.json`  |

Example:

```python
import os
QBD_INPUT_PATH = os.getenv('QBD_INPUT_PATH', 'input/sample-qbd-accounts.IIF')
```

---

## 🧱 Registry & Dispatch

- Each module registers a handler keyed to its list type (e.g., `!ACCNT`)
- Keys must be unique or raise `RegistryKeyConflictError`
- If a key is missing, a structured error is logged and raised

---

## 🛡️ Error Handling & Logging

- All critical operations log to `output/qbd-to-gnucash.log`
- Errors include parsing failures, unmapped types, and invalid trees
- Unicode decode issues are stripped and logged with file/line details
- On validation errors, the tool exits with code 2; on critical errors, with code 1
- Logging is agentic AI-compatible and follows the centralized logging module PRD

Example:

```python
def safe_decode(line, file_path):
    try:
        return line.encode('utf-8').decode('utf-8')
    except UnicodeDecodeError as e:
        logging.warning(f"Unicode decode error in {file_path}: {e}")
        return line.encode('utf-8', errors='ignore').decode('utf-8', errors='ignore')
```

---

## 🔒 Security Notes

- Tool only reads/writes plain text (CSV, JSON)
- Does not execute macros or scripts from input
- Logs and config files may contain confidential data — secure them appropriately

---

## 🧩 Extending the Tool

To add support for other QBD list types:

1. Create `modules/<type>.py`
2. Register the key and handler in `main.py`
3. Follow the same parse → map → flatten → write pipeline
4. Add or update the module PRD in `prd/<module>/`

---

## 📚 References

- [GnuCash CSV Import Guide](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)
- [GnuCash CSV Import Source (C implementation)](https://github.com/Gnucash/gnucash/blob/stable/gnucash/import-export/csv-imp/assistant-csv-account-import.c)
- [GnuCash Accounts Hierarchy Docs](https://www.gnucash.org/docs/)
- [Sample Input/Output Files](input/sample-qbd-accounts.IIF, output/accounts.csv)

---

## 🧠 Notes on Accounting Types

GnuCash recognizes **five core account types**:

- `ASSET`
- `LIABILITY`
- `EQUITY`
- `INCOME`
- `EXPENSE`

All mappings must ultimately reduce to one of these. `RECEIVABLE` and `PAYABLE` are internal subtypes used only by GnuCash’s business features. All account nodes must trace upward to one of these canonical root types.

---

## 👥 Authors & Licensing

This project is maintained by internal migration teams seeking vendor lock-in removal.  
Open-source licensing to be determined.
