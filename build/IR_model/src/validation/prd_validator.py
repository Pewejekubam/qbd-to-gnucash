"""PRD Validator Module.

This module implements validation rules from prd-governance-model-v2.3.10.md
to enforce PRD structure, versioning, and cross-reference requirements.
"""

import os
import re
from dataclasses import dataclass
from datetime import date, datetime
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Set

# Constants from Governance Model v2.3.10
VALID_DOMAINS = {
    'accounts', 'customers', 'vendors', 'items', 'sales_tax', 'job_types',
    'classes', 'price_levels', 'customer_types', 'vendor_types', 'payment_terms',
    'payment_methods', 'shipping_methods', 'sales_reps', 'messages', 'employees',
    'budgets', 'to_do', 'other_names'
}

VALID_PRD_TYPES = {'module', 'core', 'governance'}

class ValidationError(Exception):
    """Base class for PRD validation errors."""
    pass

class StructuralError(ValidationError):
    """Raised for structural violations like incorrect headers or section numbering."""
    pass
    
class ReferenceError(ValidationError):
    """Raised for invalid cross-references between PRDs."""
    pass

class VersionError(ValidationError):
    """Raised for version-related violations."""
    pass

@dataclass
class PRDVersion:
    """Represents a semantic version number."""
    major: int
    minor: int
    patch: int
    
    @classmethod
    def from_string(cls, version_str: str) -> 'PRDVersion':
        """Parse a version string like 'v1.2.3' into a PRDVersion object."""
        match = re.match(r'v(\d+)\.(\d+)\.(\d+)$', version_str)
        if not match:
            raise VersionError(f"Invalid version format: {version_str}. Must be vX.Y.Z with non-negative integers.")
        
        major, minor, patch = map(int, match.groups())
        if any(v < 0 for v in [major, minor, patch]):
            raise VersionError(f"Version components must be non-negative integers: {version_str}")
            
        return cls(major=major, minor=minor, patch=patch)
    
    def __str__(self) -> str:
        return f"v{self.major}.{self.minor}.{self.patch}"
    
    def is_compatible_with(self, other: 'PRDVersion') -> bool:
        """Check if this version is compatible with another version.
        
        Per §5.2:
        - Major version must match exactly
        - Minor version must be greater than or equal
        - Patch version is ignored for compatibility
        """
        return (self.major == other.major and 
                self.minor >= other.minor)

class PRDReferenceInfo:
    """Information about a referenced PRD."""
    def __init__(self, ref_text: str, ref_path: str, version: Optional[PRDVersion] = None):
        self.text = ref_text
        self.path = ref_path
        self.version = version

