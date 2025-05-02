import csv
import json

account_hierarchy_map = {
    'BANK': 'Assets:Current Assets',
    'AR': 'Assets:Accounts Receivable',
    'FIXASSET': 'Assets:Fixed Assets',
    'AP': 'Liabilities:Current Liabilities',
    'INCOME': 'Income',
    'EXPENSE': 'Expenses',
    'EQUITY': 'Equity',
    'ASSET': 'Assets',
    'RECEIVABLE': 'Assets:Accounts Receivable',
    'PAYABLE': 'Liabilities:Current Liabilities',
}

def convert_accounts(iif_file_path, csv_file_path, mapping_file):
    accounts = {}

    # Load the JSON mapping for accounts
    with open(mapping_file, 'r') as json_file:
        mapping = json.load(json_file)

    with open(iif_file_path, 'r') as iif_file:
        section = None
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
                    # Use default rules for unmapped accounts
                    mapping_entry = mapping.get('default_rules', {}).get('unmapped_accounts', {})

                destination_hierarchy = mapping_entry.get('destination_hierarchy', 'Uncategorized')
                gnucash_account_type = mapping_entry.get('gnucash_type', 'ASSET')
                placeholder = mapping_entry.get('placeholder', False)

                full_account_name = f"{destination_hierarchy}:{account_name}"

                # Replace colons in account names to avoid conflicts with hierarchy separator
                sanitized_account_name = account_name.replace(':', '-')

                # Ensure placeholders for each level in the hierarchy
                parts = full_account_name.split(':')
                for i in range(1, len(parts)):
                    parent_account = ':'.join(parts[:i])
                    if parent_account not in accounts:
                        accounts[parent_account] = {
                            'Type': 'ASSET',  # Default type for placeholders
                            'Account Name': parent_account.split(':')[-1].replace(':', '-'),
                            'Account Code': '',
                            'Description': '',
                            'Hidden': 'F',
                            'Placeholder': 'T',  # Parent accounts are placeholders
                            'Namespace': 'CURRENCY',
                            'Symbol': 'USD',
                        }

                # Interpret the "Hidden" attribute from the IIF file
                hidden_value = account_data[11]  # Assuming column 11 corresponds to the "Hidden" field in the IIF file
                hidden = 'T' if hidden_value == 'Y' else 'F'

                # Determine the "Placeholder" attribute
                placeholder = 'T' if ':' in full_account_name else 'F'

                # Add the leaf account
                accounts[full_account_name] = {
                    'Type': gnucash_account_type,
                    'Account Name': sanitized_account_name,
                    'Account Code': account_data[7],
                    'Description': account_data[6].replace(':', '-') if account_data[6] else '',
                    'Hidden': hidden,
                    'Placeholder': placeholder,
                    'Namespace': 'CURRENCY',
                    'Symbol': 'USD',
                }

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

def map_account_type(qbd_account_type):
    account_type_map = {
        'BANK': 'BANK',
        'AR': 'RECEIVABLE',
        'AP': 'PAYABLE',
        'FIXASSET': 'ASSET',
        'INCOME': 'INCOME',
        'EXPENSE': 'EXPENSE',
        'EQUITY': 'EQUITY',
    }

    if qbd_account_type == 'BANK':
        return 'BANK'
    elif qbd_account_type in ['AR', 'RECEIVABLE']:
        return 'RECEIVABLE'
    elif qbd_account_type in ['AP', 'PAYABLE']:
        return 'PAYABLE'
    elif qbd_account_type in ['INCOME']:
        return 'INCOME'
    elif qbd_account_type in ['EXPENSE']:
        return 'EXPENSE'
    elif qbd_account_type in ['EQUITY']:
        return 'EQUITY'
    else:
        return 'ASSET'

def get_full_account_name(account_type, account_name):
    hierarchy = account_hierarchy_map.get(account_type, '')
    if hierarchy:
        return f"{hierarchy}:{account_name}"
    else:
        return account_name

def get_placeholder_type(placeholder_account):
    if placeholder_account.startswith('Assets'):
        return 'ASSET'
    elif placeholder_account.startswith('Liabilities'):
        return 'LIABILITY'
    elif placeholder_account.startswith('Equity'):
        return 'EQUITY'
    elif placeholder_account.startswith('Income'):
        return 'INCOME'
    elif placeholder_account.startswith('Expenses'):
        return 'EXPENSE'
    else:
        return 'ASSET'