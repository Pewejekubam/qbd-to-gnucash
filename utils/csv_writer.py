import csv
import logging

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
        gnucash_accounts: List of dictionaries containing GnuCash account structure
        csv_file_path: Output path for the GnuCash CSV file
    """
    logging.debug("Entering write_gnucash_csv function.")
    logging.debug(f"CSV file path: {csv_file_path}")
    logging.debug(f"Number of accounts to write: {len(gnucash_accounts)}")
    
    # Ensure gnucash_accounts is a list of dicts
    if not isinstance(gnucash_accounts, list) or not all(isinstance(a, dict) for a in gnucash_accounts):
        raise TypeError("Expected gnucash_accounts to be a list of dictionaries")

    logging.debug("Validated gnucash_accounts is a list of dictionaries.")
    
    # Log the number of accounts
    logging.info(f"About to write {len(gnucash_accounts)} accounts to CSV file")
    
    # Sort accounts to ensure parent accounts are written before child accounts
    sorted_accounts = sorted(gnucash_accounts, key=lambda x: x['Full Account Name'])
    logging.debug(f"Sorted accounts for CSV: {sorted_accounts}")
    
    # Log the first row explicitly to avoid misinterpretation
    first_row = sorted_accounts[0]
    logging.debug(f"First row key: {first_row['Full Account Name']}")
    logging.debug(f"First row data: {first_row}")
    
    try:
        with open(csv_file_path, 'w', newline='') as csvfile:
            fieldnames = [
                'Type', 'Full Account Name', 'Account Name', 'Account Code', 
                'Description', 'Account Color', 'Notes', 'Symbol', 'Namespace', 
                'Hidden', 'Tax Info', 'Placeholder'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
            
            writer.writeheader()
            logging.info(f"CSV header written, now writing {len(sorted_accounts)} account records")
            
            account_count = 0
            for data in sorted_accounts:
                try:
                    row_data = {
                        'Type': data.get('Type', ''),
                        'Full Account Name': data.get('Full Account Name', ''),
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
                    }
                    writer.writerow(row_data)
                    account_count += 1
                    
                    # Log every 10 accounts to avoid excessive logging
                    if account_count % 10 == 0:
                        logging.info(f"Wrote {account_count} accounts so far")
                        logging.debug(f"Sample row: {row_data}")
                        
                except Exception as e:
                    logging.error(f"Error writing account {data.get('Full Account Name')}: {str(e)}")
                    # Continue with next account
            
            logging.info(f"Finished writing {account_count} accounts to CSV")
        
        logging.info(f"Successfully converted {len(gnucash_accounts)} accounts to GnuCash CSV format.")
        
    except IOError as e:
        logging.error(f"Error writing to CSV file: {e}")
    except Exception as e:
        logging.error(f"Unexpected error writing CSV: {str(e)}", exc_info=True)
    
    logging.debug("Exiting write_gnucash_csv function.")
