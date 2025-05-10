import csv
import logging

def write_csv(file_path, data, fieldnames):
    """
    Write the data to CSV at the given path with the provided fieldnames.
    """
    with open(file_path, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for row in data:
            writer.writerow(row)

def sort_accounts_hierarchically(accounts):
    """
    Sort accounts hierarchically to ensure parent accounts are listed before their children.

    Args:
        accounts: Dict[str, dict] where key is Full Account Name and value is account details

    Returns:
        List of tuples sorted hierarchically (Full Account Name, account details)
    """
    def get_hierarchy_depth(account_name):
        return account_name.count(":")

    sorted_accounts = sorted(accounts.items(), key=lambda x: (get_hierarchy_depth(x[0]), x[0]))
    
    # Logging the sorted accounts for debugging
    logging.debug("Sorted accounts:")
    for full_name, data in sorted_accounts[:5]:
        logging.debug(f"  {full_name}")
    
    return sorted_accounts

def write_gnucash_csv(gnucash_accounts, csv_file_path):
    """
    Write the GnuCash account structure to a CSV file.
    
    Args:
        gnucash_accounts: Dict[str, dict] where key is Full Account Name and value is account details
        csv_file_path: Output path for the GnuCash CSV file
    """
    logging.debug("Entering write_gnucash_csv function.")
    logging.debug(f"CSV file path: {csv_file_path}")
    logging.debug(f"Number of accounts to write: {len(gnucash_accounts)}")

    assert isinstance(gnucash_accounts, dict) and all(isinstance(v, dict) for v in gnucash_accounts.values()), "write_gnucash_csv expects a dictionary of dictionaries as input."
    logging.debug(f"First 5 accounts to write: {list(gnucash_accounts.items())[:5]}")

    if not isinstance(gnucash_accounts, dict):
        raise TypeError("Expected gnucash_accounts to be a dict")

    # Step 1: Log and ensure we correctly inject missing parents
    missing_parents = set()
    for full_name, _ in gnucash_accounts.items():
        parent_path = ":".join(full_name.split(":")[:-1])
        if parent_path and parent_path not in gnucash_accounts:
            missing_parents.add(parent_path)
    
    logging.debug(f"Missing parent accounts: {missing_parents}")

    # Ensure all missing parent accounts are added as placeholders
    for missing_parent in missing_parents:
        gnucash_accounts[missing_parent] = {
            'Type': '',
            'Account Name': missing_parent.split(":")[-1],
            'Account Code': '',
            'Description': '',
            'Account Color': '',
            'Notes': '',
            'Symbol': 'USD',
            'Namespace': 'CURRENCY',
            'Hidden': 'F',
            'Tax Info': 'F',
            'Placeholder': 'T'
        }
    
    # Step 2: Sort accounts hierarchically (parent accounts first)
    sorted_accounts = sort_accounts_hierarchically(gnucash_accounts)

    # Step 3: Log the first few sorted accounts for verification
    logging.debug("Sorted accounts list:")
    for full_name, data in sorted_accounts[:5]:
        logging.debug(f"  {full_name}: {data}")
    
    # Step 4: Write to CSV
    fieldnames = [
        'Type', 'Full Account Name', 'Account Name', 'Account Code',
        'Description', 'Account Color', 'Notes', 'Symbol', 'Namespace',
        'Hidden', 'Tax Info', 'Placeholder'
    ]

    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            writer.writeheader()
            account_count = 0
            for full_name, data in sorted_accounts:
                row_data = {
                    'Type': data.get('Type', ''),
                    'Full Account Name': full_name,
                    'Account Name': data.get('Account Name', ''),
                    'Account Code': data.get('Account Code', ''),
                    'Description': data.get('Description', ''),
                    'Account Color': '',
                    'Notes': '',
                    'Symbol': data.get('Symbol', 'USD'),
                    'Namespace': data.get('Namespace', 'CURRENCY'),
                    'Hidden': data.get('Hidden', 'F'),
                    'Tax Info': 'F',
                    'Placeholder': data.get('Placeholder', 'F')
                }
                writer.writerow(row_data)
                account_count += 1

                if account_count % 10 == 0:
                    logging.info(f"Wrote {account_count} accounts so far")
                    logging.debug(f"Sample row: {row_data}")

            logging.info(f"Finished writing {account_count} accounts to CSV")

    except IOError as e:
        logging.error(f"Error writing to CSV file: {e}")
    except Exception as e:
        logging.error(f"Unexpected error writing CSV: {str(e)}", exc_info=True)

    logging.debug("Exiting write_gnucash_csv function.")
