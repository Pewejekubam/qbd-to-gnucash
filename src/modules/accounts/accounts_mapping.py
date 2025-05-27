"""Account type mapping and lookup logic for QBD to GnuCash conversion.
Version: 1.0.7
"""
from typing import Dict, List, Any, Optional
import json
import os
from utils.error_handler import MappingLoadError
from utils.logging import setup_logging

logger = setup_logging()

def load_mapping(user_mapping_path: Optional[str] = None) -> Dict[str, Any]:
    """Load and merge mapping files for QBD to GnuCash account types.
    
    Args:
        user_mapping_path: Optional path to user-specific mapping overrides
        
    Returns:
        Combined dictionary of account_types and default_rules
        
    Raises:
        MappingLoadError: If required files are missing/unreadable
    """
    try:
        # Load baseline mapping
        baseline_path = os.path.join(os.path.dirname(__file__), 'accounts_mapping_baseline.json')
        with open(baseline_path, 'r', encoding='utf-8') as f:
            baseline = json.load(f)
        
        if not user_mapping_path:
            return baseline
            
        # Load and merge user mapping if provided
        with open(user_mapping_path, 'r', encoding='utf-8') as f:
            user_mapping = json.load(f)
            
        # Merge user mappings into baseline
        baseline['account_types'].update(user_mapping.get('account_types', {}))
        if 'default_rules' in user_mapping:
            baseline['default_rules'].update(user_mapping['default_rules'])
            
        logger.info("Account mapping files loaded and merged successfully")
        return baseline
        
    except FileNotFoundError as e:
        logger.error(f"Failed to load mapping file: {e.filename}")
        raise MappingLoadError(f"Required mapping file not found: {e.filename}")
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in mapping file: {e}")
        raise MappingLoadError(f"Invalid JSON format in mapping file: {str(e)}")


def find_unmapped_types(records: List[Dict[str, Any]], mapping: Dict[str, Any]) -> List[str]:
    """Return list of unmapped QBD account types.
    
    Args:
        records: List of account records from QBD
        mapping: Current account type mapping dictionary
        
    Returns:
        List of QBD account types that have no mapping
    """
    # Get unique QBD account types from records
    qbd_types = {r['ACCNTTYPE'] for r in records if 'ACCNTTYPE' in r}
    mapped_types = set(mapping['account_types'].keys())
    unmapped = list(qbd_types - mapped_types)
    
    if unmapped:
        logger.warning(f"Found unmapped account types: {unmapped}")
        # Write diff file according to PRD
        diff_path = os.path.join('output', 'accounts_mapping_diff.json')
        os.makedirs(os.path.dirname(diff_path), exist_ok=True)
        with open(diff_path, 'w', encoding='utf-8') as f:
            json.dump({'unmapped_types': unmapped}, f, indent=2)
            
    return unmapped


def get_gnucash_type(qbd_type: str, mapping: Dict[str, Any]) -> str:
    """Look up GnuCash account type for a QBD account type.
    
    Args:
        qbd_type: QuickBooks account type
        mapping: Account type mapping dictionary
        
    Returns:
        Corresponding GnuCash account type or default type
    """
    account_info = mapping['account_types'].get(qbd_type)
    if account_info:
        return account_info['gnucash_type']
    return mapping['default_rules']['unmapped_accounts']['gnucash_type']


def get_hierarchy_path(qbd_type: str, mapping: Dict[str, Any]) -> str:
    """Get GnuCash hierarchy path for a QBD account type.
    
    Args:
        qbd_type: QuickBooks account type
        mapping: Account type mapping dictionary
        
    Returns:
        GnuCash account hierarchy path or default path
    """
    account_info = mapping['account_types'].get(qbd_type)
    if account_info:
        return account_info['destination_hierarchy']
    return mapping['default_rules']['unmapped_accounts']['destination_hierarchy']


def is_placeholder(qbd_type: str, mapping: Dict[str, Any]) -> bool:
    """Check if an account type should be marked as a placeholder.
    
    Args:
        qbd_type: QuickBooks account type
        mapping: Account type mapping dictionary
        
    Returns:
        True if account should be a placeholder, False otherwise
    """
    account_info = mapping['account_types'].get(qbd_type)
    if account_info:
        return account_info['placeholder']
    return mapping['default_rules']['unmapped_accounts']['placeholder']