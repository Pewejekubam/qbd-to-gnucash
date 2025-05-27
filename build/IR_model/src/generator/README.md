# IR Generator Documentation

## Overview

The IR Generator is responsible for parsing PRD (Product Requirements Document) files and generating an Intermediate Representation (IR) that can be used by the code generation engine. It consists of several components working together to extract, validate, and assemble the IR.

## Components

### 1. Section Parser (`section_parser.py`)
- Parses PRD markdown files into hierarchical sections
- Extracts code blocks and cross-references
- Validates section numbering and structure

### 2. Interface Parser (`interface_parser.py`)
- Extracts interface definitions from code blocks
- Supports TypeScript interfaces and JSON Schema
- Tracks interface dependencies and versions

### 3. Dependency Graph (`dependency_graph.py`)
- Manages component relationships
- Validates version compatibility
- Detects dependency cycles
- Provides topological ordering

### 4. IR Builder (`ir_builder.py`)
- Coordinates parsing and assembly
- Validates component relationships
- Generates the complete IR structure

### 5. Metadata Parser (`metadata_parser.py`)
- Extracts metadata from PRD headers
- Determines component types
- Handles version information

## Usage

### Basic Usage

```python
from pathlib import Path
from generator.ir_builder import IRBuilder

# Initialize builder with system IR template
builder = IRBuilder(Path('system-ir.yaml'))

# Add PRDs to process
builder.add_prd(Path('core-prd-v3.6.3.md'))
builder.add_prd(Path('module-prd-accounts-v1.1.1.md'))

# Generate IR
ir = builder.build()
```

### IR Structure

The generated IR has the following structure:

```yaml
version: v1.0.0
components:
  component_name:
    version: v1.0.0
    type: module|interface|utility
    interfaces:
      - name: InterfaceName
        type: TypedDict|JSONSchema
        definition: {...}
    source_file: path/to/prd.md
relationships:
  dependencies:
    component_name: [dependency1, dependency2]
```

## Error Handling

The generator implements comprehensive error checking:

1. Invalid PRD Structure
   - Missing required sections
   - Incorrect section numbering
   - Invalid metadata

2. Interface Errors
   - Invalid interface definitions
   - Missing type information
   - Undeclared dependencies

3. Dependency Errors
   - Circular dependencies
   - Version conflicts
   - Missing dependencies

## Best Practices

1. PRD Organization
   - Use consistent section numbering
   - Place interfaces in Section 2
   - Document all dependencies

2. Version Management
   - Follow semantic versioning
   - Declare compatible versions
   - Document breaking changes

3. Interface Definition
   - Use TypeScript or JSON Schema
   - Document all parameters
   - Mark optional fields

## Development

### Adding New Features

1. Parser Enhancements
   ```python
   class CustomParser:
       def parse(self, content: str) -> Dict:
           # Implementation
           pass
   ```

2. New Validators
   ```python
   def validate_custom_rules(ir: Dict) -> List[Error]:
       # Implementation
       pass
   ```

### Testing

Run tests with:
```bash
pytest src/generator/tests/
```

Key test areas:
- Section parsing accuracy
- Interface extraction
- Dependency resolution
- Version compatibility
- Error handling

## Troubleshooting

Common issues and solutions:

1. Invalid Section Numbers
   - Check section hierarchy
   - Verify sequential numbering
   - Look for duplicate numbers

2. Dependency Cycles
   - Review component relationships
   - Check for indirect cycles
   - Consider refactoring dependencies

3. Version Conflicts
   - Verify version compatibility
   - Update dependency versions
   - Check semantic versioning rules
