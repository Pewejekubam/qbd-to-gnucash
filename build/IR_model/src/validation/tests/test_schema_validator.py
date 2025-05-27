"""Test suite for schema validator component."""

import unittest
from pathlib import Path
from textwrap import dedent
from ..schema_validator import SchemaValidator, SchemaError
import tempfile

class TestSchemaValidator(unittest.TestCase):
    """Test cases for schema validation."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def create_test_prd(self, content: str) -> Path:
        """Create a test PRD file with given content."""
        prd_path = self.temp_path / "test-prd.md"
        prd_path.write_text(content)
        return prd_path

    def test_json_schema_validation(self):
        """Test JSON Schema validation rules."""
        content = dedent("""
        # Test Schema

        ```json
        {
            "type": "object",
            "properties": {
                "name": {
                    "type": "string",
                    "description": "User's name"
                },
                "age": {
                    "type": "integer",
                    "minimum": 0
                }
            },
            "required": ["name"]
        }
        ```
        """)
        
        prd_path = self.create_test_prd(content)
        validator = SchemaValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertEqual(len(errors), 0, "Valid JSON Schema should have no errors")

    def test_invalid_json_schema(self):
        """Test detection of invalid JSON Schema."""
        content = dedent("""
        # Test Schema

        ```json
        {
            "properties": {
                "name": "not an object"
            }
        }
        ```
        """)
        
        prd_path = self.create_test_prd(content)
        validator = SchemaValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertGreater(len(errors), 0, "Invalid schema should have errors")
        self.assertTrue(any("type" in e.message for e in errors))

    def test_typescript_interface_validation(self):
        """Test TypeScript interface validation rules."""
        content = dedent("""
        # User Interface

        ```typescript
        interface User {
            name: string;
            age?: number;
            roles: string[];
            settings: {
                theme: string;
                notifications: boolean;
            }
        }
        ```
        """)
        
        prd_path = self.create_test_prd(content)
        validator = SchemaValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertEqual(len(errors), 0, "Valid TypeScript interface should have no errors")

    def test_invalid_typescript_interface(self):
        """Test detection of invalid TypeScript interface."""
        content = dedent("""
        # User Interface

        ```typescript
        interface User {
            name: string
            age: not-a-type;
            roles: []; // invalid array type
        }
        ```
        """)
        
        prd_path = self.create_test_prd(content)
        validator = SchemaValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertGreater(len(errors), 0, "Invalid interface should have errors")

    def test_schema_extraction(self):
        """Test extraction of schemas from PRD content."""
        content = dedent("""
        # First Schema
        ```json
        {"type": "object"}
        ```

        # Second Schema
        ```typescript
        interface Test {}
        ```
        """)
        
        prd_path = self.create_test_prd(content)
        validator = SchemaValidator(str(prd_path))
        schemas = validator._extract_schemas()
        self.assertEqual(len(schemas), 2, "Should extract both schemas")
        self.assertEqual(schemas["First Schema"]["type"], "json")
        self.assertEqual(schemas["Second Schema"]["type"], "typescript")

    def test_error_messages(self):
        """Test error message clarity and helpfulness."""
        content = dedent("""
        # Test Schema
        ```json
        {
            "properties": {
                "test": { }
            }
        }
        ```
        """)
        
        prd_path = self.create_test_prd(content)
        validator = SchemaValidator(str(prd_path))
        errors = validator.validate_all()
        
        self.assertTrue(errors)
        error = errors[0]
        self.assertIsInstance(error, SchemaError)
        self.assertTrue(error.message)  # Message should not be empty
        self.assertTrue(error.location)  # Location should be included
