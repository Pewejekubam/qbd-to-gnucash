"""Test utilities and common test data."""

from pathlib import Path
import tempfile
from typing import Optional

class TestUtils:
    """Utility functions for validation tests."""
    
    @staticmethod
    def create_temp_prd(content: str, filename: Optional[str] = None) -> Path:
        """Create a temporary PRD file for testing."""
        temp_dir = tempfile.mkdtemp()
        prd_path = Path(temp_dir) / (filename or "test-prd.md")
        prd_path.write_text(content)
        return prd_path

# Common test data
VALID_PRD_TEMPLATE = """# Product Requirements Document — {title}

**Document Version:** {version}
**Module Identifier:** {identifier}
**Domain:** {domain}
**Compatible Core PRD:** core-prd-v3.6.3.md
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool
**Author:** Test Author
**Last Updated:** 2025-05-27
**Governance Model:** prd-governance-model-v2.3.10.md

---

## 1. Purpose
{purpose}

---

## 2. Scope
{scope}

---

## 3. Revision History
| Version | Date | Author | Summary |
|---------|------|--------|---------|
| {version} | 2025-05-27 | TA | Initial version |
"""

VALID_JSON_SCHEMA = """{
    "type": "object",
    "properties": {
        "name": {
            "type": "string",
            "description": "Test property"
        }
    },
    "required": ["name"]
}"""

VALID_TYPESCRIPT_INTERFACE = """interface TestInterface {
    name: string;
    optional?: number;
    array: string[];
}"""
