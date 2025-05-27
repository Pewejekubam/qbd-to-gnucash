# Validation Framework Documentation

## Overview
The validation framework ensures compliance with [PRD Governance Model v2.3.10](../../../prd/prd-governance-model-v2.3.10.md) through two main components:
1. PRD Validator - Ensures structural and content compliance
2. Schema Validator - Verifies interface and data structure definitions

## Components

### PRD Validator
`prd_validator.py` enforces document-level compliance rules:

#### Key Features
- Structural validation (§2)
- Version enforcement (§5)
- Domain validation (§3)
- Update discipline (§6)
- AI agent compliance (§9)
- Governance authority (§10)
- Compliance enforcement (§11)

#### Usage Example
```python
from validation.prd_validator import PRDValidator

validator = PRDValidator("path/to/prd.md")
errors = validator.validate_all()

if errors:
    for error in errors:
        print(f"Error: {error}")
else:
    print("PRD is valid!")
```

#### Error Types
- `ValidationError` - Base class for all validation errors
- `StructuralError` - Document structure issues
- `ReferenceError` - Cross-reference problems
- `VersionError` - Version-related violations

### Schema Validator 
`schema_validator.py` verifies interface definitions and data structures:

#### Key Features
- JSON Schema validation
- TypeScript interface validation
- Property type checking
- Required field validation

#### Usage Example
```python
from validation.schema_validator import SchemaValidator

validator = SchemaValidator("path/to/prd.md")
errors = validator.validate_all()

if errors:
    for error in errors:
        print(f"Error in {error.location}: {error.message}")
else:
    print("All schemas are valid!")
```

#### Error Types
- `SchemaError` - Contains error message, location, and optional details

## Testing
The framework includes a minimal test suite focused on critical validation paths:

### PRD Validator Tests
- Structure validation
- Version compatibility
- Cross-references
- Error handling

### Schema Validator Tests
- JSON Schema validation
- TypeScript interface validation
- Schema extraction
- Error messages

### Running Tests
```powershell
# From the project root
python -m pytest build/IR_model/src/validation/tests/
```

## Error Messages
The framework provides clear, actionable error messages:

### PRD Validation Errors
- Missing/invalid sections
- Version incompatibilities
- Cross-reference failures
- Governance violations

### Schema Validation Errors
- Invalid schema structure
- Type mismatches
- Missing required fields
- Format violations

## Validation Rules

### Document Structure (§2)
- Major sections must be properly numbered and delimited
- Headers must follow correct format
- Content must be valid Markdown

### Version Enforcement (§5)
- Version numbers must follow semantic versioning
- Changelog must be properly formatted
- Version declarations must be consistent

### Domain Rules (§3)
- Domain names must use snake_case
- Must match authorized domain list
- Must be properly capitalized

### Dependencies (§8)
- Cross-references must use relative paths
- References must be version-locked
- All referenced files must exist

### AI Agent Compliance (§9)
- Interface definitions must use approved formats
- Error contracts must be explicit
- Logging must be deterministic

### Governance Authority (§10)
- Cannot override governance rules
- Must maintain precedence order
- Requires formal revision for changes

## Best Practices

### Writing Valid PRDs
1. Start with the appropriate template
2. Follow section numbering rules
3. Use proper version numbering
4. Include all required metadata
5. Use approved interface formats

### Common Issues
1. Missing section delimiters
2. Incorrect version formats
3. Invalid cross-references
4. Missing metadata fields
5. Improper schema definitions

### Troubleshooting
1. Check error messages for specific locations
2. Verify versions match in all places
3. Ensure all cross-references exist
4. Validate schema syntax
5. Check section numbering sequence

## Future Enhancements
Potential areas for expansion:
1. Integration with CI/CD pipelines
2. Enhanced schema validation
3. Automated correction suggestions
4. Extended test coverage
