"""
Account tree builder for QuickBooks IIF !ACCNT records → GnuCash CSV.
- build_tree(records): returns root node of account tree
- flatten_tree(tree): returns list of accounts in GnuCash CSV order (with 1-child promotion)
- ensure_all_parents_exist(records): inserts placeholder parents for missing hierarchy
"""
from collections import defaultdict

class AccountNode:
    def __init__(self, name, record=None):
        self.name = name
        self.record = record or {}
        self.children = []
        self.parent = None

    def add_child(self, child):
        child.parent = self
        self.children.append(child)

    def is_placeholder(self):
        return self.record.get('__placeholder__', False)

    def __repr__(self):
        return f"<AccountNode {self.name} children={len(self.children)} placeholder={self.is_placeholder()}>"

def ensure_all_parents_exist(records):
    """
    For each account, ensure all parent accounts exist in the records list.
    Insert placeholders as needed. Returns new records list.
    """
    name_to_record = {r['NAME']: r for r in records}
    all_records = records[:]
    seen = set(name_to_record)
    for rec in records:
        path = rec['NAME'].split(':')
        for i in range(1, len(path)):
            parent_name = ':'.join(path[:i])
            if parent_name not in seen:
                # Insert placeholder
                all_records.append({'NAME': parent_name, '__placeholder__': True})
                seen.add(parent_name)
    return all_records

def build_tree(records):
    """
    Build account tree from records (with all parents present).
    Returns root AccountNode (name='ROOT').
    """
    name_to_node = {}
    for rec in records:
        name = rec['NAME']
        name_to_node[name] = AccountNode(name, rec)
    root = AccountNode('ROOT')
    for node in name_to_node.values():
        path = node.name.split(':')
        if len(path) == 1:
            root.add_child(node)
        else:
            parent_name = ':'.join(path[:-1])
            parent = name_to_node.get(parent_name)
            if parent:
                parent.add_child(node)
            else:
                root.add_child(node)  # fallback, should not happen if ensure_all_parents_exist
    return root

def flatten_tree(node, parent_path=None):
    """
    Flatten tree to list of account dicts in GnuCash CSV order.
    Promotes 1-child placeholders.
    """
    parent_path = parent_path or []
    result = []
    for child in node.children:
        # Promote if placeholder with one child
        if child.is_placeholder() and len(child.children) == 1:
            result.extend(flatten_tree(child, parent_path))
        else:
            rec = child.record.copy()
            rec['FULLNAME'] = ':'.join(parent_path + [child.name]) if parent_path else child.name
            result.append(rec)
            result.extend(flatten_tree(child, parent_path + [child.name]))
    return result
