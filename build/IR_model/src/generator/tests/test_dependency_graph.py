"""Tests for the dependency graph."""

import pytest
from pathlib import Path
from ..dependency_graph import DependencyGraph

def test_dependency_graph_creation():
    """Test basic graph creation and relationships."""
    graph = DependencyGraph()
    
    # Add some nodes
    graph.add_node('module_a', 'v1.0.0', 'module')
    graph.add_node('module_b', 'v1.0.0', 'module')
    graph.add_node('interface_c', 'v1.0.0', 'interface')
    
    # Add dependencies
    graph.add_dependency('module_a', 'interface_c')
    graph.add_dependency('module_b', 'interface_c')
    
    # Check relationships
    assert len(graph.get_dependencies('module_a')) == 1
    assert len(graph.get_dependents('interface_c')) == 2

def test_cycle_detection():
    """Test dependency cycle detection."""
    graph = DependencyGraph()
    
    # Create a cycle
    graph.add_node('a', 'v1.0.0', 'module')
    graph.add_node('b', 'v1.0.0', 'module')
    graph.add_node('c', 'v1.0.0', 'module')
    
    graph.add_dependency('a', 'b')
    graph.add_dependency('b', 'c')
    graph.add_dependency('c', 'a')
    
    cycles = graph.validate_cycles()
    assert len(cycles) == 1
    assert len(cycles[0]) == 4  # a -> b -> c -> a

def test_version_validation():
    """Test version compatibility validation."""
    graph = DependencyGraph()
    
    # Add nodes with incompatible versions
    graph.add_node('module_a', 'v2.0.0', 'module')
    graph.add_node('module_b', 'v1.0.0', 'module')
    
    graph.add_dependency('module_a', 'module_b')
    
    errors = graph.validate_versions()
    assert len(errors) == 1
    assert errors[0][2].startswith('Major version mismatch')

def test_ordered_list():
    """Test topological ordering of dependencies."""
    graph = DependencyGraph()
    
    # Create a simple dependency chain
    graph.add_node('a', 'v1.0.0', 'module')
    graph.add_node('b', 'v1.0.0', 'module')
    graph.add_node('c', 'v1.0.0', 'module')
    
    graph.add_dependency('a', 'b')
    graph.add_dependency('b', 'c')
    
    ordered = graph.build_ordered_list()
    assert ordered == ['c', 'b', 'a']  # Dependencies should come first
