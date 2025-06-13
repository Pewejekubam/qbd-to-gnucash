"""IIF file parser with domain-tagged logging specification.

This module provides IIF file parsing functionality as specified in core-prd-main-v3.6.5.md
with domain-tagged console and debug logging following established standards.
"""

import csv
from typing import Dict, List, Optional

from .error_handler import IIFParseError
from .logging import log_technical_detail, log_field_mismatch

class IIFParser:
    def __init__(self, file_path: str):
        self.file_path = file_path
        self.sections: Dict[str, List[Dict[str, str]]] = {}
        self.current_section: Optional[str] = None
        self.headers: Dict[str, List[str]] = {}
    
    def parse(self) -> Dict[str, List[Dict[str, str]]]:
        """Parse the IIF file and return structured data by module key.
        
        Returns:
            Dict mapping module key names to lists of module key records.
            Each record is a dict mapping field names to values.
            
        Raises:
            IIFParseError: If the file cannot be parsed or has invalid structure.
        """
        try:
            log_technical_detail(f"[IIF-PARSER] Beginning IIF file parsing: {self.file_path}")
            
            with open(self.file_path, 'r', encoding='utf-8-sig') as f:
                line_count = 0
                for line in f:
                    line_count += 1
                    line = line.strip()
                    if not line:
                        continue
                    
                    if line.startswith('!'):
                        # New module key header
                        self._process_header(line, line_count)
                    else:
                        # Data row
                        self._process_data(line, line_count)
            
            log_technical_detail(f"[IIF-PARSER] IIF parsing completed: {len(self.sections)} module keys, {line_count} lines processed")
            return self.sections
            
        except (IOError, UnicodeError) as e:
            log_technical_detail(f"[IIF-PARSER] Failed to read IIF file {self.file_path}: {str(e)}")
            raise IIFParseError(f"Failed to read IIF file {self.file_path}: {str(e)}")
    
    def _process_header(self, line: str, line_number: int) -> None:
        """Process a module key header line starting with '!'."""
        try:
            self.current_section = line.split()[0][1:]  # Remove ! and get module key name
            fields = line.split('\t')
            self.headers[self.current_section] = fields
            self.sections[self.current_section] = []
            log_technical_detail(f"[IIF-PARSER] Found module key: {self.current_section} at line {line_number}")
            
        except IndexError as e:
            log_technical_detail(f"[IIF-PARSER] Invalid header line at {line_number}: {line}")
            raise IIFParseError(f"Invalid header line at {line_number}: {line}")
    
    def _process_data(self, line: str, line_number: int) -> None:
        """Process a data line within the current module key section."""
        if not self.current_section:
            log_technical_detail(f"[IIF-PARSER] Data line found before module key header at line {line_number}")
            raise IIFParseError(f"Data line found before module key header at line {line_number}")
            
        try:
            values = line.split('\t')
            headers = self.headers[self.current_section]
            
            if len(values) != len(headers):
                # Log field mismatch to file only (not console)
                log_field_mismatch(line_number, self.current_section, len(headers), len(values))
                
                # Pad or truncate to match headers length
                if len(values) < len(headers):
                    values.extend([''] * (len(headers) - len(values)))
                else:
                    values = values[:len(headers)]
            
            record = dict(zip(headers, values))
            self.sections[self.current_section].append(record)
            
        except (KeyError, IndexError) as e:
            log_technical_detail(f"[IIF-PARSER] Failed to process data line at {line_number}: {line}")
            raise IIFParseError(f"Failed to process data line at {line_number}: {line}")