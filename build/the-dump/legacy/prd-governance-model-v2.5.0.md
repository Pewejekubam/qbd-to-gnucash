# Product Requirements Document — PRD Governance Model

**Document Version:** v2.5.0  
**Module Identifier:** prd-governance-model-v2.5.0.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-06-10  

---

## 1. Scope
This governance model defines mandatory requirements for PRD structure, formatting, versioning, and execution within AI-assisted workflows. Compliance with this governance model is mandatory.

---

## 2. Structural Rules
### 2.1 Header Format & Structural Integrity
All numbering shall be strictly sequential without omissions or interruptions. Each section shall increment by exactly one (e.g., `1 → 2 → 3`), and all subsections shall follow hierarchical progression (`2.1 → 2.2 → 2.3`). Any deviation—such as skipped numbers or non-contiguous increments—constitutes a structural gap and triggers document invalidation.

To ensure readability and agentic processing compatibility, all section headers shall conform to structured hierarchical formatting. This guarantees **consistent collapsibility in IDEs and structured parsing for AI-driven enforcement**.

**Formatting Enforcement Rules:**
- **Header Formatting**: Major sections shall follow the `## <n>. <Title>` format, with nested subsections incrementing hierarchically (`### 2.1 → #### 2.1.1 → ##### 2.1.1.1`).
- **Sequential Structure**: No arbitrary numbering jumps, omissions, or renumbering inconsistencies.
- **IDE Compatibility**: Hierarchical formatting shall support collapsibility and logical readability in structured development environments.
- **Agentic Processing Compliance**: AI-driven validation shall process numbering rules without needing manual adjustments.

Documents failing to conform to these structural integrity requirements **shall** be rejected or corrected before further processing.

### 2.2 Semantic Stability
Section headers are immutable. No renaming, paraphrasing, or semantic alterations are permitted. All internal references shall automatically update to match any structural change.

### 2.3 Major Section Separation Rule
All major top-level sections (`## <n>. <Title>`) shall be preceded and followed by a horizontal rule line (`---`) to ensure unambiguous parsing.

The horizontal rule (`---`) shall not be used elsewhere in the document (e.g., within subsections or for thematic breaks). Any occurrence of `---` outside major section boundaries constitutes a governance violation and triggers PRD invalidation.

This rule guarantees consistent section delimitation for both human readability and agentic processing.

---

## 3. Domain Index Protocol
The **Governance Document (GD)** maintains an authoritative registry of valid QuickBooks data domains, ensuring standardization across all PRD structures. This registry serves as the **single source of truth** for domain naming. All references to "domain", "<domain>", or similar notation within this document shall be interpreted exclusively according to this registry.

#### 3.1 Domain Registration & Constraints
- Every **recognized domain** shall be formally indexed within the GD.
- Domains **shall use snake_case** to ensure machine readability.
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
All code blocks, lists, and indentation shall remain in canonical syntax without modification. No summaries, examples, or commentary may be introduced unless explicitly required by protocol.

---

## 5. Versioning Enforcement
### 5.1 Version Declaration
- Every PRD shall declare a version `vX.Y.Z` in both the filename and document metadata.

### 5.2 Semantic Versioning Rules
- `X` shall be incremented for backward-incompatible changes.
- `Y` shall be incremented for additive or backward-compatible changes.
- `Z` shall be incremented for patch-level changes, such as bug fixes or documentation updates.
- Version increments shall follow these rules strictly; non-compliant documents shall be rejected.

### 5.3 Changelog Protocol
#### **Versioning Update Requirements**
- Every PRD **shall** contain a revision history table.
- Each **new version** update **shall** correspond to a **new row**—overwriting existing entries is **strictly prohibited**.
- The revision history table **shall** have the following columns in this exact order:
  - `Version` — Semantic version identifier (`vX.Y.Z`)
  - `Date` — ISO 8601 (`YYYY-MM-DD`)
  - `Author` — Contributor's initials or name
  - `Summary` — Brief description of changes
- The revision history table **shall** be presented in **plain-text Markdown** with pipe (`|`) delimiters.
- Missing or malformed version history **shall** trigger document rejection.

#### **Revision Entry Constraints**
- **Append-only structure** → No deletion or modification of existing rows.
- **Strict chronological order** → New entries **shall** be added to the **bottom** of the table.
- **Consistent formatting enforcement** → Each column **shall** conform to its expected data type.

#### **Mandatory Table Format**
| Version | Date       | Author | Summary                                                |
|---------|------------|--------|--------------------------------------------------------|
| 1.0.0   | 2025-05-19 | —      | Initial release. Centralized logging extracted.|
| 1.0.1   | 2025-05-19 | —      | Function signature cleanup and clarification.|
| 1.0.2   | 2025-05-19 | —      | Added typing for log structures and extended examples.|
| 1.0.3   | 2025-05-21 | PJ     | Full processing through PRD template v3.5.1.|
| 1.0.4   | 2025-05-21 | PJ     | Full processing through PRD template v3.5.1 after minor edits.|

