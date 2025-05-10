# -----------------------------------------------------------------------------
# MODULE: Accounts Converter
# PURPOSE: Parse QuickBooks IIF files and convert account data to GnuCash format
# -----------------------------------------------------------------------------

import csv
import json
import logging
import os
from utils.iif_parser import parse_iif_records
from list_converters.account_tree import build_gnucash_accounts
from utils.csv_writer import write_gnucash_csv

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

def parse_iif_section(file_path, key='!ACCNT', min_fields=12):
    """
    Extracts and parses the specified section from an IIF file.

    Returns:
        accounts_data: { account_name: { type, code, description, hidden } }
        account_types: { account_type: count }
    """
    logging.debug("Entering parse_iif_section function.")
    accounts_data = {}
    account_types = {}
    section = None

    try:
        with open(file_path, 'r') as file:
            for line in file:
                line = line.strip().replace('"', '')
                if line.startswith(key):
                    section = key
                    continue
                if not line or line.startswith('!'):
                    section = None
                    continue
                if section and line.startswith('ACCNT'):
                    parts = line.split('\t')
                    if len(parts) < min_fields:
                        logging.warning(f"Skipping short ACCNT line: {line}")
                        continue
                    name = parts[1]
                    type_ = parts[4]
                    accounts_data[name] = {
                        'type': type_,
                        'code': parts[7] if len(parts) > 7 else '',
                        'description': parts[6] if len(parts) > 6 else '',
                        'hidden': 'T' if len(parts) > 11 and parts[11] == 'Y' else 'F'
                    }
                    account_types[type_] = account_types.get(type_, 0) + 1
    except FileNotFoundError:
        logging.error(f"IIF file not found: {file_path}")
    return accounts_data, account_types


def normalize_account_type(qb_type, mapping):
    """
    Looks up the GnuCash account type and destination hierarchy
    for a given QBD account type using a nested mapping structure.

    Args:
        qb_type (str): The QBD account type (e.g., "BANK", "EXP").
        mapping (dict): The full merged mapping dictionary (including "account_types").

    Returns:
        tuple: (gnucash_type, destination_hierarchy) or None if invalid or unmapped.
    """
    account_types = mapping.get("account_types", {})
    entry = account_types.get(qb_type)
    if not entry:
        return None

    gnucash_type = entry.get("gnucash_type")
    destination = entry.get("destination_hierarchy")

    if not gnucash_type or gnucash_type.upper() == "PLACEHOLDER":
        return None
    if not destination or destination.upper() == "UNMAPPED":
        return None

    return gnucash_type, destination

def add_account_to_tree(tree, path, info, gnucash_type):
    """
    Inserts an account into the tree and ensures all implied parent paths exist.

    If any parent account (e.g. "Assets:Fixed Assets") does not exist, it will be added
    as a placeholder. This avoids GnuCash import errors due to missing hierarchy.

    Args:
        tree (dict): Dictionary representing all accounts keyed by full path.
        path (str): Colon-separated GnuCash-style path.
        info (dict): Metadata for the leaf account.
        gnucash_type (str): GnuCash account type (e.g., "ASSET", "EXPENSE").
    """
    parts = path.split(':')
    current_path = ''
    for i, part in enumerate(parts):
        current_path = f"{current_path}:{part}" if current_path else part
        is_leaf = (i == len(parts) - 1)

        if current_path not in tree:
            tree[current_path] = {
                'Type': gnucash_type if is_leaf else '',
                'Account Name': part,
                'Account Code': info.get('code', '') if is_leaf else '',
                'Description': info.get('description', '') if is_leaf else '',
                'Hidden': info.get('hidden', 'F') if is_leaf else 'F',
                'Placeholder': 'F' if is_leaf else 'T',
                'Namespace': 'CURRENCY',
                'Symbol': 'USD'
            }
        elif is_leaf:
            # Overwrite metadata if this is the defined account (not auto-generated)
            tree[current_path].update({
                'Type': gnucash_type,
                'Account Code': info.get('code', ''),
                'Description': info.get('description', ''),
                'Hidden': info.get('hidden', 'F'),
                'Placeholder': 'F'
            })


