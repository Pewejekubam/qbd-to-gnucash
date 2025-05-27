"""Schema Validator Module.

This module implements validation of JSON Schema and TypeScript interface definitions
found in PRDs according to prd-governance-model-v2.3.10.md.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional
import json
import re
from dataclasses import dataclass

@dataclass
class SchemaError:
    """Represents a schema validation error."""
    message: str
    location: str  # File location or schema identifier
    details: Optional[str] = None

class SchemaValidator:
    """Validates schema and interface definitions in PRDs."""
    
    def __init__(self, prd_path: str):
        """Initialize validator with path to PRD file."""
        self.prd_path = Path(prd_path)
        self.content = self.prd_path.read_text()
        self.errors: List[SchemaError] = []

    def _extract_schemas(self) -> Dict[str, Any]:
        """Extract JSON Schema and TypeScript interface definitions."""
        schemas = {}
        # Find code blocks with schema content
        code_blocks = re.finditer(r'```([^\n]*)\n(.*?)```', self.content, re.DOTALL)
        
        for block in code_blocks:
            lang, content = block.groups()
            if lang.lower() in ('json', 'typescript', 'ts'):
                # Try to identify schema name from preceding header
                name_match = re.search(
                    r'#{1,4}\s+([^\n]+)\n\s*```[^\n]*\n',
                    self.content[:block.start()]
                )
                name = name_match.group(1) if name_match else f"schema_{len(schemas)}"
                schemas[name] = {
                    'type': lang.lower(),
                    'content': content.strip()
                }
        
        return schemas

    def validate_json_schema(self, content: str) -> List[str]:
        """Validate JSON Schema definition."""
        errors = []
        try:
            schema = json.loads(content)
            
            # Check schema has required fields
            if not isinstance(schema, dict):
                errors.append("Schema must be a JSON object")
                return errors
                
            if "type" not in schema:
                errors.append("Schema missing required 'type' field")
                
            if "properties" in schema and not isinstance(schema["properties"], dict):
                errors.append("Schema 'properties' must be an object")
                
            # Validate property definitions
            if "properties" in schema:
                for prop, def_ in schema["properties"].items():
                    if not isinstance(def_, dict):
                        errors.append(f"Property '{prop}' definition must be an object")
                    if "type" not in def_:
                        errors.append(f"Property '{prop}' missing required 'type'")
                        
        except json.JSONDecodeError as e:
            errors.append(f"Invalid JSON: {str(e)}")
            
        return errors

    def validate_typescript_interface(self, content: str) -> List[str]:
        """Validate TypeScript interface definition."""
        errors = []
        
        # Check interface declaration
        if not re.match(r'\s*interface\s+\w+\s*{', content):
            errors.append("Must start with interface declaration")
            return errors
            
        # Validate property definitions
        for line in content.split('\n'):
            # Skip empty lines and closing brace
            if not line.strip() or line.strip() == '}':
                continue
                
            # Check property format
            prop_match = re.match(r'\s*(\w+)(\?)?:\s*(.+);?\s*$', line)
            if not prop_match:
                errors.append(f"Invalid property definition: {line.strip()}")
                continue
                
            name, optional, type_ = prop_match.groups()
            
            # Validate type
            if not re.match(r'^[\w\[\]<>|&]+$', type_.strip()):
                errors.append(f"Invalid type for property '{name}': {type_}")
                
        return errors

    def validate_all(self) -> List[SchemaError]:
        """Run all schema validations."""
        schemas = self._extract_schemas()
        
        for name, schema in schemas.items():
            if schema['type'] in ('json', 'typescript', 'ts'):
                errors = []
                if schema['type'] == 'json':
                    errors = self.validate_json_schema(schema['content'])
                else:
                    errors = self.validate_typescript_interface(schema['content'])
                
                for error in errors:
                    self.errors.append(SchemaError(
                        message=error,
                        location=f"{self.prd_path}#{name}"
                    ))
        
        return self.errors
