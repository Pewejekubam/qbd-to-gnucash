import logging
import os
from utils.iif_parser import parse_iif
from list_converters.mapping import load_and_merge_mappings
from list_converters.account_tree import AccountTree
from utils.validation import AccountValidationSuite
from utils.error_handler import IIFParseError, MappingLoadError, AccountTreeError

# Placeholder for CSV writer (to be implemented in exporters/account_csv.py)
def write_accounts_csv(rows, output_path):
    import csv
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    fieldnames = [
        'Type', 'Full Account Name', 'Account Name', 'Account Code',
        'Description', 'Account Color', 'Notes', 'Symbol', 'Namespace',
        'Hidden', 'Tax Info', 'Placeholder'
    ]
    with open(output_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    logging.info(f"Wrote {len(rows)} rows to {output_path}")

def process_accounts(iif_path, mapping_baseline, mapping_specific, output_csv, diff_path=None):
    logging.info(f"Starting accounts pipeline: {iif_path}")
    try:
        records = parse_iif(iif_path)
        logging.info(f"Parsed {len(records)} account records from {iif_path}")
    except Exception as e:
        logging.error(f"IIF parsing failed: {e}")
        raise IIFParseError(str(e))

    try:
        mapping = load_and_merge_mappings(mapping_baseline, mapping_specific)
        logging.info(f"Loaded mapping files: {mapping_baseline}, {mapping_specific}")
    except Exception as e:
        logging.error(f"Mapping load failed: {e}")
        raise MappingLoadError(str(e))

    tree = AccountTree(records, mapping)
    try:
        tree.build_tree()
        logging.info("Account tree built successfully.")
    except Exception as e:
        logging.error(f"Account tree build failed: {e}")
        raise AccountTreeError(str(e))

    flat = tree.flatten_tree()
    logging.info(f"Flattened account tree to {len(flat)} rows.")

    validator = AccountValidationSuite()
    valid = validator.run_all(records, mapping, tree.tree, flat, flat)
    if not valid:
        logging.error(f"Validation failed: {validator.errors}")
        raise AccountTreeError("Validation failed. See log for details.")

    # Compose CSV rows (mapping to GnuCash fields)
    csv_rows = []
    for rec in flat:
        csv_row = {
            'Type': mapping['account_types'].get(rec.get('ACCNTTYPE', ''), {}).get('gnucash_type', ''),
            'Full Account Name': rec.get('Full Account Name', ''),
            'Account Name': rec.get('NAME', ''),
            'Account Code': rec.get('ACCNUM', ''),
            'Description': rec.get('DESC', ''),
            'Account Color': '',
            'Notes': '',
            'Symbol': '',
            'Namespace': '',
            'Hidden': rec.get('HIDDEN', ''),
            'Tax Info': '',
            'Placeholder': rec.get('placeholder', ''),
        }
        csv_rows.append(csv_row)

    write_accounts_csv(csv_rows, output_csv)
    logging.info("Accounts pipeline complete.")
    return csv_rows
