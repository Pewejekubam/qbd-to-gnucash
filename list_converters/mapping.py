import json
import os
from utils.error_handler import MappingLoadError

def load_mapping_files(baseline_path, specific_path=None):
    """Loads and merges mapping files. Returns merged mapping dict."""
    try:
        with open(baseline_path, encoding='utf-8') as f:
            baseline = json.load(f)
    except Exception as e:
        raise MappingLoadError(f"Failed to load baseline mapping: {e}")
    specific = {}
    if specific_path and os.path.exists(specific_path):
        try:
            with open(specific_path, encoding='utf-8') as f:
                specific = json.load(f)
        except Exception as e:
            raise MappingLoadError(f"Failed to load specific mapping: {e}")
    merged = dict(baseline)
    merged.update(specific)
    return merged

def write_diff_mapping(diff, diff_path):
    """Writes unmapped types to diff mapping file."""
    try:
        with open(diff_path, 'w', encoding='utf-8') as f:
            json.dump(diff, f, indent=2, ensure_ascii=False)
    except Exception as e:
        raise MappingLoadError(f"Failed to write diff mapping: {e}")

def load_and_merge_mappings(baseline_path, specific_path=None):
    """
    Loads the baseline and specific mapping files, merges them (specific overrides baseline),
    and returns:
    - combined_mapping: Dict[str, Any]
    - diff: Dict[str, Any] of unmapped QBD account types

    Raises:
        MappingLoadError if either file cannot be loaded or is invalid.
    """
    import json
    from utils.error_handler import MappingLoadError

    try:
        with open(baseline_path, encoding='utf-8') as f:
            baseline = json.load(f)
    except Exception as e:
        raise MappingLoadError(f"Failed to load baseline mapping: {e}")

    specific = {}
    if specific_path and os.path.exists(specific_path):
        try:
            with open(specific_path, encoding='utf-8') as f:
                specific = json.load(f)
        except Exception as e:
            raise MappingLoadError(f"Failed to load specific mapping: {e}")

    # Extract account_types from both
    baseline_types = baseline.get('account_types', {})
    specific_types = specific.get('account_types', {})
    # Merge: specific overrides baseline
    merged_types = dict(baseline_types)
    merged_types.update(specific_types)

    # Compute diff: QBD types in input not found in merged_types
    # (This requires the caller to provide the set of QBD types to check, so here we just return empty diff)
    diff = {}
    return merged_types, diff
