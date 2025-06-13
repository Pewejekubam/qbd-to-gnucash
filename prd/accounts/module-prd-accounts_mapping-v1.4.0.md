# Product Requirements Document — accounts_mapping.py

**Document Version:** v1.4.0  
**Module Identifier:** module-prd-accounts_mapping-v1.4.0.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-06-13  
**Compatible Core PRD:** core-prd-main-v3.9.1.md  
**Governance Model:** prd-governance-model-v2.7.0.md  

---

## 1. Scope
The `accounts_mapping` module manages the loading, validation, and user interaction workflows for QBD to GnuCash account type mappings. It provides a complete text-based workflow system with QBD path hints for handling unmapped accounts requiring user input, implements comprehensive ASCII validation and error recovery mechanisms, and coordinates seamlessly with the accounts orchestrator module. This module handles the critical mapping configuration that drives the entire accounts conversion pipeline while maintaining strict domain boundaries and governance compliance.

---

## 2. Inputs and Outputs

### 2.1 Inputs
- **Baseline mapping configuration**: `accounts_mapping_baseline.json` containing fundamental account type mappings
- **User override configurations**: Optional `accounts_mapping_specific.json` for customizations
- **Account records from orchestrator**: QBD account data passed from accounts.py for QBD path hints integration
- **User-completed mapping questions**: Text files with mapping decisions and full account paths
- **Runtime configuration**: Optional mapping file paths and validation settings

### 2.2 Outputs
- **Validated mapping configuration**: Merged and validated account type mappings for pipeline use
- **Text-based questions workspace**: `accounts_mapping_questions.txt` with QBD path hints for user editing
- **Comprehensive instructions reference**: `accounts_mapping_instructions.txt` with detailed mapping guidance
- **Processed mapping overrides**: `accounts_mapping_specific.json` generated from user questions workflow
- **Generational processed files**: `accounts_mapping_questions_v{number}.txt` for completed mapping sessions
- **Console logging output**: Hierarchical tagged messages for user guidance and debugging
- **HALT condition signals**: Boolean indicators when user action required for pipeline continuation

---

## 3. Functional Requirements

### 3.1 Overview
The accounts_mapping module loads mapping configuration files, validates schema compliance, detects unmapped account identifiers, and generates text-based workflow files for user input. The module processes user-completed mapping files and provides validated mapping configuration to the accounts processing pipeline.

### 3.2 Core Functional Behavior

#### 3.2.1 Mapping Configuration Management
- Load baseline mapping configuration from `accounts_mapping_baseline.json` with schema validation
- Merge user-specific overrides from `accounts_mapping_specific.json` when present
- Validate merged configuration against embedded schema requirements
- Provide account lookup services with fallback to default rules
- Raise MappingLoadError for configuration validation failures

#### 3.2.2 Unmapped Account Detection and Workflow Initiation
- Compare QBD accounts against mapping configuration keys
- Identify unmapped accounts requiring user mapping decisions
- Generate text-based questions files with QBD account name context
- Create dual-file output: questions workspace and instructions reference
- Log unmapped account detection with console messaging

#### 3.2.3 Text-Based Workflow with QBD Path Context
- Extract QBD account names from account records parameter
- Generate questions files displaying original QuickBooks account names
- Implement single full path input format for user mapping specification
- Create comprehensive instructions file with examples and validation rules
- Enforce ASCII-only input with validation and error reporting

#### 3.2.4 File Processing and Validation
- Parse user-completed questions files with input normalization
- Validate ASCII character compliance (printable characters 32-126)
- Handle partial completion scenarios with file preservation
- Convert completed mappings to JSON configuration format
- Implement generational file renaming for processed questions

#### 3.2.5 Error Recovery and Edge Case Handling
- Detect malformed questions files with structured error reporting
- Rename files with error suffixes for user inspection
- Provide error context with file path and validation failure details
- Handle file system errors with appropriate exception raising
- Preserve partial completion state for continued user workflow

---

## 4. Configuration & Environment

### 4.1 Config Schema
- **Baseline mapping file**: JSON format with `account_types` and `default_rules` sections
- **Schema validation**: Embedded validation for all mapping configuration files
- **Override mechanism**: Optional user-specific configuration files for customization
- **Runtime parameters**: File paths, validation flags, and workflow control settings

### 4.2 Environment Constraints
- **Python 3.8+** runtime environment required for typing support and JSON processing
- **UTF-8 encoding** for all text file operations with ASCII validation enforcement
- **File system access** for reading and writing configuration and questions files
- **Centralized logging** integration per Logging Framework PRD v1.0.5 requirements
- **Cross-platform compatibility** for file path operations and character encoding

