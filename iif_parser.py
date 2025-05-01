import re

def parse_iif_file(file_path):
    # Read the IIF file
    with open(file_path, 'r') as f:
        lines = f.readlines()

    # Initialize an empty dictionary to store the data
    data = {}

    # Iterate over the lines in the file
    for line in lines:
        # Use regular expressions to extract the relevant data
        match = re.match(r'!(\w+)\s+(.*)', line)
        if match:
            # Extract the header and data
            header = match.group(1)
            values = match.group(2).split('\t')

            # Store the data in the dictionary
            if header not in data:
                data[header] = []
            data[header].append(values)

    return data