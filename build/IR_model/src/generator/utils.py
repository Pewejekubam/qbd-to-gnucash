"""Utilities for parsing PRD files."""

import re
from pathlib import Path
from typing import List, Optional, Tuple

def split_section_number(section: str) -> List[int]:
    """Split a section number like '1.2.3' into [1, 2, 3]."""
    return [int(x) for x in section.split('.')]

def is_sequential(numbers: List[int]) -> bool:
    """Check if a list of numbers is sequential starting from 1."""
    if not numbers:
        return True
    expected = list(range(1, len(numbers) + 1))
    return numbers == expected

def extract_version(text: str) -> Optional[str]:
    """Extract version number from text.
    
    Examples:
    - v1.2.3
    - Version: v1.2.3
    - version 1.2.3
    """
    version_pattern = r'v?(\d+\.\d+\.\d+)'
    match = re.search(version_pattern, text, re.IGNORECASE)
    if match:
        version = match.group(1)
        return f"v{version}"
    return None

def extract_section_info(header: str) -> Tuple[str, str]:
    """Extract section number and title from header.
    
    Examples:
    - ## 1. Introduction -> ('1', 'Introduction')
    - ### 2.1 Setup -> ('2.1', 'Setup')
    """
    header = header.lstrip('#').strip()
    parts = header.split(' ', 1)
    if len(parts) < 2:
        return '', header
    
    number = parts[0].rstrip('.')
    title = parts[1].strip()
    return number, title

def normalize_path(base_path: Path, ref_path: str) -> Path:
    """Convert relative reference path to absolute path."""
    if ref_path.startswith('http://') or ref_path.startswith('https://'):
        return Path(ref_path)
    return (base_path / ref_path).resolve()

def extract_code_block(text: str) -> Optional[Tuple[str, str]]:
    """Extract language and content from a markdown code block."""
    code_block_pattern = r'```(\w*)\n(.*?)```'
    match = re.search(code_block_pattern, text, re.DOTALL)
    if match:
        lang = match.group(1) or 'text'
        content = match.group(2)
        return lang, content.strip()
    return None