---

## 5. Interface & Integration

### 5.1 Module Contract: accounts_mapping
- **Purpose**: Mapping configuration management and text-based user workflow coordination
- **Inputs**: Account records, mapping files, user-completed questions files
- **Outputs**: Validated mapping configuration, questions files, archive management
- **Invariants**: All mapping configuration must pass schema validation before use
- **Failure Modes**: Returns None for HALT conditions, raises structured exceptions for errors

### 5.2 Interface Contracts

#### 5.2.1 Core Interface Functions

##### `load_mapping(user_mapping_path: Optional[str] = None) -> Dict[str, Any]`
```python
def load_mapping(user_mapping_path: Optional[str] = None) -> Dict[str, Any]:
    """Load account mapping configuration with integrated text-based workflow.
    
    Args:
        user_mapping_path: Optional path to user override mapping file
        
    Returns:
        Dict containing validated account mapping rules and settings.
        Returns None when HALT condition reached (user action required).
        
    Raises:
        MappingLoadError: If mapping files cannot be loaded or fail validation
    """
```

##### `generate_text_mapping_questions(unmapped_accounts: List[str], account_records: List[Dict[str, Any]], output_dir: str) -> None`
```python
def generate_text_mapping_questions(unmapped_accounts: List[str], account_records: List[Dict[str, Any]], output_dir: str) -> None:
    """Generate user-friendly questions file for unmapped accounts with QBD path hints.
    
    Args:
        unmapped_accounts: List of QBD accounts needing mapping
        account_records: List of account records from QBD for path lookup and context
        output_dir: Directory for output file generation
        
    Raises:
        OutputWriteError: If questions file cannot be created
    """
```

##### `parse_text_mapping_file(questions_file_path: str) -> Dict[str, Any]`
```python
def parse_text_mapping_file(questions_file_path: str) -> Dict[str, Any]:
    """Parse user-completed text mapping file with full account paths and convert to JSON structure.
    
    Args:
        questions_file_path: Path to completed questions file
        
    Returns:
        Dict containing account_types mappings in baseline schema format
        
    Raises:
        MappingLoadError: If text file cannot be parsed or has invalid format
    """
```

##### `find_unmapped_types(records: List[Dict[str, Any]], mapping: Dict[str, Any]) -> List[str]`
```python
def find_unmapped_types(records: List[Dict[str, Any]], mapping: Dict[str, Any]) -> List[str]:
    """Find QBD accounts that are not mapped in the configuration.
    
    Args:
        records: List of account records from !ACCNT section
        mapping: Account mapping configuration
        
    Returns:
        List of unmapped QBD account strings
    """
```

#### 5.2.2 Enhanced Features Implementation

##### QBD Path Context Integration
- **Data Source**: Account records parameter contains QBD account data
- **Extraction Logic**: NAME field provides account identification
- **Display Format**: `QuickBooks import path: {account_name}` in questions file
- **Fallback Behavior**: Handle missing or malformed account records
- **Implementation**: Provides source system context for mapping decisions

##### Dual-File System
- **Questions Workspace**: Minimal interface for user input with essential validation rules
- **Instructions Reference**: Comprehensive documentation with examples and detailed guidance
- **File Coordination**: Questions file references instructions file
- **User Workflow**: Focused editing interface with comprehensive reference documentation

##### ASCII Validation and Input Normalization
- **Character Range**: Validate printable ASCII characters (32-126)
- **HALT Behavior**: Terminate pipeline on first non-ASCII character detection
- **Input Normalization**: Automatic cleanup of spacing around colons and path elements
- **Error Reporting**: Include character position and ASCII code information

### 5.3 Dependencies

| Module Name           | Import Path                                                                                      | Purpose                                   
|-----------------------|--------------------------------------------------------------------------------------------------|-------------------------------------------
| `typing`              | `from typing import Dict, List, Any, Optional`                                                  | Type annotations for interface contracts |
| `json`                | `import json`                                                                                    | Configuration file parsing and generation |
| `os`                  | `import os`                                                                                      | File system operations and path handling |
| `error_handler.py`    | `from utils.error_handler import MappingLoadError, OutputWriteError`                           | Standardized exception classes            |
| `logging.py`          | `from utils.logging import logging`                                                             | Centralized logging configuration         |

