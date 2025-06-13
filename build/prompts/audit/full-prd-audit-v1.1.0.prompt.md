## 📋 Audit Prompt: PRD-Only Governance Compliance Audit (v1.1.0)

You are tasked with performing a **deep, section-by-section governance compliance audit** on all **Product Requirements Documents (PRDs)** located in the `./prd/` directory of this project.

---

### 🎯 Objective
Identify and annotate **all violations** of the **PRD Governance Model v2.3.10**, including but not limited to:

- Section misnumbering, mislabeling, or heading drift
- Violations of separation-of-concerns (e.g., module logic in core PRD)
- Incorrect placement of logic, implementation detail, or roadmap speculation
- Missing or malformed structural sections (e.g., missing `3.2 Scope`, `6.1 Directory Layout`)
- Typos, formatting errors, or indentation violations that affect legibility or machine-readability
- Deprecated section references or internal links that no longer resolve
- Inconsistent file or heading naming (e.g., `accounts-prd` vs `module-prd-accounts`)
- Use of prohibited conventions (e.g., soft guarantees, underspecified placeholders)

---

### 🔍 Scope of Audit
Audit **only the following documents**:

- `core-prd-main-v*.md` (Core Product Requirements Document)
- All `module-prd-*.md` files (Module-specific PRDs under `./prd/`)
- Explicitly exclude all `README.md` files at this stage

Treat all PRDs as **authoritative**, even if labeled as drafts. Internal consistency is mandatory. If a PRD refers to another that does not yet exist or has drifted, flag the reference.

---

---

### 🧭 Audit Method  
1. Move **section-by-section** through each PRD from top to bottom.  
2. For each section:  
    - Identify **governance violations** with a citation (e.g., “Governance §4.2”)  
    - Recommend specific **corrective actions**  
    - Assign a **compliance grade**:  
        - ✅ Pass | ⚠️ Needs Revision | ❌ Fail  

3. **Strict Version-Locking Enforcement**  
    - Flag any **PRD references that are not explicitly version-locked** (e.g., `[Core PRD Section 7.3]` → ❌ Fail)  
    - Require all **cross-PRD references to use absolute version identifiers** (e.g., `[Core PRD v3.6.4 Section 7.3](../core-prd-v3.6.4.md#73-logging-strategy)`)  
    - Ensure **all anchor links are stable** and do not rely on section numbering that may change.  

4. **Pure GD Compliance Auditing** *(Revision Applied Here 👇)*  
    - **Audit ONLY compliance items explicitly mandated by the GD.**  
    - **DO NOT flag discretionary risks or suggest best practices.**  
    - Strictly enforce **placement rules as defined in GD §5.4.1 and §7.1** without discretionary interpretation.  
    - Ensure **directory mismatches, misplaced PRDs, or invalid domain associations trigger strict violations.**  

5. At the end of each PRD:  
    - Provide a **per-document summary**:  
        - Total ✅ / ⚠️ / ❌ by section  
        - Top 3 structural risks or drift points  
        - **List all unversioned PRD references that require correction**  
        - **List any PRDs that violate directory placement rules**  
        - Action plan to bring the PRD to full compliance  

---
---

### 📁 Output Format
Return your audit in **structured markdown**, following this format:

```md
## Audit: module-prd-accounts-v1.0.6.md

### Section 3.1 Project Overview
- ❌ **Governance Violation**: Uses vague forward-looking language (“will eventually support…”), violating Governance §4.1, §5.2
- 🛠️ Fix: Replace with definitive scope tied to current version
- ✅ Grade: ❌ Fail

### Section 6.1 Directory Layout
- ⚠️ Formatting error: Inconsistent bullet indentation on subfolders
- ✅ Grade: ⚠️ Needs Revision
````

---

### ⚙️ Instructions

* Do **not** rewrite or reformat the PRDs—just audit.
* Be strict. If a clause or heading seems ambiguous, **flag it**.
* Apply the **PRD Governance Model v2.3.10** as the absolute standard. No external style rules apply unless explicitly codified there.

```
