# -----------------------------------------------------------------------------
# MODULE: Mapping Utilities
# PURPOSE: Load, save, and merge account mapping configurations
# -----------------------------------------------------------------------------

import os
import json
import logging

# Fallback logging configuration
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Paths relative to your project root; adjust if needed
BASELINE_MAPPING_FILE = os.path.join("config", "account_mapping_baseline.json")
SPECIFIC_MAPPING_FILE = os.path.join("output", "specific_account_mapping.json")


def _load_json(path):
    """
    Load JSON from disk, or return None if missing/invalid.
    """
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def _save_json(path, data):
    """
    Save `data` as pretty-printed JSON to `path`.
    """
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)
    logging.info(f"Saved mapping file: {path}")


def _merge_mappings(baseline_accounts, specific_accounts):
    """
    Merge two dicts of account mappings, giving precedence to `specific_accounts`.
    """
    logging.debug(f"Type of baseline_accounts: {type(baseline_accounts)}")
    logging.debug(f"Type of specific_accounts: {type(specific_accounts)}")
    logging.debug(f"Content of baseline_accounts: {baseline_accounts}")
    logging.debug(f"Content of specific_accounts: {specific_accounts}")

    merged = {}
    # Start from baseline
    for acct_type, entry in baseline_accounts.items():
        if not isinstance(entry, dict):
            logging.error(f"Invalid entry in baseline_accounts: {acct_type} -> {entry}")
            raise TypeError(f"Expected dict for baseline_accounts[{acct_type}], got {type(entry)}")
        merged[acct_type] = entry

    for acct_type, entry in specific_accounts.items():
        if not isinstance(entry, dict):
            logging.error(f"Invalid entry in specific_accounts: {acct_type} -> {entry}")
            raise TypeError(f"Expected dict for specific_accounts[{acct_type}], got {type(entry)}")
        merged[acct_type] = entry
    return merged


def _get_default_rule(baseline):
    """
    Return the fallback rule for unmapped types.
    """
    return baseline.get("default_rules", {}) \
                   .get("unmapped_accounts", {
                       "gnucash_type": "ASSET",
                       "destination_hierarchy": "Assets:Uncategorized",
                       "placeholder": False
                   })


def get_account_mapping():
    """
    Load, merge, and return (mapping, default_rule).

    mapping: {
      "<QBD_TYPE>": {
         "gnucash_type": "...",
         "destination_hierarchy": "...",
         "placeholder": <bool>
      },
      ...
    }
    default_rule: fallback entry for any QBD types not present in mapping.
    """
    logging.debug("Entering get_account_mapping function.")
    logging.debug(f"Baseline mapping file: {BASELINE_MAPPING_FILE}")
    logging.debug(f"Specific mapping file: {SPECIFIC_MAPPING_FILE}")
    logging.debug("Entering function to process specific mapping.")
    logging.debug(f"Specific mapping file path: {SPECIFIC_MAPPING_FILE}")

    # 1) Load baseline (must exist)
    baseline = _load_json(BASELINE_MAPPING_FILE)
    if baseline is None:
        raise RuntimeError(f"Cannot load baseline mapping: {BASELINE_MAPPING_FILE}")

    baseline_accounts = baseline.get("account_types", {})
    default_rule = _get_default_rule(baseline)

    # 2) Load specific overrides (may be missing on first run)
    specific = _load_json(SPECIFIC_MAPPING_FILE)
    logging.debug(f"Initial specific value: {specific}")
    if specific is None:
        logging.info(f"Specific mapping not found: {SPECIFIC_MAPPING_FILE}; creating stub.")
        # stub out all known types so user can fill in
        logging.debug("Starting stub creation...")
        logging.debug(f"Baseline accounts: {json.dumps(baseline_accounts, indent=2)}")
        stub = {
            acct_type: {
                "gnucash_type": "PLACEHOLDER",
                "destination_hierarchy": "Unmapped",
                "placeholder": True
            }
            for acct_type in sorted(baseline_accounts.keys())
        }
        # Log the structure of the stub before saving
        logging.debug(f"Stub structure: {json.dumps(stub, indent=2)}")
        _save_json(SPECIFIC_MAPPING_FILE, stub)
        specific = stub
        logging.debug(f"Stub assigned to specific: {json.dumps(specific, indent=2)}")

    # Ensure baseline_accounts is a dictionary
    if not isinstance(baseline_accounts, dict):
        logging.error(f"Baseline accounts is not a dictionary: {type(baseline_accounts)}")
        baseline_accounts = {}

    # Ensure specific is a dictionary
    if not isinstance(specific, dict):
        logging.error(f"Specific mapping is not a dictionary: {type(specific)}")
        specific = {}

    # Log the types and content of baseline_accounts and specific before merging
    logging.debug(f"Type of baseline_accounts before merging: {type(baseline_accounts)}")
    logging.debug(f"Content of baseline_accounts before merging: {json.dumps(baseline_accounts, indent=2)}")
    logging.debug(f"Type of specific before merging: {type(specific)}")
    logging.debug(f"Content of specific before merging: {json.dumps(specific, indent=2)}")

    # 3) Merge
    merged = _merge_mappings(baseline_accounts, specific)

    logging.debug("Exiting get_account_mapping function.")
    return merged, default_rule
