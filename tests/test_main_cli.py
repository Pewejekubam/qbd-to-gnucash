# Agentic affirmation: This test file is compliant with PRD v3.6.3 and Governance Document v2.3.10.
"""
Integration tests for CLI entrypoint (main.py) covering argument handling, exit codes, and log output.
"""
import subprocess
import sys
import os
import pytest

def test_main_cli_success(tmp_path):
    input_path = os.path.join('tests', 'data', 'sample-qbd-accounts.IIF')
    output_path = tmp_path / 'accounts.csv'
    log_path = tmp_path / 'qbd-to-gnucash.log'
    result = subprocess.run([
        sys.executable, '-m', 'src.main',
        '-i', input_path,
        '-o', str(output_path),
        '--log', str(log_path)
    ], capture_output=True, text=True)
    assert result.returncode == 0
    assert output_path.exists()
    with open(log_path, encoding='utf-8') as f:
        log_content = f.read()
    assert 'Pipeline completed successfully.' in log_content

def test_main_cli_missing_input(tmp_path):
    output_path = tmp_path / 'accounts.csv'
    log_path = tmp_path / 'qbd-to-gnucash.log'
    result = subprocess.run([
        sys.executable, '-m', 'src.main',
        '-i', 'tests/data/nonexistent.IIF',
        '-o', str(output_path),
        '--log', str(log_path)
    ], capture_output=True, text=True)
    assert result.returncode == 1
    with open(log_path, encoding='utf-8') as f:
        log_content = f.read()
    assert 'Critical error' in log_content or 'Unhandled exception' in log_content

def test_main_cli_validation_error(tmp_path):
    # Use a file with unmapped account type to trigger validation error
    test_iif = tmp_path / 'unmapped.IIF'
    with open(test_iif, 'w', encoding='utf-8') as f:
        f.write('NAME\tACCNTTYPE\tDESC\tPARENT\n')
        f.write('Assets\tEQUITY\tEquity account\t\n')
    output_path = tmp_path / 'accounts.csv'
    log_path = tmp_path / 'qbd-to-gnucash.log'
    result = subprocess.run([
        sys.executable, '-m', 'src.main',
        '-i', str(test_iif),
        '-o', str(output_path),
        '--log', str(log_path)
    ], capture_output=True, text=True)
    assert result.returncode == 2
    with open(log_path, encoding='utf-8') as f:
        log_content = f.read()
    assert 'Validation error' in log_content
