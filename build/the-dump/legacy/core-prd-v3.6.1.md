<!-- filepath: c:\git-root\qbd-to-gnucash\prd\core-prd-v3.6.1.md -->
# Core PRD: QuickBooks Desktop to GnuCash Conversion Tool

**Document Version:** v3.6.1  
**State:** Under Review / Workflow Discrepancy  
**Author:** Pewe Jekubam

---

## 1. Scope
This project delivers a modular, command-line conversion tool for migrating financial data from QuickBooks Desktop (QBD) into GnuCash using structured import files. The core framework applies a consistent, extensible processing pipeline—centralized input ingestion and parsing, followed by dispatching well-defined payloads to domain modules for mapping and output generation—which is reused across all modules. Each domain module (e.g., Accounts, Vendors, Transactions, and others) is responsible for converting its respective QBD data as received from the dispatcher into GnuCash-compatible formats, as defined in its own PRD. The core PRD defines the shared architecture, orchestration, and extension points for all modules.

This project is CLI-only; no graphical user interface or CLI arguments will be developed or supported.

### 1.1 Target Audience
This tool is intended for technical users — accountants, bookkeepers, or developers — performing structured financial data migration from QBD to GnuCash. Familiarity with the principles of double-entry accounting and GnuCash's account-type model is strongly recommended.

---

## 2. Structural Rules
// ...insert content per governance model v2.3.10, e.g., header format, sequential structure, etc....
---

## 3. Background Context
QuickBooks Desktop is a proprietary platform, and many users are migrating to open-source accounting systems for reasons including cost, longevity, and transparency. However, the lack of compatible conversion tooling presents a serious barrier. This project exists to fill that gap, enabling clean migration of core data without data loss or manual recreation.

---

## 4. Formatting Protocols
// ...insert content per governance model v2.3.10, e.g., Markdown enforcement, canonical syntax, etc....
---

## 5. Versioning Enforcement
### 5.1 Revision History
| Version | Date       | Author | Summary                                                |
|---------|------------|--------|--------------------------------------------------------|
| 3.6.1   | 2025-05-25 | PJ     | Reorganized for full compliance with governance v2.3.10 |
| 3.6.0   | 2025-05-24 | PJ     | Corrected domain module naming                         |
| 3.5.1   | 2025-05-23 | PJ     | Remediated governance audit violations                 |
| 3.5.0   | 2025-05-22 | PJ     | Finalized full extraction and compliance               |
| 3.4.1   | 2025-05-21 | PJ     | Split module logic into dedicated files                |
| 3.4.0   | 2025-05-20 | PJ     | Added explicit JSON Schema and Python typing examples  |
| 3.3.1   | 2025-05-19 | PJ     | Standardized terminology for mapping diff file         |
| 3.1.0   | 2025-05-18 | PJ     | Mandated explicit function signatures                  |
| 3.0.1   | 2025-05-17 | PJ     | Minor clarifications and error handling improvements   |
| 3.0.0   | 2025-05-16 | PJ     | Core PRD established as root of modular PRD system     |
| 2.7.3   | 2025-05-15 | PJ     | Final monolithic PRD before modularization             |

---

## 6. Update Discipline
// ...insert content per governance model v2.3.10, e.g., targeted edits, ordered insertion, renumbering consistency....
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
// ...insert content per governance model v2.3.10, e.g., relative linking, reference validation....
---

## 9. AI Agent Compliance
// ...insert content per governance model v2.3.10, e.g., execution guarantee, interface definitions, exception & exit contracts, logging constraints....
