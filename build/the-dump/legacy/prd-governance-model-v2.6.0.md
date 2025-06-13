# Product Requirements Document — PRD Governance Model

**Document Version:** v2.6.0  
**Module Identifier:** prd-governance-model-v2.6.0.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-06-10  

---

## 1. Scope
This governance model defines mandatory requirements for PRD structure, formatting, versioning, and execution within AI-assisted workflows. Compliance with this governance model is mandatory.

---

## 2. Structural Rules and Document Standards
### 2.1 Header Format & Structural Integrity
All numbering shall be strictly sequential without omissions or interruptions. Each section shall increment by exactly one (e.g., `1 → 2 → 3`), and all subsections shall follow hierarchical progression (`2.1 → 2.2 → 2.3`). Any deviation—such as skipped numbers or non-contiguous increments—constitutes a structural gap and triggers document invalidation.

**Section Numbering Requirements**
- Top-level sections shall use format: `## <n>. <Title>`
- Subsections shall use hierarchical numbering: `### <n>.<m> <Title>`
- Sub-subsections shall continue pattern: `#### <n>.<m>.<p> <Title>`
- All section numbers shall be sequential without gaps
- Cross-references shall use full section numbering: `Section <n>.<m>`

**Formatting Enforcement Rules**
- **Header Formatting**: Major sections shall follow the `## <n>. <Title>` format, with nested subsections incrementing hierarchically
- **Sequential Structure**: No arbitrary numbering jumps, omissions, or renumbering inconsistencies
- **IDE Compatibility**: Hierarchical formatting shall support collapsibility and logical readability in structured development environments
- **Agentic Processing Compliance**: AI-driven validation shall process numbering rules without needing manual adjustments

### 2.2 Semantic Stability
Section headers are immutable. No renaming, paraphrasing, or semantic alterations are permitted. All internal references shall automatically update to match any structural change.

### 2.3 Major Section Separation Rule
All major top-level sections (`## <n>. <Title>`) shall be preceded and followed by a horizontal rule line (`---`) to ensure unambiguous parsing. The horizontal rule (`---`) shall not be used elsewhere in the document.

### 2.4 Formatting Protocols
Only Markdown is permitted. No embedded HTML, LaTeX, or rich text formatting is allowed. All code blocks, lists, and indentation shall remain in canonical syntax without modification.

### 2.5 Documentation Quality Standards
- **Clarity**: All specifications shall be unambiguous and implementable by autonomous agents
- **Completeness**: No critical implementation details may be omitted from specifications
- **Specification Accuracy**: PRD specifications shall reflect actual implementation requirements
- **Consistency**: Specifications shall not contain internal contradictions

Documents failing to conform to these structural integrity requirements **shall** be rejected or corrected before further processing.

---

## 3. Domain Index Protocol
The **Governance Document (GD)** maintains an authoritative registry of valid QuickBooks data domains, ensuring standardization across all PRD structures. This registry serves as the **single source of truth** for domain naming.

### 3.1 Domain Registration & Constraints
- Every **recognized domain** shall be formally indexed within the GD
- Domains **shall use snake_case** to ensure machine readability
- **No other naming conventions exist.** This section represents the exclusive naming authority

### 3.2 Authoritative Domain Index
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

## 4. Versioning and Change Control
### 4.1 Version Declaration
Every PRD shall declare a version `vX.Y.Z` in both the filename and document metadata.

### 4.2 Semantic Versioning Rules
- `X` shall be incremented for backward-incompatible changes
- `Y` shall be incremented for additive or backward-compatible changes
- `Z` shall be incremented for patch-level changes, such as bug fixes or documentation updates
- Version increments shall follow these rules strictly; non-compliant documents shall be rejected

### 4.3 Revision History Requirements
- Every PRD **shall** contain a revision history table
- Each **new version** update **shall** correspond to a **new row**—overwriting existing entries is **strictly prohibited**
- **Append-only structure** → No deletion or modification of existing rows
- **Strict chronological order** → New entries **shall** be added to the **bottom** of the table
- The revision history table **shall** have the following columns in this exact order:
  - `Version` — Semantic version identifier (`vX.Y.Z`)
  - `Date` — ISO 8601 (`YYYY-MM-DD`)
  - `Author` — Contributor's initials or name
  - `Summary` — Brief description of changes
- Missing or malformed version history **shall** trigger document rejection

### 4.4 Naming & Location Protocol
All PRDs shall conform to strict structural and naming rules to enable deterministic agentic execution.

#### 4.4.1 Directory Location Rules
- All PRDs shall reside under a root directory named `prd/`
- Core PRDs shall reside in: `prd/`
- Governance PRD shall reside in: `prd/`
- Module PRDs shall reside in: `prd/<domain>/` where `<domain>` is a valid domain name as defined in Section 3
- No PRD may exist outside the `prd/` directory tree

