"""Quick Start Guide for the Validation Framework.

This module provides example usage and quick reference for the validation framework.
"""

from pathlib import Path
from typing import List
from .prd_validator import PRDValidator, ValidationError
from .schema_validator import SchemaValidator, SchemaError

def validate_prd_file(prd_path: str) -> List[ValidationError]:
    """Validate a single PRD file.
    
    Args:
        prd_path: Path to the PRD file to validate
        
    Returns:
        List of validation errors, empty if valid
    """
    validator = PRDValidator(prd_path)
    return validator.validate_all()

def validate_schemas_in_prd(prd_path: str) -> List[SchemaError]:
    """Validate all schemas in a PRD file.
    
    Args:
        prd_path: Path to the PRD file containing schemas
        
    Returns:
        List of schema errors, empty if valid
    """
    validator = SchemaValidator(prd_path)
    return validator.validate_all()

def validate_prd_directory(directory: str) -> dict:
    """Validate all PRD files in a directory.
    
    Args:
        directory: Path to directory containing PRD files
        
    Returns:
        Dictionary mapping file paths to lists of errors
    """
    results = {}
    dir_path = Path(directory)
    
    for prd_file in dir_path.glob("**/*.md"):
        # Skip README files
        if prd_file.name.startswith("README"):
            continue
            
        # Validate PRD structure and content
        prd_errors = validate_prd_file(str(prd_file))
        
        # Validate schemas if present
        schema_errors = validate_schemas_in_prd(str(prd_file))
        
        if prd_errors or schema_errors:
            results[str(prd_file)] = {
                "prd_errors": prd_errors,
                "schema_errors": schema_errors
            }
            
    return results

def print_validation_results(results: dict) -> None:
    """Pretty print validation results.
    
    Args:
        results: Dictionary of validation results
    """
    if not results:
        print("✅ All files are valid!")
        return
        
    for file_path, errors in results.items():
        print(f"\n📄 {file_path}")
        
        if errors["prd_errors"]:
            print("\nPRD Validation Errors:")
            for error in errors["prd_errors"]:
                print(f"❌ {error}")
                
        if errors["schema_errors"]:
            print("\nSchema Validation Errors:")
            for error in errors["schema_errors"]:
                print(f"❌ {error.message} at {error.location}")

# Example usage
if __name__ == "__main__":
    import sys
    
    if len(sys.argv) != 2:
        print("Usage: python -m validation.quickstart <prd_file_or_directory>")
        sys.exit(1)
        
    path = sys.argv[1]
    if Path(path).is_dir():
        results = validate_prd_directory(path)
    else:
        results = {
            path: {
                "prd_errors": validate_prd_file(path),
                "schema_errors": validate_schemas_in_prd(path)
            }
        }
    
    print_validation_results(results)
