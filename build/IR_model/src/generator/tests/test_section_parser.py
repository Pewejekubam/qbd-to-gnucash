"""Tests for the section parser."""

import pytest
from pathlib import Path
from ..section_parser import Section, SectionParser

def test_section_parsing():
    """Test basic section parsing."""
    content = """# Title
Some content

## 1. First Section
First section content

### 1.1 Subsection
Subsection content

## 2. Second Section
Second section content"""

    parser = SectionParser(Path('test.md'))
    sections = parser.parse(content)
    
    assert len(sections) == 2
    assert sections[0].number == '1'
    assert sections[0].title == 'First Section'
    assert len(sections[0].subsections) == 1
    assert sections[1].number == '2'
    assert sections[1].title == 'Second Section'

def test_code_block_extraction():
    """Test code block extraction."""
    content = """## 1. Test Section
```typescript
interface Test {
    field: string;
}
```

Some text

```python
def test():
    pass
```"""

    parser = SectionParser(Path('test.md'))
    sections = parser.parse(content)
    
    assert len(sections) == 1
    assert len(sections[0].code_blocks) == 2
    assert sections[0].code_blocks[0][0] == 'typescript'
    assert sections[0].code_blocks[1][0] == 'python'

def test_reference_extraction():
    """Test reference extraction."""
    content = """## 1. Test Section
See [link](./test.md) and <https://example.com>
"""

    parser = SectionParser(Path('test.md'))
    sections = parser.parse(content)
    
    assert len(sections) == 1
    assert len(sections[0].references) == 2
    assert './test.md' in sections[0].references
    assert 'https://example.com' in sections[0].references

def test_section_numbering_validation():
    """Test section number validation."""
    content = """## 1. First
Content

## 3. Third
Content"""

    parser = SectionParser(Path('test.md'))
    parser.parse(content)
    errors = parser.validate_section_numbers()
    
    assert len(errors) == 1  # Should detect missing section 2
