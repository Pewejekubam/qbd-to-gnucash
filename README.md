
# QBD to GnuCash Conversion Tool

A CLI utility for converting QuickBooks Desktop (QBD) financial data into GnuCash-compatible CSVs, beginning with the Chart of Accounts.

---

## 🚀 Overview

This tool automates the migration of account data from proprietary `.IIF` exports from QuickBooks Desktop into clean, structured `accounts.csv` files that GnuCash can import.

Designed for:
- Technical operators, accountants, and developers
- Agentic AI compatibility (modular, declarative, config-driven)
- Future extensibility (Customers, Vendors, Transactions, etc.)

---

## ✅ Features

- Converts QBD Chart of Accounts to GnuCash CSV format
- Preserves account hierarchy and type mapping
- Generates diff files for unmapped QBD types
- Logs each processing phase for traceability
- Modular design with clean CLI integration

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
└── main.py               # Entrypoint CLI orchestrator
```

---

## 🧩 Supported Inputs

- QuickBooks Desktop `.IIF` files containing `!ACCNT` entries only
- Output: `accounts.csv` formatted for GnuCash import
- Mapping files:
  - `mappings/account_mapping_baseline.json`
  - `output/accounts_mapping_specific.json` (user override)
  - `output/accounts_mapping_diff.json` (auto-generated)

---

## 🛠️ Getting Started

### Requirements

- Python 3.8–3.12
- No external dependencies (stdlib only)

### Installation

```bash
git clone <repo-url>
cd qbd-to-gnucash
```

### Running the Tool

1. Place your `.IIF` file in `input/`
2. Run the converter:
   ```bash
   python main.py
   ```
3. Inspect output:
   - `output/accounts.csv`
   - `output/accounts_mapping_diff.json` (if unmapped types found)
   - `output/qbd-to-gnucash.log` for diagnostics

---

## 🔁 Mapping Workflow

1. Tool reads `baseline` mapping.
2. Applies `specific` overrides (if present).
3. Writes `diff` file for any unmapped QBD account types.
4. User updates `specific` and reruns.

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

---

## 📁 Sample Input

```text
!ACCNT	NAME	ACCNTTYPE	DESC	ACCNUM	HIDDEN
ACCNT	Checking	BANK	Main checking account	1000	N
ACCNT	Accounts Receivable	AR		1100	N
ACCNT	Accounts Payable	AP		2000	N
```

### Output (`accounts.csv`)
```csv
Type,Full Account Name,Account Name,Account Code,...
ASSET,Assets:Current Assets:Bank:Checking,Checking,1000,...
ASSET,Assets:Accounts Receivable,Accounts Receivable,1100,...
LIABILITY,Liabilities:Accounts Payable,Accounts Payable,2000,...
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

---

## ⚙️ Configuration

The following environment variables can override default paths:

| Key                    | Default Path                         |
|------------------------|--------------------------------------|
| `QBD_INPUT_PATH`       | `input/sample-qbd-accounts.IIF`      |
| `GNC_OUTPUT_PATH`      | `output/accounts.csv`                |
| `MAPPING_BASELINE_PATH`| `mappings/account_mapping_baseline.json` |
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

---

## 🧪 Testing (Planned)

- Place test `.IIF` files in `input/`
- Run:  
  ```bash
  python -m unittest discover
  ```
- Test cases will validate malformed files, unmapped types, and tree flattening

---

## 📚 References

- [GnuCash CSV Import Guide](https://www.gnucash.org/viewdoc.phtml?rev=5&lang=C&doc=guide)
- [GnuCash Accounts Hierarchy Docs](https://www.gnucash.org/docs/)

---

## 🧠 Notes on Accounting Types

GnuCash recognizes **five core account types**:

- `ASSET`
- `LIABILITY`
- `EQUITY`
- `INCOME`
- `EXPENSE`

All mappings must ultimately reduce to one of these. `RECEIVABLE` and `PAYABLE` are internal subtypes used only by GnuCash’s business features.

---

## 👥 Authors & Licensing

This project is maintained by internal migration teams seeking vendor lock-in removal.  
Open-source licensing to be determined.
