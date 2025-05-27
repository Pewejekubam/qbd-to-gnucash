"""Tests for the interface parser."""

import pytest
from pathlib import Path
from ..interface_parser import InterfaceParser

def test_typescript_interface_parsing():
    """Test TypeScript interface parsing."""
    content = """```typescript
interface TestInterface {
    field1: string;
    optional?: number;
    complex: Array<string>;
}
```"""

    parser = InterfaceParser(Path('test.md'))
    interfaces = parser.parse_section('1.1', content)
    
    assert len(interfaces) == 1
    interface = interfaces[0]
    assert interface.name == 'TestInterface'
    assert interface.type == 'TypedDict'
    assert len(interface.definition) == 3
    assert interface.definition['optional']['optional'] == True

def test_json_schema_parsing():
    """Test JSON Schema parsing."""
    content = """```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "TestSchema",
    "type": "object",
    "properties": {
        "field1": { "type": "string" }
    }
}
```"""

    parser = InterfaceParser(Path('test.md'))
    interfaces = parser.parse_section('1.1', content)
    
    assert len(interfaces) == 1
    interface = interfaces[0]
    assert interface.name == 'TestSchema'
    assert interface.type == 'JSON Schema'
    assert 'properties' in interface.definition

def test_dependency_extraction():
    """Test dependency extraction from interfaces."""
    content = """```typescript
import { OtherType } from './other';

interface TestInterface {
    field1: string;
    ref: OtherType;
    items: Item[];
}
```"""

    parser = InterfaceParser(Path('test.md'))
    interfaces = parser.parse_section('1.1', content)
    
    assert len(interfaces) == 1
    interface = interfaces[0]
    assert './other' in interface.dependencies
    assert 'OtherType' in interface.dependencies
    assert 'Item' in interface.dependencies
