"""Test suite for PRD validator component."""

import unittest
from pathlib import Path
from textwrap import dedent
from ..prd_validator import PRDValidator, ValidationError, StructuralError, VersionError
import tempfile

class TestPRDValidator(unittest.TestCase):
    """Test cases for PRD validation."""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.temp_path = Path(self.temp_dir)

    def create_test_prd(self, content: str, filename: str = "module-prd-accounts-v1.0.0.md") -> Path:
        """Create a test PRD file with given content."""
        prd_path = self.temp_path / filename
        prd_path.write_text(content)
        return prd_path

    def test_valid_prd_structure(self):
        """Test validation of correct PRD structure."""
        content = dedent("""
        # Product Requirements Document — Accounts

        **Document Version:** v1.0.0
        **Module Identifier:** module-prd-accounts-v1.0.0.md
        **Domain:** accounts
        **Compatible Core PRD:** core-prd-v3.6.3.md
        **System Context:** QuickBooks Desktop to GnuCash Conversion Tool
        **Author:** Test Author
        **Last Updated:** 2025-05-27
        **Governance Model:** prd-governance-model-v2.3.10.md

        ---

        ## 1. Purpose
        Test purpose description.

        ---

        ## 2. Scope
        Test scope description.

        ---

        ## 3. Revision History
        | Version | Date | Author | Summary |
        |---------|------|--------|---------|
        | v1.0.0  | 2025-05-27 | TA | Initial version |
        """)
        
        prd_path = self.create_test_prd(content)
        validator = PRDValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertEqual(len(errors), 0, "Valid PRD should have no errors")

    def test_version_validation(self):
        """Test version number validation rules."""
        # Test invalid version in filename
        prd_path = self.create_test_prd("# Test", "module-prd-accounts-v1.md")
        validator = PRDValidator(str(prd_path))
        with self.assertRaises(VersionError):
            validator.validate_all()

        # Test version mismatch
        content = dedent("""
        # Test
        **Document Version:** v1.0.1
        """)
        prd_path = self.create_test_prd(content, "module-prd-accounts-v1.0.0.md")
        validator = PRDValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertTrue(any(isinstance(e, VersionError) for e in errors))

    def test_section_numbering(self):
        """Test section numbering validation."""
        content = dedent("""
        # Title

        ## 1. First
        Content

        ## 3. Third
        Content
        """)
        
        prd_path = self.create_test_prd(content)
        validator = PRDValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertTrue(any(isinstance(e, StructuralError) for e in errors))
        self.assertTrue(any("sequential" in e.args[0] for e in errors))

    def test_cross_references(self):
        """Test cross-reference validation."""
        content = dedent("""
        # Title

        Reference to [invalid link](bad-path.md)
        """)
        
        prd_path = self.create_test_prd(content)
        validator = PRDValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertTrue(any("reference" in e.args[0].lower() for e in errors))

    def test_metadata_validation(self):
        """Test metadata field validation."""
        content = dedent("""
        # Title

        **Document Version:** v1.0.0
        Missing other required fields
        """)
        
        prd_path = self.create_test_prd(content)
        validator = PRDValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertTrue(any("metadata" in e.args[0].lower() for e in errors))

    def test_domain_validation(self):
        """Test domain name validation."""
        # Test invalid domain name
        prd_path = self.create_test_prd("# Test", "module-prd-invalid-v1.0.0.md")
        validator = PRDValidator(str(prd_path))
        errors = validator.validate_all()
        self.assertTrue(any("domain" in e.args[0].lower() for e in errors))

    def test_error_messages(self):
        """Test error message clarity and helpfulness."""
        content = "Invalid content"
        prd_path = self.create_test_prd(content)
        validator = PRDValidator(str(prd_path))
        errors = validator.validate_all()
        
        self.assertTrue(errors)
        error = errors[0]
        self.assertIsInstance(error, ValidationError)
        self.assertTrue(error.args[0])  # Message should not be empty