### 5.4 Naming & Location Protocol
All PRDs shall conform to strict structural and naming rules to enable deterministic agentic execution.

#### 5.4.1 Directory Location Rules
- All PRDs shall reside under a root directory named `prd/`.
- Core PRDs shall reside in: `prd/`
- Governance PRD shall reside in: `prd/`
- Module PRDs shall reside in: `prd/<domain>/` where `<domain>` is a valid domain name as defined in Section 3 (Domain Index Protocol).
- No PRD may exist outside the `prd/` directory tree.
- All README files shall reside alongside their corresponding PRDs.

#### 5.4.2 Filename Format Rules
All PRD filenames shall conform to the following format:
```
<type>-prd-<domain>[_<tag>]-v<MAJOR>.<MINOR>.<PATCH>.md
```
Where:
- `<type>` is one of: `module`, `core`, `governance`
- `<domain>` is a valid domain name as defined in Section 3 (Domain Index Protocol)
- `<tag>` is optional, shall be lowercase and snake_case (e.g., `accounts_mapping`)
- `<MAJOR>.<MINOR>.<PATCH>` follows strict [semantic versioning](#52-semantic-versioning-rules)

#### 5.4.3 Validation Rules
- The `<domain>` component of the filename shall match a valid domain name in Section 3 (Domain Index Protocol).
- The `<domain>` shall match the name of the immediate parent folder.
- The optional `<tag>`, if present, shall not conflict with any other domain folder name.
- Version components (`MAJOR`, `MINOR`, `PATCH`) are **mandatory** and shall be integers ≥ 0.
- Filenames shall match the declared version in the `## 1. Metadata` block exactly.

#### 5.4.4 Resolution Model
- **Link Resolution**: All relative links within PRDs shall be resolved from the `prd/` directory root.
- **Path Inference**: Agents shall not attempt path inference or resolution correction; all paths shall be explicitly defined.
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
Edits shall strictly modify the targeted logic. Collateral adjustments are prohibited.

### 6.2 Ordered Insertion
Insertions shall occur at precisely the correct semantic location.

### 6.3 Renumbering Consistency
Renumbering shall occur coherently across all affected sections in a single correction pass.

---

## 7. Modular PRD Definition
### 7.1 Domain Boundaries
Each module PRD is associated with a recognized domain, as defined by the authoritative Domain Index Protocol (see Section 3). Domains exist exclusively within this indexed registry. No inferred or constructed domain definitions are permitted.

Module PRDs reside in their respective indexed domain directories (`prd/<domain>/`). All domain associations, naming, and structural validation are governed by the Domain Index Protocol.

### 7.2 Version Locking
Modules shall declare their compatible core PRD version explicitly. Domain-specific logic shall not reside within the core PRD.

### 7.3 Abstraction Criteria
Any shared behavior shall be universally applicable before being abstracted.

---

## 8. PRD Reference and Linking Standards
### 8.1 Path Resolution Rules
- All relative links shall resolve from the `prd/` directory root
- No path inference or correction is permitted
- All paths shall be explicitly defined

### 8.2 Inter-PRD Linking Format
- Format: `[Document vX.Y.Z Section N: Description](relative-path-from-prd-root)`
- Version specification mandatory in both link text and filename
- Anchor links shall use canonical section numbering

**✅ Correct Inter-PRD Examples:**
- `[Core PRD v3.6.5 Section 16: Error Classes](../core-prd-main-v3.6.5.md#16-authoritative-error-classes--error-code-table)`
- `[Logging Framework PRD v1.0.4 Section 5: Interface](../logging/module-prd-logging-v1.0.4.md#5-interface--integration)`

**❌ Incorrect Inter-PRD Examples:**
- `[Section 16: Error Classes](../core-prd-main-v3.6.5.md#16-authoritative-error-classes--error-code-table)` *(missing document qualification)*
- `[Core PRD](core-prd-main.md)` *(missing version, wrong path)*

### 8.3 Intra-PRD Linking Format
- Format: `[Section X.Y: Description](#xy-section-title-kebab-case)`
- All internal references shall link to numbered sections
- No vague references permitted

**✅ Correct Intra-PRD Examples:**
- `[Section 7.1.1: Domain Module Naming](#711-domain-module-naming-and-containment-rules)`
- `[Domain Index Protocol](#3-domain-index-protocol)`

**❌ Incorrect Intra-PRD Examples:**
- `[Section 7.1.1](#domain-module-naming)` *(incorrect anchor format)*
- `See Section 7.1.1` *(no link)*

### 8.4 Reference Validation
Invalid references shall trigger rejection—no silent failures. Cross-version references require explicit version-lock enforcement. See Section 14.1 for complete cross-document validation requirements.

---

## 9. AI Agent Compliance and Quality Assurance
### 9.1 Execution Guarantee
PRDs shall be executable by autonomous agents without transformation.

### 9.2 Agent Processing Requirements
All PRD specifications shall be deterministic and unambiguous for agentic processing. Implementation-specific requirements (interface definitions, exception contracts, logging constraints) are defined in the Core PRD.

### 9.3 Specification Completeness Requirements
All PRDs shall meet minimum completeness standards:
- **Interface Specifications**: Complete function signatures with types and exceptions
- **Error Handling**: All error conditions documented with appropriate error codes
- **Example Usage**: Realistic examples for all public interfaces

### 9.4 Specification Accuracy Validation
- **Implementation Alignment**: PRD specifications shall reflect actual implementation requirements
- **Feasibility Review**: All specified requirements shall be technically achievable
- **Consistency Verification**: Specifications shall not contain internal contradictions

### 9.5 Documentation Quality Standards
- **Clarity**: All specifications shall be unambiguous and implementable by autonomous agents
- **Completeness**: No critical implementation details may be omitted from specifications
- **Maintenance**: PRDs shall be updated when implementation requirements change

---

## 10. Governance Authority
### 10.1 Precedence Order
This protocol overrides all prior formatting practices, inline notes, and AI model heuristics. For specification conflicts, see Section 13 for detailed authority hierarchy and resolution procedures.

### 10.2 Revision Rules
No agent or human may override governance without a formally published revision.

---

## 11. Compliance Enforcement
### 11.1 Agent Affirmation
AI agents shall affirm this governance before making structural edits.

### 11.2 Human Validation
Human contributors shall pass protocol validation before submitting or merging changes.

### 11.3 Invalidation Triggers
All violations shall trigger PRD invalidation and document rejection. Affected versions shall not be processed.

---

## 12. Structural Numbering Standards
### 12.1 Section Numbering Rules
- Top-level sections shall use format: `## <n>. <Title>`
- Subsections shall use hierarchical numbering: `### <n>.<m> <Title>`
- Sub-subsections shall continue pattern: `#### <n>.<m>.<p> <Title>`

### 12.2 Numbering Sequence Requirements
- All section numbers shall be sequential without gaps
- No skipping of numbers (e.g., 1, 2, 4 is invalid)
- No duplicate numbering within the same hierarchical level

### 12.3 Cross-Reference Format
- Internal references shall use full section numbering: `Section <n>.<m>`
- Anchor links shall match section numbers exactly: `#<n><m>-title-in-kebab-case`

---

## 13. Interface Authority Precedence Rules

### 13.1 Authority Hierarchy
When PRD specifications conflict across documents, resolution follows this precedence:
- **Governance Document**: Structural rules, versioning, and PRD format requirements (highest authority)
- **Core PRD**: Cross-module architectural patterns and shared interface contracts
- **Module PRD**: Domain-specific implementation specifications (shall comply with above)

### 13.2 Specification Conflict Resolution
- **Detection**: PRD updates shall be validated for conflicts before acceptance
- **Resolution Process**: Lower-precedence documents shall be updated to align with higher-precedence specifications
- **Documentation**: All authorized deviations shall be explicitly documented with rationale

### 13.3 Change Propagation Rules
- Changes to Governance Document trigger review of all PRDs for compliance
- Changes to Core PRD architectural patterns require Module PRD alignment verification
- Module PRD changes affecting shared interfaces require Core PRD review

---

## 14. Specification Consistency Requirements

### 14.1 Cross-Document Validation
PRDs shall maintain consistency across documents to prevent specification conflicts:
- **Reference Integrity**: All cross-references between PRDs shall resolve to valid sections (see Section 8 for linking standards)
- **Terminology Consistency**: Shared terms shall have consistent definitions across all PRDs

### 14.2 Enforcement Discipline
- **Pre-Acceptance Validation**: All PRD updates shall pass consistency checks before acceptance
- **Violation Response**: Conflicting specifications trigger immediate governance review and document rejection
- **Resolution Timeline**: Specification conflicts shall be resolved within current version cycle

### 14.3 Change Control Framework
- **Impact Assessment**: PRD changes shall document potential impacts on other PRDs
- **Notification Process**: Changes affecting shared specifications require notification to dependent PRD owners
- **Version Coordination**: Related PRD updates should be synchronized when possible

---

## 15. Revision History

| Version | Date       | Author | Summary                                                |
|---------|------------|--------|--------------------------------------------------------|
| 2.3.10  | 2025-05-24 | PJ     | Previous version with domain index and structural rules |
| 2.4.0   | 2025-06-10 | PJ     | Added Interface Authority Precedence Rules, Specification Consistency Requirements, and Module Entry Point Standards per CR-2025-002 |
| 2.4.1   | 2025-06-10 | PJ     | Standardized "shall" language, merged quality assurance into agent compliance, enhanced linking standards with full qualification requirements, refined structural numbering standards |