"""Parser for interface contracts in PRD files."""

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Union

from .utils import extract_code_block, extract_version

@dataclass
class InterfaceContract:
    """Represents a parsed interface contract."""
    name: str
    type: str  # 'TypedDict', 'JSON Schema', etc.
    version: str
    definition: Dict
    dependencies: List[str]
    source_section: str  # Section number where interface was found

class InterfaceParser:
    """Parser for interface contracts in PRD files."""
    
    INTERFACE_MARKERS = [
        'interface',
        'type',
        'schema',
        'contract',
        'TypedDict',
    ]
    
    def __init__(self, prd_path: Path):
        self.prd_path = Path(prd_path)
        self.interfaces: List[InterfaceContract] = []
    
    def parse_section(self, section_number: str, content: str) -> List[InterfaceContract]:
        """Parse interfaces from a section's content."""
        interfaces = []
        
        # Look for TypeScript/JSON Schema code blocks
        code_block = extract_code_block(content)
        if code_block:
            lang, code = code_block
            if lang.lower() in ('typescript', 'ts'):
                interface = self._parse_typescript(code, section_number)
                if interface:
                    interfaces.append(interface)
            elif lang.lower() in ('json', 'jsonschema'):
                interface = self._parse_json_schema(code, section_number)
                if interface:
                    interfaces.append(interface)
        
        return interfaces
    
    def _parse_typescript(self, code: str, section: str) -> Optional[InterfaceContract]:
        """Parse TypeScript interface/type definition."""
        # Look for interface or type definition
        lines = code.split('\n')
        first_line = lines[0].strip()
        
        for marker in self.INTERFACE_MARKERS:
            if marker in first_line.lower():
                # Extract name
                name = first_line.split(marker)[1].strip().split('{')[0].strip()
                
                # Parse definition into dict format
                definition = {}
                current_field = None
                
                for line in lines[1:]:
                    line = line.strip()
                    if not line or line == '}':
                        continue
                    
                    # Handle field definition
                    if ':' in line:
                        field_name, field_type = line.split(':', 1)
                        field_name = field_name.strip()
                        field_type = field_type.strip().rstrip(';')
                        
                        definition[field_name] = {
                            'type': field_type,
                            'optional': field_name.endswith('?'),
                        }
                
                return InterfaceContract(
                    name=name,
                    type='TypedDict',
                    version=extract_version(code) or 'v1.0.0',
                    definition=definition,
                    dependencies=self._extract_dependencies(code),
                    source_section=section
                )
        
        return None
    
    def _parse_json_schema(self, code: str, section: str) -> Optional[InterfaceContract]:
        """Parse JSON Schema definition."""
        try:
            schema = json.loads(code)
            if '$schema' in schema or 'type' in schema:
                name = schema.get('title', 'Schema')
                return InterfaceContract(
                    name=name,
                    type='JSON Schema',
                    version=extract_version(code) or 'v1.0.0',
                    definition=schema,
                    dependencies=self._extract_dependencies(code),
                    source_section=section
                )
        except json.JSONDecodeError:
            return None
        
        return None
    
    def _extract_dependencies(self, code: str) -> List[str]:
        """Extract dependencies from interface code."""
        deps = []
        
        # Look for import statements
        for line in code.split('\n'):
            if 'import' in line:
                # Extract module name from import statement
                match = re.search(r'from [\'"](.+)[\'"]', line)
                if match:
                    deps.append(match.group(1))
        
        # Look for references to other types
        type_refs = re.findall(r':\s*(\w+)[\[\],;]', code)
        deps.extend(ref for ref in type_refs if ref not in ('string', 'number', 'boolean', 'any'))
        
        return list(set(deps))
