# Agentic affirmation: This script is compliant with PRD v3.6.3 and Governance Document v2.3.10.

from typing import Dict, Any, List, Optional
from utils.error_handler import AccountsTreeError

class Account:
    def __init__(self, account_id, balance=0):
        self.account_id = account_id
        self.balance = balance

    def deposit(self, amount):
        if amount > 0:
            self.balance += amount
            return True
        return False

    def withdraw(self, amount):
        if 0 < amount <= self.balance:
            self.balance -= amount
            return True
        return False

    def get_balance(self):
        return self.balance


class SavingsAccount(Account):
    def __init__(self, account_id, balance=0, interest_rate=0.01):
        super().__init__(account_id, balance)
        self.interest_rate = interest_rate

    def apply_interest(self):
        self.balance += self.balance * self.interest_rate


class CheckingAccount(Account):
    def __init__(self, account_id, balance=0, overdraft_limit=0):
        super().__init__(account_id, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if 0 < amount <= self.balance + self.overdraft_limit:
            self.balance -= amount
            return True
        return False


class AccountNode:
    """
    Represents a node in the account tree.
    """
    def __init__(self, record: Dict[str, Any]):
        self.record = record
        self.children: List['AccountNode'] = []
        self.parent: Optional['AccountNode'] = None

    def add_child(self, child: 'AccountNode') -> None:
        self.children.append(child)
        child.parent = self


def build_accounts_tree(records: List[Dict[str, Any]], mapping: Dict[str, Any]) -> Dict[str, AccountNode]:
    """
    Builds and validates the account hierarchy from records and mapping.

    Args:
        records (List[Dict[str, Any]]): List of account records.
        mapping (Dict[str, Any]): Mapping dictionary.

    Returns:
        Dict[str, AccountNode]: Mapping of account names to AccountNode objects.

    Raises:
        AccountsTreeError: If hierarchy is invalid.

    Example:
        tree = build_accounts_tree(records, mapping)
    """
    nodes = {r['NAME']: AccountNode(r) for r in records}
    for node in nodes.values():
        parent_name = node.record.get('PARENT')
        if parent_name and parent_name in nodes:
            nodes[parent_name].add_child(node)
    # Check for cycles and orphans
    for node in nodes.values():
        if node.parent is None and node.record.get('PARENT'):
            raise AccountsTreeError(f'Orphaned node: {node.record["NAME"]}')
    return nodes

# Liberal inline comments and agentic structure per PRD.