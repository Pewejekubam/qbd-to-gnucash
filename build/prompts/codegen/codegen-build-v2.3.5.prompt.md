# 🛠️ QBD to GnuCash Conversion Tool — Agentic Multi-Phase Build Prompt v2.3.5

> **Environment Preparation Notice:**  
> All environment setup (backup, deletion, scaffolding, restoration) is performed manually using `codegen-setup-env-v2.0.1.py` prior to code generation.  
> The agent must assume a PRD/GD-compliant, clean environment and must not perform or repeat any setup actions.

---

# 🚦 INTRINSIC COMPLIANCE FRAMEWORK

## 🛡️ PRD Validity and Verification (Governance Binding)

- **Valid PRD Definition:**
  - Only Product Requirements Documents (PRDs) located under the `prd/` directory are valid for implementation and compliance.
  - Any PRD or requirements document outside the `prd/` directory is not authoritative and must not be used for code generation, interface contracts, or compliance checks.
  - All valid PRDs must have verifiable, explicit upstream compliance to the Governance Document (GD), specifically `prd-governance-model-v2.3.10.md`.
    - The PRD must reference the relevant GD version and section(s) in its header or introduction.
    - The PRD must include a compliance statement or a compliance matrix mapping its requirements to the GD.
    - If a PRD lacks verifiable GD compliance, it is not valid and must not be used. The agent must halt and request clarification or correction.

- **Procedural PRD Verification:**
  - Before using any PRD for requirements, interface contracts, or implementation, the agent must:
    1. Confirm the PRD is located under the `prd/` directory.
    2. Check that the PRD header or introduction explicitly references the GD (`prd-governance-model-v2.3.10.md`) by version and section.
    3. Verify the PRD contains a compliance statement or matrix mapping to the GD.
    4. If any of these criteria are not met, the agent must halt and request a valid, GD-compliant PRD.

- **Citation and Enforcement:**
  - All code, comments, and build prompt citations must reference only valid PRDs from the `prd/` directory.
  - Any ambiguity or attempt to use a non-authoritative PRD must halt the build and trigger a request for correction or clarification.

---

All phases and outputs of this build are governed by the following **foundational, self-enforcing constraints**:

- **Mandatory PRD Lookup and Citation:**
  - Before any code, function, or module is generated, the agent must explicitly consult and cite the authoritative PRD documentation (including any referenced external specifications, e.g., GnuCash CSV import logic) relevant to the implementation.
  - If a PRD section or external spec is referenced in the requirements, the agent must acknowledge and cite it in the build prompt and in code comments.
  - If any contract, field, or format is ambiguous or missing in the PRD, the agent must halt and request clarification before proceeding.
  - **All input and output operations (including file writes, reads, and in-memory data exchange) must be derived solely from the authoritative PRD and module interface contracts. No code, function, or process may read from or write to storage or memory except as explicitly defined in the PRD. Any ambiguity or deviation must halt the build and trigger a request for clarification.**

- **Strict Output File Typing and Scope:**
  - For each module, the scope and type of output files must be explicitly enforced as defined in the PRD.
  - **For the accounts mapping module (`accounts_mapping.py`), the ONLY permitted JSON output is the `accounts_mapping_diff.json` file, which lists unmapped types. No other processed output in JSON format may be produced, written, or referenced by this module.**
  - Any reference to JSON output in requirements, code, or documentation for this module must be interpreted solely as the creation of `accounts_mapping_diff.json`. Any deviation or ambiguity in output file type or scope must halt the build and trigger a request for clarification.

- **PRD Contract Derivation:**
  - All function signatures, module structures, and behaviors are to be **directly derived from the authoritative PRD/GD**. Generation must not proceed if any contract is ambiguous or missing; the agent must halt and request clarification.
  - All module and function responsibilities are defined by the PRD and must be implemented as such, not as post-hoc corrections.

- **PRD Enforcement Checkpoints:**
  - At each build phase, the agent must validate that all generated code, function signatures, and data structures strictly match the PRD-defined formats (including field order, required columns, and output structure).
  - Any deviation, ambiguity, or misalignment at any phase triggers an immediate halt and request for correction or clarification.
  - If a structured output (e.g., accounts.csv, JSON) is required, the agent must confirm it is directly derived from the PRD and cite the relevant PRD section in code comments.
  - **All file and memory I/O operations must be explicitly defined in the PRD/module contract. No module or orchestrator writes or reads data except as specified in the PRD. All output file types, names, and locations must be cited with PRD section references in code comments.**

- **Execution Order Enforcement:**
  - **No file discovery, data processing, or side-effect imports may occur before logging is fully initialized.**
  - All imports must be side-effect free until after logging setup. Any violation halts generation.
  - Pre-execution validation of dependencies and importability is required before any main logic runs.

