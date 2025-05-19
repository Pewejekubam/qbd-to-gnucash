"""
IIF Parser Utility
- Parses .IIF files and extracts !ACCNT records
- Returns normalized list of account dicts
"""
import csv
from utils.error_handler import IIFParseError

def parse_iif_accounts(iif_path):
    try:
        with open(iif_path, 'r', encoding='utf-8-sig') as f:
            lines = f.readlines()
    except Exception as e:
        raise IIFParseError(f"Failed to read IIF file: {e}")

    accnt_section = False
    headers = []
    records = []
    for line in lines:
        line = line.strip()
        if not line:
            continue
        if line.startswith('!ACCNT'):
            accnt_section = True
            headers = [h.strip() for h in line.split('\t')]
            continue
        if accnt_section:
            if line.startswith('!') and not line.startswith('!ACCNT'):
                break  # End of ACCNT section
            row = [v.strip() for v in line.split('\t')]
            if len(row) != len(headers):
                continue  # skip malformed
            record = dict(zip(headers, row))
            records.append(record)
    if not records:
        raise IIFParseError("No !ACCNT records found in IIF file.")
    return records