def flatten_account_tree(tree):
    """
    Flattens and optionally normalizes the account tree.
    Removes placeholder accounts with exactly one child IF that child is a leaf.
    Promotes the child up one level.

    Returns:
        dict: Updated tree with singleton placeholder parents removed when safe.
    """
    from collections import defaultdict

    # Build parent-to-children map
    children_map = defaultdict(list)
    for full_path in tree.keys():
        if ':' in full_path:
            parent = full_path.rsplit(':', 1)[0]
            children_map[parent].append(full_path)

    # Track changes
    to_promote = []
    to_remove = []

    for parent, children in children_map.items():
        if len(children) == 1:
            parent_entry = tree.get(parent)
            child_path = children[0]
            child_entry = tree.get(child_path)

            # Check: is the child a leaf (i.e. no children of its own)?
            child_has_children = any(
                k != child_path and k.startswith(f"{child_path}:") for k in tree
            )

            if (
                parent_entry
                and parent_entry.get('Placeholder') == 'T'
                and child_entry
                and child_entry.get('Placeholder') == 'F'
                and not child_has_children
            ):
                to_promote.append((parent, child_path))
                to_remove.append(parent)

    # Promote child and remove placeholder parent
    for parent, child in to_promote:
        new_path = parent
        child_data = tree.pop(child)
        child_data['Placeholder'] = 'F'
        tree[new_path] = child_data
        to_remove.append(parent)

    # Clean up placeholders
    for path in to_remove:
        if path in tree:
            del tree[path]

    return tree

def convert_accounts(iif_file_path, output_path, baseline_map_path, specific_map_path):
    """
    Main entry for converting QBD accounts to GnuCash-compatible CSV.
    - Parses IIF
    - Applies mapping
    - Builds flattened account tree
    - Writes CSV output
    """

    logging.info(f"Converting accounts from: {iif_file_path}")

    # -----------------------------
    # Load mapping
    # -----------------------------
    # Load baseline mapping first
    with open(baseline_map_path, 'r') as f:
        baseline_map = json.load(f)

    # Initialize combined mapping with baseline
    combined_map = {
        "account_types": baseline_map.get("account_types", {}),
        "default_rules": baseline_map.get("default_rules", {}),
        "basic_accounting_types": baseline_map.get("basic_accounting_types", {}),
        "metadata": baseline_map.get("metadata", {})
    }

    # Merge specific mapping if it exists
    if os.path.exists(specific_map_path):
        with open(specific_map_path, 'r') as f:
            specific_map = json.load(f)
        combined_map["account_types"].update(specific_map.get("account_types", {}))
        logging.info("Merged specific mapping into baseline.")
    else:
        logging.info(f"Specific mapping file not found: {specific_map_path} — will create if needed.")

    # -----------------------------
    # Parse IIF accounts section
    # -----------------------------
    records = parse_iif_records(iif_file_path, '!ACCNT')  # <--- MUST return list[dict]
    logging.debug(f"Parsed {len(records)} records from IIF file.")
    logging.debug(f"Parsed records: {records}")

    if not records:
        logging.error("No records found in IIF file for !ACCNT section.")
        return

    # Normalize keys in parsed records
    records = [
        {k.upper(): v for k, v in row.items()}
        for row in records
    ]

    if not isinstance(records, list) or (records and not isinstance(records[0], dict)):
        raise ValueError("Parsed IIF records must be a list of dictionaries.")

    # -----------------------------
    # Build structured account tree
    # -----------------------------
    tree = build_gnucash_accounts(records, combined_map)
    logging.debug(f"Built account tree with {len(tree)} entries.")
    logging.debug(f"Output path for CSV: {output_path}")

    # Try logging first mapped account safely
    try:
        first_key = next(iter(tree))
        logging.warning(f"First mapped account: {tree[first_key]}")
    except StopIteration:
        logging.warning("Tree is empty — no mapped accounts found.")
    except Exception as e:
        logging.error(f"Could not log first mapped account: {str(e)}")

    # -----------------------------
    # Detect unmapped types
    # -----------------------------
    qb_account_types = {row.get('ACCNTTYPE', '').strip().upper() for row in records}
    mapped_types = set(combined_map.get("account_types", {}).keys())
    unmapped = sorted(qb_account_types - mapped_types)
    logging.warning(f"Unmapped account types detected: {unmapped}")

    logging.debug(f"Unmapped types: {unmapped}")

    if unmapped:
        logging.error("Unmapped account types found. Please review and update the specific mapping file.")
        with open(specific_map_path, 'w') as f:
            json.dump({t: {
                "gnucash_type": "PLACEHOLDER",
                "destination_hierarchy": "Unmapped",
                "placeholder": True
            } for t in unmapped}, f, indent=4)
        logging.info(f"A new specific mapping file has been created at {specific_map_path}.")
        # Commented out to continue writing CSV for now
        # return

    # -----------------------------
    # Write output CSV
    # -----------------------------
    logging.debug(f"Type of 'tree': {type(tree)}")
    logging.debug(f"Content of 'tree': {list(tree.items())[:5]}" if isinstance(tree, dict) else f"Content of 'tree': {tree[:5]}")
    write_gnucash_csv(tree, output_path)
    logging.info(f"Successfully wrote accounts to {output_path}")

