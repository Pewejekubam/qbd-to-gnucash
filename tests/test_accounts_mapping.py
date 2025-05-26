# Agentic affirmation: This test file is compliant with PRD v3.6.3 and Governance Document v2.3.10.
"""
Unit tests for accounts_mapping.py public functions.
"""
import pytest
from modules.accounts.accounts_mapping import load_mapping, find_unmapped_types
from utils.error_handler import MappingLoadError
import os

def test_load_mapping_success(tmp_path):
    # Use the baseline mapping shipped with the codebase
    baseline_path = os.path.join(os.path.dirname(__file__), '../../src/modules/accounts/accounts_mapping_baseline.json')
    mapping = load_mapping(baseline_path)
    assert 'account_types' in mapping
    assert 'default_rules' in mapping

def test_load_mapping_missing_file():
    import uuid
    missing_path = f"missing_{uuid.uuid4()}.json"
    with pytest.raises(MappingLoadError):
        load_mapping(missing_path)

def test_find_unmapped_types():
    records = [
        {'NAME': 'Assets', 'ACCNTTYPE': 'BANK'},
        {'NAME': 'Equity', 'ACCNTTYPE': 'EQUITY'}
    ]
    mapping = {'account_types': {'BANK': {}}, 'default_rules': {}}
    unmapped = find_unmapped_types(records, mapping)
    assert 'EQUITY' in unmapped
    assert 'BANK' not in unmapped
