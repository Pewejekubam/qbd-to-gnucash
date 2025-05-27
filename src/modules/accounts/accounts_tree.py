"""Account tree structure and type promotion logic for GnuCash accounts.
Version: 1.0.7
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from utils.error_handler import TreeConstructionError
from utils.logging import setup_logging

logger = setup_logging()

@dataclass
class AccountNode:
    name: str
    account_type: str
    full_name: str
    parent: Optional['AccountNode'] = None
    children: List['AccountNode'] = None
    is_placeholder: bool = False
    description: str = ""
    
    def __post_init__(self):
        if self.children is None:
            self.children = []

class AccountTree:
    """Represents GnuCash account hierarchy with type promotion rules."""
    
    def __init__(self):
        self.root = None
        self.nodes_by_fullname = {}
        
    def build_from_records(self, records: List[Dict[str, Any]], mapping: Dict[str, Any]) -> None:
        """Build account tree from QBD records with proper type promotion.
        
        Args:
            records: List of account records from QBD
            mapping: Account type mapping dictionary
            
        Raises:
            TreeConstructionError: If tree cannot be constructed
        """
        try:
            # Sort records by full name to ensure parents are created first
            sorted_records = sorted(records, key=lambda x: x['FULLNAME'])
            
            for record in sorted_records:
                path_parts = record['FULLNAME'].split(':')
                current_path = []
                current_node = None
                
                for part in path_parts:
                    current_path.append(part)
                    full_name = ':'.join(current_path)
                    
                    if full_name not in self.nodes_by_fullname:
                        is_leaf = (full_name == record['FULLNAME'])
                        parent_node = current_node
                        
                        # Determine account type and placeholder status
                        if is_leaf:
                            account_type = record['GNUCASH_TYPE']
                            is_placeholder = record.get('IS_PLACEHOLDER', False)
                            description = record.get('DESC', "")
                        else:
                            # Use parent type rules from mapping
                            parent_info = mapping['default_rules']['parent_accounts']
                            account_type = parent_info['gnucash_type']
                            is_placeholder = parent_info['placeholder']
                            description = ""
                        
                        # Create new node
                        node = AccountNode(
                            name=part,
                            account_type=account_type,
                            full_name=full_name,
                            parent=parent_node,
                            is_placeholder=is_placeholder,
                            description=description
                        )
                        
                        if parent_node:
                            parent_node.children.append(node)
                        else:
                            self.root = node
                            
                        self.nodes_by_fullname[full_name] = node
                        current_node = node
                    else:
                        current_node = self.nodes_by_fullname[full_name]
                        
        except KeyError as e:
            logger.error(f"Missing required field in record: {e}")
            raise TreeConstructionError(f"Missing required field in record: {str(e)}")
            
    def promote_types(self) -> None:
        """Apply type promotion rules to ensure consistent account hierarchy."""
        def _promote_types_recursive(node: AccountNode) -> None:
            if not node.children:
                return
                
            # Collect child types for promotion rules
            child_types = {child.account_type for child in node.children}
            
            # Apply promotion rules (example: if all children are ASSET, parent should be ASSET)
            if len(child_types) == 1 and not node.is_placeholder:
                node.account_type = next(iter(child_types))
                
            # Recursively promote types in children
            for child in node.children:
                _promote_types_recursive(child)
                
        if self.root:
            _promote_types_recursive(self.root)
            
    def validate_placeholders(self) -> List[str]:
        """Validate placeholder rules and return violations.
        
        Returns:
            List of full names of accounts violating placeholder rules
        """
        violations = []
        
        def _check_placeholders(node: AccountNode) -> None:
            if node.children and not node.is_placeholder:
                violations.append(node.full_name)
            elif not node.children and node.is_placeholder:
                violations.append(node.full_name)
            for child in node.children:
                _check_placeholders(child)
                
        if self.root:
            _check_placeholders(self.root)
        return violations