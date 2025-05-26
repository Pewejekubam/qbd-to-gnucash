# Agentic affirmation: This test file is compliant with PRD v3.6.3 and Governance Document v2.3.10.
"""
Unit tests for accounts_validation.py public functions.
"""
import pytest
from modules.accounts.accounts_validation import run_validation_pass
from utils.error_handler import ValidationError
from modules.accounts.accounts_tree import AccountNode

def test_run_validation_pass_success():
    accounts = {
        'Assets': AccountNode({'NAME': 'Assets', 'ACCNTTYPE': 'BANK', 'PARENT': None}),
        'Checking': AccountNode({'NAME': 'Checking', 'ACCNTTYPE': 'BANK', 'PARENT': 'Assets'})
    }
    mapping = {'account_types': {'BANK': {}}, 'default_rules': {}}
    run_validation_pass({'accounts': accounts, 'mapping': mapping})

def test_run_validation_pass_unmapped_type():
    accounts = {
        'Assets': AccountNode({'NAME': 'Assets', 'ACCNTTYPE': 'EQUITY', 'PARENT': None})
    }
    mapping = {'account_types': {'BANK': {}}, 'default_rules': {}}
    with pytest.raises(ValidationError):
        run_validation_pass({'accounts': accounts, 'mapping': mapping})
