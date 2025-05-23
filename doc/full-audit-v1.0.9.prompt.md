# 📋 Audit Prompt

You are tasked with performing a **deep, section-by-section governance compliance audit** on all Product Requirements Documents (PRDs) and module READMEs located in the `./prd/` directory of this project.

---

## 📌 Objective

Your job is to **identify and annotate all violations** of the **PRD Governance Model v1.0.0**, including but not limited to:

- Section misnumbering, mislabeling, or breaks in heading continuity
- Violations of separation-of-concerns (e.g., module-specific content in the core PRD)
- Incorrect placement of logic, implementation detail, or roadmap speculation
- Missing or malformed structural sections (e.g., missing 3.2 Scope, 6.1 Directory Layout)
- Typos, formatting errors, or indentation/spacing violations that disrupt legibility or machine readability
- Governance section references that do not resolve or no longer apply
- Incorrect or inconsistent file/section naming (e.g., "module-prd-accounts" vs "accounts-prd")
- Usage of prohibited or deprecated conventions (e.g., soft guarantees, ambiguous future scope, embedded roadmap language)

---

## 🔍 Scope of Audit

Perform this audit **on all documentation files** under the `./prd/` tree, including:

- All `core-prd-v*.md` files (core PRDs)
- All `module-prd-*.md` files (module-specific PRDs)
- All `README.md` files located in subdirectories (e.g., `prd/accounts/README.md`)

**Treat all PRDs and READMEs as implementation-driving artifacts.** Documents not explicitly labeled as deprecated or exploratory must be assumed to drive automated generation workflows or be parseable by deterministic tooling.

If inconsistencies exist between PRD and README content within a module, flag both for reconciliation.

---

## 🧭 Audit Procedure

1. **Start at the top of each document.**
2. **For each section or major heading:**
   - Identify **governance violations**, citing the relevant clause (e.g., "Governance §4.2")
   - Recommend **corrective actions** that would bring the section into compliance
   - Note any structural issues, naming drift, or ambiguity
   - Provide a **compliance grade**:
     - ✅ Pass | ⚠️ Needs Revision | ❌ Fail

2.5 **Check Codegen Fitness**
   - Determine whether the section supports **agentic code generation** with:
     - Deterministic function, class, or schema descriptions
     - Explicit, machine-parsable format definitions
     - Absence of speculative or non-resolvable language ("should", "might", "could")
   - Flag any **soft requirements**, **underspecified behaviors**, or **missing structural contracts**
   - Mark each section as:
     - 📎 Fully Codegen Ready
     - 🌀 Needs Constraint Tightening
     - 🛑 Not Codegen Ready

2.6 **Verify Canonical Headings**
   - Each PRD must follow the **canonical heading structure** as defined in the Governance Model (e.g., 1. Purpose, 2. Scope…)
   - Flag any missing sections, renamed headings, or section reordering unless justified by governance clause or module exemption

1a. **Metadata Header Check**
   - Confirm presence of document metadata at the top:
     - Version number, file name, author, last updated timestamp, system context
   - Cross-check filename version (e.g., `module-prd-accounts-v1.0.6.md`) against the declared version inside the file
   - ✅ Grade as Pass/Fail

---

## 📁 Output Format

Return your output as a **structured markdown report**, clearly separating findings by document and section. Use this format:

```md
## Audit: module-prd-accounts-v1.0.6.md

### Metadata Header
- ✅ Present and matches filename
- ✅ Grade: ✅ Pass

### Section 3.1 Project Overview
- ❌ **Governance Violation**: Contains roadmap references to future modules (Governance §4.1, §5.2)
- 🛠️ Fix: Remove mention of “first module” and reframe as a reusable modular framework
- ✅ Grade: ❌ Fail
- 📎 Codegen Readiness: 🛑 Not Codegen Ready

### Section 6.1 Directory Layout
- ⚠️ Formatting issues with indentation of subdirectories
- ✅ Grade: ⚠️ Needs Revision
- 📎 Codegen Readiness: 📎 Fully Codegen Ready
````

---

## 🧩 Summary Requirements

Conclude each file audit with a **per-document summary** including:

* ✅ Total pass/warning/fail count by section
* 🔺 Top 3 governance risks or drift points
* 🛠️ Action plan to bring the document into full governance and codegen compliance

---

## ✳️ Governance Reference

Use **PRD Governance Model v1.0.0**, including its **canonical PRD template structure and section numbering**, as your strict enforcement baseline.

**Do not apply external best practices unless explicitly codified** in the Governance Model or referenced via an approved exception.

---

## 🚫 Constraints

* Do not rewrite the PRDs or READMEs. Focus on **audit and annotation** only.
* Be strict. If in doubt, err on the side of governance enforcement.
* Flag **ambiguous**, **non-actionable**, or **underspecified** areas clearly.
* Highlight any drift between PRDs and their corresponding README files.

```
