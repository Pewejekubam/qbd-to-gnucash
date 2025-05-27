"""Tests for the system integration pipeline."""
import pytest
from pathlib import Path
import tempfile
import shutil
from typing import Generator

from ..system_integrator import SystemIntegrator
from ..ir_builder import IRBuilder
from utils.error_handler import IntegrationError, ValidationError

@pytest.fixture
def test_output_dir() -> Generator[Path, None, None]:
    """Fixture providing temporary test output directory."""
    with tempfile.TemporaryDirectory() as tmpdir:
        yield Path(tmpdir)

@pytest.fixture
def system_integrator(test_output_dir: Path) -> SystemIntegrator:
    """Fixture providing configured SystemIntegrator instance."""
    system_ir = Path(__file__).parent.parent.parent / 'system-ir.yaml'
    return SystemIntegrator(system_ir)

def test_basic_integration_pipeline(system_integrator: SystemIntegrator, 
                                 test_output_dir: Path,
                                 test_prd_paths: list[Path]):
    """Test basic integration pipeline functionality."""
    system_integrator.run_integration_pipeline(test_prd_paths, test_output_dir)
    
    # Verify expected outputs were generated
    assert test_output_dir.exists()
    assert (test_output_dir / "integration-report.md").exists()
    
    # Check for core module outputs
    accounts_dir = test_output_dir / "accounts"
    assert accounts_dir.exists()
    assert (accounts_dir / "accounts.py").exists()
    assert (accounts_dir / "tests").exists()
    assert (accounts_dir / "docs").exists()

def test_validation_only_mode(system_integrator: SystemIntegrator,
                            test_output_dir: Path,
                            test_prd_paths: list[Path]):
    """Test validation-only mode."""
    system_integrator.run_integration_pipeline(
        test_prd_paths, 
        test_output_dir,
        validate_only=True
    )
    
    # Verify no code was generated
    assert not test_output_dir.exists()
    
    # But checkpoints were recorded
    assert "ir_generated" in system_integrator.checkpoints
    assert system_integrator.checkpoints["ir_generated"]

def test_checkpoint_tracking(system_integrator: SystemIntegrator,
                           test_output_dir: Path,
                           test_prd_paths: list[Path]):
    """Test checkpoint tracking system."""
    system_integrator.run_integration_pipeline(test_prd_paths, test_output_dir)
    
    # Verify expected checkpoints
    assert "ir_generated" in system_integrator.checkpoints
    assert "system_validated" in system_integrator.checkpoints
    
    for prd in test_prd_paths:
        checkpoint = f"prd_parsed_{prd.stem}"
        assert checkpoint in system_integrator.checkpoints
        
def test_integration_error_handling(system_integrator: SystemIntegrator,
                                  test_output_dir: Path):
    """Test error handling in integration pipeline."""
    with pytest.raises(IntegrationError):
        # Try to integrate non-existent PRDs
        system_integrator.run_integration_pipeline(
            [Path("non-existent.md")],
            test_output_dir
        )
        
def test_system_validation(system_integrator: SystemIntegrator,
                          test_output_dir: Path,
                          test_prd_paths: list[Path]):
    """Test system-wide validation checks."""
    # First generate valid system
    system_integrator.run_integration_pipeline(test_prd_paths, test_output_dir)
    
    # Verify validation succeeds for valid system
    system_integrator._validate_system(test_output_dir)
    
    # Corrupt generated files and verify validation fails
    shutil.rmtree(test_output_dir / "accounts" / "tests")
    with pytest.raises(ValidationError):
        system_integrator._validate_system(test_output_dir)

def test_system_validation_failures(system_integrator: SystemIntegrator,
                                test_output_dir: Path,
                                test_prd_paths: list[Path]):
    """Test various system validation failure scenarios."""
    # First generate valid system
    system_integrator.run_integration_pipeline(test_prd_paths, test_output_dir)
    
    # Case 1: Missing required subdirectory
    shutil.rmtree(test_output_dir / "accounts" / "tests")
    with pytest.raises(ValidationError) as exc:
        system_integrator._validate_system(test_output_dir)
    assert "Required directory missing" in str(exc.value)
    
    # Case 2: Missing Python files
    shutil.rmtree(test_output_dir)
    system_integrator.run_integration_pipeline(test_prd_paths, test_output_dir)
    for py_file in (test_output_dir / "accounts").glob("*.py"):
        py_file.unlink()
    with pytest.raises(ValidationError) as exc:
        system_integrator._validate_system(test_output_dir)
    assert "No Python files found" in str(exc.value)
    
    # Case 3: Missing documentation
    shutil.rmtree(test_output_dir)
    system_integrator.run_integration_pipeline(test_prd_paths, test_output_dir)
    shutil.rmtree(test_output_dir / "accounts" / "docs")
    with pytest.raises(ValidationError) as exc:
        system_integrator._validate_system(test_output_dir)
    assert "Required directory missing" in str(exc.value)
    
def test_compliance_report(system_integrator: SystemIntegrator,
                         test_output_dir: Path,
                         test_prd_paths: list[Path]):
    """Test compliance report generation."""
    system_integrator.run_integration_pipeline(test_prd_paths, test_output_dir)
    
    report_path = test_output_dir / "integration-report.md"
    assert report_path.exists()
    
    content = report_path.read_text()
    assert "# Integration Compliance Report" in content
    assert "## Completed Checkpoints" in content
    assert "✅" in content  # Verify checkmarks for completed items

def test_detailed_compliance_report(system_integrator: SystemIntegrator,
                                 test_output_dir: Path,
                                 test_prd_paths: list[Path]):
    """Test detailed compliance report contents."""
    system_integrator.run_integration_pipeline(test_prd_paths, test_output_dir)
    
    report_path = test_output_dir / "integration-report.md"
    content = report_path.read_text()
    
    # Check section headers
    assert "# Integration Compliance Report" in content
    assert "## Generated Modules" in content
    assert "## Completed Checkpoints" in content
    assert "## System Status" in content
    
    # Check checkpoint categories
    assert "### Parsing Phase" in content
    assert "### Generation Phase" in content
    assert "### Validation Phase" in content
    
    # Verify checkpoint details
    assert "✅ prd_parsed_" in content
    assert "✅ module_generated_" in content
    assert "✅ system_validated" in content
    
    # Verify module details
    assert "### accounts" in content
    assert "#### Files Generated" in content
