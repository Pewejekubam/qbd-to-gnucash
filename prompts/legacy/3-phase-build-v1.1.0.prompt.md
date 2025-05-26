
# 🛠️ QBD to GnuCash Conversion Tool — Agentic 3-Phase Build Prompt

This prompt drives the implementation of a modular Python CLI tool for converting QuickBooks Desktop (.IIF) exports into GnuCash-compatible CSVs. Only the Chart of Accounts (`!ACCNT`) is in scope for this build. A complete PRD (v3.6.3) is provided and assumed available in the `prd/` directory. It defines:
- File layout and module responsibilities
- Input/output format contracts
- Mapping, config, and error handling logic
- Validation, logging, fallback, and phase orchestration rules

This project follows a 3-phase build model. Each phase should be completed before the next begins.

---

## ✅ Phase 1 — Core Framework and Utilities 🎯

### Goals:
- Implement only the features explicitly defined in the PRD — no feature drift
- Use Python 3.8–3.12, standard library only
- Establish modular design under the `src/` root directory, specifically:
  - `src/utils/`
  - `src/list_converters/`
  - `src/main.py`

### Tasks:
1. **`src/main.py`** - Entry point and registry dispatch (initial stub is sufficient)
2. **`src/utils/iif_parser.py`** - Parses `.IIF` files for `!ACCNT` records - Normalizes headers and returns structured records
3. **`src/utils/error_handler.py`** - Defines custom exceptions with clear PRD-based error codes - Supports structured error handling
4. **`src/module/accounts/accounts_mapping.py`** - Loads and merges `accounts_mapping_baseline.json` and `accounts_mapping_specific.json` - Writes `accounts_mapping_diff.json` if needed
5. **`src/utils/logging.py`** - Initializes logging based on PRD guidelines - Ensures `output/` directory exists at project root - Formats logs with timestamps, levels, module/function context - Logging must flush synchronously on exit

### Notes:
- Do not implement any other QBD list types or GUI support.
- Ensure no duplicate modules exist at the top-level outside `src/`.

### Completion Response:
> ✅ Phase 1 complete. Ready to begin Phase 2 — proceed?

---

## ✅ Phase 2 — Account Tree, Validation, and Orchestration 🧱

### Now that Phase 1 components are considered implemented and available in the codebase, build the following logic modules:

1. **`src/modules/accounts/accounts_tree.py`** - Builds a full accounts tree from IIF records
   - Implements:
     - `build_tree()`
     - `ensure_all_parents_exist()`
     - `flatten_tree()` (handles placeholder promotion and 1-child rule)
   - Preserves account paths like `Assets:Bank:Checking`

2. **`src/modules/accounts/accounts_validation.py`** - Implements `AccountValidationSuite` per PRD Section 6.8
   - Methods:
     - `validate_iif_record(record: dict)`
     - `validate_mapping(qbd_type: str, mapping: dict)`
     - `validate_account_tree(tree: dict)`
     - `validate_flattened_tree(tree: dict)`
     - `validate_csv_row(row: dict)`
     - `run_all(...)`
   - Validation must support both hard erroring and dry-run trace mode

3. **`src/modules/accounts/accounts.py`** - Pipeline coordinator for `!ACCNT` list type
   - Handles full flow:
     - Parsing
     - Mapping
     - Tree construction
     - Validation
     - Output CSV generation
   - Uses all utilities from Phase 1 and Phase 2
   - Raises structured exceptions and logs major steps
   - If unmapped types remain, generates `accounts_mapping_diff.json` and exits with code `2`

### Completion Response:
> ✅ Phase 2 complete. Ready to begin Phase 3 — proceed?

---

## ✅ Phase 3 — Integration, CLI, and Final Execution Flow 🎬

### This phase finalizes the CLI behavior and integrates all previous logic.

1. **Update `src/main.py` to:**
   - Register the `!ACCNT` key using a registry dispatch pattern
   - Dispatch to `src/modules/accounts/accounts.py`
   - Initialize logger via `src/utils/logging.py`
   - Catch and log any structured exceptions (`IIFParseError`, `MappingLoadError`, etc.)
   - Ensure `main()` is CLI-safe and guarded with `if __name__ == "__main__":`

2. **CLI Handling:**
   - Accepts no arguments; ignores any CLI input per PRD 15.1
   - Loads config from environment variables or fallback defaults

3. **End-to-End Flow:**
   - Input: `input/sample-qbd-accounts.IIF`
   - Output: `output/accounts.csv`
   - Log file: `output/qbd-to-gnucash.log`
   - Mapping diff (if needed): `output/accounts_mapping_diff.json`

4. **Failure Scenarios:**
   - If unmapped types remain → write diff, log issue, exit with code `2`
   - If mapping or IIF file fails to load → structured log, exit with code `1`

5. **Ensure all logging is flushed before exit, even on unhandled exceptions.**

### Completion Response:
> ✅ Phase 3 complete. Tool is ready for user testing and review.

---

## 🧠 Guidance & Notes

- Do not repeat code from previous phases unless explicitly asked
- All logging, error handling, and validation must conform to the PRD
- You may assume a `src/modules/account/accounts_mapping_baseline.json` file is present
- Mapping-specific overrides may or may not be present on first run
- Focus on correctness, clarity, and modularity

---