### 5.4 External Requirements
- **Core PRD Compliance**: All interface patterns follow Core PRD v3.9.1 Section 11.3.1 standards
- **Error Handling**: References authoritative error registry from Core PRD v3.9.1 Section 14
- **Logging Standards**: Complies with Logging Framework PRD v1.0.5 for all console and file logging
- **File Operations**: Cross-platform compatibility using os.path.join for all file system operations
- **Character Encoding**: UTF-8 encoding with ASCII validation for all text file operations

---

## 6. Validation & Error Handling

### 6.1 Validation Rules
- **Configuration Schema**: All mapping files must conform to embedded JSON schema validation
- **ASCII Compliance**: Text input files must contain only printable ASCII characters (32-126)
- **Path Format**: User-provided account paths must start with valid fundamental accounting types
- **Mapping Completeness**: All required account mappings must be present before pipeline continuation
- **File Integrity**: Questions files must be parseable and contain valid mapping data structure
- **Account Type Validation**: All QBD accounts must resolve to valid GnuCash type assignments

### 6.2 Error Classes & Exit Codes
Error classes and exit codes shall be implemented per [Core PRD v3.9.1 Section 11.3.2: Error Implementation Protocol](../core-prd-main-v3.9.1.md#1132-error-implementation-protocol). All error handling shall reference the authoritative registry in [Core PRD v3.9.1 Section 14: Authoritative Error Classes & Error Code Table](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table).

**Primary Error Classes:**
- **MappingLoadError (E1101)**: Mapping file missing, unreadable, or invalid schema
- **OutputWriteError (E0104)**: Output file cannot be written due to permissions or system issues
- **ValidationError (E0102)**: Input or output data fails schema or format validation

### 6.3 Error Context and Recovery
- **Structured Context**: All errors include file path, line number, and specific validation failure information
- **Recovery Guidance**: Error messages provide actionable steps for user resolution
- **File Preservation**: Malformed files renamed with error suffixes for user inspection and correction
- **Graceful Degradation**: Partial completion scenarios preserve user progress for continued editing

---

## 7. Logging & Observability

This module complies with the centralized logging module requirements as defined in [Logging Framework PRD v1.0.5](../logging/module-prd-logging-v1.0.5.md) and [Core PRD v3.9.1 Section 7.3: Logging Strategy](../core-prd-main-v3.9.1.md#73-logging-strategy). All logging and error handling shall reference the authoritative error classes, codes, and severity levels as defined in [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table).

### 7.1 Console Logging Standards
- **`[ACCOUNTS-MAPPING]`**: Configuration loading, validation, and file operations
- **`[ACCOUNTS-UNMAPPED-PROCESSING]`**: Unmapped account detection and workflow coordination
- **Hierarchical Structure**: All tags follow established precedence for user clarity
- **User Guidance**: Clear messaging for HALT conditions and required user actions
- **Progress Tracking**: Detailed status reporting for configuration loading and processing phases

### 7.2 Logging Requirements
- **Structured Output**: All log entries include sufficient metadata for debugging and audit purposes
- **Deterministic Format**: Consistent message patterns for automated processing and analysis
- **Flush Safety**: All critical events flushed to ensure capture during unexpected termination
- **Error Context**: Complete error information with file paths, line numbers, and validation details

---

## 8. Versioning & Change Control

### 8.1 Revision History
| Version | Date       | Author | Summary                           
|---------|------------|--------|-----------------------------------
| v1.0.0  | 2025-05-21 | PJ     | Initial governance-compliant PRD with text workflow foundation
| v1.0.1  | 2025-05-21 | PJ     | Interface contract specifications and validation requirements
| v1.0.2  | 2025-05-21 | PJ     | Enhanced error handling and example usage documentation
| v1.0.3  | 2025-05-21 | PJ     | Full processing through PRD template v3.5.1 for structural compliance
| v1.0.4  | 2025-05-21 | PJ     | Agentic compatibility enhancements and deterministic specifications
| v1.0.5  | 2025-05-21 | PJ     | Production readiness features and edge case handling documentation
| v1.0.6  | 2025-05-21 | PJ     | Text workflow integration and user interaction specifications
| v1.0.7  | 2025-05-21 | PJ     | Comprehensive text processing and validation requirements
| v1.0.8  | 2025-05-21 | PJ     | Enhanced user experience and file lifecycle management
| v1.0.9  | 2025-05-23 | PJ     | Module and core PRD document naming restructure for governance compliance
| v1.1.0  | 2025-05-23 | PJ     | Enhanced text workflow specifications and ASCII validation requirements
| v1.2.0  | 2025-06-03 | PJ     | Standardized error classes and logging section alignment with authoritative registry
| v1.3.0  | 2025-06-10 | PJ     | Module PRD alignment: Core PRD v3.9.1 compatibility and governance v2.7.0 compliance
| v1.3.1  | 2025-06-10 | PJ     | Enhanced text workflow features and production readiness specifications
| v1.3.2  | 2025-06-11 | PJ     | Console logging standards and agentic compatibility enhancements
| v1.4.0  | 2025-06-13 | PJ     | QBD account name context integration: account_records parameter added, dual-file system implemented, ASCII validation enhancements, account terminology corrections

### 8.2 Upstream/Downstream Impacts
- **Upstream Dependencies**: Receives account records from accounts.py orchestrator
- **Downstream Dependencies**: Provides validated mapping configuration to tree, validation, and export modules
- **Interface Changes**: account_records parameter added for QBD account name context integration
- **Data Flow**: Mapping configuration drives tree construction and validation phases

---

## 9. Non-Functional Requirements
- **Performance**: Process typical mapping workflows (1-50 unmapped accounts) in under 10 seconds
- **Reliability**: All user input preserved during error conditions with clear recovery paths
- **Usability**: Dual-file system provides focused workspace with comprehensive reference documentation
- **Maintainability**: Deterministic specifications enable autonomous agent implementation and testing
- **Compatibility**: Cross-platform file operations with consistent behavior across operating systems

---

## 10. Example Calls for Public Functions/Classes

### 10.1 Enhanced Interface Usage Examples

```python
from modules.accounts.accounts_mapping import load_mapping, generate_text_mapping_questions, find_unmapped_types
from utils.error_handler import MappingLoadError

# Mapping configuration loading
try:
    mapping = load_mapping()
    if mapping is None:
        print("HALT condition: User action required for mapping completion")
    else:
        print(f"Loaded {len(mapping['account_types'])} account mappings")
except MappingLoadError as e:
    print(f"Mapping configuration error: {e}")

# Questions generation with QBD account name context
account_records = [
    {'NAME': 'Contractor Income', 'ACCNTTYPE': 'MISC_LABOR_INCOME', 'DESC': 'Independent contractor payments'},
    {'NAME': 'Office Equipment', 'ACCNTTYPE': 'FIXED_ASSET', 'DESC': 'Computer equipment'}
]

unmapped_accounts = find_unmapped_types(account_records, mapping)
if unmapped_accounts:
    generate_text_mapping_questions(unmapped_accounts, account_records, 'output/')
    print(f"Generated questions file with QBD account name context for {len(unmapped_accounts)} accounts")
```

### 10.2 Text Workflow Integration Example

```python
# Workflow integration example
def handle_mapping_workflow(account_records, output_dir):
    """Complete mapping workflow with QBD account name context."""
    
    # Load mapping configuration
    mapping = load_mapping()
    if mapping is None:
        return False  # HALT condition active
    
    # Check for unmapped accounts
    unmapped = find_unmapped_types(account_records, mapping)
    if unmapped:
        # Generate questions with QBD account name context
        generate_text_mapping_questions(unmapped, account_records, output_dir)
        print("[ACCOUNTS-UNMAPPED-PROCESSING] Generated questions file with QBD account name context")
        print("[ACCOUNTS-UNMAPPED-PROCESSING] Edit the file and restart pipeline to continue")
        return False  # HALT for user action
    
    return True  # Continue pipeline processing
```

---

## 11. Appendix (Optional)

### 11.1 Data Schemas and Additional References

#### Enhanced Questions File Format
```
Where should these accounts go in GnuCash?

[MISC_LABOR_INCOME]
QuickBooks import path: Contractor Income
Enter the full GnuCash account path here: 

================================================================================
WARNING: ASCII only (A-Z, 0-9, basic punctuation). Special characters cause failure.
REQUIREMENT: Must start with Assets | Liabilities | Equity | Income | Expenses

Enter full account path using colons: "Income:Service Revenue:Labor"
See accounts_mapping_instructions.txt for examples and detailed help.
```

#### Configuration Schema Structure
```json
{
  "account_types": {
    "QBD_ACCOUNT_TYPE": {
      "gnucash_type": "GNUCASH_TYPE",
      "destination_hierarchy": "Full:Account:Path"
    }
  },
  "default_rules": {
    "unmapped_accounts": {
      "gnucash_type": "EXPENSE",
      "destination_hierarchy": "Expenses:Uncategorized"
    }
  }
}
```

#### QBD Account Name Context Data Flow
```
account_records (from orchestrator)
    ↓
Extract NAME field for context
    ↓
Generate "QuickBooks import path: {name}"
    ↓
Include in questions file for mapping context
    ↓
Mapping decisions with source account identification
```