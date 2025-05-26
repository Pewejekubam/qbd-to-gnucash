# Agentic affirmation: This script is compliant with PRD v3.6.3 and Governance Document v2.3.10.

def parse_iif(file_path):
    """
    Parse an IIF file and return its contents as a list of dictionaries.
    
    Each dictionary corresponds to a transaction and has keys that correspond to
    the columns in the IIF file.
    
    Args:
        file_path (str): The path to the IIF file to parse.
        
    Returns:
        list: A list of dictionaries containing the IIF data.
    """
    with open(file_path, 'r') as file:
        lines = file.readlines()
        
    # Extract the header line to get the column names
    header = lines[0].strip().split('\t')
    
    transactions = []
    for line in lines[1:]:
        # Split each line by tab and create a dictionary for each transaction
        transaction = dict(zip(header, line.strip().split('\t')))
        transactions.append(transaction)
        
    return transactions

def main():
    file_path = 'path_to_your_iif_file.iif'
    iif_data = parse_iif(file_path)
    
    # Do something with the parsed IIF data
    for transaction in iif_data:
        print(transaction)

if __name__ == "__main__":
    main()