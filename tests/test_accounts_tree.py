# Agentic affirmation: This test file is compliant with PRD v3.6.3 and Governance Document v2.3.10.
"""
Unit tests for accounts_tree.py public functions.
"""
import pytest
from modules.accounts.accounts_tree import build_accounts_tree, AccountNode
from utils.error_handler import AccountsTreeError

def test_build_accounts_tree_success():
    records = [
        {'NAME': 'Assets', 'ACCNTTYPE': 'BANK', 'PARENT': None},
        {'NAME': 'Checking', 'ACCNTTYPE': 'BANK', 'PARENT': 'Assets'}
    ]
    mapping = {'account_types': {'BANK': {}}, 'default_rules': {}}
    tree = build_accounts_tree(records, mapping)
    assert 'Assets' in tree
    assert 'Checking' in tree
    assert isinstance(tree['Assets'], AccountNode)
    assert tree['Checking'].parent == tree['Assets']

def test_build_accounts_tree_orphan():
    records = [
        {'NAME': 'Orphan', 'ACCNTTYPE': 'BANK', 'PARENT': 'Nonexistent'}
    ]
    mapping = {'account_types': {'BANK': {}}, 'default_rules': {}}
    with pytest.raises(AccountsTreeError):
        build_accounts_tree(records, mapping)
