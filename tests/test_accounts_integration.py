# Agentic affirmation: This test file is compliant with PRD v3.6.3 and Governance Document v2.3.10.
"""
Integration test for the end-to-end accounts pipeline using sample .IIF input.
"""
import pytest
import os
import json
from modules.accounts.accounts import run_accounts_pipeline
from utils.logging import get_logger

def test_accounts_pipeline_integration(tmp_path):
    iif_path = tmp_path / 'sample-qbd-accounts.IIF'
    with open(iif_path, 'w', encoding='utf-8') as f:
        f.write('NAME\tACCNTTYPE\tDESC\tPARENT\n')
        f.write('Assets\tBANK\tBank account\t\n')
        f.write('Checking\tBANK\tChecking account\tAssets\n')
    output_path = tmp_path / 'accounts.csv'
    logger = get_logger(str(tmp_path / 'test.log'))
    run_accounts_pipeline(str(iif_path), str(output_path), logger)
    assert output_path.exists()
    with open(output_path, encoding='utf-8') as f:
        lines = f.readlines()
    assert 'Assets' in ''.join(lines)
    assert 'Checking' in ''.join(lines)
