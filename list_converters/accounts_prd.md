Absolutely — here’s a **Product Requirements Document (PRD)** tailored to your current `accounts.py` script. It reflects its existing logic and outlines structured recommendations for improvement through **normalization, factorization, and logging**.

---

# 📝 Product Requirements Document (PRD)

### Title: QBD → GnuCash Account Conversion Module

**Author**: ChatGPT
**Owner**: \[You]
**Last Updated**: 2025-05-08

---

## 1. Purpose

This script converts a QuickBooks Desktop (QBD) `!ACCNT` IIF export into a GnuCash-compatible `Accounts.csv` file. It performs mapping of account types, reconstructs hierarchical account paths, and generates a structured output suitable for GnuCash CSV import.

---

## 2. Scope

### **Inputs**

* A QBD `.IIF` file containing `!ACCNT` lines.
* A `baseline_mapping.json` file defining default QBD-to-GnuCash account type mappings.
* An optional `specific_mapping.json` file capturing user-defined overrides or unmapped types.

### **Outputs**

* A `Accounts.csv` file containing:

  * `name` (full GnuCash-style account path)
  * `type` (GnuCash account type)
  * `description`

* Optionally updated `specific_mapping.json` with any new unmapped QBD types found during conversion.

---

## 3. Functional Requirements

| Feature                    | Description                                                                                           |
| -------------------------- | ----------------------------------------------------------------------------------------------------- |
| **IIF Parsing**            | Reads `!ACCNT` lines and extracts fields such as name, type, and description.                         |
| **Account Type Mapping**   | Applies `baseline_mapping`, then `specific_mapping`, with fallback to `"UNKNOWN"` for unmapped types. |
| **Hierarchy Construction** | Builds a nested dictionary structure representing account paths (e.g., `Assets:Bank:Checking`).       |
| **Placeholder Promotion**  | Ensures parent accounts created as placeholders are updated if real data later appears.               |
| **CSV Output**             | Produces `Accounts.csv` with full paths and resolved types.                                           |
| **Mapping Feedback Loop**  | Automatically logs and persists any new unmapped QBD types to `specific_mapping.json`.                |

---

## 4. Non-Functional Requirements

* Must not crash on partial/malformed input.
* Should generate logging output for unmapped types, missing files, and structural anomalies.
* Performance should scale to at least thousands of account entries per file.

---

## 5. Assumptions

* Input `.IIF` files are unmodified exports from QBD.
* Only the `!ACCNT` list type is handled in this module.
* Account names are consistently delimited by `:` for hierarchy.

---

## 6. Recommendations for Refactor (Normalization & Factorization)

### 🔧 **1. Break Up `build_gnucash_accounts()`**

Split into focused helper functions:

| Function                                                      | Role                                                     |
| ------------------------------------------------------------- | -------------------------------------------------------- |
| `parse_iif_section(file_path, key, min_fields)`               | Parses `.IIF` data and extracts records by section       |
| `normalize_account_type(qb_type, baseline_map, specific_map)` | Resolves mapping with override support                   |
| `add_account_to_tree(tree, path_parts, account_info)`         | Inserts into nested dict structure, handles placeholders |
| `flatten_account_tree(tree, parent_path="")`                  | Recursively flattens for CSV export                      |

These allow unit testing, reuse, and simplified debugging.

---

### 🪵 **2. Normalize All Logging**

* Replace `print()` calls with `logging.info()` or `logging.warning()`
* Add a standard log format and logging level at the top of the module

Example:

```python
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
```

---

### 🔁 **3. Make Account Mapping Pure**

Encapsulate the mapping logic in a pure function:

```python
def normalize_account_type(qb_type, baseline_map, specific_map) -> str:
    ...
```

This improves testability and allows you to reuse this logic in future converters (e.g., for Vendors or Customers).

---

### 📦 **4. Return Metadata from `convert_accounts()`**

Let the function return a dictionary like:

```python
{
  "total_accounts": 123,
  "unmapped_types": 2,
  "output_path": "Accounts.csv"
}
```

This helps with integration, logging, and future test automation.

---

## 7. Out of Scope

* Other list types (`!CUST`, `!VEND`, etc.)
* Transaction logic (`!TRNS`, `!SPL`)
* CSV validation against GnuCash schema
* GnuCash import automation

---

## 8. Future Enhancements

| Feature                      | Benefit                                    |
| ---------------------------- | ------------------------------------------ |
| `.env` support for paths     | Simplifies config in cross-platform setups |
| Preview/report mode          | Show what would be written before writing  |
| Dry run mode                 | Useful for debugging and verification      |
| Support multiple input files | Improve batch processing flow              |

---

Would you like a full rewrite of `accounts.py` that applies this PRD (specifically the factorization and logging normalization), or would you prefer to start with one section at a time (like `parse_iif_section()`)?
