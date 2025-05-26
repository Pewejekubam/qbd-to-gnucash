# 🛠️ QBD to GnuCash Conversion Tool — Agentic Multi-Phase Build Prompt v2.1.7

This prompt governs the **agentic, governance-compliant** build of a modular Python CLI tool for converting QuickBooks Desktop (.IIF) exports into GnuCash-compatible CSVs. Only the **Chart of Accounts (`!ACCNT`)** is in scope. The **PRD (v3.6.3)** and **Governance Document (v2.3.10)** are authoritative and located in the `prd/` directory. All **requirements, structure, and compliance rules** are defined therein.

---

## 🧩 Multi-Phase Build Model

Each phase must be completed **in strict sequence**, following **all mandates** without deviation.  
At the **end of each phase**, the agent must output:
- A **precise, well-formatted summary** of steps completed.
- A **clear statement** of readiness for the next phase.  
The agent **must halt and await human or automated review** before proceeding.

**Acceptance checklists** enforce compliance. Placeholders and stub implementations **must never pass any phase**.

---

### ✅ **Phase 1 — Backup, Prune, Recreate, and Scaffold**  

🚨 **STOP! Phase 1 involves irreversible changes. The agent must halt here and await explicit confirmation before proceeding.**  
🚨 **No deletion, backup, or reconstruction may occur until the user types:** `"YES"`  

⚠️ **WARNING:** The `/src/` directory is about to be **deleted and rebuilt from scratch** according to the PRD and Governance Document.  
**All existing files and directories (except explicitly preserved `.json` config files) will be removed.**  
Proceeding **cannot be undone.**  

✅ **Ready to execute Phase 1?** Type `"YES"` to confirm, or `"NO"` to halt.  

---

**Goals:**  
- **Backup all existing `.json` config files**, ensuring their full contents are retained.  
- **Delete `/src/` completely**—all files and subdirectories must be purged before recreation.  
- **Recreate the full directory tree**, adhering strictly to the PRD and Governance Document.  
- **Restore backed-up `.json` files** to their original locations **without modification**.  
- **Scaffold empty files** for all required scripts—no content from prior versions should persist.  
- **Insert agentic affirmation comments** at the top of each script, verifying PRD/GD compliance.

**Acceptance Checklist:**  
- [ ] **All existing files in `/src/` are deleted before recreation**  
- [ ] **Directory and file structure matches PRD and GD exactly**  
- [ ] **All `.json` config files explicitly listed in PRD are preserved with contents intact**  
- [ ] **All required scripts are scaffolded as empty files—no legacy content retained**  
- [ ] **Affirmation comments present in all scripts**  

**Completion Response:**  
> ✅ **Phase 1 complete. Ready to begin Phase 2 — proceed?**

---

### ✅ **Phase 2 — Core Framework and Utilities Implementation**  

**Goals:**  
- Implement `main.py` as a **fully functional modular entrypoint**. It must:  
  - **Serve as the core orchestrator**—ingesting structured inputs and dispatching payloads to domain modules.  
  - **Initialize and configure structured logging** per PRD directives.  
  - **Manage error handling using PRD-defined exception classes** (`IIFParseError`, `MappingLoadError`, etc.).  
  - **Enforce structured error handling rules** exactly as specified in the PRD.  
  - **Implement exit code management strictly**:  
    - `0` for success  
    - `1` for critical error  
    - `2` for validation error  
  - **Include agentic affirmation comments** verifying compliance with PRD/GD.  

**Acceptance Checklist:**  
- [ ] **`main.py` serves as the core processing entrypoint—no CLI argument parsing included**  
- [ ] **Structured logging, error handling, and exit code enforcement are present**  
- [ ] **All PRD-required exception classes are defined and correctly used**  
- [ ] **Affirmation comment is present and accurate**  

**Completion Response:**  
> ✅ **Phase 2 complete. Ready to begin Phase 3 — proceed?**  

---

### ✅ **Phase 3 — Accounts Module Implementation**  

**Goals:**  
- Implement **all required files** for the accounts module:  
  - `accounts.py`, `accounts_mapping.py`, `accounts_tree.py`, `accounts_validation.py`  
- Follow **module PRDs precisely**—no deviations.  
- Ensure **all public functions/classes have explicit type hints, docstrings, and example usages**.  
- Use **liberal inline comments** for maintainability.  

**Acceptance Checklist:**  
- [ ] **All accounts module files are implemented as per PRD**  
- [ ] **All public functions/classes have type hints, docstrings, and example usages**  
- [ ] **Inline comments are present for maintainability**  
- [ ] **Affirmation comments are present in all scripts**  

**Completion Response:**  
> ✅ **Phase 3 complete. Ready to begin Phase 4 — proceed?**

---

### ✅ **Phase 4 — Compliance Audit and Affirmation** _(Final Phase)_  

**Goals:**  
- Perform a **strict compliance audit** of all code.  
- Verify that **`main.py` is fully functional** and meets **all PRD requirements**.  
- Ensure **outputs (code, comments) are agentic, maintainable, and PRD/GD-compliant**.  

**Acceptance Checklist:**  
- [ ] **`main.py` is fully functional and PRD-compliant**—never a stub  
- [ ] **Affirmation comments are present throughout**  

**Completion Response:**  
> ✅ **Phase 4 complete. Build is PRD/GD-compliant and ready for release.**

---

## **📝 Notes**  
- At each phase, the agent **must halt** with a precise summary of work completed and next steps.  
- **All outputs (code, comments) must be agentic, maintainable, and PRD/GD-compliant.**  
- If any referenced PRD is incomplete or missing required interface details, the agent **must halt and request explicit guidance**.  
- If compliance enforcement is required but **no automated validator is present**, the agent **should recommend manual review**.  

