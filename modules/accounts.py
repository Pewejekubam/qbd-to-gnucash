"""
!ACCNT handler: Orchestrates parsing, mapping, tree, validation, and CSV output for QBD → GnuCash accounts.
"""
import logging
from utils.iif_parser import parse_iif_accounts
from list_converters.mapping import load_mapping
from list_converters.account_tree import ensure_all_parents_exist, build_tree, flatten_tree
from utils.validation import AccountValidationSuite
from utils.error_handler import IIFParseError, MappingLoadError, AccountTreeError
import csv
import os
import json

def run_accounts_pipeline(iif_path, mapping_path, csv_path, log_path, mapping_diff_path):
    logging.basicConfig(filename=log_path, level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')
    logging.info('Starting !ACCNT pipeline')
    try:
        records = parse_iif_accounts(iif_path)
        logging.info(f'Parsed {len(records)} IIF account records')
    except Exception as e:
        logging.error(f'IIF parse error: {e}')
        logging.shutdown()  # Ensure log is flushed
        raise IIFParseError(str(e))

    try:
        mapping = load_mapping(mapping_path)
        logging.info(f'Loaded mapping from {mapping_path}')
    except Exception as e:
        logging.error(f'Mapping load error: {e}')
        logging.shutdown()  # Ensure log is flushed
        raise MappingLoadError(str(e))

    # Insert parent placeholders
    all_records = ensure_all_parents_exist(records)
    tree = build_tree(all_records)
    flat = flatten_tree(tree)

    # Validation
    validator = AccountValidationSuite(mapping)
    valid = validator.run_all(all_records, tree, flat, flat)  # flat used as csv_rows for now
    if not valid:
        logging.error(f'Validation failed: {validator.errors}')
        logging.shutdown()  # Ensure log is flushed
        raise AccountTreeError(f'Validation failed: {validator.errors}')

    # Check for unmapped types
    unmapped = sorted({r['ACCNTTYPE'] for r in all_records if r['ACCNTTYPE'] not in mapping})
    if unmapped:
        with open(mapping_diff_path, 'w', encoding='utf-8') as f:
            json.dump({'unmapped_types': unmapped}, f, indent=2)
        logging.error(f'Unmapped account types: {unmapped}')
        logging.shutdown()  # Ensure log is flushed
        os._exit(2)

    # Write CSV
    fieldnames = ['name', 'type', 'parent', 'description']
    with open(csv_path, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for rec in flat:
            # Map to GnuCash CSV row
            name = rec['NAME']
            accnttype = rec['ACCNTTYPE']
            parent = ':'.join(name.split(':')[:-1]) if ':' in name else ''
            row = {
                'name': name,
                'type': mapping.get(accnttype, accnttype),
                'parent': parent,
                'description': rec.get('DESC', '')
            }
            writer.writerow(row)
    logging.info(f'Wrote {len(flat)} accounts to {csv_path}')
