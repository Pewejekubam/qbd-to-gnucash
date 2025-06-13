# 🛠️ QBD to GnuCash Conversion Tool — Agentic Multi-Phase Build Prompt v2.2.6

> **Environment Preparation Notice:**  
> All environment setup (backup, deletion, scaffolding, restoration) is performed manually using `codegen-setup-env-v2.0.1.py` prior to code generation.  
> The agent must assume a PRD/GD-compliant, clean environment and must not perform or repeat any setup actions.

---

This prompt governs the **agentic, governance-compliant** build of a modular Python CLI tool for converting QuickBooks Desktop (.IIF) exports into GnuCash-compatible CSVs. Only the **Chart of Accounts (`!ACCNT`)** is in scope. The **PRD (v3.6.3)** and **Governance Document (v2.3.10)** are authoritative and located in the `prd/` directory. All **requirements, structure, and compliance rules** are defined therein.

---

## 🔗 Critical Interface Definitions

**Workflow Requirements:**
- The tool must, when executed (e.g., `python -m src.main` from the project root), automatically scan the `input/` directory for all `.IIF` files.
- For each `.IIF` file, the tool must process the file using the orchestrator logic and output results to the `output/` directory (e.g., as `.json` files with matching base names).
- No command line arguments or options are required or permitted for specifying input files; the tool’s operation is fully automated and directory-driven as per PRD.
- **The `src/main.py` file must include a correct `if __name__ == "__main__" or __name__.endswith(".main"):` block to ensure execution when run as a module.**

**Logging Compliance Directive:**
- **All logs must be human-readable, syslog-style text output.**
- **Structured JSON logging is strictly prohibited** in both console and file outputs.
- **Log format must adhere to:**  
  `'%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s'`
- **Log file location:** `output/qbd-to-gnucash.log`
- **No additional logging configuration may override this format.**

**Logging Requirements:**
- **Logging initialization is a standalone procedural step and must occur before any file discovery or processing.**
- The logging setup must ensure that logs are written to `output/qbd-to-gnucash.log` and that the log directory is created if it does not exist.
- All errors, warnings, and key processing steps must be logged using the centralized logging facility.
- The logging setup must be robust: if logging cannot be initialized, the tool must print a clear error to stderr and exit with code 1.
- **No file scanning or IIF processing may occur before logging is fully initialized.**

**Procedural Validation of Logging Format:**
- After logging setup, enforce a validation check that confirms the **first line of the log file** matches the expected format.
- If validation fails, halt execution and log a corrective error.
- Example test directive:  
  *“Phase 1 must confirm that the first log entry written to `output/qbd-to-gnucash.log` matches the expected timestamped format. If deviations occur, the build must fail.”*

**Input Interface Contract:**
- `main.py` exposes `process_iif_data(iif_content: str, config: Dict[str, Any]) -> Dict[str, Any]`
- Input: Raw IIF string content and a configuration dictionary
- Output: Structured result dictionary with success/error status
- Error propagation: All exceptions bubble up with structured context

**Standard Data Structure Examples:**
```python
# Input Config Example:
{"output_format": "csv", "validation_level": "strict"}

# Success Response Example:
{"status": "success", "data": {...}, "metadata": {...}}

# Error Response Example:
{"status": "error", "code": 2, "message": "...", "details": {...}}
```

**Module Interface Requirements:**
- `accounts.py`: Core account data structures and parsing. **The `process()` function must, as an inherent procedural step, write its processed output (e.g., accounts.csv) directly to the output/ directory. This is not a post-processing or orchestrator responsibility, but a built-in function of the module.**
- `accounts_mapping.py`: Account type/category mapping logic
- `accounts_tree.py`: Hierarchical account relationship management
- `accounts_validation.py`: Account data validation and integrity checks
- All modules expose consistent `process()` functions accepting standardized data structures

**Agentic Affirmation Template:**
```python
# AGENTIC AFFIRMATION: Compliant with PRD v3.6.3 & GD v2.3.10
# Generated: [Phase X] | Validation: PASSED | Maintainability: HIGH
```

**Standard Error Handling Pattern:**
```python
try:
    result = operation()
    return success_response(result)
except SpecificError as e:
    logger.error(f"Operation failed: {e}")
    return error_response(error_code=2, message=str(e))
```

---

## 🧩 Multi-Phase Build Model

Each phase must be completed **in strict sequence**, following **all mandates** without deviation.  
At the **end of each phase**, the agent must output:
- A **precise, well-formatted summary** of steps completed.
- A **clear statement** of readiness for the next phase.  
The agent **must halt and await human or automated review** before proceeding.

**Acceptance checklists** enforce compliance. Placeholders and stub implementations **must never pass any phase**.

