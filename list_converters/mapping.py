"""
Mapping Loader for QBD to GnuCash Account Types
- Loads mapping from registry
- Merges user overrides if present
- Provides mapping lookup and diff logic
"""
import json
import os
from utils.error_handler import MappingLoadError

REGISTRY_PATH = os.path.join('registry', 'mapping', 'account_mapping_baseline.json')


def load_mapping(user_mapping_path=None):
    try:
        with open(REGISTRY_PATH, 'r', encoding='utf-8') as f:
            base_mapping = json.load(f)
    except Exception as e:
        raise MappingLoadError(f"Failed to load base mapping: {e}")
    user_mapping = {}
    if user_mapping_path and os.path.exists(user_mapping_path):
        try:
            with open(user_mapping_path, 'r', encoding='utf-8') as f:
                user_mapping = json.load(f)
        except Exception as e:
            raise MappingLoadError(f"Failed to load user mapping: {e}")
    merged = {**base_mapping, **user_mapping}
    return merged

def find_unmapped_types(records, mapping):
    unmapped = set()
    for rec in records:
        typ = rec.get('ACCNTTYPE')
        if typ and typ not in mapping:
            unmapped.add(typ)
    return sorted(unmapped)
