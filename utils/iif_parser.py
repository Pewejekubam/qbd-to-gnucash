import re
from utils.error_handler import IIFParseError

def parse_iif(filepath):
    """Parses IIF file and returns list of account records. Raises IIFParseError on malformed input."""
    records = []
    try:
        with open(filepath, encoding='utf-8', errors='ignore') as f:
            lines = f.readlines()
    except Exception as e:
        raise IIFParseError(f"Failed to read IIF file: {filepath}: {e}")

    accnt_header = None
    accnt_fields = []
    for idx, line in enumerate(lines):
        line = line.strip('\r\n')
        if line.startswith('!ACCNT'):
            accnt_header = line.split('\t')
            accnt_fields = accnt_header[1:]
            continue
        if accnt_header and not line.startswith('!') and line:
            parts = line.split('\t')
            if len(parts) < len(accnt_header):
                raise IIFParseError(f"Malformed ACCNT line at {idx+1}: {line}")
            record = dict(zip(accnt_header[1:], parts[1:]))
            # Strip whitespace and quotes from all values
            for k in record:
                v = record[k]
                if isinstance(v, str):
                    record[k] = v.strip().strip('"')
            records.append(record)
    if not records:
        raise IIFParseError("No !ACCNT records found in IIF file.")
    return records
