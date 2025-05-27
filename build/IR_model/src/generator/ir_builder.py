"""IR Builder component for assembling the complete IR from parsed PRD components."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set

from .section_parser import SectionParser
from .interface_parser import InterfaceParser
from .dependency_graph import DependencyGraph
from .metadata_parser import (
    extract_metadata,
    determine_component_type,
    extract_title
)

@dataclass
class IRComponent:
    """A component in the IR."""
    name: str
    version: str
    type: str  # module, interface, utility
    interfaces: List[Dict]
    dependencies: Set[str]
    source_file: Path

class IRBuilder:
    """Builds the complete IR from parsed PRD components."""
    
    def __init__(self, system_ir_path: Path):
        """Initialize the IR builder.
        
        Args:
            system_ir_path: Path to the system-ir.yaml template file
        """
        self.system_ir_path = Path(system_ir_path)
        self.components: Dict[str, IRComponent] = {}
        self.dependency_graph = DependencyGraph()
    
    def add_prd(self, prd_path: Path) -> None:
        """Parse and add a PRD file to the IR.
        
        Args:
            prd_path: Path to the PRD markdown file
        """
        # Parse sections
        section_parser = SectionParser(prd_path)
        content = prd_path.read_text()
        sections = section_parser.parse(content)
        
        # Parse interfaces
        interface_parser = InterfaceParser(prd_path)
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
        
        # Extract component info
        name = self._extract_component_name(sections)
        version = self._extract_version(sections)
        type = self._extract_component_type(sections)
        
        # Add to IR
        component = IRComponent(
            name=name,
            version=version,
            type=type,
            interfaces=[i.__dict__ for i in interfaces],
            dependencies=set(),
            source_file=prd_path
        )
        
        self.components[name] = component
        
        # Add to dependency graph
        self.dependency_graph.add_node(
            name=name,
            version=version,
            type=type,
            path=prd_path
        )
        
        # Add interface dependencies
        for interface in interfaces:
            for dep in interface.dependencies:
                if dep in self.components:
                    self.dependency_graph.add_dependency(name, dep)
                    component.dependencies.add(dep)
    
    def build(self) -> Dict:
        """Build the complete IR.
        
        Returns:
            Dict containing the complete IR structure
        """
        # Validate dependencies
        self._validate_dependencies()
        
        # Build ordered component list
        ordered_components = self.dependency_graph.build_ordered_list()
        
        # Assemble IR
        ir = {
            'version': 'v1.0.0',  # IR schema version
            'components': {},
            'relationships': {
                'dependencies': {}
            }
        }
        
        # Add components in dependency order
        for name in ordered_components:
            component = self.components[name]
            ir['components'][name] = {
                'version': component.version,
                'type': component.type,
                'interfaces': component.interfaces,
                'source_file': str(component.source_file)
            }
            
            # Add dependencies
            if component.dependencies:
                ir['relationships']['dependencies'][name] = sorted(component.dependencies)
        
        return ir
    
    def _validate_dependencies(self) -> None:
        """Validate all dependencies are resolvable and versions are compatible."""
        # Check for cycles
        cycles = self.dependency_graph.validate_cycles()
        if cycles:
            cycle_str = ' -> '.join(cycles[0])
            raise ValueError(f"Dependency cycle detected: {cycle_str}")
        
        # Check versions
        version_errors = self.dependency_graph.validate_versions()
        if version_errors:
            errors = [f"{a} -> {b}: {msg}" for a, b, msg in version_errors]
            raise ValueError(
                "Version compatibility errors:\n" + 
                "\n".join(f"- {e}" for e in errors)
            )
      def _extract_component_name(self, sections: List) -> str:
        """Extract component name from PRD sections.
        
        First tries to extract from metadata, then falls back to title.
        
        Args:
            sections: List of parsed sections
            
        Returns:
            Component name string
        """
        # Extract metadata from content
        content = sections[0].content if sections else ""
        metadata = extract_metadata(content)
        
        # Try name from metadata
        if 'name' in metadata:
            return metadata['name']
            
        # Try title from sections
        title = extract_title(sections)
        if title:
            # Convert title to component name format
            name = title.lower().replace(' ', '_')
            return name
            
        # Fall back to filename-based name
        if sections and hasattr(sections[0], 'source_file'):
            return Path(sections[0].source_file).stem
            
        return "unnamed_component"
    
    def _extract_version(self, sections: List) -> str:
        """Extract version from PRD sections.
        
        Looks for version in metadata and validates format.
        
        Args:
            sections: List of parsed sections
            
        Returns:
            Version string in vX.Y.Z format
        """
        content = sections[0].content if sections else ""
        metadata = extract_metadata(content)
        
        # Look for version in metadata
        version = metadata.get('version', '').strip()
        if version:
            # Ensure v prefix
            if not version.startswith('v'):
                version = f"v{version}"
            
            # Validate format
            if re.match(r'^v\d+\.\d+\.\d+$', version):
                return version
        
        return "v1.0.0"  # Default version
    
    def _extract_component_type(self, sections: List) -> str:
        """Extract component type from PRD sections.
        
        Determines type based on metadata and content structure.
        
        Args:
            sections: List of parsed sections
            
        Returns:
            Component type string: 'module', 'interface', or 'utility'
        """
        content = sections[0].content if sections else ""
        metadata = extract_metadata(content)
        
        return determine_component_type(sections, metadata)
