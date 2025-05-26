# 🛠️ QBD to GnuCash Conversion Tool — Agentic Multi-Phase Build Prompt v2.1.1

This prompt governs the agentic, governance-compliant build of a modular Python CLI tool for converting QuickBooks Desktop (.IIF) exports into GnuCash-compatible CSVs. Only the Chart of Accounts (`!ACCNT`) is in scope for this build. The PRD (v3.6.3) and Governance Document (v2.3.10) are authoritative and located in the `prd/` directory. All requirements, structure, and compliance rules are defined therein.

---

## 🧩 Multi-Phase Build Model

Each phase must be completed in strict sequence. At the end of each phase, the agent must output a well-formatted, easily read summary of steps accomplished and expectations for the next step, then halt and await human or automated review before proceeding.

Each phase must include an explicit acceptance checklist verifying all requirements are met before advancing. Placeholders or stub implementations are not permitted to pass any phase.

---

### ✅ Phase 1 — Scaffold and Directory Structure Generation

**Goals:**
- Wipe and recreate the directory and file structure for the core and accounts module, as specified in the PRD and Governance Document.
- **Preserve** all `.json` config files (e.g., mapping baselines) that ship with the codebase.
- No placeholders for out-of-scope modules.
- Insert an agentic affirmation comment at the top of each script, stating compliance with the PRD and governance model.

**Acceptance Checklist:**
- [ ] Directory and file structure matches PRD and Governance Document
- [ ] All .json config files preserved
- [ ] No out-of-scope placeholders present
- [ ] Affirmation comment present in all scripts

**Completion Response:**
> ✅ Phase 1 complete. Ready to begin Phase 2 — proceed?

---

### ✅ Phase 2 — Core Framework and Utilities Implementation

**Goals:**
- Implement `main.py` as a fully functional CLI entrypoint. It must:
  - Parse arguments for `input`, `output`, and `log file`.
  - Initialize and configure structured logging as per PRD.
  - Orchestrate the accounts pipeline end-to-end.
  - Define and use all PRD-required exception classes (e.g., `IIFParseError`, `MappingLoadError`, etc.).
  - Enforce structured error handling for all PRD-defined exceptions.
  - Manage exit codes strictly: `0` for success, `1` for critical error, `2` for validation error.
  - Include an example usage comment at the top.
  - Be a complete, working CLI entrypoint (not a stub or placeholder).
- Implement all utilities in `src/utils/` as specified in the PRD.
- Include all interface contracts, error handling, and logging as specified in the PRD.
- Scaffold extension points for future modules.
- Use only Python 3.8+ standard library.

**Acceptance Checklist:**
- [ ] `main.py` is a fully functional CLI entrypoint (not a stub)
- [ ] Argument parsing, logging, error handling, and exit code logic are present and PRD-compliant
- [ ] All PRD-required exception classes are defined and used
- [ ] Example usage comment is present
- [ ] Affirmation comment is present and accurate

**Completion Response:**
> ✅ Phase 2 complete. Ready to begin Phase 3 — proceed?

---

### ✅ Phase 3 — Accounts Module Implementation

**Goals:**
- Implement all required files for the accounts module (`accounts.py`, `accounts_mapping.py`, `accounts_tree.py`, `accounts_validation.py`), following the module PRDs exactly.
- Ensure all public functions/classes have explicit type hints, docstrings, and example usages.
- Use liberal inline comments for future contributors.

**Acceptance Checklist:**
- [ ] All accounts module files implemented as per PRD
- [ ] All public functions/classes have type hints, docstrings, and example usages
- [ ] Inline comments are present for maintainability
- [ ] Affirmation comments are present

**Completion Response:**
> ✅ Phase 3 complete. Ready to begin Phase 4 — proceed?

---

### ✅ Phase 4 — Test Suite Generation and Test Data Copy

**Goals:**
- Copy all `.IIF` files from `input/` into a dedicated test suite directory (e.g., `tests/data/`).
- Generate unit tests for all public functions (using pytest).
- Generate integration tests for the end-to-end pipeline, using the copied `.IIF` files as input and writing all test output to the test directory.
- Generate integration tests that invoke the CLI entrypoint (`main.py`) as a subprocess. These tests must:
  - Validate correct argument handling, exit codes, and structured log output for all major error scenarios (e.g., missing input, validation error, critical error).
  - Ensure all structured exception handling and exit code logic behaves as specified in the PRD.
- Do not generate or require additional input files beyond those already present.

**Acceptance Checklist:**
- [ ] CLI/exit code test coverage is present and PRD-compliant
- [ ] Integration tests invoke `main.py` as a subprocess and validate all required behaviors
- [ ] Affirmation comments are present in all test files

**Completion Response:**
> ✅ Phase 4 complete. Ready to begin Phase 5 — proceed?

---

### ✅ Phase 5 — Compliance Audit and Affirmation

**Goals:**
- Perform a strict compliance audit of all code and tests.
- Verify that `main.py` is fully functional, not a placeholder, and meets all PRD requirements for CLI, argument parsing, error handling, logging, and exit code management.
- Confirm that CLI invocation tests cover all core failure and success modes, including argument handling, exit codes, and log output.
- Ensure all outputs (code, tests, comments) are agentic, maintainable, and PRD/GD-compliant.

**Acceptance Checklist:**
- [ ] `main.py` is fully functional and PRD-compliant (not a stub)
- [ ] All CLI/exit code behaviors match PRD mandates
- [ ] CLI invocation tests cover all required scenarios
- [ ] Affirmation comments are present throughout

**Completion Response:**
> ✅ Phase 5 complete. Build is PRD/GD-compliant and ready for release.

---

## 📝 Notes
- At each phase, the agent must halt with a clear, well-formatted summary of what was accomplished and what is expected next, then await human or automated review before proceeding.
- All outputs (code, tests, comments) must be agentic, maintainable, and PRD/GD-compliant.
- If any referenced PRD is incomplete or missing required interface details, the agent must halt and request explicit guidance.
- If compliance enforcement is required but no automated validator is present, the agent should recommend manual review.

---
