"""
AccountValidationSuite for staged, composable validation of account conversion pipeline.
"""
class AccountValidationSuite:
    def __init__(self, mapping):
        self.mapping = mapping
        self.errors = []

    def validate_iif_record(self, record):
        # Minimal: NAME, ACCNTTYPE required
        missing = [k for k in ('NAME', 'ACCNTTYPE') if k not in record or not record[k]]
        if missing:
            self.errors.append(f"Missing fields {missing} in IIF record: {record}")
            return False
        return True

    def validate_mapping(self, record):
        # ACCNTTYPE must be mapped
        accnttype = record.get('ACCNTTYPE')
        if accnttype not in self.mapping:
            self.errors.append(f"Unmapped ACCNTTYPE: {accnttype} in {record}")
            return False
        return True

    def validate_account_tree(self, tree):
        # Tree must have at least one child (not just ROOT)
        if not getattr(tree, 'children', []):
            self.errors.append("Account tree is empty.")
            return False
        return True

    def validate_flattened_tree(self, flat):
        # Each account must have FULLNAME, NAME, ACCNTTYPE
        ok = True
        for rec in flat:
            for k in ('FULLNAME', 'NAME', 'ACCNTTYPE'):
                if k not in rec or not rec[k]:
                    self.errors.append(f"Missing {k} in flattened account: {rec}")
                    ok = False
        return ok

    def validate_csv_row(self, row):
        # Minimal: all required GnuCash columns present
        required = ('name', 'type', 'parent')
        missing = [k for k in required if k not in row or not row[k]]
        if missing:
            self.errors.append(f"Missing CSV fields {missing} in row: {row}")
            return False
        return True

    def run_all(self, iif_records, tree, flat, csv_rows):
        ok = True
        for rec in iif_records:
            ok &= self.validate_iif_record(rec)
            ok &= self.validate_mapping(rec)
        ok &= self.validate_account_tree(tree)
        ok &= self.validate_flattened_tree(flat)
        for row in csv_rows:
            ok &= self.validate_csv_row(row)
        return ok