- **Format Consistency:**
  - **Logging must always be human-readable, syslog-style text. JSON logs are strictly prohibited.**
  - Structured JSON output files are permitted only for processed data, never for logs.
  - **For the accounts mapping module, structured JSON output is strictly limited to `accounts_mapping_diff.json` as defined above.**
  - All output files (logs, CSVs, JSONs) must be validated for format compliance before any phase is considered complete.

- **Phase Gatekeeping:**
  - Each phase’s checklist is a **hard gate**: generation cannot proceed unless all constraints are met as inherent properties of the generated code.
  - Any deviation, ambiguity, or misalignment at any phase triggers an immediate halt and request for correction or clarification.

---

# 🔍 PRD Lookup and Enforcement Procedures

- **PRD Lookup Requirement:**
  - Before generating or updating any code, the agent must perform a lookup of the relevant PRD documentation and cite the specific section(s) used.
  - If the PRD references external specifications (e.g., GnuCash CSV import logic on GitHub), the agent must acknowledge and cite these sources in the build prompt and in code comments.
  - **Before any I/O code is generated, the agent must lookup and cite the exact PRD section authorizing the operation. If the PRD is silent or ambiguous, the agent must halt and request clarification.**

- **Enforcement Checkpoints:**
  - At each build phase, the agent must check that all function signatures, module structures, and output formats match the PRD and cited external specifications exactly.
  - If any mismatch is detected, the agent must halt generation and request clarification or correction.
  - **Before phase completion, cross-check all I/O operations against the PRD and module contracts. Any operation not explicitly PRD-cited must be removed or corrected.**

- **Checklist Enhancements:**
  - Each phase checklist must include explicit validation that PRD mandates and external spec requirements have been looked up, cited, and enforced in the generated code.
  - The agent must confirm PRD adherence at multiple build phases, not just retroactively.
  - **All I/O operations in code must be accompanied by a code comment referencing the relevant PRD section authorizing the operation.**

---

## 🔗 Critical Interface Definitions

**Workflow Requirements:**
- The tool must, when executed (e.g., `python -m src.main` from the project root), automatically scan the `input/` directory for all `.IIF` files.
- For each `.IIF` file, the tool must process the file using the orchestrator logic and output results to the `output/` directory according to the module and interface contracts and README-based file structures.
- No command line arguments or options are required or permitted for specifying input files; the tool’s operation is fully automated and directory-driven as per PRD.
- **The `src/main.py` file must include a correct `if __name__ == "__main__" or __name__.endswith(".main"):` block to ensure execution when run as a module.**

**Logging Compliance Directive:**
- **All logs must be human-readable, syslog-style text output.**
- **Structured JSON logging is strictly prohibited** in both console and file outputs.
- **Log format must adhere to:**  
  `'%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s'`
- **Log file location:** `output/qbd-to-gnucash.log`
- **No additional logging configuration may override this format.**
- **Only the log file (`qbd-to-gnucash.log`) must be human-readable, text-based. Structured JSON output files are permitted and required for storing processed data results. Logging facilities must never use JSON serialization (`json.dumps()`) in log entries.**

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
- `accounts_mapping.py`: Account type/category mapping logic. **The ONLY JSON output produced by this module is the `accounts_mapping_diff.json` file, which lists unmapped types. No other processed output in JSON format is produced or written by this module. All code, documentation, and requirements must reflect this restriction.**
- `accounts_tree.py`: Hierarchical account relationship management
- `accounts_validation.py`: Account data validation and integrity checks
- All modules expose consistent `process()` functions accepting standardized data structures
- **All generated modules must strictly follow PRD-defined function contracts. Any function signature or module structure deviation from PRD specifications must trigger a build failure requiring correction. Example: `iif_parser.py` must expose `parse(iif_content: str) -> Dict[str, Any]` and handle structured extraction for IIF records.**

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
  - **All imports must be side-effect free until after logging is initialized.**
  - **Pre-execution validation must confirm all required modules are present and importable before any processing.**
  - **Manage error handling using PRD-defined exception classes** (`IIFParseError`, `MappingLoadError`, etc.).  
  - **Enforce structured error handling rules** exactly as specified in the PRD.  
  - **Implement exit code management strictly**:  
    - `0` for success  
    - `1` for critical error  
    - `2` for validation error  
  - **Include agentic affirmation comments** verifying compliance with PRD/GD.  
  - **Include a correct `if __name__ == "__main__" or __name__.endswith(".main"):` block to ensure execution when run as a module.**
  - **All file and memory I/O operations must be explicitly defined in the PRD/module contract and cited in code comments.**

