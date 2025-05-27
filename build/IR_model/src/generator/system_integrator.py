"""System Integration Component for coordinating the IR build system.

This component provides the high-level integration pipeline that coordinates:
1. PRD parsing and IR generation
2. Code generation from IR
3. Testing and validation checkpoints
4. Build system compliance reporting

Version: 1.0.0
Compatible with Core PRD v3.6.3
"""
from pathlib import Path
from typing import Dict, List, Optional, Any
import os
import logging

from .ir_builder import IRBuilder
from .module_generator import ModuleGenerator
from .prd_parser import PRDParser
from .interface_parser import InterfaceParser

from utils.error_handler import (
    GenerationError, 
    ValidationError,
    IntegrationError
)
from utils.logging import setup_logging

logger = setup_logging()

class SystemIntegrator:
    """Handles system-wide integration and orchestration."""
    
    def __init__(self, system_ir_path: Path):
        """Initialize the system integrator.
        
        Args:
            system_ir_path: Path to system IR template
        """
        self.system_ir_path = Path(system_ir_path)
        self.ir_builder = IRBuilder(system_ir_path)
        self.module_generator = ModuleGenerator()
        self.checkpoints: Dict[str, bool] = {}
        
    def run_integration_pipeline(self, 
                               prd_paths: List[Path], 
                               output_dir: Path,
                               validate_only: bool = False) -> None:
        """Run the complete integration pipeline.
        
        Args:
            prd_paths: List of PRD files to process
            output_dir: Output directory for generated code
            validate_only: Only run validation, skip code generation
            
        Raises:
            IntegrationError: If integration pipeline fails
        """
        try:
            # Phase 1: IR Generation
            logger.info("Starting IR generation phase")
            self._reset_checkpoints()
            
            for prd_path in prd_paths:
                self.ir_builder.add_prd(prd_path)
                self._record_checkpoint(f"prd_parsed_{prd_path.stem}")
                
            ir = self.ir_builder.build()
            self._record_checkpoint("ir_generated")
            
            if validate_only:
                logger.info("Validation complete")
                return
                
            # Phase 2: Code Generation
            logger.info("Starting code generation phase")
            os.makedirs(output_dir, exist_ok=True)
            
            for name, component in ir['components'].items():
                if component['type'] == 'module':
                    component_dir = output_dir / name
                    self.module_generator.generate_module(component, component_dir)
                    self._record_checkpoint(f"module_generated_{name}")
                    
            # Phase 3: System-wide Validation
            logger.info("Running system-wide validation")
            self._validate_system(output_dir)
            self._record_checkpoint("system_validated")
            
            # Generate completion report
            self._generate_compliance_report(output_dir)
            logger.info("Integration pipeline completed successfully")
            
        except Exception as e:
            logger.error(f"Integration pipeline failed: {str(e)}")
            raise IntegrationError(f"Integration pipeline failed: {str(e)}")
            
    def _reset_checkpoints(self) -> None:
        """Reset all integration checkpoints."""
        self.checkpoints.clear()
        
    def _record_checkpoint(self, checkpoint: str) -> None:
        """Record a completed checkpoint.
        
        Args:
            checkpoint: Name of the completed checkpoint
        """
        self.checkpoints[checkpoint] = True
        logger.info(f"Checkpoint completed: {checkpoint}")
        
    def _validate_system(self, output_dir: Path) -> None:
        """Run system-wide validation checks.
        
        Args:
            output_dir: Directory containing generated code
            
        Raises:
            ValidationError: If system validation fails
        """
        try:
            logger.info("Starting system-wide validation")
            
            # 1. Directory Structure Validation
            if not output_dir.exists():
                raise ValidationError(f"Output directory does not exist: {output_dir}")
                
            # 2. Module Directory Validation
            for component_dir in output_dir.glob("*"):
                if component_dir.is_dir():
                    # Verify required subdirectories
                    required_subdirs = ["tests", "docs"]
                    for subdir in required_subdirs:
                        if not (component_dir / subdir).exists():
                            raise ValidationError(
                                f"Required directory missing: {component_dir.name}/{subdir}"
                            )
                            
                    # Verify module files
                    if not any(component_dir.glob("*.py")):
                        raise ValidationError(
                            f"No Python files found in module: {component_dir.name}"
                        )
                        
                    # Verify test files
                    if not any((component_dir / "tests").glob("test_*.py")):
                        raise ValidationError(
                            f"No test files found in module: {component_dir.name}"
                        )
                        
                    # Verify documentation files  
                    if not any((component_dir / "docs").glob("*.md")):
                        raise ValidationError(
                            f"No documentation found in module: {component_dir.name}"
                        )
            
            # 3. Checkpoint Order Validation
            required_checkpoints = [
                "ir_generated",
                "system_validated"
            ]
            
            for checkpoint in required_checkpoints:
                if checkpoint not in self.checkpoints:
                    raise ValidationError(f"Missing required checkpoint: {checkpoint}")
            
            # 4. Module Generation Validation
            components = [d.name for d in output_dir.glob("*") if d.is_dir()]
            for component in components:
                if f"module_generated_{component}" not in self.checkpoints:
                    raise ValidationError(
                        f"Module generation checkpoint missing: {component}"
                    )
                    
            # 5. Compliance Contract Validation
            compliance_report = output_dir / "integration-report.md"
            if not compliance_report.exists():
                raise ValidationError("Compliance report not generated")
            
            logger.info("System validation passed")
            
        except Exception as e:
            logger.error(f"System validation failed: {str(e)}")
            raise ValidationError(f"System validation failed: {str(e)}")
            
    def _generate_compliance_report(self, output_dir: Path) -> None:
        """Generate integration compliance report.
        
        Args:
            output_dir: Output directory for report
        """
        report_path = output_dir / "integration-report.md"
        
        with open(report_path, 'w') as f:
            f.write("# Integration Compliance Report\n\n")
            
            # 1. Generated Modules
            f.write("## Generated Modules\n\n")
            modules = [d for d in output_dir.glob("*") if d.is_dir()]
            if modules:
                for module_dir in modules:
                    f.write(f"### {module_dir.name}\n")
                    f.write("#### Files Generated\n")
                    files = list(module_dir.rglob("*.py"))
                    for file in files:
                        f.write(f"- {file.relative_to(module_dir)}\n")
                    f.write("\n")
            else:
                f.write("No modules were generated\n\n")
                
            # 2. Completed Checkpoints
            f.write("\n## Completed Checkpoints\n\n")
            
            # Sort checkpoints by type
            parsing_checkpoints = []
            generation_checkpoints = []
            validation_checkpoints = []
            
            for checkpoint in sorted(self.checkpoints.keys()):
                if checkpoint.startswith("prd_parsed"):
                    parsing_checkpoints.append(checkpoint)
                elif checkpoint.startswith("module_generated"):
                    generation_checkpoints.append(checkpoint)
                else:
                    validation_checkpoints.append(checkpoint)
            
            # Print checkpoints by category
            f.write("### Parsing Phase\n")
            for checkpoint in parsing_checkpoints:
                status = "✅" if self.checkpoints[checkpoint] else "❌"
                f.write(f"- {status} {checkpoint}\n")
            
            f.write("\n### Generation Phase\n")
            for checkpoint in generation_checkpoints:
                status = "✅" if self.checkpoints[checkpoint] else "❌"
                f.write(f"- {status} {checkpoint}\n")
            
            f.write("\n### Validation Phase\n")
            for checkpoint in validation_checkpoints:
                status = "✅" if self.checkpoints[checkpoint] else "❌"
                f.write(f"- {status} {checkpoint}\n")
            
            # 3. System Status
            f.write("\n## System Status\n\n")
            try:
                self._validate_system(output_dir)
                f.write("✅ System validation passed\n")
            except ValidationError as e:
                f.write(f"❌ System validation failed: {str(e)}\n")
                
        logger.info(f"Generated compliance report: {report_path}")
