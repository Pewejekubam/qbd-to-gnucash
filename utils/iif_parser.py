"""
IIF Parser Utility

This module provides a utility function to extract structured records from
QuickBooks IIF files, filtering by a specific header (e.g., !ACCNT, !TERMS).
"""

import logging

def parse_iif_records(file_path, target_key):
    """
    Parses a QuickBooks IIF file and extracts rows under a specified header.

    Args:
        file_path (str): Path to the .IIF file.
        target_key (str): The target header key to extract (e.g., '!ACCNT').

    Returns:
        List[Dict[str, str]]: A list of records where each row is a dict mapping column names to values.
    """

    logging.debug("Entering parse_iif_records function.")
    logging.debug(f"File path: {file_path}, Target key: {target_key}")

    records = []
    headers = []
    capture = False

    try:
        with open(file_path, 'r', encoding='utf-8-sig') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue

                # Start capturing when the desired header block is found
                if line.startswith('!') and target_key in line:
                    headers = [h.strip() for h in line.split('\t')]
                    logging.debug(f"Captured headers: {headers}")
                    capture = True
                    continue

                # Stop capturing if a new header section begins
                if capture and line.startswith('!') and target_key not in line:
                    capture = False
                    continue

                # If we're capturing data rows, map values to headers
                if capture and not line.startswith('!'):
                    values = [v.strip() for v in line.split('\t')]
                    record = dict(zip(headers, values))
                    records.append(record)

        logging.debug(f"Parsed {len(records)} records under key '{target_key}' from file: {file_path}")
        if records:
            logging.debug(f"Sample record: {records[0]}")
        logging.debug(f"Captured records: {records}")

    except FileNotFoundError:
        logging.error(f"IIF file not found: {file_path}")
    except Exception as e:
        logging.error(f"Error while parsing IIF file: {e}")

    logging.debug(f"Parsed records: {records}")
    logging.debug("Exiting parse_iif_records function.")

    return records