---

### ✅ **Phase 1 — Core Framework and Utilities Implementation**

**Goals:**  
- Implement `main.py` as a **fully functional modular entrypoint**. It must:  
  - **Serve as the core orchestrator**—ingesting structured inputs and dispatching payloads to domain modules via the `process_iif_data` interface.  
  - **Import and orchestrate accounts modules via their `process()` functions**.
  - **Initialize and configure structured logging before any processing or file discovery occurs, and ensure logging is robust and PRD-compliant.**
  - **Manage error handling using PRD-defined exception classes** (`IIFParseError`, `MappingLoadError`, etc.).  
  - **Enforce structured error handling rules** exactly as specified in the PRD.  
  - **Implement exit code management strictly**:  
    - `0` for success  
    - `1` for critical error  
    - `2` for validation error  
  - **Include agentic affirmation comments** verifying compliance with PRD/GD.  
  - **Include a correct `if __name__ == "__main__" or __name__.endswith(".main"):` block to ensure execution when run as a module.**

**Acceptance Checklist:**  
- [ ] **`main.py` serves as the core processing entrypoint—no CLI argument parsing or file path arguments included**  
- [ ] **When run as a module (e.g., `python -m src.main`), `main.py` automatically processes all `.IIF` files in the `input/` directory and writes results to `output/`**  
- [ ] **Logging is initialized before any file discovery or processing.**
- [ ] **All logs (console + file) follow the PRD-defined human-readable format.**
- [ ] **Log validation step is completed before proceeding to Phase 2.**
- [ ] **Structured JSON logging is explicitly blocked in all logging configurations.**
- [ ] **Structured logging is initialized before any processing or file discovery, and logging, error handling, and exit code enforcement are present**  
- [ ] **All PRD-required exception classes are defined and correctly used**  
- [ ] **Affirmation comment is present and accurate**  
- [ ] **`process_iif_data` interface is implemented as specified**
- [ ] **Accounts modules are imported and orchestrated via their `process()` functions**
- [ ] **A correct `if __name__ == "__main__" or __name__.endswith(".main"):` block is present and functional**

**Completion Response:**  
> ✅ **Phase 1 complete. Ready to begin Phase 2 — proceed?**

---

### ✅ **Phase 2 — Accounts Module Implementation**

**Goals:**  
- Implement **all required files** for the accounts module:  
  - `accounts.py`, `accounts_mapping.py`, `accounts_tree.py`, `accounts_validation.py`  
- Follow **module PRDs precisely**—no deviations.  
- Ensure **all public functions/classes have explicit type hints, docstrings, and example usages**.  
- Use **liberal inline comments** for maintainability.  
- Each module must expose a `process()` function accepting and returning standardized data structures as defined in the interface requirements.
- **The accounts.py module must write its processed output (e.g., accounts.csv) to the output/ directory as a required side effect of its process() function, in addition to returning structured data.**

**Acceptance Checklist:**  
- [ ] `accounts.py` implements a `process()` function that **writes output/accounts.csv as an inherent step**.
- [ ] **Logging initialization occurs before any processing or file discovery.**
- [ ] **Error handling follows PRD-defined exception classes.**
- [ ] **Affirmation comment is present verifying governance compliance.**
- [ ] All public functions/classes have type hints, docstrings, and example usages
- [ ] Inline comments are present for maintainability
- [ ] Each module exposes a `process()` function with the correct signature

**Completion Response:**  
> ✅ **Phase 2 complete. Ready to begin Phase 3 — proceed?**

---

### ✅ **Phase 3 — Compliance Audit and Affirmation** _(Final Phase)_

**Goals:**  
- Perform a **strict compliance audit** of all code.  
- Verify that **`main.py` is fully functional** and meets **all PRD requirements**.  
- Ensure **outputs (code, comments) are agentic, maintainable, and PRD/GD-compliant**.  

**Acceptance Checklist:**  
- [ ] **`main.py` is fully functional and PRD-compliant**—never a stub  
- [ ] **Affirmation comments are present throughout**  
- [ ] **All interface contracts and data flows match the definitions above**
- [ ] **Logging is initialized before any processing or file discovery, and the main block is present and correct**

**Completion Response:**  
> ✅ **Phase 3 complete. Build is PRD/GD-compliant and ready for release.**

---

## **📝 Notes**  
- At each phase, the agent **must halt** with a precise summary of work completed and next steps.  
- **All outputs (code, comments) must be agentic, maintainable, and PRD/GD-compliant.**  
- If any referenced PRD is incomplete or missing required interface details, the agent **must halt and request explicit guidance**.  
- If compliance enforcement is required but **no automated validator is present**, the agent **should recommend manual review**.


