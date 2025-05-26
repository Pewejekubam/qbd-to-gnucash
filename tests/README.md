# Agentic affirmation: This test file is compliant with PRD v3.6.3 and Governance Document v2.3.10.

# QBD to GnuCash Conversion Tool — Test Suite

This directory contains unit and integration tests for the QBD to GnuCash conversion tool, as required by the PRD and governance model.

## Structure
- `test_accounts.py` — Unit tests for accounts pipeline interface
- `test_accounts_mapping.py` — Unit tests for mapping loader/merger
- `test_accounts_tree.py` — Unit tests for account tree builder
- `test_accounts_validation.py` — Unit tests for validation logic
- `test_accounts_integration.py` — Integration test for the accounts pipeline
- `test_main_cli.py` — Integration tests for CLI entrypoint, exit codes, and log output
- `data/` — Test input files (copied from input/)

## Running Tests

Run all tests with:

    pytest tests/

All tests are agentic, PRD-compliant, and cover required behaviors for CLI, error handling, and pipeline logic.
