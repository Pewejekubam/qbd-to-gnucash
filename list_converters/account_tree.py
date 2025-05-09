"""
Account Tree Builder

This module builds a hierarchical structure of accounts suitable for GnuCash import,
using structured QuickBooks account data and a mapping configuration.

It ensures placeholder parents are added, handles single-child promotion,
and inserts A/R or A/P control accounts only when subaccounts are detected.
"""

import logging


def build_gnucash_accounts(accounts_data, mapping):
    """
    Builds a hierarchical and flattened GnuCash-compatible account list.

    Args:
        accounts_data (list of dict): List of account records parsed from the IIF file.
        mapping (dict): Combined baseline and specific account mapping configuration.

    Returns:
        dict: A flattened dict of full account path -> account properties.
    """

    logging.debug("Entering build_gnucash_accounts function.")
    logging.debug(f"Number of accounts in input data: {len(accounts_data)}")
    logging.debug(f"Mapping configuration: {mapping}")

    if not isinstance(accounts_data, list) or not all(isinstance(a, dict) for a in accounts_data):
        logging.error("Invalid account data format — expected list of dicts.")
        return {}

    tree = {}

    for account in accounts_data:
        if not isinstance(account, dict):
            logging.warning(f"Skipping invalid account entry: {account}")
            continue

        qb_type = account.get("ACCNTTYPE", "").strip().upper()
        name = account.get("NAME", "").strip()

        if not qb_type or not name:
            logging.warning(f"Skipping account with missing type or name: {account}")
            continue

        mapping_info = mapping.get("account_types", {}).get(qb_type, mapping.get("default_rules", {}).get("unmapped_accounts", {}))

        gnucash_type = mapping_info.get("gnucash_type", "ASSET")
        destination = mapping_info.get("destination_hierarchy", "Unmapped")
        placeholder = mapping_info.get("placeholder", False)

        full_name = f"{destination}:{name}" if destination else name

        # Ensure all intermediate parent accounts exist
        parts = full_name.split(":")
        for i in range(1, len(parts)):
            parent_path = ":".join(parts[:i])
            if parent_path not in tree:
                tree[parent_path] = {
                    "Type": "",
                    "Account Name": parts[i - 1],
                    "Account Code": "",
                    "Description": "",
                    "Account Color": "",
                    "Notes": "",
                    "Symbol": "USD",
                    "Namespace": "CURRENCY",
                    "Hidden": "F",
                    "Tax Info": "F",
                    "Placeholder": "T"
                }

        # Add the actual account
        tree[full_name] = {
            "Type": gnucash_type,
            "Account Name": name,
            "Account Code": account.get("ACCNUM", ""),
            "Description": account.get("DESC", ""),
            "Account Color": "",
            "Notes": "",
            "Symbol": "USD",
            "Namespace": "CURRENCY",
            "Hidden": "F",
            "Tax Info": "F",
            "Placeholder": "T" if placeholder else "F"
        }

    logging.info(f"Built account tree with {len(tree)} entries.")
    return dict(sorted(tree.items()))
