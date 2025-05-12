
---

### 1. **Explicit Inputs/Outputs & File Contracts**
- **Add sample input and output files** (even partial) as appendices or links. This helps clarify edge cases, field names, and expected formats.
- **Define file naming conventions** (e.g., `input/accounts.iif`, accounts.csv) and required directory structure at runtime.
- **Specify CSV field order** and required/optional columns for GnuCash import.

---

### 2. **API/Function Contracts**
- For each module (e.g., `iif_parser.py`, `mapping.py`), **list the main functions/classes, their signatures, and expected exceptions**.
- Example:
    ```python
    # iif_parser.py
    def parse_iif(filepath: str) -> List[Dict[str, str]]:
        """Parses IIF file and returns list of account records."""
    ```

---

### 3. **Configuration & Environment**
- **Clarify config precedence**: If both environment variables and config files are present, which takes priority?
- **List all environment variables/config keys** with descriptions and defaults.

---

### 4. **Validation & Error Handling**
- **Define error codes/messages as constants** in a shared module (e.g., `errors.py`).
- **Specify log file location and rotation policy** (if any).
- **Clarify: Should the tool exit nonzero on validation errors, or only on critical failures?**

---

### 6. **Testing & Acceptance**
- **List minimal test cases** (e.g., empty file, duplicate accounts, missing parents, unmapped types).
- **Specify how validation failures are surfaced** (stderr, log file, exit code).
---

### 8. **Dependencies & Versioning**
- **Specify Python version constraints** (e.g., 3.8–3.12).
- **State how to run tests** (e.g., `python -m unittest discover`).

---

### 9. **Documentation & Onboarding**
- **Add a “Getting Started” section**: clone repo, set up Python, run first conversion.
- **Link to GnuCash CSV import docs** and any sample data.

---

### 10. **Clarify Extensibility Points**
- **Explicitly list extension hooks** (e.g., how to add a new module for Vendors).
- **Describe how new mapping files should be structured and discovered**.

---
