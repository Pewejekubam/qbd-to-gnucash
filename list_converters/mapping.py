import json
import os

def load_mappings(baseline_mapping_file, specific_mapping_file):
    with open(baseline_mapping_file, 'r') as baseline_file:
        baseline_mapping = json.load(baseline_file)

    if os.path.exists(specific_mapping_file):
        with open(specific_mapping_file, 'r') as specific_file:
            specific_mapping = json.load(specific_file)
        baseline_mapping.update(specific_mapping)

    return baseline_mapping

def handle_unmapped_account_types(account_types, mapping, specific_mapping_file):
    unmapped_account_types = [account_type for account_type in account_types if account_type not in mapping]

    if unmapped_account_types:
        specific_mapping = {account_type: {"gnucash_type": "PLACEHOLDER", "destination_hierarchy": "Unmapped", "placeholder": True} for account_type in unmapped_account_types}

        with open(specific_mapping_file, 'w') as specific_file:
            json.dump(specific_mapping, specific_file, indent=4)

        print(f"Unmapped account types found. A new specific mapping file has been created at {specific_mapping_file}. Please review and update it.")
        raise ValueError("Unmapped account types found. Please review and update the specific mapping file.")

    return mapping