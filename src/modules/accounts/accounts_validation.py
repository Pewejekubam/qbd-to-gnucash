"""Account validation rules and checks for QBD to GnuCash conversion.
Version: 1.0.2
"""
from typing import Dict, List, Any, Set
from utils.error_handler import ValidationError
from utils.logging import setup_logging

logger = setup_logging()

def run_validation_pass(tree: Dict[str, Any]) -> None:
    """Run all validation rules on the account tree.
    
    Args:
        tree: Account hierarchy tree to validate
        
    Raises:
        ValidationError: If any validation rules fail
    """
    try:
        # Check for cycles in hierarchy
        validate_no_cycles(tree)
        logger.info("No cycles found in account hierarchy")
        
        # Validate AR/AP accounts
        validate_ar_ap_accounts(tree)
        logger.info("AR/AP account validation passed")
        
        # Check account types
        validate_account_types(tree)
        logger.info("Account type validation passed")
        
        # Validate hierarchy paths
        validate_hierarchy_paths(tree)
        logger.info("Hierarchy path validation passed")

        # Validate placeholder rules
        validate_placeholder_accounts(tree)
        logger.info("Placeholder account validation passed")
        
    except ValidationError as e:
        logger.error(f"Account validation failed: {str(e)}")
        raise


def validate_no_cycles(tree: Dict[str, Any]) -> None:
    """Check for cycles in the account hierarchy.
    
    Args:
        tree: Account hierarchy tree to check
        
    Raises:
        ValidationError: If a cycle is detected
    """
    visited: Set[str] = set()
    path: Set[str] = set()
    
    def _check_node(node_id: str) -> None:
        if node_id in path:
            raise ValidationError(
                f"Cycle detected in account hierarchy: {' -> '.join(path)}"
            )
            
        if node_id in visited:
            return
            
        visited.add(node_id)
        path.add(node_id)
        
        node = tree[node_id]
        for child_id in node['children']:
            _check_node(child_id)
            
        path.remove(node_id)
        
    _check_node('root')


def validate_ar_ap_accounts(tree: Dict[str, Any]) -> None:
    """Validate AR/AP account rules.
    
    Args:
        tree: Account hierarchy tree to check
        
    Raises:
        ValidationError: If AR/AP validation rules fail
    """
    ar_accounts = []
    ap_accounts = []
    
    def _scan_node(node: Dict[str, Any]) -> None:
        if node['type'] == 'RECEIVABLE':
            ar_accounts.append(node['name'])
        elif node['type'] == 'PAYABLE':
            ap_accounts.append(node['name'])
            
        for child in node['children'].values():
            _scan_node(child)
            
    _scan_node(tree['root'])
    
    # Must have exactly one AR and one AP account
    if len(ar_accounts) != 1:
        raise ValidationError(
            f"Must have exactly one AR account, found {len(ar_accounts)}: {ar_accounts}"
        )
        
    if len(ap_accounts) != 1:
        raise ValidationError(
            f"Must have exactly one AP account, found {len(ap_accounts)}: {ap_accounts}"
        )


def validate_account_types(tree: Dict[str, Any]) -> None:
    """Validate account type constraints.
    
    Args:
        tree: Account hierarchy tree to check
        
    Raises:
        ValidationError: If account type validation fails
    """
    valid_types = {'ASSET', 'LIABILITY', 'EQUITY', 'INCOME', 'EXPENSE', 
                  'RECEIVABLE', 'PAYABLE'}
    
    def _validate_node(node: Dict[str, Any]) -> None:
        if node['type'] and node['type'] not in valid_types:
            raise ValidationError(
                f"Invalid account type {node['type']} for account {node['name']}"
            )
            
        for child in node['children'].values():
            _validate_node(child)
            
    _validate_node(tree['root'])


def validate_hierarchy_paths(tree: Dict[str, Any]) -> None:
    """Validate account hierarchy paths.
    
    Args:
        tree: Account hierarchy tree to check
        
    Raises:
        ValidationError: If hierarchy path validation fails
    """
    paths: Set[str] = set()
    
    def _validate_node(node: Dict[str, Any], current_path: str) -> None:
        if node['name'] != 'ROOT':
            full_path = f"{current_path}:{node['name']}" if current_path else node['name']
            
            # Check for duplicate paths
            if full_path in paths:
                raise ValidationError(f"Duplicate account path found: {full_path}")
            paths.add(full_path)
            
            # Verify path matches node's full_path
            if full_path != node['full_path']:
                raise ValidationError(
                    f"Path mismatch for {node['name']}: "
                    f"expected {full_path}, got {node['full_path']}"
                )
            
        for child in node['children'].values():
            _validate_node(child, node['full_path'])
            
    _validate_node(tree['root'], '')


def validate_placeholder_accounts(tree: Dict[str, Any]) -> None:
    """Validate placeholder account rules.
    
    Args:
        tree: Account hierarchy tree to check
        
    Raises:
        ValidationError: If placeholder validation rules fail
    """
    def _validate_node(node: Dict[str, Any]) -> None:
        has_children = bool(node['children'])
        
        # Skip root node
        if node['name'] != 'ROOT':
            # Parent accounts (has children) must be placeholders
            if has_children and not node.get('is_placeholder', False):
                raise ValidationError(
                    f"Parent account {node['name']} must be marked as placeholder"
                )
            
            # Leaf accounts (no children) must not be placeholders
            if not has_children and node.get('is_placeholder', False):
                raise ValidationError(
                    f"Leaf account {node['name']} cannot be a placeholder"
                )

        # Recursively validate children
        for child in node['children'].values():
            _validate_node(child)
            
    # Start validation from root
    _validate_node(tree['root'])