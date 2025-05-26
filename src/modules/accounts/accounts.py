# Agentic affirmation: This script is compliant with PRD v3.6.3 and Governance Document v2.3.10.

from typing import Any
from utils.iif_parser import parse_iif
from modules.accounts.accounts_mapping import load_mapping
from modules.accounts.accounts_tree import build_accounts_tree
from modules.accounts.accounts_validation import run_validation_pass
from utils.error_handler import IIFParseError, MappingLoadError, AccountsTreeError, ValidationError, OutputError
import csv

def run_accounts_pipeline(input_path: str, output_path: str, logger: Any) -> None:
    """
    Orchestrate the accounts conversion pipeline from input IIF to output CSV.
    Args:
        input_path (str): Path to the QBD .IIF file (Chart of Accounts export)
        output_path (str): Path to the output CSV file
        logger (Any): Logger instance for structured logging
    Raises:
        IIFParseError, MappingLoadError, AccountsTreeError, ValidationError, OutputError
    Example:
        run_accounts_pipeline('input/sample-qbd-accounts.IIF', 'output/accounts.csv', logger)
    """
    try:
        logger.info(f"Loading mapping configuration...")
        mapping = load_mapping()
        logger.info(f"Parsing IIF file: {input_path}")
        records = parse_iif(input_path)
        # Filter for !ACCNT section only (per PRD scope)
        accnt_records = [r for r in records if r.get('!ACCNT') or r.get('ACCNTTYPE')]
        if not accnt_records:
            raise IIFParseError("No !ACCNT records found in input file.")
        logger.info(f"Building account tree...")
        tree = build_accounts_tree(accnt_records, mapping)
        logger.info(f"Running validation pass...")
        run_validation_pass({'accounts': tree, 'mapping': mapping})
        logger.info(f"Writing output CSV: {output_path}")
        # Write output CSV in GnuCash-compatible format
        with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['NAME', 'ACCNTTYPE', 'DESC', 'PARENT']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for node in tree.values():
                writer.writerow({k: node.record.get(k, '') for k in fieldnames})
        logger.info("Accounts pipeline completed successfully.")
    except (IIFParseError, MappingLoadError, AccountsTreeError, ValidationError, OutputError):
        raise
    except Exception as e:
        logger.error(f"Unexpected error in accounts pipeline: {e}")
        raise OutputError(str(e))