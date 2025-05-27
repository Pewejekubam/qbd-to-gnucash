"""Tests for the IR builder component."""

import pytest
from pathlib import Path
from ..ir_builder import IRBuilder

def test_ir_builder_basic(test_prd_path):
    """Test basic IR building functionality."""
    builder = IRBuilder(Path('system-ir.yaml'))
    builder.add_prd(test_prd_path)
    
    ir = builder.build()
    assert 'components' in ir
    assert 'relationships' in ir
    assert 'dependencies' in ir['relationships']

def test_dependency_resolution(test_prd_path):
    """Test dependency resolution between components."""
    builder = IRBuilder(Path('system-ir.yaml'))
    
    # Add test PRDs
    builder.add_prd(test_prd_path)
    
    # Build IR
    ir = builder.build()
    
    # Verify dependencies are properly ordered
    component_order = list(ir['components'].keys())
    for name, deps in ir['relationships']['dependencies'].items():
        component_idx = component_order.index(name)
        for dep in deps:
            dep_idx = component_order.index(dep)
            assert dep_idx < component_idx  # Dependencies should come before dependents

def test_version_validation():
    """Test version compatibility validation."""
    builder = IRBuilder(Path('system-ir.yaml'))
    
    # Add components with incompatible versions
    with pytest.raises(ValueError) as exc:
        builder.add_prd(Path('incompatible-versions.md'))
        builder.build()
    
    assert "Version compatibility errors" in str(exc.value)

def test_cycle_detection():
    """Test dependency cycle detection."""
    builder = IRBuilder(Path('system-ir.yaml'))
    
    # Add components that form a cycle
    with pytest.raises(ValueError) as exc:
        builder.add_prd(Path('cyclic-dependencies.md'))
        builder.build()
    
    assert "Dependency cycle detected" in str(exc.value)
