import logging
from utils.error_handler import IIFParseError, MappingLoadError, AccountTreeError

class AccountValidationSuite:
    def __init__(self):
        self.errors = []

    def validate_iif_record(self, record):
        # Required fields: NAME, ACCNTTYPE
        name = record.get('NAME', '').strip().strip('"')
        accnttype = record.get('ACCNTTYPE', '').strip().strip('"')
        if not name:
            msg = f"Missing required field: NAME in record {record}"
            self.errors.append(msg)
            logging.error(msg)
            return False
        if not accnttype:
            msg = f"Empty account type (ACCNTTYPE) in record {record}"
            self.errors.append(msg)
            logging.error(msg)
            return False
        return True

    def validate_mapping(self, qb_type, mapping):
        if qb_type not in mapping.get('account_types', {}):
            msg = f"Unmapped account type: {qb_type}"
            self.errors.append(msg)
            logging.error(msg)
            return False
        return True

    def validate_account_tree(self, tree):
        # Check for missing parents, circular paths, etc.
        def check(node, path=None, seen=None):
            path = path or []
            seen = seen or set()
            for seg, data in node.items():
                full_path = ':'.join(path + [seg])
                if full_path in seen:
                    msg = f"Circular path detected: {full_path}"
                    self.errors.append(msg)
                    logging.error(msg)
                seen.add(full_path)
                check(data['_children'], path + [seg], seen)
        check(tree)
        return not self.errors

    def validate_flattened_tree(self, flat):
        # Check for 1-child promotion and placeholder rules
        for rec in flat:
            if rec.get('placeholder') == 'T' and not rec.get('ACCNTTYPE'):
                msg = f"Placeholder missing ACCNTTYPE: {rec}"
                self.errors.append(msg)
                logging.error(msg)
        return not self.errors

    def validate_csv_row(self, row):
        # Check for required CSV fields
        required = [
            'Type', 'Full Account Name', 'Account Name', 'Account Code',
            'Description', 'Account Color', 'Notes', 'Symbol', 'Namespace',
            'Hidden', 'Tax Info', 'Placeholder'
        ]
        for field in required:
            if field not in row:
                msg = f"Missing CSV field: {field} in row {row}"
                self.errors.append(msg)
                logging.error(msg)
                return False
        return True

    def run_all(self, records, mapping, tree, flat, csv_rows):
        for rec in records:
            self.validate_iif_record(rec)
        for rec in records:
            qb_type = rec.get('ACCNTTYPE', '').strip().strip('"')
            self.validate_mapping(qb_type, mapping)
        self.validate_account_tree(tree)
        self.validate_flattened_tree(flat)
        for row in csv_rows:
            self.validate_csv_row(row)
        return not self.errors