#### 4.4.2 Filename Format Rules
All PRD filenames shall conform to the following format:
```
<type>-prd-<domain>[_<tag>]-v<MAJOR>.<MINOR>.<PATCH>.md
```
Where:
- `<type>` is one of: `module`, `core`, `governance`
- `<domain>` is a valid domain name as defined in Section 3 (Domain Index Protocol)
- `<tag>` is optional, shall be lowercase and snake_case (e.g., `accounts_mapping`)
- `<MAJOR>.<MINOR>.<PATCH>` follows strict semantic versioning rules

#### 4.4.3 Validation Rules
- The `<domain>` component of the filename shall match a valid domain name in Section 3
- The `<domain>` shall match the name of the immediate parent folder
- Version components (`MAJOR`, `MINOR`, `PATCH`) are **mandatory** and shall be integers ≥ 0
- Filenames shall match the declared version in the document metadata exactly

---

## 5. PRD Reference and Linking Standards
### 5.1 Path Resolution Rules
- All relative links shall resolve from the `prd/` directory root
- No path inference or correction is permitted
- All paths shall be explicitly defined

### 5.2 Inter-PRD Linking Format
- Format: `[Document vX.Y.Z Section N: Description](relative-path-from-prd-root)`
- Version specification mandatory in both link text and filename
- Anchor links shall use canonical section numbering

**✅ Correct Inter-PRD Examples:**
- `[Core PRD v3.7.0 Section 16: Error Classes](../core-prd-main-v3.7.0.md#16-authoritative-error-classes--error-code-table)`
- `[Logging Framework PRD v1.0.4 Section 5: Interface](../logging/module-prd-logging-v1.0.4.md#5-interface--integration)`

**❌ Incorrect Inter-PRD Examples:**
- `[Section 16: Error Classes](../core-prd-main-v3.7.0.md#16-authoritative-error-classes--error-code-table)` *(missing document qualification)*
- `[Core PRD](core-prd-main.md)` *(missing version, wrong path)*

### 5.3 Intra-PRD Linking Format
- Format: `[Section X.Y: Description](#xy-section-title-kebab-case)`
- All internal references shall link to numbered sections
- No vague references permitted

**✅ Correct Intra-PRD Examples:**
- `[Section 7.1.1: Domain Module Naming](#711-domain-module-naming-and-containment-rules)`
- `[Domain Index Protocol](#3-domain-index-protocol)`

**❌ Incorrect Intra-PRD Examples:**
- `[Section 7.1.1](#domain-module-naming)` *(incorrect anchor format)*
- `See Section 7.1.1` *(no link)*

### 5.4 Reference Validation
Invalid references shall trigger rejection—no silent failures. Cross-version references require explicit version-lock enforcement.

---

## 6. Modular PRD Definition
### 6.1 Domain Boundaries
Each module PRD is associated with a recognized domain, as defined by the authoritative Domain Index Protocol (see Section 3). Domains exist exclusively within this indexed registry. No inferred or constructed domain definitions are permitted.

### 6.2 Version Locking
Modules shall declare their compatible core PRD version explicitly. Domain-specific logic shall not reside within the core PRD.

### 6.3 Abstraction Criteria
Any shared behavior shall be universally applicable before being abstracted.

---

## 7. AI Agent Compliance
### 7.1 Execution Guarantee
PRDs shall be executable by autonomous agents without transformation.

### 7.2 Deterministic Requirements
All PRD specifications shall be deterministic and unambiguous for agentic processing. Implementation-specific requirements (interface definitions, exception contracts, logging constraints) are defined in the Core PRD.

### 7.3 Interface Completeness Standards
All PRDs shall meet minimum completeness standards:
- **Interface Specifications**: Complete function signatures with types and exceptions
- **Error Handling**: All error conditions documented with appropriate error codes
- **Example Usage**: Realistic examples for all public interfaces

---

## 8. Governance Authority
### 8.1 Precedence Order
This protocol overrides all prior formatting practices, inline notes, and AI model heuristics. Precedence hierarchy: Governance Document > Core PRD > Module PRD.

### 8.2 Revision Rules
No agent or human may override governance without a formally published revision.

---

## 9. Compliance Enforcement
### 9.1 Agent Affirmation
AI agents shall affirm this governance before making structural edits.

### 9.2 Human Validation
Human contributors shall pass protocol validation before submitting or merging changes.

### 9.3 Invalidation Triggers
All violations shall trigger PRD invalidation and document rejection. Affected versions shall not be processed.

---

## 10. Revision History

| Version | Date       | Author | Summary |
|---------|------------|--------|---------|
| 2.3.10  | 2025-05-24 | PJ     | Previous version with domain index and structural rules |
| 2.4.0   | 2025-06-10 | PJ     | Added Interface Authority Precedence Rules, Specification Consistency Requirements, and Module Entry Point Standards per CR-2025-002 |
| 2.4.1   | 2025-06-10 | PJ     | Standardized "shall" language, merged quality assurance into agent compliance, enhanced linking standards with full qualification requirements, refined structural numbering standards |
| 2.5.0   | 2025-06-10 | PJ     | Manual edit increment per development team decision |
| 2.6.0   | 2025-06-10 | PJ     | Agentic streamlining: eliminated redundant sections, consolidated overlapping content, removed meta-commentary for pure operational focus |