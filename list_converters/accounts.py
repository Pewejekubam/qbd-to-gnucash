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
    Ensures that all levels in a hierarchical account path are added to the tree,
    inserting placeholders for intermediate parents if missing, and populating the
    leaf account with full metadata.
    """
    parts = path.split(":")
    current_path = ""
    
    for i, part in enumerate(parts):
        current_path = f"{current_path}:{part}" if current_path else part
        is_leaf = i == len(parts) - 1

        if current_path not in tree:
            tree[current_path] = {
                "Type": gnucash_type if is_leaf else "",
                "Account Name": part,
                "Account Code": info.get("ACCNUM", "") if is_leaf else "",
                "Description": info.get("DESC", "") if is_leaf else "",
                "Account Color": "",
                "Notes": "",
                "Symbol": "USD",
                "Namespace": "CURRENCY",
                "Hidden": "F",
                "Tax Info": "F",
                "Placeholder": "F" if is_leaf else "T",
            }

        elif is_leaf:
            # If the leaf was already inserted as a placeholder earlier, update it with real info
            tree[current_path].update({
                "Type": gnucash_type,
                "Account Code": info.get("ACCNUM", ""),
                "Description": info.get("DESC", ""),
                "Placeholder": "F",
            })


def flatten_account_tree(tree):
    """
    Enforce the "1-child rule":
    - If a placeholder has exactly one child and that child is a leaf (not a placeholder and has no children),
      promote the child into the parent's position and remove the original placeholder and the redundant child.
    """
    import logging
    from collections import defaultdict

    # Step 1: Build a child map: parent path → [child paths]
    child_map = defaultdict(list)
    for full_name in tree:
        parts = full_name.split(":")
        if len(parts) > 1:
            parent = ":".join(parts[:-1])
            child_map[parent].append(full_name)

    # Step 2: Find parent placeholders with a single child
    to_promote = []
    for parent, children in child_map.items():
        if len(children) != 1:
            continue

        child = children[0]
        parent_entry = tree.get(parent)
        child_entry = tree.get(child)

        if not parent_entry or not child_entry:
            continue

        is_placeholder = parent_entry.get("Placeholder") == "T"
        child_is_leaf = (
            child_entry.get("Placeholder") == "F" and
            not any(
                other != child and other.startswith(f"{child}:")
                for other in tree
            )
        )

        if is_placeholder and child_is_leaf:
            to_promote.append((parent, child))

    # Step 3: Promote child into parent, remove both original entries
    for parent, child in to_promote:
        logging.debug(f"Promoting single child '{child}' to replace placeholder parent '{parent}'")

        # Promote the child into the parent's slot
        child_data = tree[child].copy()
        child_data["Placeholder"] = "F"
        tree[parent] = child_data

        # Remove the original nested child
        if child in tree:
            del tree[child]

    return tree

def ensure_all_parents_exist(tree):
    """
    Ensures all intermediate parent accounts are present in the tree as placeholders.
    """
    new_entries = {}

    all_required_parents = set()
    for full_name in tree.keys():
        parts = full_name.split(":")
        for i in range(1, len(parts)):
            parent_path = ":".join(parts[:i])
            all_required_parents.add(parent_path)

    for parent_path in all_required_parents:
        if parent_path not in tree and parent_path not in new_entries:
            part = parent_path.split(":")[-1]
            new_entries[parent_path] = {
                "Type": "",
                "Account Name": part,
                "Account Code": "",
                "Description": "",
                "Account Color": "",
                "Notes": "",
                "Symbol": "USD",
                "Namespace": "CURRENCY",
                "Hidden": "F",
                "Tax Info": "F",
                "Placeholder": "T",
            }

    if new_entries:
        tree.update(new_entries)
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
    tree = ensure_all_parents_exist(tree)  # Ensure all intermediate parents exist
    tree = flatten_account_tree(tree)
    logging.info("Flattened account tree using 1-child rule.")
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

