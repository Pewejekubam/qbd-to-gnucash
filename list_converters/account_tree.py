import logging
from utils.error_handler import AccountTreeError

class AccountTree:
    def __init__(self, records, mapping):
        self.records = records
        self.mapping = mapping
        self.tree = {}
        self.flat_accounts = []

    def build_tree(self):
        """Builds the account tree from IIF records, inserting placeholders as needed."""
        self.tree = {}
        for rec in self.records:
            path = rec.get('NAME', '').strip()
            if not path:
                continue
            segments = path.split(':')
            node = self.tree
            for i, seg in enumerate(segments):
                if seg not in node:
                    node[seg] = {'_children': {}, '_record': None}
                if i == len(segments) - 1:
                    node[seg]['_record'] = rec
                node = node[seg]['_children']
        self.ensure_all_parents_exist()
        return self.tree

    def ensure_all_parents_exist(self):
        """Ensures all parent accounts exist, inserting placeholders if needed."""
        def insert_placeholders(node, path_prefix=None):
            path_prefix = path_prefix or []
            for seg, data in node.items():
                full_path = ':'.join(path_prefix + [seg])
                if data['_record'] is None:
                    # Insert placeholder record
                    data['_record'] = {
                        'NAME': seg,
                        'Full Account Name': full_path,
                        'ACCNTTYPE': None,
                        'placeholder': 'T',
                    }
                insert_placeholders(data['_children'], path_prefix + [seg])
        insert_placeholders(self.tree)

    def flatten_tree(self):
        """Flattens the tree into a list, promoting 1-child placeholders as needed."""
        flat = []
        def walk(node, parent_path=None):
            parent_path = parent_path or []
            for seg, data in node.items():
                full_path = ':'.join(parent_path + [seg])
                rec = data['_record']
                rec = dict(rec)  # Copy
                rec['Full Account Name'] = full_path
                flat.append(rec)
                # 1-child promotion: if placeholder and only one child, promote child
                children = data['_children']
                if rec.get('placeholder') == 'T' and len(children) == 1:
                    for child_seg, child_data in children.items():
                        walk({child_seg: child_data}, parent_path + [seg])
                else:
                    walk(children, parent_path + [seg])
        walk(self.tree)
        self.flat_accounts = flat
        return flat

    def validate(self):
        """Returns a list of validation errors for the tree."""
        errors = []
        def check(node, path=None):
            path = path or []
            for seg, data in node.items():
                rec = data['_record']
                if not rec or not rec.get('NAME'):
                    errors.append(f"Missing NAME at {'/'.join(path + [seg])}")
                check(data['_children'], path + [seg])
        check(self.tree)
        return errors