**Acceptance Checklist (Phase Gate):**  
- [ ] `main.py` is the core orchestrator; no CLI argument parsing or file path arguments included  
- [ ] When run as a module, `main.py` automatically processes all `.IIF` files in the `input/` directory and writes results to `output/`  
- [ ] **Logging is initialized before any file discovery or processing.**  
- [ ] **All imports are side-effect free until after logging is initialized.**
- [ ] **Pre-execution validation confirms all required modules are present and importable.**
- [ ] All logs (console + file) follow the PRD-defined human-readable format.  
- [ ] Log validation step is completed before proceeding to Phase 2.  
- [ ] Structured JSON logging is explicitly blocked in all logging configurations.  
- [ ] Structured logging is initialized before any processing or file discovery, and logging, error handling, and exit code enforcement are present  
- [ ] All PRD-required exception classes are defined and correctly used  
- [ ] Affirmation comment is present and accurate  
- [ ] `process_iif_data` interface is implemented as specified  
- [ ] Accounts modules are imported and orchestrated via their `process()` functions  
- [ ] A correct `if __name__ == "__main__" or __name__.endswith(".main"):` block is present and functional  
- [ ] **Generated function signatures and module responsibilities are derived directly from PRD definitions.**
- [ ] IIF parser exposes the mandated function signature (`parse(iif_content: str) -> Dict[str, Any]`).  
- [ ] **Any deviation, ambiguity, or misalignment halts generation and triggers a request for correction or clarification.**
- [ ] **All output files (logs, CSVs, JSONs) must be validated for format compliance before phase completion.**
- [ ] **All file and memory I/O operations are explicitly defined in the PRD/module contract and cited in code comments.**

**Procedural Enforcement for Phase 1 Completion:**
> Before outputting "Phase 1 complete," the agent must:
> - Read the contents of `src/main.py`.
> - Validate that all required orchestrator logic, logging setup, error handling, and interface functions are present and non-stubbed.
> - If any required logic is missing, stubbed, or not PRD-compliant, halt and request correction or further instruction.
> - Only output "Phase 1 complete" if all requirements are met in the actual file content.

**Completion Response:**  
> ✅ **Phase 1 complete. Ready to begin Phase 2 — proceed?**

---

### ✅ **Phase 2 — Accounts Module Implementation**

**Goals:**  
- Implement all required files for the accounts module:  
  - `accounts.py`, `accounts_mapping.py`, `accounts_tree.py`, `accounts_validation.py`  
- **All public functions/classes must have explicit type hints, docstrings, and example usages, as defined in the PRD.**
- Use liberal inline comments for maintainability.  
- Each module must expose a `process()` function accepting and returning standardized data structures as defined in the interface requirements.
- **The accounts.py module must write its processed output (e.g., accounts.csv) to the output/ directory as a required side effect of its process() function, in addition to returning structured data.**
- **All file and memory I/O operations must be explicitly defined in the PRD/module contract and cited in code comments.**

**Acceptance Checklist (Phase Gate):**  
- [ ] `accounts.py` implements a `process()` function that writes output/accounts.csv as an inherent step.  
- [ ] Logging initialization occurs before any processing or file discovery.  
- [ ] Error handling follows PRD-defined exception classes.  
- [ ] Affirmation comment is present verifying governance compliance.  
- [ ] All public functions/classes have type hints, docstrings, and example usages  
- [ ] Inline comments are present for maintainability  
- [ ] Each module exposes a `process()` function with the correct signature  
- [ ] **All output files (logs, CSVs, JSONs) are validated for format compliance before phase completion.**
- [ ] **Any deviation, ambiguity, or misalignment halts generation and triggers a request for correction or clarification.**
- [ ] **All file and memory I/O operations are explicitly defined in the PRD/module contract and cited in code comments.**

**Completion Response:**  
> ✅ **Phase 2 complete. Ready to begin Phase 3 — proceed?**

---

### ✅ **Phase 3 — Compliance Audit and Affirmation** _(Final Phase)_

**Goals:**  
- Perform a strict compliance audit of all code.  
- Verify that `main.py` is fully functional and meets all PRD requirements.  
- Ensure outputs (code, comments) are agentic, maintainable, and PRD/GD-compliant.  
- **All outputs must be validated for format and contract compliance before release.**
- **All file and memory I/O operations must be explicitly defined in the PRD/module contract and cited in code comments.**

**Acceptance Checklist (Phase Gate):**  
- [ ] `main.py` is fully functional and PRD-compliant—never a stub  
- [ ] Affirmation comments are present throughout  
- [ ] All interface contracts and data flows match the definitions above  
- [ ] Logging is initialized before any processing or file discovery, and the main block is present and correct  
- [ ] **All outputs are validated for format and contract compliance before release.**
- [ ] **Any deviation, ambiguity, or misalignment halts generation and triggers a request for correction or clarification.**
- [ ] **All file and memory I/O operations are explicitly defined in the PRD/module contract and cited in code comments.**

**Completion Response:**  
> ✅ **Phase 3 complete. Build is PRD/GD-compliant and ready for release.**

---

## **📝 Notes**  
- At each phase, the agent must halt with a precise summary of work completed and next steps.  
- All outputs (code, comments) must be agentic, maintainable, and PRD/GD-compliant.  
- If any referenced PRD is incomplete or missing required interface details, the agent must halt and request explicit guidance.  
- If compliance enforcement is required but no automated validator is present, the agent should recommend manual review.


