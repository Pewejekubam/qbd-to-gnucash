import csv
import json
import os
import logging


def load_mappings(baseline_mapping_file, specific_mapping_file):
    """
    Load and merge baseline and specific mappings from JSON files.
    
    Args:
        baseline_mapping_file: Path to the baseline mapping JSON file
        specific_mapping_file: Path to the specific mapping JSON file
    
    Returns:
        dict: Merged mapping configuration
    """
    # Load the baseline mapping
    try:
        with open(baseline_mapping_file, 'r') as baseline_file:
            baseline_mapping = json.load(baseline_file)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Error loading baseline mapping file: {e}")
        return None

    # Initialize or load specific mapping
    if os.path.exists(specific_mapping_file):
        try:
            with open(specific_mapping_file, 'r') as specific_file:
                specific_mapping = json.load(specific_file)
        except json.JSONDecodeError as e:
            print(f"Error loading specific mapping file: {e}")
            specific_mapping = {"account_types": {}, "default_rules": baseline_mapping["default_rules"]}
    else:
        specific_mapping = {"account_types": {}, "default_rules": baseline_mapping["default_rules"]}

    # Ensure the configuration has the required basic accounting type mappings
    if "basic_accounting_types" not in baseline_mapping:
        # Add the standard mapping as a fallback
        baseline_mapping["basic_accounting_types"] = {
            "ASSET": "Assets",
            "LIABILITY": "Liabilities",
            "EQUITY": "Equity", 
            "INCOME": "Income",
            "EXPENSE": "Expenses"
        }

    # Merge baseline and specific mappings
    return {
        "account_types": {**baseline_mapping.get("account_types", {}), **specific_mapping.get("account_types", {})},
        "default_rules": specific_mapping.get("default_rules", {}),
        "basic_accounting_types": baseline_mapping.get("basic_accounting_types", {})
    }


def extract_accounts_from_iif(iif_file_path):
    """
    Extract account data from QuickBooks IIF file.
    
    Args:
        iif_file_path: Path to the QuickBooks IIF file
    
    Returns:
        tuple: (accounts_data, account_types, accounts_by_type)
    """
    accounts_data = {}
    account_types = {}
    accounts_by_type = {}
    
    try:
        with open(iif_file_path, 'r') as iif_file:
            section = None
            for line in iif_file:
                line = line.strip().replace('"', '')
                if line.startswith('!ACCNT'):
                    section = 'ACCNT'
                    continue
                elif not line or line.startswith('!'):
                    section = None
                    continue
                
                if section == 'ACCNT' and line.startswith('ACCNT'):
                    account_data = line.split('\t')
                    if len(account_data) < 12:
                        print(f"Warning: Invalid account data format: {line}")
                        continue
                    
                    account_name = account_data[1]
                    account_type = account_data[4]
                    
                    # Store account data
                    accounts_data[account_name] = {
                        'type': account_type,
                        'code': account_data[7] if len(account_data) > 7 else '',
                        'description': account_data[6] if len(account_data) > 6 and account_data[6] else '',
                        'hidden': 'T' if len(account_data) > 11 and account_data[11] == 'Y' else 'F'
                    }
                    
                    # Track account types and count
                    account_types[account_type] = account_types.get(account_type, 0) + 1
                    
                    # Group accounts by type for easier processing
                    if account_type not in accounts_by_type:
                        accounts_by_type[account_type] = []
                    accounts_by_type[account_type].append(account_name)
                    
        return accounts_data, account_types, accounts_by_type
    except FileNotFoundError:
        print(f"Error: IIF file not found: {iif_file_path}")
        return {}, {}, {}


