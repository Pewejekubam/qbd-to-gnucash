# 🛠️ QBD to GnuCash Conversion Tool — Agentic Multi-Phase Build Prompt v2.0.0

This prompt governs the agentic, governance-compliant build of a modular Python CLI tool for converting QuickBooks Desktop (.IIF) exports into GnuCash-compatible CSVs. Only the Chart of Accounts (`!ACCNT`) is in scope for this build. The PRD (v3.6.3) and Governance Document (v2.3.10) are authoritative and located in the `prd/` directory. All requirements, structure, and compliance rules are defined therein.

---

## 🧩 Multi-Phase Build Model

Each phase must be completed in strict sequence. At the end of each phase, the agent must output a well-formatted, easily read summary of steps accomplished and expectations for the next step, then halt and await human or automated review before proceeding.

---

### ✅ Phase 1 — Scaffold and Directory Structure Generation

**Goals:**
- Wipe and recreate the directory and file structure for the core and accounts module, as specified in the PRD and Governance Document.
- **Preserve** all `.json` config files (e.g., mapping baselines) that ship with the codebase.
- No placeholders for out-of-scope modules.
- Insert an agentic affirmation comment at the top of each script, stating compliance with the PRD and governance model.

**Completion Response:**
> ✅ Phase 1 complete. Ready to begin Phase 2 — proceed?

---

### ✅ Phase 2 — Core Framework and Utilities Implementation

**Goals:**
- Implement `main.py`, core orchestration logic, and all utilities in `src/utils/`.
- Include all interface contracts, error handling, and logging as specified in the PRD.
- Scaffold extension points for future modules.
- Use only Python 3.8+ standard library.

**Completion Response:**
> ✅ Phase 2 complete. Ready to begin Phase 3 — proceed?

---

### ✅ Phase 3 — Accounts Module Implementation

**Goals:**
- Implement all required files for the accounts module (`accounts.py`, `accounts_mapping.py`, `accounts_tree.py`, `accounts_validation.py`), following the module PRDs exactly.
- Ensure all public functions/classes have explicit type hints, docstrings, and example usages.
- Use liberal inline comments for future contributors.

**Completion Response:**
> ✅ Phase 3 complete. Ready to begin Phase 4 — proceed?

---

### ✅ Phase 4 — Test Suite Generation and Test Data Copy

**Goals:**
- Copy all `.IIF` files from `input/` into a dedicated test suite directory (e.g., `tests/data/`).
- Generate unit tests for all public functions (using pytest).
- Generate integration tests for the end-to-end pipeline, using the copied `.IIF` files as input and writing all test output to the test directory.
- Do not generate or require additional input files beyond those already present.

**Completion Response:**
> ✅ Phase 4 complete. Ready to begin Phase 5 — proceed?

---

### ✅ Phase 5 — Compliance Audit and Affirmation

**Goals:**
- Run the code-centric audit using the prompt in `doc/full-code-audit-v1.0.0.prompt.md` to check for PRD/GD compliance of the codebase.
- Insert or update agentic affirmation comments in all scripts, indicating compliance with the PRD and governance model.
- If the audit recommends changes, apply them and re-audit until all actionable issues are resolved.

**Completion Response:**
> ✅ Phase 5 complete. Ready to begin Phase 6 — proceed?

---

### ✅ Phase 6 — (Optional) Final Human Review

**Goals:**
- Human review of the entire codebase, structure, and documentation before further development (no formal hand-off required).

---

## 📝 Notes
- At each phase, the agent must halt with a clear, well-formatted summary of what was accomplished and what is expected next, then await human or automated review before proceeding.
- All outputs (code, tests, comments) must be agentic, maintainable, and PRD/GD-compliant.
- If any referenced PRD is incomplete or missing required interface details, the agent must halt and request explicit guidance.
- If compliance enforcement is required but no automated validator is present, the agent should recommend manual review.

---
