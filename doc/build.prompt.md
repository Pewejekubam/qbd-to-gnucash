You are an AI engineer implementing a modular Python CLI tool for converting QuickBooks Desktop (.IIF) exports into GnuCash-compatible CSVs. Only the Chart of Accounts (`!ACCNT`) is in scope.

🧾 A complete PRD (v2.7.2) is provided. It includes:
- File layout and module responsibilities
- Input/output format contracts
- Mapping and config logic
- Validation phases
- Error handling, logging, and fallback rules

🎯 Your goals:
- Implement exactly what the PRD describes — no feature drift
- Use only the Python standard library (Python 3.8–3.12 compatible)
- Follow the modular design (`utils/`, `modules/`, `registry/`, `main.py`)
- All logic should be clean, testable, and agent-friendly

👟 Start by:
1. Listing the files you’ll generate and their purpose
2. Generating the first implementation batch:
   - `main.py` — entrypoint and registry dispatch
   - `utils/iif_parser.py` — parses `.IIF` files
   - `utils/error_handler.py` — defines custom exception classes
   - `list_converters/mapping.py` — loads and merges mapping files

These are low-level, reusable components needed by `accounts.py`, which will coordinate the domain-specific logic afterward.

📌 Do not implement GUI support, QIF workflows, or list types beyond `!ACCNT`.

Let me know once those are complete and ready for the next phase (`account_tree.py`, validation suite, and `accounts.py` orchestration).



---

Great. Now proceed with the next phase as defined in the PRD.

Please generate the following modules:

1. `list_converters/account_tree.py`  
   - Build the account tree from normalized IIF records  
   - Ensure full hierarchy resolution and parent placeholder insertion  
   - Provide `build_tree()`, `flatten_tree()`, and `ensure_all_parents_exist()` as specified  
   - Handle 1-child promotion during flattening

2. `utils/validation.py`  
   - Implement `AccountValidationSuite` as described in the PRD  
   - Each method should support composable, staged validation
   - Methods: `validate_iif_record`, `validate_mapping`, `validate_account_tree`, `validate_flattened_tree`, `validate_csv_row`, and `run_all`

3. `modules/accounts.py`  
   - This is the `!ACCNT` handler  
   - Orchestrates the full pipeline: parsing → mapping → tree → validation → CSV write  
   - Uses `iif_parser`, `mapping`, `account_tree`, `csv_writer`, and `validation`  
   - Raises structured errors and logs each step

Let me know once these are implemented and ready for integration into `main.py`.

---

Great. Please proceed with the final integration phase.

1. Update `main.py` to:
   - Register the `!ACCNT` key and dispatch to `modules/accounts.py`
   - Include logging for entry, dispatch, and exit
   - Handle structured exceptions (e.g., `IIFParseError`, `MappingLoadError`, `AccountTreeError`)
   - Ensure `main()` is runnable from the CLI

2. Add a `__main__` guard and minimal CLI arg parsing (if needed)

3. Test the end-to-end pipeline using:
   - `input/sample-qbd-accounts.IIF`
   - Expected output: `output/accounts.csv`
   - Log file: `output/qbd-to-gnucash.log`

4. If unmapped types are detected, ensure:
   - `accounts_mapping_diff.json` is generated
   - Program exits with code 2 as described in the PRD

Let me know when the integration is complete and the tool produces usable CSV output.