def handle_unmapped_account_types(account_types, mapping, specific_mapping_file):
    """
    Identify unmapped account types and update the mapping accordingly.
    
    Args:
        account_types: Dictionary of account types found in the IIF file
        mapping: Current mapping configuration
        specific_mapping_file: Path to the specific mapping JSON file
    
    Returns:
        dict: Updated mapping configuration
    """
    # Define the five basic accounting types in GnuCash
    basic_account_types = {
        "ASSET": "Assets",
        "LIABILITY": "Liabilities",
        "EQUITY": "Equity", 
        "INCOME": "Income",
        "EXPENSE": "Expenses"
    }
    
    # Get type mapping from configuration instead of hardcoding
    account_type_to_basic = {}
    
    # Build the mapping from configuration
    for qb_type, mapping_info in mapping["account_types"].items():
        gnucash_type = mapping_info.get("gnucash_type", "ASSET")
        # Map each QuickBooks type to its basic GnuCash type
        account_type_to_basic[qb_type] = gnucash_type
        # Also include the GnuCash type mapping to itself
        account_type_to_basic[gnucash_type] = gnucash_type
    
    # Identify unmapped account types and update mapping with default rules
    unmapped_types = {}
    for account_type in account_types:
        if account_type not in mapping["account_types"]:
            # Use default rules from the JSON configuration for unmapped accounts
            default_rule = mapping["default_rules"].get("unmapped_accounts", {
                "gnucash_type": "ASSET",
                "destination_hierarchy": "Assets:Uncategorized",
                "placeholder": False
            })
            
            # Ensure the default rule maps to one of the five basic types from config
            default_gnucash_type = default_rule["gnucash_type"]
            # If the type is in our derived mapping, use it; otherwise try the default type directly
            basic_type = account_type_to_basic.get(default_gnucash_type, default_gnucash_type)
            
            # Validate against the basic accounting types from config
            if basic_type not in mapping.get("basic_accounting_types", {}):
                print(f"Warning: Default rule uses invalid GnuCash type '{default_gnucash_type}'. Using 'ASSET' instead.")
                basic_type = "ASSET"
                
            # Make sure the destination hierarchy starts with the appropriate top-level
            destination = default_rule["destination_hierarchy"]
            top_level = mapping["basic_accounting_types"].get(basic_type, "Assets")
            
            if not destination.startswith(top_level):
                # Adjust the destination to start with the correct top level
                destination = f"{top_level}:{destination.split(':', 1)[1] if ':' in destination else 'Uncategorized'}"
            
            unmapped_types[account_type] = {
                "gnucash_type": default_rule["gnucash_type"],  # Keep the original type
                "destination_hierarchy": destination,  # Use the corrected destination
                "placeholder": default_rule.get("placeholder", False)
            }
    
    # Update specific mapping if we found unmapped types
    if unmapped_types:
        specific_mapping = {"account_types": {}, "default_rules": mapping["default_rules"]}
        
        # Load existing specific mapping if it exists
        if os.path.exists(specific_mapping_file):
            try:
                with open(specific_mapping_file, 'r') as specific_file:
                    specific_mapping = json.load(specific_file)
            except json.JSONDecodeError:
                pass
        
        specific_mapping["account_types"].update(unmapped_types)
        try:
            with open(specific_mapping_file, 'w') as specific_file:
                json.dump(specific_mapping, specific_file, indent=4)
            print(f"Specific mapping file updated with {len(unmapped_types)} unmapped account types.")
        except IOError as e:
            print(f"Warning: Could not write to specific mapping file: {e}")
        
        # Update the mapping with the newly added types
        mapping["account_types"].update(unmapped_types)
    
    return mapping, mapping.get("basic_accounting_types", {})


def build_gnucash_accounts(accounts_data, mapping):
    """
    Generate GnuCash account structure from QuickBooks account data.
    
    Args:
        accounts_data: Dictionary containing QuickBooks account data
        mapping: Mapping configuration for account types
    
    Returns:
        dict: GnuCash account structure
    """
    logging.basicConfig(level=logging.INFO)
    gnucash_accounts = {}
    
    # Get basic accounting types from the config
    basic_account_types = mapping.get("basic_accounting_types", {
        "ASSET": "Assets",
        "LIABILITY": "Liabilities",
        "EQUITY": "Equity", 
        "INCOME": "Income",
        "EXPENSE": "Expenses"
    })
    
    # Add top-level placeholders
    for basic_type, account_name in basic_account_types.items():
        gnucash_accounts[account_name] = {
            'Type': basic_type,
            'Account Name': account_name,
            'Account Code': '',
            'Description': f'Top-level {account_name} account',
            'Hidden': 'F',
            'Placeholder': 'T',
            'Namespace': 'CURRENCY',
            'Symbol': 'USD',
        }
    
    # Process accounts from the IIF file
    for account_name, data in accounts_data.items():
        try:
            account_type = data['type']
            mapping_entry = mapping["account_types"].get(account_type)
            if not mapping_entry:
                logging.warning(f"No mapping found for account type: {account_type}")
                continue
            
            gnucash_type = mapping_entry.get('gnucash_type', 'ASSET')
            destination = mapping_entry.get('destination_hierarchy', 'Uncategorized')
            top_level = basic_account_types.get(gnucash_type, "Assets")
            
            if not destination.startswith(top_level):
                destination = f"{top_level}:{destination.split(':', 1)[1]}" if ':' in destination else top_level
            
            full_account_name = f"{destination}:{account_name}"
            parts = full_account_name.split(':')
            current_path = ""
            
            for i, part in enumerate(parts):
                current_path = f"{current_path}:{part}" if current_path else part
                if i == len(parts) - 1:
                    gnucash_accounts[current_path] = {
                        'Type': gnucash_type,
                        'Account Name': part,
                        'Account Code': data['code'],
                        'Description': data['description'],
                        'Hidden': data['hidden'],
                        'Placeholder': 'F',
                        'Namespace': 'CURRENCY',
                        'Symbol': 'USD',
                    }
                elif current_path not in gnucash_accounts:
                    gnucash_accounts[current_path] = {
                        'Type': gnucash_type,
                        'Account Name': part,
                        'Account Code': '',
                        'Description': f'Parent account for {part}',
                        'Hidden': 'F',
                        'Placeholder': 'T',
                        'Namespace': 'CURRENCY',
                        'Symbol': 'USD',
                    }
        except Exception as e:
            logging.error(f"Error processing account '{account_name}': {e}", exc_info=True)
    
    # Remove redundant placeholders
    for account in list(gnucash_accounts.keys()):
        try:
            # Ensure the account still exists in gnucash_accounts
            if account not in gnucash_accounts:
                continue
            
            if gnucash_accounts[account]['Placeholder'] == 'T':
                # Check if it has exactly one child
                children = [key for key in gnucash_accounts if key.startswith(f"{account}:")]
                if len(children) == 1:
                    child = children[0]
                    # Promote the child and remove the placeholder
                    gnucash_accounts[account] = gnucash_accounts.pop(child)
        except Exception as e:
            logging.error(f"Error processing placeholder '{account}': {e}", exc_info=True)
    
    return gnucash_accounts


