import csv

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

def convert_accounts(iif_file_path, csv_file_path):
    accounts = {}

    with open(iif_file_path, 'r') as iif_file:
        section = None
        for line in iif_file:
            line = line.strip().replace('"', '')
            if line.startswith('!ACCNT'):
                section = 'ACCNT'
            elif section == 'ACCNT' and line.startswith('ACCNT'):
                account_data = line.split('\t')
                if len(account_data) > 5:
                    account_name = account_data[1]
                    account_type = account_data[4]
                    full_account_name = get_full_account_name(account_type, account_name)

                    # Construct hierarchy
                    parts = full_account_name.split(':')
                    for i in range(1, len(parts)):
                        parent_account = ':'.join(parts[:i])
                        if parent_account not in accounts:
                            accounts[parent_account] = {
                                'Type': get_placeholder_type(parent_account),
                                'Account Name': parent_account.split(':')[-1],
                                'Account Code': '',
                                'Description': '',
                                'Hidden': 'F',
                                'Placeholder': 'T',
                            }

                    # Initialize leaf account
                    gnucash_account_type = map_account_type(account_type)
                    accounts[full_account_name] = {
                        'Type': gnucash_account_type,
                        'Account Name': account_name,
                        'Account Code': account_data[7],
                        'Description': account_data[6] if account_data[6] else '',
                        'Hidden': 'F' if account_data[12] == 'N' else 'T',
                        'Placeholder': 'F',
                    }

    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['Type', 'Full Account Name', 'Account Name', 'Account Code', 'Description', 'Account Color', 'Notes', 'Symbol', 'Namespace', 'Hidden', 'Tax Info', 'Placeholder']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)

        writer.writeheader()
        for account, data in accounts.items():
            writer.writerow({
                'Type': data.get('Type', ''),
                'Full Account Name': account,
                'Account Name': data.get('Account Name', ''),
                'Account Code': data.get('Account Code', ''),
                'Description': data.get('Description', ''),
                'Account Color': '',
                'Notes': '',
                'Symbol': '',
                'Namespace': 'CURRENCY',
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