class PRDValidator:
    """Validator for PRD documents following governance-model-v2.3.10."""
    
    # Constants from Section 3.2 Domain Index Protocol
    VALID_DOMAINS = {
        'accounts', 'customers', 'vendors', 'items', 'sales_tax',
        'job_types', 'classes', 'price_levels', 'customer_types',
        'vendor_types', 'payment_terms', 'payment_methods',
        'shipping_methods', 'sales_reps', 'messages', 'employees',
        'budgets', 'to_do', 'other_names'
    }

    def __init__(self, prd_path: str):
        """Initialize validator with path to PRD file."""
        self.prd_path = Path(prd_path)
        if not self.prd_path.exists():
            raise FileNotFoundError(f"PRD file not found: {prd_path}")
        
        self.content = self.prd_path.read_text()
        self.sections = self._parse_sections()
        self.version = self._parse_version()
        self.errors: List[ValidationError] = []
        
    def _parse_sections(self) -> Dict[str, str]:
        """Parse PRD content into sections."""
        sections = {}
        current_section = ""
        current_content = []
        
        for line in self.content.split('\n'):
            if line.startswith('## '):
                if current_section:
                    sections[current_section] = '\n'.join(current_content)
                current_section = line[3:].strip()
                current_content = [line]
            else:
                current_content.append(line)
                
        if current_section:
            sections[current_section] = '\n'.join(current_content)
            
        return sections

    def _parse_version(self) -> PRDVersion:
        """Extract version from PRD filename and metadata."""
        # Get version from filename
        match = re.search(r'-v(\d+\.\d+\.\d+)\.md$', self.prd_path.name)
        if not match:
            raise VersionError(f"Invalid filename format: {self.prd_path.name}")
        return PRDVersion.from_string('v' + match.group(1))

    def validate_filename(self) -> None:
        """Validate filename format per §5.4 Naming & Location Protocol."""
        name = self.prd_path.name
        
        # Check basic format
        pattern = r'^(module|core|governance)-prd-([a-z_]+)(?:_[a-z_]+)?-v\d+\.\d+\.\d+\.md$'
        if not re.match(pattern, name):
            raise ValidationError(f"Invalid filename format: {name}")
            
        # Extract components
        match = re.match(r'^([^-]+)-prd-([^-_]+)(?:_([^-]+))?-v\d+\.\d+\.\d+\.md$', name)
        if not match:
            raise ValidationError(f"Could not parse filename components: {name}")
            
        prd_type, domain, tag = match.groups()
        
        # Validate type
        if prd_type not in VALID_PRD_TYPES:
            raise ValidationError(f"Invalid PRD type: {prd_type}")
            
        # Validate domain
        if prd_type == 'module' and domain not in VALID_DOMAINS:
            raise ValidationError(f"Invalid domain: {domain}")
            
        # Validate location
        if prd_type == 'module':
            if not str(self.prd_path.parent).endswith(f'/prd/{domain}'):
                raise ValidationError(
                    f"Module PRD must be in prd/{domain}/ directory"
                )
        else:
            if not str(self.prd_path.parent).endswith('/prd'):
                raise ValidationError(
                    f"{prd_type} PRD must be in prd/ directory"
                )
    def validate_structure(self) -> None:
        """Validate PRD structure per §2 Structural Rules."""
        self.validate_section_headers()
        self.validate_section_delimiters()
        self.validate_section_numbering()
        self.validate_section_content()
        
    def validate_section_headers(self) -> None:
        """Validate header formatting per §2.1."""
        # Validate document starts with title
        if not self.content.startswith('# '):
            self.errors.append(StructuralError("Document must start with level-1 title"))
            
        lines = self.content.split('\n')
        current_section = None
        current_major_num = 0
        
        for i, line in enumerate(lines):
            # Validate major section format
            if line.startswith('## '):
                match = re.match(r'## (\d+)\. ([A-Z][A-Za-z\s]+)$', line)
                if not match:
                    self.errors.append(StructuralError(
                        f"Invalid major section format at line {i}: {line}"
                    ))
                else:
                    section_num = int(match.group(1))
                    if section_num != current_major_num + 1:
                        self.errors.append(StructuralError(
                            f"Invalid section number at line {i}: Expected {current_major_num + 1}, got {section_num}"
                        ))
                    current_major_num = section_num
                    current_section = section_num
                    
            # Validate subsection format and numbering
            elif line.startswith('### '):
                match = re.match(r'### (\d+)\.(\d+)\s+([A-Z][A-Za-z\s]+)$', line)
                if not match:
                    self.errors.append(StructuralError(
                        f"Invalid subsection format at line {i}: {line}"
                    ))
                else:
                    major, minor = map(int, [match.group(1), match.group(2)])
                    if major != current_section:
                        self.errors.append(StructuralError(
                            f"Subsection {major}.{minor} at line {i} has incorrect major number"
                        ))
                        
            # Validate subsubsection format
            elif line.startswith('#### '):
                match = re.match(r'#### (\d+)\.(\d+)\.(\d+)\s+([A-Z][A-Za-z\s]+)$', line)
                if not match:
                    self.errors.append(StructuralError(
                        f"Invalid subsubsection format at line {i}: {line}"
                    ))

    def validate_section_delimiters(self) -> None:
        """Validate section delimiter rules per §2.3."""
        lines = self.content.split('\n')
        in_major_section = False
        last_hr_line = -1
        
        for i, line in enumerate(lines):
            # Check horizontal rule usage
            if line.strip() == '---':
                if last_hr_line == i - 1:
                    self.errors.append(StructuralError(
                        f"Multiple consecutive horizontal rules at line {i}"
                    ))
                if not in_major_section and not lines[i+1].strip().startswith('## '):
                    self.errors.append(StructuralError(
                        f"Horizontal rule at line {i} not followed by major section"
                    ))
                last_hr_line = i
                
            # Track major sections
            elif line.startswith('## '):
                if in_major_section and lines[i-1].strip() != '---':
                    self.errors.append(StructuralError(
                        f"Major section at line {i} not preceded by horizontal rule"
                    ))
                in_major_section = True
                
        # Verify final section is properly closed
        if in_major_section and lines[-1].strip() != '---':
            self.errors.append(StructuralError(
                "Final major section not closed with horizontal rule"
            ))
            
    def validate_section_numbering(self) -> None:
        """Validate section numbering hierarchy per §2.1."""
        # Validate sequential section numbers
        section_numbers = []
        for section in self.sections:
            match = re.match(r'(\d+)\. ', section)
            if not match:
                continue
            section_numbers.append(int(match.group(1)))

        expected = list(range(1, len(section_numbers) + 1))
        if section_numbers != expected:
            self.errors.append(StructuralError(
                f"Section numbers must be sequential: {section_numbers}"
            ))
            
        # Validate subsection hierarchy
        for section_text in self.sections.values():
            subsection_numbers = []
            for line in section_text.split('\n'):
                if line.startswith('### '):
                    match = re.match(r'### (\d+\.\d+)', line)
                    if match:
                        subsection_numbers.append(match.group(1))
            
            # Validate subsection sequence
            for i in range(len(subsection_numbers)-1):
                curr = [int(x) for x in subsection_numbers[i].split('.')]
                next_ = [int(x) for x in subsection_numbers[i+1].split('.')]
                if next_[0] != curr[0] or next_[1] != curr[1] + 1:
                    self.errors.append(StructuralError(
                        f"Invalid subsection sequence: {subsection_numbers[i]} -> {subsection_numbers[i+1]}"
                    ))
                    
    def validate_section_content(self) -> None:
        """Validate section content rules per §2.2 and §4."""
        # Check for disallowed HTML
        for line in self.content.split('\n'):
            if re.search(r'<(?!\/?(antml|VSCode|function))[^>]+>', line):
                self.errors.append(StructuralError(
                    f"HTML tags not allowed: {line}"
                ))
                
    def validate_version_declaration(self) -> None:
        """Validate version declaration per §5.1."""
        # Extract version from metadata
        metadata_match = re.search(
            r'\*\*Document Version:\*\* v(\d+\.\d+\.\d+)', self.content
        )
        if not metadata_match:
            raise VersionError("Missing Document Version in metadata")
            
        metadata_version = PRDVersion.from_string('v' + metadata_match.group(1))
        
        # Compare with filename version
        if str(metadata_version) != str(self.version):
            raise VersionError(
                f"Version mismatch: {metadata_version} (metadata) vs {self.version} (filename)"
            )

    def validate_changelog(self) -> None:
        """Validate changelog format per §5.3."""
        pattern = r'\|\s*Version\s*\|\s*Date\s*\|\s*Author\s*\|\s*Summary\s*\|[\s\S]*?\|[-\s|]*\|([\s\S]*?)(?=\n\n)'
        
        match = re.search(pattern, self.content)
        if not match:
            raise StructuralError("Missing or malformed changelog table")
            
        entries = []
        for line in match.group(1).strip().split('\n'):
            if not line.strip():
                continue
            parts = [p.strip() for p in line.split('|')]
            if len(parts) != 5:  # Including empty first/last elements
                raise StructuralError(f"Invalid changelog entry format: {line}")
                
            version, date_str, author, summary = parts[1:5]
            
            # Validate version format
            if not re.match(r'v?\d+\.\d+\.\d+', version.strip()):
                raise VersionError(f"Invalid version format in changelog: {version}")
                
            # Validate date format
            try:
                datetime.strptime(date_str.strip(), '%Y-%m-%d')
            except ValueError:
                raise StructuralError(
                    f"Invalid date format in changelog: {date_str}"
                )
                
            entries.append((version, date_str))
            
        # Check chronological order
        dates = [datetime.strptime(d, '%Y-%m-%d') for _, d in entries]
        if dates != sorted(dates):
            raise StructuralError("Changelog entries must be in chronological order")

    def validate_cross_references(self) -> None:
        """Validate cross-references per §8 Inter-PRD Dependencies."""
        ref_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        for section in self.sections.values():
            for match in re.finditer(ref_pattern, section):
                ref_text, ref_path = match.groups()
                if not ref_path.startswith(('../', './')):
                    if not (ref_path.startswith('http://') or ref_path.startswith('https://')):
                        raise ReferenceError(
                            f"Invalid reference path format: {ref_path}. "
                            "Must use relative paths."
                        )

                # Check if referenced PRD exists
                if not (ref_path.startswith('http://') or ref_path.startswith('https://')):
                    ref_file = Path(self.prd_path.parent / ref_path)
                    if not ref_file.exists():
                        raise ReferenceError(f"Referenced file not found: {ref_path}")

    def validate_version_compatibility(self) -> None:
        """Validate version compatibility requirements per §7.2 and §8.2."""
        if not self.is_module_prd():
            return  # Only module PRDs need compatibility checks
            
        # Find compatible core PRD version
        core_version = None
        for line in self.content.split('\n'):
            if "Compatible Core PRD:" in line:
                match = re.search(r'core-prd-v(\d+\.\d+\.\d+)\.md', line)
                if match:
                    try:
                        core_version = PRDVersion.from_string('v' + match.group(1))
                    except VersionError as e:
                        self.errors.append(VersionError(
                            f"Invalid core PRD version format: {e}"
                        ))
                break
                
        if not core_version:
            self.errors.append(VersionError(
                "Module PRDs must declare compatible core PRD version"
            ))
            return
            
        # Validate core PRD compatibility
        try:
            core_prd_path = self.prd_path.parent.parent / f"core-prd-v{core_version.major}.{core_version.minor}.{core_version.patch}.md"
            if not core_prd_path.exists():
                self.errors.append(VersionError(
                    f"Referenced core PRD version {core_version} not found"
                ))
        except Exception as e:
            self.errors.append(VersionError(
                f"Error checking core PRD compatibility: {e}"
            ))

    def validate_version_references(self) -> None:
        """Validate version-locked references per §8.2."""
        ref_pattern = r'\[([^\]]+)\]\(([^)]+)-v(\d+\.\d+\.\d+)\.md\)'
        for section in self.sections.values():
            for match in re.finditer(ref_pattern, section):
                ref_text, ref_path, version_str = match.groups()
                try:
                    version = PRDVersion.from_string('v' + version_str)
                    ref_info = PRDReferenceInfo(ref_text, ref_path, version)
                    
                    # Verify referenced version exists
                    full_path = self.prd_path.parent / ref_path
                    if not full_path.with_name(f"{ref_path}-v{version_str}.md").exists():
                        self.errors.append(VersionError(
                            f"Referenced version {version} of {ref_path} not found"
                        ))
                        
                except VersionError as e:
                    self.errors.append(VersionError(
                        f"Invalid version in reference [{ref_text}]: {e}"
                    ))

    def validate_semantic_versioning(self) -> None:
        """Validate semantic versioning rules per §5.2."""
        if not self.is_module_prd():
            return  # Only check module PRDs
            
        changelog_versions = self._get_changelog_versions()
        if not changelog_versions:
            return  # Changelog validation will catch this
            
        # Check version increments
        for i in range(len(changelog_versions) - 1):
            curr = changelog_versions[i]
            prev = changelog_versions[i + 1]
            
            if curr.major > prev.major:
                # Major version bump - validate breaking change is documented
                if "breaking change" not in self._get_changelog_summary(curr).lower():
                    self.errors.append(VersionError(
                        f"Major version increment to {curr} requires documenting breaking changes"
                    ))
            elif curr.major == prev.major and curr.minor > prev.minor:
                # Minor version bump - validate new feature is documented
                if "add" not in self._get_changelog_summary(curr).lower():
                    self.errors.append(VersionError(
                        f"Minor version increment to {curr} should document new features"
                    ))
                    
    def _get_changelog_versions(self) -> List[PRDVersion]:
        """Extract versions from changelog entries."""
        versions = []
        changelog_pattern = r'\|\s*(v?\d+\.\d+\.\d+)\s*\|'
        for section in self.sections.values():
            if "Revision History" in section:
                for match in re.finditer(changelog_pattern, section):
                    try:
                        version_str = match.group(1)
                        if not version_str.startswith('v'):
                            version_str = 'v' + version_str
                        versions.append(PRDVersion.from_string(version_str))
                    except VersionError:
                        continue
        return versions
        
    def _get_changelog_summary(self, version: PRDVersion) -> str:
        """Get the changelog summary for a specific version."""
        changelog_pattern = rf'\|\s*v?{version.major}\.{version.minor}\.{version.patch}\s*\|[^|]+\|[^|]+\|\s*([^|]+)\s*\|'
        for section in self.sections.values():
            if "Revision History" in section:
                match = re.search(changelog_pattern, section)
                if match:
                    return match.group(1)
        return ""

    def is_module_prd(self) -> bool:
        """Check if this is a module PRD."""
        return bool(re.match(r'^module-prd-', self.prd_path.name))

    def validate_domain_name(self) -> None:
        """Validate domain naming per §3.1 Domain Registration & Constraints."""
        if not self.is_module_prd():
            return  # Only module PRDs need domain validation
            
        # Extract domain name from filename
        match = re.search(r'-prd-([^-_]+)', self.prd_path.name)
        if not match:
            raise StructuralError("Cannot extract domain name from filename")
            
        domain = match.group(1)
        
        # Validate snake_case
        if not re.match(r'^[a-z][a-z0-9_]*$', domain):
            raise StructuralError(
                f"Domain '{domain}' must use snake_case with lowercase letters"
            )
            
        # Validate against authorized list
        if domain not in self.VALID_DOMAINS:
            raise StructuralError(
                f"Domain '{domain}' not found in authorized domain list"
            )

    def _validate_interface_definitions(self) -> None:
        """Validate interface definitions per §9.2."""
        valid_formats = ["TypedDict", "JSON Schema", "enum"]
        for section in self.sections.values():
            # Look for interface/schema definitions in code blocks
            code_blocks = re.finditer(r'```[^\n]*\n(.*?)```', section, re.DOTALL)
            for block in code_blocks:
                code = block.group(1)
                # Validate only contains approved formats
                if any(format in code for format in valid_formats):
                    continue
                if "type" in code or "interface" in code.lower():
                    self.errors.append(StructuralError(
                        "Interface definitions must use TypedDict, JSON Schema, or strict enums"
                    ))

    def _validate_error_contracts(self) -> None:
        """Validate error handling contracts per §9.3."""
        has_exit_codes = False
        has_exceptions = False
        
        # Check for exit code and exception definitions
        for section in self.sections.values():
            if "Exit Code" in section or "exit code" in section.lower():
                has_exit_codes = True
            if "Exception" in section or "Error" in section:
                has_exceptions = True
                
        if not (has_exit_codes and has_exceptions):
            self.errors.append(StructuralError(
                "Missing explicit exit codes or exception definitions"
            ))

    def validate_update_discipline(self) -> None:
        """Validate update discipline rules per §6."""
        self._validate_targeted_edits()
        self._validate_ordered_insertion()
        self._validate_renumbering_consistency()

    def _validate_targeted_edits(self) -> None:
        """Validate targeted edits per §6.1."""
        # Get the changelog summary for latest version
        changelog_versions = self._get_changelog_versions()
        if not changelog_versions:
            return
            
        latest_version = changelog_versions[0] # Most recent version first
        summary = self._get_changelog_summary(latest_version)
        
        # Look for words indicating broad changes
        broad_terms = ["refactor", "rewrite", "restructure", "reorganize"]
        if any(term in summary.lower() for term in broad_terms):
            self.errors.append(StructuralError(
                "Updates must be targeted and avoid collateral changes"
            ))

    def _validate_ordered_insertion(self) -> None:
        """Validate semantic insertion order per §6.2."""
        section_pattern = r'## (\d+)\. ([^\n]+)'
        sections = re.finditer(section_pattern, self.content)
        
        # Check sections are logically ordered
        prev_name = ""
        for match in sections:
            section_name = match.group(2).lower()
            
            # Check if metadata sections are at the start
            if "metadata" in section_name and prev_name:
                self.errors.append(StructuralError(
                    "Metadata sections must be at document start"
                ))
                
            # Check if appendix/examples are at the end
            if ("appendix" in prev_name or "example" in prev_name) and not (
                "appendix" in section_name or "example" in section_name
            ):
                self.errors.append(StructuralError(
                    "Appendix and example sections must be at document end"
                ))
                
            prev_name = section_name

    def _validate_renumbering_consistency(self) -> None:
        """Validate renumbering consistency per §6.3."""
        # Track section number gaps
        section_nums = []
        subsection_nums = {}
        
        for section in self.sections:
            # Get major section number
            match = re.match(r'(\d+)\.', section)
            if not match:
                continue
            major_num = int(match.group(1))
            section_nums.append(major_num)
            
            # Get subsection numbers
            subsections = re.finditer(r'### (\d+)\.(\d+)', self.sections[section])
            curr_subsections = []
            for submatch in subsections:
                sub_major = int(submatch.group(1))
                sub_minor = int(submatch.group(2))
                if sub_major != major_num:
                    self.errors.append(StructuralError(
                        f"Subsection {sub_major}.{sub_minor} has wrong major number"
                    ))
                curr_subsections.append(sub_minor)
            
            if curr_subsections:
                subsection_nums[major_num] = curr_subsections
        
        # Check for gaps in section numbering
        if section_nums != list(range(1, max(section_nums) + 1)):
            self.errors.append(StructuralError("Gaps detected in section numbering"))
            
        # Check subsection numbering
        for major, subs in subsection_nums.items():
            if subs != list(range(1, len(subs) + 1)):
                self.errors.append(StructuralError(
                    f"Gaps detected in subsection numbering under section {major}"
                ))

    def validate_metadata(self) -> None:
        """Validate metadata fields and placeholders per template requirements."""
        required_fields = [
            "Document Version",
            "Module Identifier",
            "System Context",
            "Author",
            "Last Updated",
            "Governance Model"
        ]
        
        # Additional fields for module PRDs
        if self.is_module_prd():
            required_fields.extend([
                "Domain",
                "Compatible Core PRD"
            ])
            
        # Check for required metadata fields
        for field in required_fields:
            if not re.search(rf'\*\*{field}:\*\*\s+\S', self.content):
                self.errors.append(StructuralError(
                    f"Missing required metadata field: {field}"
                ))
                
        # Check for unresolved placeholders
        placeholder_pattern = r'\[(Module Name|Describe[^\]]*|YYYY-MM-DD|version|.*_name|X\.Y\.Z)\]'
        matches = re.finditer(placeholder_pattern, self.content)
        for match in matches:
            self.errors.append(StructuralError(
                f"Unresolved placeholder: {match.group()}"
            ))

    def validate_governance_authority(self) -> None:
        """Validate governance authority rules per §10."""
        # Check if document attempts to override governance
        override_keywords = ["override", "ignore", "bypass", "waive"]
        governance_terms = ["governance", "protocol", "rule", "requirement"]
        
        for section in self.sections.values():
            for override in override_keywords:
                for term in governance_terms:
                    if re.search(
                        rf'\b{override}\b.*\b{term}\b', 
                        section.lower()
                    ):
                        self.errors.append(StructuralError(
                            "Governance rules cannot be overridden without formal revision"
                        ))

        # Validate precedence declaration for extensions
        if "_" in self.prd_path.stem:  # Tagged/extension PRD
            if not any("follows: governance > core PRD > module PRD" in s 
                      for s in self.sections.values()):
                self.errors.append(StructuralError(
                    "Extension PRDs must declare governance precedence order"
                ))

    def validate_compliance_requirements(self) -> None:
        """Validate compliance enforcement requirements per §11."""
        # Check for AI agent affirmation
        if not any("AI agent compliance" in s.lower() for s in self.sections.values()):
            self.errors.append(StructuralError(
                "Missing AI agent compliance affirmation"
            ))

        # Check for validation requirements
        validation_section = None
        for section in self.sections.values():
            if "validation" in section.lower():
                validation_section = section
                break

        if validation_section:
            required_validations = [
                "structural", "version", "reference"
            ]
            for validation in required_validations:
                if not re.search(rf'\b{validation}\b', validation_section.lower()):
                    self.errors.append(StructuralError(
                        f"Missing required {validation} validation rules"
                    ))
        else:
            self.errors.append(StructuralError(
                "Missing validation requirements section"
            ))

    def validate_all(self) -> List[ValidationError]:
        """Run all validation checks and return any errors."""
        try:
            self.validate_filename()
            self.validate_structure()
            self.validate_version_declaration()
            self.validate_changelog()
            self.validate_cross_references()
            
            # Version validation
            self.validate_version_compatibility()
            self.validate_version_references()
            self.validate_semantic_versioning()
            
            # Domain validation
            self.validate_domain_name()
            
            # AI Agent compliance validation
            self._validate_interface_definitions()
            self._validate_error_contracts()
            
            # Update discipline validation
            self.validate_update_discipline()
            
            # Newly added validations
            self.validate_metadata()
            self.validate_governance_authority()
            self.validate_compliance_requirements()
            
            return self.errors
        except ValidationError as e:
            self.errors.append(e)
            return self.errors
def validate_prd(prd_path: str) -> List[str]:
    """Validate a PRD file and return any validation errors."""
    try:
        validator = PRDValidator(prd_path)
        validator.validate_all()
        return []
    except ValidationError as e:
        return [str(e)]
    except Exception as e:
        return [f"Unexpected error: {str(e)}"]