def write_gnucash_csv(gnucash_accounts, csv_file_path):
    """
    Write the GnuCash account structure to a CSV file.
    
    Args:
        gnucash_accounts: Dictionary containing GnuCash account structure
        csv_file_path: Output path for the GnuCash CSV file
    """
    # Sort accounts to ensure parent accounts are written before child accounts
    sorted_accounts = sorted(gnucash_accounts.items(), key=lambda x: x[0])
    
    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = [
                'Type', 'Full Account Name', 'Account Name', 'Account Code', 
                'Description', 'Account Color', 'Notes', 'Symbol', 'Namespace', 
                'Hidden', 'Tax Info', 'Placeholder'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            
            writer.writeheader()
            for full_account_name, data in sorted_accounts:
                writer.writerow({
                    'Type': data.get('Type', ''),
                    'Full Account Name': full_account_name,
                    'Account Name': data.get('Account Name', ''),
                    'Account Code': data.get('Account Code', ''),
                    'Description': data.get('Description', ''),
                    'Account Color': '',
                    'Notes': '',
                    'Symbol': data.get('Symbol', 'USD'),
                    'Namespace': data.get('Namespace', 'CURRENCY'),
                    'Hidden': data.get('Hidden', 'F'),
                    'Tax Info': 'F',
                    'Placeholder': data.get('Placeholder', 'F'),
                })
        
        print(f"Successfully converted {len(gnucash_accounts)} accounts to GnuCash CSV format.")
        
    except IOError as e:
        print(f"Error writing to CSV file: {e}")


def convert_accounts(iif_file_path, csv_file_path, baseline_mapping_file, specific_mapping_file):
    """
    Convert QuickBooks IIF account data to GnuCash CSV format.
    
    Args:
        iif_file_path: Path to the QuickBooks IIF file
        csv_file_path: Output path for the GnuCash CSV file
        baseline_mapping_file: Path to the baseline mapping JSON file
        specific_mapping_file: Path to the specific mapping JSON file (will be created if it doesn't exist)
    """
    # Step 1: Load configuration mappings
    mapping = load_mappings(baseline_mapping_file, specific_mapping_file)
    if mapping is None:
        return
    
    # Step 2: Extract account data from IIF file
    accounts_data, account_types, accounts_by_type = extract_accounts_from_iif(iif_file_path)
    if not accounts_data:
        return
    
    # Step 3: Handle unmapped account types
    mapping, _ = handle_unmapped_account_types(account_types, mapping, specific_mapping_file)
    
    # Step 4: Build GnuCash account structure
    gnucash_accounts = build_gnucash_accounts(accounts_data, mapping)
    
    # Step 5: Write output to CSV
    write_gnucash_csv(gnucash_accounts, csv_file_path)


if __name__ == "__main__":
    # Example usage
    convert_accounts(
        "accounts.iif",
        "gnucash_accounts.csv",
        "baseline_mapping.json",
        "specific_mapping.json"
    )