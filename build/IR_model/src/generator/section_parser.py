"""Parser for PRD markdown sections."""

import re
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
from pathlib import Path

from .utils import (
    extract_code_block,
    extract_section_info,
    extract_version,
    is_sequential,
    normalize_path,
    split_section_number,
)

@dataclass
class Section:
    """A section in the PRD document."""
    number: str
    title: str
    content: str
    level: int = 2  # Default to h2 (##)
    subsections: List['Section'] = field(default_factory=list)
    code_blocks: List[Tuple[str, str]] = field(default_factory=list)
    references: List[str] = field(default_factory=list)

class SectionParser:
    """Parser for PRD markdown sections."""
    
    def __init__(self, prd_path: Path):
        self.prd_path = Path(prd_path)
        self.root_sections: List[Section] = []
        self._current_section: Optional[Section] = None
        self._section_stack: List[Section] = []
    
    def parse(self, content: str) -> List[Section]:
        """Parse PRD content into sections."""
        lines = content.split('\n')
        current_content = []
        
        for line in lines:
            if line.startswith('#'):
                # Save content of previous section
                if self._current_section and current_content:
                    self._current_section.content = '\n'.join(current_content)
                    self._extract_code_blocks(self._current_section)
                    self._extract_references(self._current_section)
                
                # Start new section
                self._handle_section_header(line)
                current_content = []
            else:
                current_content.append(line)
        
        # Handle content of last section
        if self._current_section and current_content:
            self._current_section.content = '\n'.join(current_content)
            self._extract_code_blocks(self._current_section)
            self._extract_references(self._current_section)
        
        return self.root_sections
    
    def _handle_section_header(self, line: str) -> None:
        """Process a section header line."""
        level = len(re.match(r'^#+', line).group())
        number, title = extract_section_info(line)
        
        section = Section(
            number=number,
            title=title,
            content='',
            level=level
        )
        
        if not self._section_stack:
            # First section
            self.root_sections.append(section)
            self._section_stack.append(section)
        else:
            while self._section_stack:
                parent = self._section_stack[-1]
                if parent.level < level:
                    # Current section is a subsection of parent
                    parent.subsections.append(section)
                    break
                self._section_stack.pop()
            
            if not self._section_stack:
                # No valid parent found, must be a root section
                self.root_sections.append(section)
            
            self._section_stack.append(section)
        
        self._current_section = section
    
    def _extract_code_blocks(self, section: Section) -> None:
        """Extract code blocks from section content."""
        current_pos = 0
        content = section.content
        
        while True:
            code_block_match = re.search(r'```(\w*)\n(.*?)```', content[current_pos:], re.DOTALL)
            if not code_block_match:
                break
            
            lang = code_block_match.group(1) or 'text'
            code = code_block_match.group(2).strip()
            section.code_blocks.append((lang, code))
            
            current_pos += code_block_match.end()
    
    def _extract_references(self, section: Section) -> None:
        """Extract references from section content."""
        # Find markdown links [text](url)
        links = re.findall(r'\[([^\]]+)\]\(([^)]+)\)', section.content)
        section.references.extend(ref for _, ref in links)
        
        # Find bare URLs
        urls = re.findall(r'<(https?://[^>]+)>', section.content)
        section.references.extend(urls)

    def validate_section_numbers(self) -> List[str]:
        """Validate section numbering is sequential and properly nested."""
        errors = []
        
        def check_section(section: Section, parent_num: str = '') -> None:
            if not section.number:
                return
            
            # Check if section number starts with parent number
            if parent_num and not section.number.startswith(f"{parent_num}."):
                errors.append(
                    f"Section {section.number} ({section.title}) "
                    f"should start with {parent_num}"
                )
            
            # Get all sibling section numbers at this level
            siblings = []
            if parent_num:
                parent_prefix = f"{parent_num}."
                siblings = [
                    int(s.number[len(parent_prefix):])
                    for s in self.root_sections
                    if s.number.startswith(parent_prefix)
                ]
            else:
                siblings = [
                    int(s.number.split('.')[0])
                    for s in self.root_sections
                    if s.number
                ]
            
            if not is_sequential(sorted(siblings)):
                errors.append(
                    f"Sections under {parent_num or 'root'} are not sequential: "
                    f"{', '.join(str(x) for x in siblings)}"
                )
            
            # Recursively check subsections
            for subsection in section.subsections:
                check_section(subsection, section.number)
        
        for section in self.root_sections:
            check_section(section)
        
        return errors
