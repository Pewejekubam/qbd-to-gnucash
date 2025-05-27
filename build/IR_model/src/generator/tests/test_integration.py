"""Integration tests for PRD parsing system."""

import pytest
from pathlib import Path

from ..section_parser import SectionParser
from ..interface_parser import InterfaceParser
from ..dependency_graph import DependencyGraph

def test_full_prd_parsing(test_prd_path):
    """Test complete PRD parsing workflow."""
    # 1. Parse sections
    section_parser = SectionParser(test_prd_path)
    content = test_prd_path.read_text()
    sections = section_parser.parse(content)
    
    # Verify basic structure
    assert len(sections) == 3  # Overview, Interfaces, Dependencies
    assert sections[0].number == '1'
    assert sections[1].number == '2'
    assert sections[2].number == '3'
    
    # 2. Parse interfaces
    interface_parser = InterfaceParser(test_prd_path)
    interfaces = []
    
    for section in sections:
        if section.number.startswith('2'):  # Interface sections
            for subsection in section.subsections:
                interfaces.extend(
                    interface_parser.parse_section(
                        subsection.number,
                        subsection.content
                    )
                )
    
    # Verify interfaces
    assert len(interfaces) == 2  # TypeScript interface and JSON Schema
    assert interfaces[0].type == 'TypedDict'
    assert interfaces[1].type == 'JSON Schema'
    
    # 3. Build dependency graph
    graph = DependencyGraph()
    
    # Add main module
    graph.add_node(
        'test_module',
        'v1.0.0',
        'module',
        test_prd_path
    )
    
    # Add interface nodes
    for interface in interfaces:
        graph.add_node(
            interface.name,
            interface.version,
            'interface'
        )
        graph.add_dependency('test_module', interface.name)
    
    # Add external dependencies
    graph.add_node('logging', 'v1.0.4', 'module')
    graph.add_node('error_handler', 'v1.0.0', 'module')
    graph.add_dependency('test_module', 'logging')
    graph.add_dependency('test_module', 'error_handler')
    
    # Validate graph
    assert len(graph.validate_cycles()) == 0  # No cycles
    assert len(graph.validate_versions()) == 0  # No version conflicts
    
    # Verify dependency order
    ordered = graph.build_ordered_list()
    assert ordered[0] in ('logging', 'error_handler')  # Dependencies first
    assert ordered[-1] == 'test_module'  # Main module last

def test_validation_errors(test_prd_path):
    """Test error detection in parsing and validation."""
    # 1. Test section number validation
    bad_content = """# Test PRD
## 1. First
Content
## 3. Third  # Missing section 2
Content
"""
    
    section_parser = SectionParser(test_prd_path)
    sections = section_parser.parse(bad_content)
    errors = section_parser.validate_section_numbers()
    assert len(errors) == 1  # Should detect missing section 2
    
    # 2. Test interface parsing errors
    bad_interface = """```typescript
interface BadInterface {
    field: InvalidType;  # Undefined type
}
```"""
    
    interface_parser = InterfaceParser(test_prd_path)
    interfaces = interface_parser.parse_section('2.1', bad_interface)
    assert len(interfaces) == 1
    assert 'InvalidType' in interfaces[0].dependencies  # Should detect external dependency
    
    # 3. Test dependency validation
    graph = DependencyGraph()
    graph.add_node('module_a', 'v2.0.0', 'module')
    graph.add_node('module_b', 'v1.0.0', 'module')  # Incompatible version
    graph.add_dependency('module_a', 'module_b')
    
    version_errors = graph.validate_versions()
    assert len(version_errors) == 1  # Should detect version mismatch
