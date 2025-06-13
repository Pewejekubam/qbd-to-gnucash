"""Account hierarchy builder with double-entry accounting structure.

Fixed version that prevents phantom intermediate nodes when accounts have similar names.
"""

from typing import Dict, List, Optional, Set

from utils.error_handler import ValidationError
from utils.logging import log_technical_detail, log_config_mapping, log_config_placement

class AccountNode:
    def __init__(self, name: str, acc_type: str, account_code: str = "", source_record: dict = None):
        self.name = name
        self.type = acc_type
        self.account_code = account_code
        self.parent: Optional[AccountNode] = None
        self.children: List[AccountNode] = []
        self.full_name = name
        self.original_qbd_name = name  # Preserve original QuickBooks name
        
        # Systematic field preservation - capture ALL source data
        self.source_record = source_record or {}
        self.original_description = self.source_record.get('DESC', '')
        self.original_hidden = self.source_record.get('HIDDEN', '')
        self.original_placeholder = self.source_record.get('PLACEHOLDER', '')
        self.original_tax_info = self.source_record.get('TAXINFO', '')
        self.original_notes = self.source_record.get('NOTES', '')
        self.original_color = self.source_record.get('COLOR', '')
        
        # Log systematic field capture for user visibility
        captured_fields = [k for k, v in self.source_record.items() if v]
        if captured_fields:
            log_technical_detail(f"Field capture: '{name}' preserved {len(captured_fields)} source fields: {captured_fields}")
        else:
            log_technical_detail(f"Field capture: '{name}' no additional source fields found")

    def add_child(self, child: 'AccountNode') -> None:
        """Add a child node to this account."""
        child.parent = self
        if self.full_name == "Root":
            child.full_name = child.name
        else:
            child.full_name = f"{self.full_name}:{child.name}"
        self.children.append(child)

    def apply_1_child_rule(self) -> None:
        """Apply 1-child rule: eliminate redundant parent-child pairs with same name by structural removal."""
        # Process children first (bottom-up to avoid iterator issues during removal)
        for child in self.children[:]:  # Use slice copy to avoid modification during iteration
            child.apply_1_child_rule()
        
        if len(self.children) == 1 and self.name != "Root":
            child = self.children[0]
            
            # The 1-child rule should only apply when parent and child have the SAME NAME
            if self.name == child.name:
                # Structural elimination: merge child into parent and remove redundant child
                if self._types_compatible_for_promotion(self.type, child.type):
                    log_technical_detail(f"Config: Applied 1-child rule - eliminated redundant '{self.name}' by merging child into parent")
                    
                    # Promote parent to child's type
                    self.type = child.type
                    
                    # Absorb child's properties if needed (prefer non-empty values)
                    if hasattr(child, 'account_code') and child.account_code and not getattr(self, 'account_code', ''):
                        self.account_code = child.account_code
                    
                    # Systematically preserve any non-empty source data from child
                    for field_name in ['original_description', 'original_hidden', 'original_placeholder', 
                                     'original_tax_info', 'original_notes', 'original_color']:
                        child_value = getattr(child, field_name, '')
                        parent_value = getattr(self, field_name, '')
                        if child_value and not parent_value:
                            setattr(self, field_name, child_value)
                            log_technical_detail(f"Config: Absorbed '{field_name}' from eliminated child")
                    
                    # Merge source records (child data takes precedence for non-empty values)
                    for key, value in getattr(child, 'source_record', {}).items():
                        if value and not self.source_record.get(key):
                            self.source_record[key] = value
                    
                    # Move grandchildren up to parent level (eliminate the redundant middle layer)
                    grandchildren = child.children[:]  # Copy to avoid modification during iteration
                    self.children.remove(child)  # Remove the redundant child
                    
                    for grandchild in grandchildren:
                        grandchild.parent = self
                        # Update full_name for moved grandchildren
                        grandchild._update_full_name()
                        self.children.append(grandchild)
                        
                    log_technical_detail(f"Config: Moved {len(grandchildren)} grandchildren up to eliminate redundant layer")
                    
                else:
                    log_technical_detail(f"Config: 1-child rule skipped for '{self.name}' - type incompatible despite same name")
            else:
                log_technical_detail(f"Config: 1-child rule skipped for '{self.name}' - different name from child '{child.name}' (legitimate hierarchy)")

    def _update_full_name(self) -> None:
        """Update full_name based on current parent hierarchy."""
        if self.parent and self.parent.name != "Root":
            self.full_name = f"{self.parent.full_name}:{self.name}"
        else:
            self.full_name = self.name
        
        # Recursively update children
        for child in self.children:
            child._update_full_name()

    def _types_compatible_for_promotion(self, parent_type: str, child_type: str) -> bool:
        """Check if parent type can be promoted to child type without violating constraints."""
        # Define basic accounting type groups for promotion compatibility
        type_groups = {
            'ASSET': ['ASSET', 'BANK', 'OCASSET', 'FIXASSET', 'RECEIVABLE'],
            'LIABILITY': ['LIABILITY', 'CCARD', 'OCLIAB', 'LTLIAB', 'PAYABLE'],
            'EQUITY': ['EQUITY'],
            'INCOME': ['INCOME', 'INC', 'EXINC'],
            'EXPENSE': ['EXPENSE', 'EXP', 'EXEXP', 'COGS']
        }
        
        # Find which group each type belongs to
        parent_group = None
        child_group = None
        
        for group, types in type_groups.items():
            if parent_type in types:
                parent_group = group
            if child_type in types:
                child_group = group
        
        # Promotion is allowed only within the same accounting type group
        return parent_group == child_group

