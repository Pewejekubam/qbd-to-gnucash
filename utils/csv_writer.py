import csv

def write_csv(file_path, data, fieldnames):
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

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