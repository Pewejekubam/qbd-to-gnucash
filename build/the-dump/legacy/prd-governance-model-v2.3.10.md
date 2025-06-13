# Product Requirements Document — PRD Governance Model

**Document Version:** v2.3.10  
**Module Identifier:** prd-governance-model-v2.3.10.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-05-24  

---

## 1. Scope
This governance model defines mandatory requirements for PRD structure, formatting, versioning, and execution within AI-assisted workflows. All compliance is required. No deviations are permitted.

---

## 2. Structural Rules
### 2.1 Header Format & Structural Integrity
All numbering must be strictly sequential without omissions or interruptions. Each section must increment by exactly one (e.g., `1 → 2 → 3`), and all subsections must follow hierarchical progression (`2.1 → 2.2 → 2.3`). Any deviation—such as skipped numbers or non-contiguous increments—constitutes a structural gap and triggers document invalidation.

To ensure readability and agentic processing compatibility, all section headers must conform to structured hierarchical formatting. This guarantees **consistent collapsibility in IDEs and structured parsing for AI-driven enforcement**.

**Formatting Enforcement Rules:**
- **Header Formatting**: Major sections must follow the `## <n>. <Title>` format, with nested subsections incrementing hierarchically (`### 2.1 → #### 2.1.1 → ##### 2.1.1.1`).
- **Sequential Structure**: No arbitrary numbering jumps, omissions, or renumbering inconsistencies.
- **IDE Compatibility**: Hierarchical formatting must support collapsibility and logical readability in structured development environments.
- **Agentic Processing Compliance**: AI-driven validation must process numbering rules without needing manual adjustments.

Documents failing to conform to these structural integrity requirements **must** be rejected or corrected before further processing.

### 2.2 Semantic Stability
Section headers are immutable. No renaming, paraphrasing, or semantic alterations are permitted. All internal references must automatically update to match any structural change.

### 2.3 Major Section Separation Rule
All major top-level sections (`## <n>. <Title>`) must be preceded and followed by a horizontal rule line (`---`) to ensure unambiguous parsing.

The horizontal rule (`---`) must not be used elsewhere in the document (e.g., within subsections or for thematic breaks). Any occurrence of `---` outside major section boundaries constitutes a governance violation and triggers PRD invalidation.

This rule guarantees consistent section delimitation for both human readability and agentic processing.

---

## 3. Domain Index Protocol
The **Governance Document (GD)** maintains an authoritative registry of valid QuickBooks data domains, ensuring standardization across all PRD structures. This registry serves as the **single source of truth** for domain naming. All references to "domain", "<domain>", or similar notation within this document shall be interpreted exclusively according to this registry.

#### 3.1 Domain Registration & Constraints
- Every **recognized domain** must be formally indexed within the GD.
- Domains **must use snake_case** to ensure machine readability.
- **No other naming conventions exist.** This section represents the exclusive naming authority.

#### 3.2 Authoritative Domain Index
```
accounts
customers
vendors
items
sales_tax
job_types
classes
price_levels
customer_types
vendor_types
payment_terms
payment_methods
shipping_methods
sales_reps
messages
employees
budgets
to_do
other_names
```

---

## 4. Formatting Protocols
### 4.1 Markdown Enforcement
Only Markdown is permitted. No embedded HTML, LaTeX, or rich text formatting is allowed.

### 4.2 Canonical Syntax
All code blocks, lists, and indentation must remain in canonical syntax without modification. No summaries, examples, or commentary may be introduced unless explicitly required by protocol.

---

## 5. Versioning Enforcement
### 5.1 Version Declaration
- Every PRD must declare a version `vX.Y.Z` in both the filename and document metadata.

### 5.2 Semantic Versioning Rules
- `X` must be incremented for backward-incompatible changes.
- `Y` must be incremented for additive or backward-compatible changes.
- `Z` must be incremented for patch-level changes, such as bug fixes or documentation updates.
- Version increments must follow these rules strictly; non-compliant documents must be rejected.

### 5.3 Changelog Protocol
#### **Versioning Update Requirements**
- Every PRD **must** contain a revision history table.
- Each **new version** update **must** correspond to a **new row**—overwriting existing entries is **strictly prohibited**.
- The revision history table **must** have the following columns in this exact order:
  - `Version` — Semantic version identifier (`vX.Y.Z`)
  - `Date` — ISO 8601 (`YYYY-MM-DD`)
  - `Author` — Contributor’s initials or name
  - `Summary` — Brief description of changes
- The revision history table **must** be presented in **plain-text Markdown** with pipe (`|`) delimiters.
- Missing or malformed version history **must** trigger document rejection.

#### **Revision Entry Constraints**
- **Append-only structure** → No deletion or modification of existing rows.
- **Strict chronological order** → New entries **must** be added to the **bottom** of the table.
- **Consistent formatting enforcement** → Each column **must** conform to its expected data type.

#### **Mandatory Table Format**
| Version | Date       | Author | Summary                                                |
|---------|------------|--------|--------------------------------------------------------|
| 1.0.0   | 2025-05-19 | —      | Initial release. Centralized logging extracted.|
| 1.0.1   | 2025-05-19 | —      | Function signature cleanup and clarification.|
| 1.0.2   | 2025-05-19 | —      | Added typing for log structures and extended examples.|
| 1.0.3   | 2025-05-21 | PJ     | Full processing through PRD template v3.5.1.|
| 1.0.4   | 2025-05-21 | PJ     | Full processing through PRD template v3.5.1 after minor edits.|

### 5.4 Naming & Location Protocol
All PRDs must conform to strict structural and naming rules to enable deterministic agentic execution.

