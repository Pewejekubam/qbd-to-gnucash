"""Dependency graph builder for PRD components."""

from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple

@dataclass
class DependencyNode:
    """A node in the dependency graph."""
    name: str
    version: str
    type: str  # module, interface, utility
    dependencies: Set[str]
    required_by: Set[str]
    path: Optional[Path] = None

class DependencyGraph:
    """Builds and manages dependency relationships between PRD components."""
    
    def __init__(self):
        self.nodes: Dict[str, DependencyNode] = {}
    
    def add_node(self, 
                name: str,
                version: str,
                type: str,
                path: Optional[Path] = None) -> None:
        """Add a node to the graph."""
        if name not in self.nodes:
            self.nodes[name] = DependencyNode(
                name=name,
                version=version,
                type=type,
                dependencies=set(),
                required_by=set(),
                path=path
            )
    
    def add_dependency(self, 
                      from_node: str, 
                      to_node: str) -> None:
        """Add a dependency relationship between nodes."""
        if from_node not in self.nodes or to_node not in self.nodes:
            return
        
        self.nodes[from_node].dependencies.add(to_node)
        self.nodes[to_node].required_by.add(from_node)
    
    def get_dependencies(self, node: str) -> Set[str]:
        """Get all dependencies for a node."""
        if node not in self.nodes:
            return set()
        return self.nodes[node].dependencies
    
    def get_dependents(self, node: str) -> Set[str]:
        """Get all nodes that depend on the given node."""
        if node not in self.nodes:
            return set()
        return self.nodes[node].required_by
    
    def validate_cycles(self) -> List[List[str]]:
        """Find any dependency cycles in the graph.
        
        Returns:
            List of cycles found, where each cycle is a list of node names.
        """
        cycles = []
        visited = set()
        path = []
        
        def dfs(node: str) -> None:
            if node in path:
                # Found a cycle
                cycle_start = path.index(node)
                cycles.append(path[cycle_start:] + [node])
                return
            
            if node in visited:
                return
            
            visited.add(node)
            path.append(node)
            
            for dep in self.nodes[node].dependencies:
                dfs(dep)
            
            path.pop()
        
        # Run DFS from each node
        for node in self.nodes:
            if node not in visited:
                dfs(node)
        
        return cycles
    
    def validate_versions(self) -> List[Tuple[str, str, str]]:
        """Validate version compatibility between nodes.
        
        Returns:
            List of (from_node, to_node, error_message) for incompatible versions
        """
        errors = []
        
        for node_name, node in self.nodes.items():
            for dep_name in node.dependencies:
                dep_node = self.nodes[dep_name]
                
                # Compare major versions
                node_major = int(node.version.lstrip('v').split('.')[0])
                dep_major = int(dep_node.version.lstrip('v').split('.')[0])
                
                if node_major != dep_major:
                    errors.append((
                        node_name,
                        dep_name,
                        f"Major version mismatch: {node.version} -> {dep_node.version}"
                    ))
        
        return errors
    
    def build_ordered_list(self) -> List[str]:
        """Build a topologically ordered list of nodes.
        
        Returns:
            List of node names in dependency order (dependencies before dependents)
        """
        ordered = []
        visited = set()
        
        def visit(node: str) -> None:
            if node in visited:
                return
            
            visited.add(node)
            
            # Visit all dependencies first
            for dep in self.nodes[node].dependencies:
                visit(dep)
            
            ordered.append(node)
        
        # Visit all nodes
        for node in self.nodes:
            if node not in visited:
                visit(node)
        
        return ordered
