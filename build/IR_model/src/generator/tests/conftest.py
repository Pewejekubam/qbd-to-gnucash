"""Test utilities and fixtures."""

import pytest
from pathlib import Path

@pytest.fixture
def test_prd_content():
    """Sample PRD content for testing."""
    return """# Test PRD
Version: v1.0.0
Type: module

## 1. Overview
This is a test PRD.

### 1.1 Purpose
Testing the parser.

## 2. Interfaces

### 2.1 Core Interface
```typescript
interface TestInterface {
    field1: string;
    optional?: number;
}
```

### 2.2 Schema
```json
{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "TestSchema",
    "type": "object",
    "properties": {
        "field1": { "type": "string" }
    }
}
```

## 3. Dependencies

### 3.1 Required Modules
- logging (v1.0.4)
- error_handler

### 3.2 Optional Dependencies
None
"""

@pytest.fixture
def test_prd_path(tmp_path):
    """Create a temporary PRD file for testing."""
    prd_file = tmp_path / "test-prd-v1.0.0.md"
    prd_file.write_text(test_prd_content())
    return prd_file

@pytest.fixture
def sample_interface_ts():
    """Sample TypeScript interface."""
    return """interface SampleInterface {
    id: string;
    name: string;
    optional?: boolean;
    items: string[];
}"""

@pytest.fixture
def sample_schema_json():
    """Sample JSON Schema."""
    return """{
    "$schema": "http://json-schema.org/draft-07/schema#",
    "title": "Sample",
    "type": "object",
    "properties": {
        "id": { "type": "string" },
        "count": { "type": "number" }
    },
    "required": ["id"]
}"""
