# Agentic affirmation: This test file is compliant with PRD v3.6.3 and Governance Document v2.3.10.
"""
Unit tests for accounts.py public interface.
"""
import pytest
from modules.accounts.accounts import run_accounts_pipeline
from utils.error_handler import IIFParseError, MappingLoadError, AccountsTreeError, OutputError, ValidationError
import tempfile
from utils.logging import get_logger

# Example minimal valid payload for !ACCNT
@pytest.fixture
def valid_payload(tmp_path):
    return {
        'section': '!ACCNT',
        'records': [
            {'NAME': 'Assets', 'ACCNTTYPE': 'BANK', 'DESC': 'Bank account', 'PARENT': None},
            {'NAME': 'Checking', 'ACCNTTYPE': 'BANK', 'DESC': 'Checking account', 'PARENT': 'Assets'}
        ],
        'input_path': str(tmp_path / 'sample-qbd-accounts.IIF'),
        'output_dir': str(tmp_path),
        'log_path': str(tmp_path / 'qbd-to-gnucash.log'),
        'mapping_config': {
            'account_types': {'BANK': {'gnucash_type': 'BANK', 'hierarchy_path': 'Assets:Bank'}},
            'default_rules': {}
        },
        'extra_config': {}
    }

def test_run_accounts_pipeline_success(valid_payload, tmp_path):
    input_path = valid_payload['input_path']
    output_path = tmp_path / 'accounts.csv'
    logger = get_logger(str(tmp_path / 'test.log'))
    # Write a minimal IIF file for the test
    with open(input_path, 'w', encoding='utf-8') as f:
        f.write('NAME\tACCNTTYPE\tDESC\tPARENT\n')
        f.write('Assets\tBANK\tBank account\t\n')
        f.write('Checking\tBANK\tChecking account\tAssets\n')
    run_accounts_pipeline(str(input_path), str(output_path), logger)
    assert output_path.exists()

def test_run_accounts_pipeline_invalid_section(valid_payload, tmp_path):
    input_path = valid_payload['input_path']
    output_path = tmp_path / 'accounts.csv'
    logger = get_logger(str(tmp_path / 'test.log'))
    # Write a minimal IIF file with no !ACCNT section (type VEND is unmapped)
    with open(input_path, 'w', encoding='utf-8') as f:
        f.write('NAME\tACCNTTYPE\tDESC\tPARENT\n')
        f.write('Vendor\tVEND\tVendor\t\n')
    with pytest.raises(ValidationError):
        run_accounts_pipeline(str(input_path), str(output_path), logger)
