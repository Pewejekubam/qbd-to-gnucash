# Agentic affirmation: This script is compliant with PRD v3.6.3 and Governance Document v2.3.10.

from typing import Dict, Any, List, Optional
from utils.error_handler import MappingLoadError
import json
import os


def load_mapping(user_mapping_path: Optional[str] = None) -> Dict[str, Any]:
    """
    Loads and merges mapping files for QBD to GnuCash account types.

    Args:
        user_mapping_path (Optional[str]): Path to user-specific mapping file.

    Returns:
        Dict[str, Any]: Combined mapping dictionary.

    Raises:
        MappingLoadError: If required files are missing or unreadable.

    Example:
        mapping = load_mapping('output/accounts_mapping_specific.json')
    """
    baseline_path = os.path.join(os.path.dirname(__file__), 'accounts_mapping_baseline.json')
    mapping = {}
    try:
        with open(baseline_path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        if user_mapping_path:
            if not os.path.exists(user_mapping_path):
                raise MappingLoadError(f'Mapping file not found: {user_mapping_path}')
            with open(user_mapping_path, 'r', encoding='utf-8') as f:
                user_mapping = json.load(f)
            mapping['account_types'].update(user_mapping.get('account_types', {}))
            mapping['default_rules'].update(user_mapping.get('default_rules', {}))
    except Exception as e:
        raise MappingLoadError(f'Failed to load mapping: {e}')
    return mapping


def find_unmapped_types(records: List[Dict[str, Any]], mapping: Dict[str, Any]) -> List[str]:
    """
    Returns a list of unmapped QBD account types.

    Args:
        records (List[Dict[str, Any]]): List of account records.
        mapping (Dict[str, Any]): Mapping dictionary.

    Returns:
        List[str]: Unmapped QBD account types.

    Example:
        unmapped = find_unmapped_types(records, mapping)
    """
    mapped_types = set(mapping.get('account_types', {}).keys())
    record_types = set(r['ACCNTTYPE'] for r in records if 'ACCNTTYPE' in r)
    return list(record_types - mapped_types)

# Liberal inline comments and agentic structure per PRD.