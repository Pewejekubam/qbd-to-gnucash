import re
from pathlib import Path
from typing import Optional

def extract_metadata(content: str) -> dict:
    """Extract metadata from the header of a PRD file.
    
    Looks for metadata in the format:
    Version: v1.0.0
    Type: module
    Compatible Core PRD: v3.6.3
    etc.
    
    Args:
        content: The full PRD content
        
    Returns:
        Dictionary of metadata key-value pairs
    """
    metadata = {}
    
    # Get content up to first section header
    header_match = re.search(r'^(.*?)^#\s', content, re.MULTILINE | re.DOTALL)
    if not header_match:
        return metadata
        
    header = header_match.group(1)
    
    # Extract key-value pairs
    for line in header.split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()
            metadata[key.lower()] = value
            
    return metadata

def determine_component_type(sections: list, metadata: dict) -> str:
    """Determine the component type from PRD content and metadata.
    
    Args:
        sections: List of parsed sections
        metadata: Extracted metadata dictionary
        
    Returns:
        Component type: 'module', 'interface', 'utility', etc.
    """
    # Check metadata first
    type_key = 'type'
    if type_key in metadata:
        type_value = metadata[type_key].lower()
        if type_value in ('module', 'interface', 'utility'):
            return type_value
            
    # Check content patterns
    for section in sections:
        # Module pattern: Has interface and implementation sections
        if section.number.startswith('2') and 'Interface' in section.title:
            return 'module'
        if section.number.startswith('3') and 'Implementation' in section.title:
            return 'module'
            
    # Default to utility if no clear indicators
    return 'utility'

def extract_title(sections: list) -> Optional[str]:
    """Extract the component title from the PRD sections.
    
    Args:
        sections: List of parsed sections
        
    Returns:
        Title string or None if not found
    """
    # Check first section for title
    if sections and sections[0].level == 1:
        return sections[0].title.strip()
    return None