#### 5.4.1 Directory Location Rules
- All PRDs must reside under a root directory named `prd/`.
- Core PRDs must reside in: `prd/`
- Governance PRD must reside in: `prd/`
- Module PRDs must reside in: `prd/<domain>/` where `<domain>` is a valid domain name as defined in Section 3 (Domain Index Protocol).
- No PRD may exist outside the `prd/` directory tree.
- All README files must reside alongside their corresponding PRDs.

#### 5.4.2 Filename Format Rules
All PRD filenames must conform to the following format:
```
<type>-prd-<domain>[_<tag>]-v<MAJOR>.<MINOR>.<PATCH>.md
```
Where:
- `<type>` is one of: `module`, `core`, `governance`
- `<domain>` is a valid domain name as defined in Section 3 (Domain Index Protocol)
- `<tag>` is optional, must be lowercase and snake_case (e.g., `accounts_mapping`)
- `<MAJOR>.<MINOR>.<PATCH>` follows strict [semantic versioning](#52-semantic-versioning-rules)

#### 5.4.3 Validation Rules
- The `<domain>` component of the filename must match a valid domain name in Section 3 (Domain Index Protocol).
- The `<domain>` must match the name of the immediate parent folder.
- The optional `<tag>`, if present, must not conflict with any other domain folder name.
- Version components (`MAJOR`, `MINOR`, `PATCH`) are **mandatory** and must be integers ≥ 0.
- Filenames must match the declared version in the `## 1. Metadata` block exactly.

#### 5.4.4 Resolution Model
- **Link Resolution**: All relative links within PRDs must be resolved from the `prd/` directory root.
- **Path Inference**: Agents must not attempt path inference or resolution correction; all paths must be explicitly defined.
- **Invalidation**: Any deviation from the specified link resolution model will result in structural invalidation of the document.

#### 5.4.5 Tag Usage & Compliance
- A PRD filename **without a `<tag>`** represents the **core definition** of its `<domain>`. Tagged variants are considered **extensions or submodules**.
- Tags are validated against **indexed domain names** to prevent unintended classification errors.
- No additional constraints on `<tag>` uniqueness beyond existing filename uniqueness checks.

#### 5.4.6 Examples
**✅ Valid Filenames:**
- `module-prd-accounts-v1.1.2.md` → in `prd/accounts/`
- `module-prd-accounts_mapping-v1.0.7.md` → in `prd/accounts/`
- `module-prd-logging-v1.0.4.md` → in `prd/logging/`
- `core-prd-v3.6.4.md` → in `prd/`

**❌ Invalid Filenames & Violations:**
- `accounts-module-prd-v1.1.md` → (wrong order, missing patch version)
- `module-prd-vendors-v1.0.md` → (in wrong directory if not under `prd/vendors/`)
- `prd-module-logging-v1.0.0.md` → (non-compliant prefix)
- `module-prd-Logging-v1.0.0.md` → (invalid capitalization)
- `module_prd-accounts-v1.2.0.md` → (wrong delimiter: `_` instead of `-`)

---

## 6. Update Discipline
### 6.1 Targeted Edits
Edits must strictly modify the targeted logic. Collateral adjustments are prohibited.

### 6.2 Ordered Insertion
Insertions must occur at precisely the correct semantic location.

### 6.3 Renumbering Consistency
Renumbering must occur coherently across all affected sections in a single correction pass.

---

## 7. Modular PRD Definition
### 7.1 Domain Boundaries
Each module PRD is associated with a recognized domain, as defined by the authoritative Domain Index Protocol (see Section 3). Domains exist exclusively within this indexed registry. No inferred or constructed domain definitions are permitted.

Module PRDs reside in their respective indexed domain directories (`prd/<domain>/`). All domain associations, naming, and structural validation are governed by the Domain Index Protocol.

### 7.2 Version Locking
Modules must declare their compatible core PRD version explicitly. Domain-specific logic must not reside within the core PRD.

### 7.3 Abstraction Criteria
Any shared behavior must be universally applicable before being abstracted.

---

## 8. Inter-PRD Dependencies
### 8.1 Relative Linking
All module references must use relative paths and canonical anchor links.

### 8.2 Reference Validation
Invalid references must trigger rejection—no silent failures. Cross-version references require explicit version-lock enforcement.

---

## 9. AI Agent Compliance
### 9.1 Execution Guarantee
PRDs must be executable by autonomous agents without transformation.

### 9.2 Interface Definitions
Acceptable formats: TypedDict, JSON Schema, strict enumerations.

### 9.3 Exception & Exit Contracts
Exception types, exit codes, and validation suites must be explicitly defined.

### 9.4 Logging Constraints
Logging must be deterministic and flush-safe. No heuristic assumptions are allowed.

---

## 10. Governance Authority
### 10.1 Precedence Order
This protocol overrides all prior formatting practices, inline notes, and AI model heuristics. Precedence follows: governance > core PRD > module PRD.

### 10.2 Revision Rules
No agent or human may override governance without a formally published revision.

---

## 11. Compliance Enforcement
### 11.1 Agent Affirmation
AI agents must affirm this governance before making structural edits.

### 11.2 Human Validation
Human contributors must pass protocol validation before submitting or merging changes.

### 11.3 Invalidation Triggers
All violations trigger PRD invalidation. Affected versions must not be processed.

---

## 12. Numbering Example
## 1. Scope
## 2. Structural Rules
### 2.1 Header Format
### 2.2 Semantic Stability
### 2.3 Major Section Separation Rule
## 3. Domain Index Protocol
## 4. Formatting Protocols
## 5. Versioning Enforcement
## 6. Update Discipline
## 7. Modular PRD Definition
## 8. Inter-PRD Dependencies
## 9. AI Agent Compliance
## 10. Governance Authority
## 11. Compliance Enforcement
## 12. Numbering Example
