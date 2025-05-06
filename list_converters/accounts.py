import csv
import json
import os

def convert_accounts(iif_file_path, csv_file_path, baseline_mapping_file, specific_mapping_file):
    accounts = {}

    # Load the baseline mapping
    with open(baseline_mapping_file, 'r') as baseline_file:
        baseline_mapping = json.load(baseline_file)

    # Check if the specific mapping file exists
    if os.path.exists(specific_mapping_file):
        with open(specific_mapping_file, 'r') as specific_file:
            specific_mapping = json.load(specific_file)
    else:
        specific_mapping = {"account_types": {}, "default_rules": baseline_mapping["default_rules"]}

    # Merge baseline and specific mappings
    mapping = {
        "account_types": {**baseline_mapping["account_types"], **specific_mapping["account_types"]},
        "default_rules": specific_mapping["default_rules"]
    }

    with open(iif_file_path, 'r') as iif_file:
        section = None
        account_type_counts = {}
        unmapped_accounts = {}

        # First pass: Identify unmapped accounts
        for line in iif_file:
            line = line.strip().replace('"', '')
            if line.startswith('!ACCNT'):
                section = 'ACCNT'
            elif section == 'ACCNT' and line.startswith('ACCNT'):
                account_data = line.split('\t')
                account_type = account_data[4]

                # Count occurrences of each account type
                account_type_counts[account_type] = account_type_counts.get(account_type, 0) + 1

                # Check if account type is in the mapping
                if account_type not in mapping["account_types"]:
                    # Use the account_type from IIF file to determine correct GnuCash type
                    gnucash_type = "ASSET"  # Default
                    destination = "Assets:Uncategorized"
                    
                    # Map based on QuickBooks account type abbreviations
                    if account_type == "EXP":
                        gnucash_type = "EXPENSE"
                        destination = "Expenses:Uncategorized"
                    elif account_type in ["INC", "INCOME"]:
                        gnucash_type = "INCOME"
                        destination = "Income:Uncategorized"
                    elif account_type in ["EQUITY"]:
                        gnucash_type = "EQUITY"
                        destination = "Equity:Uncategorized"
                    elif account_type in ["OCLIAB", "LTLIAB"]:
                        gnucash_type = "LIABILITY"
                        destination = "Liabilities:Uncategorized"
                    
                    unmapped_accounts[account_type] = {
                        "gnucash_type": gnucash_type,
                        "destination_hierarchy": destination,
                        "placeholder": False
                    }

        # Update the specific mapping file with unmapped accounts
        specific_mapping["account_types"].update(unmapped_accounts)
        with open(specific_mapping_file, 'w') as specific_file:
            json.dump(specific_mapping, specific_file, indent=4)
        print(f"Specific mapping file updated with {len(unmapped_accounts)} unmapped accounts.")

        # Update the mapping with the newly created specific mapping
        mapping["account_types"].update(unmapped_accounts)

        # Reset file pointer for the second pass
        iif_file.seek(0)
        section = None

        # Second pass: Process accounts and generate CSV data
        additional_unmapped_accounts = {}
        for line in iif_file:
            line = line.strip().replace('"', '')
            if line.startswith('!ACCNT'):
                section = 'ACCNT'
            elif section == 'ACCNT' and line.startswith('ACCNT'):
                account_data = line.split('\t')
                account_type = account_data[4]
                account_name = account_data[1]

                # Check if account type is in the mapping
                mapping_entry = mapping.get('account_types', {}).get(account_type)
                if not mapping_entry:
                    # Use default rules for unmapped accounts, but respect the original account type
                    gnucash_type = "ASSET"  # Default
                    destination = "Assets:Uncategorized"
                    
                    # Map based on QuickBooks account type abbreviations
                    if account_type == "EXP":
                        gnucash_type = "EXPENSE"
                        destination = "Expenses:Uncategorized"
                    elif account_type in ["INC", "INCOME"]:
                        gnucash_type = "INCOME"
                        destination = "Income:Uncategorized"
                    elif account_type in ["EQUITY"]:
                        gnucash_type = "EQUITY"
                        destination = "Equity:Uncategorized"
                    elif account_type in ["OCLIAB", "LTLIAB"]:
                        gnucash_type = "LIABILITY"
                        destination = "Liabilities:Uncategorized"
                    
                    mapping_entry = {
                        'gnucash_type': gnucash_type,
                        'destination_hierarchy': destination,
                        'placeholder': False
                    }
                    # Add to additional unmapped accounts
                    additional_unmapped_accounts[account_type] = mapping_entry

                # Map the destination hierarchy and type
                destination_hierarchy = mapping_entry.get('destination_hierarchy', 'Uncategorized')
                gnucash_account_type = mapping_entry.get('gnucash_type', 'ASSET')

                # Determine if nesting is required
                if account_type_counts[account_type] > 1:
                    full_account_name = f"{destination_hierarchy}:{account_name}"
                else:
                    full_account_name = account_name

                # Replace colons in account names to avoid conflicts with hierarchy separator
                sanitized_account_name = account_name.replace(':', '-')

                # Ensure placeholders for each level in the hierarchy if nesting is required
                if account_type_counts[account_type] > 1:
                    parts = full_account_name.split(':')
                    for i in range(1, len(parts)):
                        parent_account = ':'.join(parts[:i])
                        if parent_account not in accounts:
                            accounts[parent_account] = {
                                'Type': mapping_entry['gnucash_type'],
                                'Account Name': parent_account.split(':')[-1].replace(':', '-'),
                                'Account Code': '',
                                'Description': '',
                                'Hidden': 'F',
                                'Placeholder': 'T',
                                'Namespace': 'CURRENCY',
                                'Symbol': 'USD',
                            }

                # Interpret the "Hidden" attribute from the IIF file
                hidden_value = account_data[11]
                hidden = 'T' if hidden_value == 'Y' else 'F'

                # Add the account
                accounts[full_account_name] = {
                    'Type': gnucash_account_type,
                    'Account Name': sanitized_account_name,
                    'Account Code': account_data[7],
                    'Description': account_data[6].replace(':', '-') if account_data[6] else '',
                    'Hidden': hidden,
                    'Placeholder': 'F',
                    'Namespace': 'CURRENCY',
                    'Symbol': 'USD',
                }

        # Update the specific mapping file with additional unmapped accounts
        if additional_unmapped_accounts:
            specific_mapping["account_types"].update(additional_unmapped_accounts)
            with open(specific_mapping_file, 'w') as specific_file:
                json.dump(specific_mapping, specific_file, indent=4)
            print(f"Specific mapping file updated with {len(additional_unmapped_accounts)} additional unmapped accounts.")

    # Ensure the five basic accounting types are present
    accounts = ensure_basic_accounts(accounts, baseline_mapping)

    # Sort accounts to ensure parent accounts are written before child accounts
    sorted_accounts = sorted(accounts.items(), key=lambda x: x[0])

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Type', 'Full Account Name', 'Account Name', 'Account Code', 'Description', 'Account Color', 'Notes', 'Symbol', 'Namespace', 'Hidden', 'Tax Info', 'Placeholder']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

        writer.writeheader()
        for account, data in sorted_accounts:
            writer.writerow({
                'Type': data.get('Type', ''),
                'Full Account Name': account,
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

    print(f"Converted {len(accounts)} accounts")

def ensure_basic_accounts(accounts, baseline_mapping):
    """
    Ensure the five basic accounting types are present in the accounts dictionary.
    """
    for account, account_type in baseline_mapping["account_types"].items():
        if account not in accounts:
            accounts[account] = {
                'Type': account_type['gnucash_type'],
                'Account Name': account,
                'Account Code': '',
                'Description': f'Top-level {account} account',
                'Hidden': 'F',
                'Placeholder': 'T',
                'Namespace': 'CURRENCY',
                'Symbol': 'USD',
            }

    return accounts