def build_accounts_tree(accounts: List[Dict[str, str]], mapping: Dict[str, any] = None) -> AccountNode:
    """Build account hierarchy with proper double-entry accounting structure.
    
    Args:
        accounts: List of account records from ACCNT module key
        mapping: Account mapping configuration with destination hierarchies
        
    Returns:
        Root node of the properly structured account tree
        
    Raises:
        ValidationError: If hierarchy cannot be constructed or AR/AP rules violated
    """
    if mapping is None:
        mapping = {}
    
    # Create the fundamental double-entry accounting structure
    root = AccountNode("Root", "ROOT")
    
    # Create the five fundamental accounting type nodes
    fundamental_types = {
        'Assets': AccountNode("Assets", "ASSET"),
        'Liabilities': AccountNode("Liabilities", "LIABILITY"), 
        'Equity': AccountNode("Equity", "EQUITY"),
        'Income': AccountNode("Income", "INCOME"),
        'Expenses': AccountNode("Expenses", "EXPENSE")
    }
    
    # Add fundamental types to root
    for type_node in fundamental_types.values():
        root.add_child(type_node)
    
    # Track AR/AP accounts for uniqueness validation
    ar_accounts: Set[str] = set()
    ap_accounts: Set[str] = set()
    
    # Build intermediate hierarchy nodes based on destination_hierarchy
    hierarchy_nodes: Dict[str, AccountNode] = {}
    hierarchy_nodes.update(fundamental_types)  # Include fundamental types
    
    # Process each account and place in proper hierarchy
    for account in accounts:
        qbd_name = account['NAME']
        qbd_type = account['ACCNTTYPE']
        account_code = account.get('ACCNUM', '')
        
        # Get mapping for this account type
        type_mapping = mapping.get('account_types', {}).get(qbd_type, {})
        gnucash_type = type_mapping.get('gnucash_type', 'EXPENSE')  # Default fallback
        destination_hierarchy = type_mapping.get('destination_hierarchy', 'Expenses')
        
        # User configuration feedback: Show mapping decisions (file only)
        if type_mapping:
            log_config_mapping(qbd_name, qbd_type, gnucash_type, destination_hierarchy)
        else:
            fallback_rule = mapping.get('default_rules', {}).get('unmapped_accounts', {})
            fallback_type = fallback_rule.get('gnucash_type', 'EXPENSE')
            fallback_hierarchy = fallback_rule.get('destination_hierarchy', 'Expenses')
            log_technical_detail(f"Config: Account type '{qbd_type}' not mapped, using fallback -> {fallback_type} at {fallback_hierarchy}")
            # Use fallback values
            gnucash_type = fallback_type
            destination_hierarchy = fallback_hierarchy
        
        # Special AR/AP validation per PRD Section 7.1
        if qbd_type == 'AR':
            ar_accounts.add(qbd_name)
            log_technical_detail(f"Config: Registered AR account '{qbd_name}' - will enforce uniqueness")
        elif qbd_type == 'AP':
            ap_accounts.add(qbd_name)
            log_technical_detail(f"Config: Registered AP account '{qbd_name}' - will enforce uniqueness")
    
    # Validate AR/AP uniqueness rules
    if len(ar_accounts) > 1:
        raise ValidationError(f"Multiple AR accounts found: {ar_accounts}. Only one AR root account allowed per PRD Section 7.1")
    if len(ap_accounts) > 1:
        raise ValidationError(f"Multiple AP accounts found: {ap_accounts}. Only one AP root account allowed per PRD Section 7.1")
    
    # Create intermediate hierarchy nodes as needed - FIXED VERSION
    def ensure_hierarchy_path(path: str) -> AccountNode:
        """Ensure all nodes in hierarchy path exist, creating as needed.
        
        FIXED: Only create intermediate nodes when they don't conflict with actual accounts.
        """
        if path in hierarchy_nodes:
            return hierarchy_nodes[path]
        
        parts = path.split(':')
        current_path = ""
        parent_node = root
        
        for i, part in enumerate(parts):
            if i == 0:
                current_path = part
            else:
                current_path = f"{current_path}:{part}"
            
            if current_path not in hierarchy_nodes:
                # CRITICAL FIX: Check if this intermediate node would conflict with actual accounts
                # Only create intermediate nodes if they won't be replaced by actual accounts later
                should_create_intermediate = True
                
                # Check if any actual account will occupy this exact position
                for account in accounts:
                    account_qbd_name = account['NAME']
                    account_qbd_type = account['ACCNTTYPE']
                    account_mapping = mapping.get('account_types', {}).get(account_qbd_type, {})
                    account_dest_hierarchy = account_mapping.get('destination_hierarchy', 'Expenses')
                    
                    # If this is a top-level account that should go directly under the parent
                    if ':' not in account_qbd_name:  # Top-level account
                        expected_full_path = f"{account_dest_hierarchy}:{account_qbd_name}"
                        if current_path == account_dest_hierarchy and part == account_qbd_name:
                            should_create_intermediate = False
                            log_technical_detail(f"Config: Skipping intermediate node '{part}' - will be replaced by actual account '{account_qbd_name}'")
                            break
                
                if should_create_intermediate:
                    # Determine appropriate type for intermediate node
                    if current_path in fundamental_types:
                        node_type = fundamental_types[current_path].type
                    else:
                        # Inherit type from parent or infer from position
                        node_type = parent_node.type
                    
                    new_node = AccountNode(part, node_type)
                    hierarchy_nodes[current_path] = new_node
                    parent_node.add_child(new_node)
                    log_technical_detail(f"Config: Created intermediate hierarchy node '{part}' under '{parent_node.full_name}'")
            
            parent_node = hierarchy_nodes.get(current_path, parent_node)
        
        return hierarchy_nodes.get(path, parent_node)
    
    # Place each account in its proper location
    for account in accounts:
        qbd_name = account['NAME']
        qbd_type = account['ACCNTTYPE'] 
        account_code = account.get('ACCNUM', '')
        
        # Get mapping for this account type
        type_mapping = mapping.get('account_types', {}).get(qbd_type, {})
        gnucash_type = type_mapping.get('gnucash_type', 'EXPENSE')
        destination_hierarchy = type_mapping.get('destination_hierarchy', 'Expenses')
        
        # Handle QuickBooks sub-account names (containing colons)
        if ':' in qbd_name:
            # This is a sub-account - create intermediate nodes as needed
            parts = qbd_name.split(':')
            
            # Find the parent account in the same destination hierarchy
            parent_account_name = parts[0]  # The first part is the parent account name
            parent_account = None
            
            # Look for the parent account that should have been processed already
            parent_node = None
            for processed_account in accounts:
                if processed_account['NAME'] == parent_account_name:
                    # Find where this parent was placed
                    parent_mapping = mapping.get('account_types', {}).get(processed_account['ACCNTTYPE'], {})
                    parent_dest_hierarchy = parent_mapping.get('destination_hierarchy', 'Expenses')
                    parent_path = f"{parent_dest_hierarchy}:{parent_account_name}"
                    if parent_path in hierarchy_nodes:
                        parent_node = hierarchy_nodes[parent_path]
                        break
            
            if not parent_node:
                # Parent not found, use the destination hierarchy
                parent_node = ensure_hierarchy_path(destination_hierarchy)
            
            current_parent = parent_node
            
            log_technical_detail(f"Config: Processing hierarchical account '{qbd_name}' with {len(parts)} levels")
            
            for i, part in enumerate(parts):
                if i == len(parts) - 1:
                    # This is the final account - preserve ALL source data
                    account_node = AccountNode(part, gnucash_type, account_code, account)
                    account_node.original_qbd_name = qbd_name
                    current_parent.add_child(account_node)
                    log_config_placement(part, current_parent.full_name, gnucash_type)
                else:
                    # This is an intermediate account - check if it already exists
                    intermediate_name = part
                    existing_child = None
                    for child in current_parent.children:
                        if child.name == intermediate_name:
                            existing_child = child
                            break
                    
                    if existing_child:
                        current_parent = existing_child
                        log_technical_detail(f"Config: Using existing intermediate node '{intermediate_name}'")
                    else:
                        # Create intermediate node - no source record for intermediates
                        intermediate_node = AccountNode(intermediate_name, gnucash_type, "")
                        current_parent.add_child(intermediate_node)
                        current_parent = intermediate_node
                        log_technical_detail(f"Config: Created intermediate node '{intermediate_name}' under '{current_parent.parent.full_name if current_parent.parent else 'Root'}'")
        else:
            # Top-level account under its destination hierarchy
            parent_node = ensure_hierarchy_path(destination_hierarchy)
            
            # CRITICAL FIX: Create the account directly under the destination hierarchy
            # Don't create intermediate nodes that match the account name
            account_node = AccountNode(qbd_name, gnucash_type, account_code, account)
            account_node.original_qbd_name = qbd_name
            parent_node.add_child(account_node)
            
            # Update hierarchy registry to point to the actual account
            account_full_path = f"{destination_hierarchy}:{qbd_name}"
            hierarchy_nodes[account_full_path] = account_node
            
            log_config_placement(qbd_name, parent_node.full_name, gnucash_type)
    
    # Apply 1-child rule per PRD Section 4.2
    root.apply_1_child_rule()
    
    # Count final accounts for logging
    def count_accounts(node: AccountNode) -> int:
        count = 1 if node.name != "Root" else 0
        for child in node.children:
            count += count_accounts(child)
        return count
    
    total_accounts = count_accounts(root)
    log_technical_detail(f"Built double-entry accounting tree with {total_accounts} accounts")
    log_technical_detail(f"AR accounts: {len(ar_accounts)}, AP accounts: {len(ap_accounts)}")
    
    return root