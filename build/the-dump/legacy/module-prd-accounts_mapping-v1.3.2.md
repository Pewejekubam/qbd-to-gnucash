# Product Requirements Document — Mapping Module  

**Document Version:** v1.3.2
**Module Identifier:** module-prd-accounts_mapping-v1.3.2.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-06-12  
**Compatible Core PRD:** core-prd-main-v3.9.1.md  
**Governance Model:** prd-governance-model-v2.7.0.md  

---

## 1. Scope
Loads, merges, and validates account type mapping files. Provides lookup services for resolving QBD types to GnuCash account types and hierarchy paths. Manages text-based mapping workflow for unmapped account types requiring user interaction with comprehensive edge case handling and production-ready error recovery.

---

## 2. Inputs and Outputs

### 2.1 Inputs
- Baseline mapping JSON (required)
- Specific mapping JSON (optional override)
- Text-based questions file (`accounts_mapping_questions.txt`) when present
- QBD account records for unmapped type detection

### 2.2 Outputs
- Combined dictionary of `account_types` and `default_rules`
- Text-based questions file for unmapped types (`accounts_mapping_questions.txt`)
- Generational archive files (`accounts_mapping_questions_v{number}.txt`)
- Updated specific mapping JSON with user-provided mappings

---

## 3. Functional Requirements  

### 3.1 Overview  
- Load and merge mapping files  
- Provide lookup services for QBD to GnuCash account types  
- Handle unmapped types through text-based user workflow
- Manage file lifecycle for user interaction and generational naming

### 3.2 Detailed Behavior  

#### 3.2.1 Loading Mapping Files  
- Loads baseline and specific mapping JSON files  
- Merges the two files into a single dictionary with specific overriding baseline

#### 3.2.2 Lookup Services  
- Provides exact QBD key lookups (e.g., `BANK`, `OCASSET`, `AR`)  
- Fallback behavior is defined by `default_rules`  

#### 3.2.3 Unmapped Types Detection
- Returns a list of unmapped QBD account types  
- Logs all key loads, fallbacks, and mapping mismatches  

#### 3.2.4 Text Workflow File Lifecycle Management
- Detects presence of `accounts_mapping_questions.txt` file in output directory
- Implements complete orchestration through `load_mapping()` function with priority sequence
- Processes completed questions file with structure validation and error recovery
- Implements generational versioning system using rename operations for completed files only
- Coordinates HALT conditions when user interaction requirements detected
- Manages file priority sequence: questions file → specific override → baseline mapping
- Provides structured error recovery guidance for malformed user input
- Handles partial completion scenarios with file preservation for continued editing

#### 3.2.5 Enhanced Questions File Generation
- Renders verbatim template containing critical requirements as specified in [Section 12.1: Text Questions File Format](#121-text-questions-file-format)
- Includes process explanation and file lifecycle documentation within generated file
- Provides enhanced examples showing proper fundamental categorization
- Instructs users to consult QuickBooks Desktop Chart of Accounts for guidance
- Uses generational rename terminology throughout user-facing content
- Includes ASCII-only character warning with clipboard paste guidance

#### 3.2.6 PRD Specification Compliance
- This module shall implement processing rules as specified in [Core PRD v3.9.1 Section 11.4: Input File Discovery and Processing Model](../core-prd-main-v3.9.1.md#114-input-file-discovery-and-processing-model)
- Text workflow orchestration shall conform to requirements defined in [Accounts PRD v1.3.1 Section 4.2: Core Module Behavior](../accounts/module-prd-accounts-v1.3.1.md#42-core-module-behavior-accountspy)
- Interface contracts shall maintain precedence hierarchy established in [Core PRD v3.9.1 Section 11.5: Interface Authority Precedence Rules](../core-prd-main-v3.9.1.md#115-interface-authority-precedence-rules)

---

## 4. Configuration & Environment

### 4.1 Config Schema
- Mapping File Schema (accounts_mapping_specific.json, accounts_mapping_baseline.json):
  ```JSON
  {
    "$schema": "http://json-schema.org/draft-07/schema#",
    "type": "object",
    "properties": {
      "account_types": {
        "type": "object",
        "additionalProperties": {
          "type": "object",
          "properties": {
            "gnucash_type": {"type": "string"},
            "hierarchy_path": {"type": "string"}
          },
          "required": ["gnucash_type", "hierarchy_path"]
        }
      },
      "default_rules": {
        "type": "object",
        "additionalProperties": {"type": "string"}
      }
    },
    "required": ["account_types", "default_rules"]
  }
  ```

### 4.2 Environment Constraints
- Input mapping files shall follow expected schema
- Text workflow files shall be writable in output directory
- Module-specific logging/error handling requirements are handled by the centralized logging module

---

## 5. Interface & Integration  

### 5.1 Interface Contracts  

#### Complete Orchestration Interface
```python
def load_mapping(user_mapping_path: Optional[str] = None) -> Dict[str, Any]:
    """Load account mapping with integrated text workflow orchestration.
    
    Execution Algorithm:
    1. IF accounts_mapping_questions.txt exists:
       a. CALL parse_text_mapping_file(questions_path)
       b. CALL validate_mapping_completeness(parsed, unmapped_types)
       c. IF complete: CALL finalize_mapping_file(path, True) → continue
       d. IF partial: CALL finalize_mapping_file(path, False) → RETURN False
    2. ELIF accounts_mapping_specific.json exists:
       a. LOAD and merge with baseline
    3. ELSE: LOAD baseline only
    
    Args:
        user_mapping_path (Optional[str]): Optional path to user override mapping file
    Returns:
        Dict[str, Any]: Validated account mapping rules and settings
        Structure: {
            "account_types": Dict[str, {"gnucash_type": str, "destination_hierarchy": str}],
            "default_rules": Dict[str, Any]
        }
    Raises:
        MappingLoadError: If mapping files cannot be loaded or fail validation
    """
```

#### Refactored Parsing Interface
```python
def parse_text_mapping_file(questions_file_path: str) -> Dict[str, Any]:
    """Parse questions file with input validation and normalization.
    
    Input Processing Rules:
    - ASCII validation range: printable characters (32-126)
    - Line-by-line scanning with immediate HALT on first non-ASCII detection
    - Case normalization: Assets/Liabilities/Equity/Income/Expenses → title case
    - Whitespace parsing: single spaces preserved, double spaces terminate parsing
    - Y/N answer extraction: first [yYnN] character detected per line
    - Special character validation: colons allowed for hierarchy, QBD-valid characters permitted
    
    Args:
        questions_file_path (str): Full path to questions file
    Returns:
        Dict[str, Any]: Parsed mappings (complete or partial)
        Structure: {
            "account_types": Dict[str, {"gnucash_type": str, "destination_hierarchy": str}],
            "default_rules": Dict[str, Any]
        }
    Raises:
        MappingLoadError: Non-ASCII content, invalid characters, or parsing failure
    """
```

#### Completeness Validation Interface
```python
def validate_mapping_completeness(parsed_mappings: Dict[str, Any], 
                                 required_types: List[str]) -> bool:
    """Validate if all required account types have mappings.
    
    Args:
        parsed_mappings (Dict[str, Any]): Parsed mapping results from questions file
        required_types (List[str]): List of unmapped QBD account types requiring answers
    Returns:
        bool: True if all required types mapped, False if partial completion
    Raises:
        ValidationError: If mapping structure invalid
    """
```

#### File Lifecycle Management Interface
```python
def finalize_mapping_file(questions_file_path: str, 
                         is_complete: bool, 
                         is_malformed: bool = False) -> None:
    """Manage questions file lifecycle based on processing outcome.
    
    Args:
        questions_file_path (str): Path to original questions file
        is_complete (bool): True if all mappings complete
        is_malformed (bool): True if file parsing failed
    Side Effects:
        - Complete: Renames to accounts_mapping_questions_v{number}.txt
        - Partial: Preserves original filename for continued editing
        - Malformed: Renames with error suffix
    Raises:
        OutputWriteError: If file operations fail (E0104)
    """
```

#### Enhanced Questions Generation Interface
```python
def generate_text_mapping_questions(unmapped_types: List[str], output_path: str) -> None:
    """Generate comprehensive questions file with enhanced user guidance.
    
    Args:
        unmapped_types (List[str]): QBD types requiring mapping
        output_path (str): Directory path for questions file output
    Side Effects:
        Creates accounts_mapping_questions.txt with ASCII warnings and enhanced instructions
    Raises:
        OutputWriteError: If file cannot be written (E0104)
    """
```

#### find_unmapped_types  
- **Arguments:** `records: List[Dict[str, Any]]`, `mapping: Dict[str, Any]`  
- **Return Type:** `List[str]`  
- **Exceptions:** None  
- **Description:** Returns a list of unmapped QBD account types.  

### 5.2 Dependencies

| Module Name           | Import Path                                                | Purpose                                   
|-----------------------|------------------------------------------------------------|-------------------------------------------
| typing                | from typing import Dict, List, Any, Optional              | Type annotations for interface contracts |
| json                  | import json                                                | JSON file loading and parsing             |
| os                    | import os                                                  | File system operations and path handling  |
| error_handler.py      | from utils.error_handler import MappingLoadError, OutputWriteError | Standardized exception classes    |
| logging.py            | from utils.logging import setup_logging                   | Centralized logging configuration         |

**External PRD Dependencies:**
- [Logging Framework PRD v1.0.5](../logging/module-prd-logging-v1.0.5.md) - Centralized logging compliance
- [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table) - Error code registry
- [Core PRD v3.9.1 Section 11.5](../core-prd-main-v3.9.1.md#115-interface-authority-precedence-rules) - Interface authority  

---

## 6. Validation & Error Handling

### 6.1 Validation Rules
- Input mapping files shall follow expected schema with JSON validation
- Text questions file structure validation (format compliance, not business logic)
- All lookups shall use exact QBD keys
- User responses shall include required fields (account name, parent indication)
- Generated mappings shall conform to baseline schema structure

### 6.2 Error Classes & Exit Codes  
- All error classes shall reference [Core PRD v3.9.1 Section 14: Authoritative Error Classes & Error Code Table](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table). All errors shall be raised and logged in compliance with the centralized logging module requirements.

### 6.2.1 Text Workflow Error Messages

**File Processing Messages:**
```
[ACCOUNTS-MAPPING] Found completed questions file, processing user mappings
[ACCOUNTS-MAPPING] Successfully parsed {count} account mappings from questions file
[ACCOUNTS-MAPPING] Completeness validation: {complete_count} of {total_count} required types mapped
[ACCOUNTS-MAPPING] Questions file renamed to accounts_mapping_questions_v{number}.txt
[ACCOUNTS-MAPPING] Generated mappings saved to accounts_mapping_specific.json
```

**Partial Completion Messages:**
```
[ACCOUNTS-MAPPING] Questions file contains incomplete mappings
[ACCOUNTS-MAPPING] Complete all account type mappings and restart pipeline
[ACCOUNTS-UNMAPPED-PROCESSING] Pipeline HALT: User action required
```

**Error Conditions:**
```
[ACCOUNTS-MAPPING] File appears corrupted or severely malformed
[ACCOUNTS-MAPPING] Questions file renamed to accounts_mapping_questions_v{number}.txt
[ACCOUNTS-MAPPING] Recommend deleting or renaming the processed file and restarting pipeline
[ACCOUNTS-UNMAPPED-PROCESSING] Pipeline HALT: Processing stopped
```

**Input Validation Error Messages:**
```
[ACCOUNTS-MAPPING] Non-ASCII characters detected in questions file - please re-edit using standard ASCII characters only
[ACCOUNTS-MAPPING] Invalid characters detected in account name: {invalid_chars}
[ACCOUNTS-MAPPING] File system error occurred during questions file processing
[ACCOUNTS-MAPPING] Questions file appears empty or corrupted
```

**Input Normalization Messages:**
```
[ACCOUNTS-MAPPING] Input normalization applied: case corrected for {account_name}
[ACCOUNTS-MAPPING] Whitespace normalized in user input
[ACCOUNTS-MAPPING] Special characters validated for GnuCash compatibility
```

**User Guidance Messages:**
```
[ACCOUNTS-UNMAPPED-PROCESSING] Found {count} unmapped account types requiring user input
[ACCOUNTS-UNMAPPED-PROCESSING] Generated questions file: accounts_mapping_questions.txt
[ACCOUNTS-UNMAPPED-PROCESSING] Edit the file and restart pipeline to continue
[ACCOUNTS-UNMAPPED-PROCESSING] Pipeline HALT: User action required
```

---

## 7. Logging & Observability
- This module complies with the centralized logging module requirements as defined in [Logging Framework module PRD v1.0.4](../logging/module-prd-logging-v1.0.4.md) and [Core PRD v3.9.1 Section 7.3: Logging Strategy](../core-prd-main-v3.9.1.md#73-logging-strategy). All logging and error handling shall reference the authoritative error classes, codes, and severity levels as defined in [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table). Logging shall be structured, deterministic, and flush-safe, and shall capture all error events, validation failures, and key processing steps with sufficient metadata for downstream auditing and debugging.

---

## 8. Versioning & Change Control

### 8.1 Revision History
| Version | Date       | Author     | Summary                  
|---------|------------|------------|--------------------------
| v1.0.0  | 2025-05-19 | PJ         | Initial release          
| v1.0.2  | 2025-05-19 | PJ         | Add explicit JSON Schema 
| v1.0.4  | 2025-05-19 | PJ         | Align with PRD-base v3.4.0
| v1.0.5  | 2025-05-21 | PJ         | Full processing through PRD template v3.5.1
| v1.0.6  | 2025-05-23 | PJ         | Updated logging and core PRD references for governance compliance
| v1.0.7  | 2025-05-23 | PJ         | module and core PRD document naming and location restructure
| v1.0.8  | 2025-06-03 | PJ         | Standardized Error Classes & Exit Codes and Logging & Observability sections to reference authoritative error code table
| v1.1.0  | 2025-06-11 | PJ         | Major additive release: complete text-based mapping workflow integration, new interface contracts, file lifecycle management, error handling patterns, deterministic language enforcement, upstream PRD version locking
| v1.3.0  | 2025-06-12 | PJ         | Major enhancement: console logging standards, comprehensive edge case handling, input validation with ASCII enforcement, partial completion logic, refined interface contracts per CR-003-v4.0.0
| v1.3.1  | 2025-06-12 | PJ         | Enhanced agentic compatibility with algorithmic specifications extracted from working implementation
| v1.3.2  | 2025-06-12 | PJ         | Declarative language enforcement: eliminated temporal references, converted prohibitive language, standardized shall/must usage, enhanced dependency mapping, removed redundant sections

---

## 9. Console Logging Standards

### 8.2 Upstream/Downstream Impacts
Changes to this module may affect other modules that rely on the mapping functionality. Text workflow integration affects accounts.py orchestration and user interaction patterns.

### 9.1 Hierarchical Tag Convention
This module follows established console logging conventions to maintain consistency across the conversion tool while preserving domain-specific autonomy.

**Tag Structure:**
- `[ACCOUNTS-MAPPING]` - Main mapping configuration and file management
- `[ACCOUNTS-UNMAPPED-PROCESSING]` - Unmapped type detection and text workflow processing

### 9.2 Implementation Requirements
- All console logging uses centralized logging functions (`log_user_info()`, `log_user_error()`, etc.)
- Tags are included in message content, not enforced by core infrastructure
- ASCII characters only for terminal compatibility
- All console output lines shall be tagged with appropriate hierarchy

### 9.3 Text Workflow Console Patterns

**Unmapped Type Detection:**
```
[ACCOUNTS-UNMAPPED-PROCESSING] Found {count} unmapped account types requiring user input
[ACCOUNTS-UNMAPPED-PROCESSING] Generated questions file: accounts_mapping_questions.txt
[ACCOUNTS-UNMAPPED-PROCESSING] Pipeline HALT: User action required
```

**Questions File Processing:**
```
[ACCOUNTS-MAPPING] Found completed questions file, processing user mappings
[ACCOUNTS-MAPPING] Successfully parsed {count} account mappings from questions file
[ACCOUNTS-MAPPING] Questions file renamed to accounts_mapping_questions_v{number}.txt
[ACCOUNTS-MAPPING] Generated mappings saved to accounts_mapping_specific.json
```

**Partial Completion Patterns:**
```
[ACCOUNTS-MAPPING] Questions file contains incomplete mappings
[ACCOUNTS-MAPPING] Complete all account type mappings and restart pipeline
[ACCOUNTS-UNMAPPED-PROCESSING] Pipeline HALT: User action required
```

**Error Recovery Patterns:**
```
[ACCOUNTS-UNMAPPED-PROCESSING] File appears corrupted or severely malformed
[ACCOUNTS-MAPPING] Questions file renamed to accounts_mapping_questions_v{number}.txt
[ACCOUNTS-MAPPING] Recommend deleting or renaming the processed file and restarting pipeline
[ACCOUNTS-UNMAPPED-PROCESSING] Pipeline HALT: Processing stopped
```

**Edge Case Handling Patterns:**
```
[ACCOUNTS-MAPPING] File system error occurred during questions file processing
[ACCOUNTS-MAPPING] Non-ASCII content detected - pipeline halted for user correction
[ACCOUNTS-MAPPING] Input validation completed with normalization applied
```

### 9.4 HALT Condition Messaging
- HALT conditions signal user action requirements through console messaging
- Pipeline coordination achieved through `False` return values from module functions
- User guidance emphasizes consulting QuickBooks Desktop Chart of Accounts
- Error recovery instructions provide clear next steps for malformed input

---

## 10. Non-Functional Requirements
- Text workflow files shall be human-readable and editable with standard text editors
- File operations shall be atomic to prevent corruption during user editing
- Error messages shall provide clear guidance for user recovery actions

---

## 11. Example Calls for Public Functions/Classes

### 11.1 load_mapping

```python
# Normal case
mapping = load_mapping('output/accounts_mapping_specific.json')
# Edge case: missing file
try:
    mapping = load_mapping('output/missing.json')
except MappingLoadError as e:
    print(e)
```

### 11.2 Text Workflow Integration

```python
# Detect unmapped types and generate questions
unmapped = find_unmapped_types(records, mapping)
if unmapped:
    generate_text_mapping_questions(unmapped, 'output/')
    # Pipeline halts for user input
    return False

# Process completed questions file
try:
    user_mappings = parse_text_mapping_file('output/accounts_mapping_questions.txt')
    # Integrate user mappings into pipeline
except MappingLoadError as e:
    print(f"Questions file parsing failed: {e}")
    return False
```

### 11.3 Complete Workflow Example

```python
# Full text-based mapping workflow with partial completion handling
def process_mapping_with_text_workflow(records, output_dir):
    # Load existing mappings
    mapping = load_mapping(f'{output_dir}/accounts_mapping_specific.json')
    
    # Check for existing questions file
    questions_file = f'{output_dir}/accounts_mapping_questions.txt'
    if os.path.exists(questions_file):
        try:
            # Parse questions file
            parsed_mappings = parse_text_mapping_file(questions_file)
            
            # Check completeness
            unmapped = find_unmapped_types(records, mapping)
            is_complete = validate_mapping_completeness(parsed_mappings, unmapped)
            
            if is_complete:
                # Complete - finalize and continue
                finalize_mapping_file(questions_file, is_complete=True)
                mapping.update(parsed_mappings)
            else:
                # Partial - preserve file and halt
                finalize_mapping_file(questions_file, is_complete=False)
                return False  # HALT for user completion
                
        except MappingLoadError as e:
            # Malformed - rename with error and halt
            finalize_mapping_file(questions_file, is_complete=False, is_malformed=True)
            print(f"Parse error: {e}")
            return False
    
    # Continue with normal processing
    return True
```

---

## 12. Appendix (Optional)

### 12.1 Text Questions File Format

**Generated Format with Enhanced Instructions:**
```
Where should these accounts go in GnuCash?

NON-ASCII CHARACTER WARNING:
This file shall contain only standard ASCII characters (A-Z, a-z, 0-9, basic punctuation).
Non-ASCII characters will cause immediate pipeline failure with descriptive error.
If pasting from QuickBooks, verify no special characters were copied.

CRITICAL REQUIREMENT:
ALL ACCOUNTS SHALL BE PLACED UNDER ONE OF THESE 5 FUNDAMENTAL CATEGORIES:
- Assets (bank accounts, receivables, inventory, equipment)
- Liabilities (payables, loans, credit cards, accrued expenses)  
- Equity (owner's equity, retained earnings, capital)
- Income (sales, service revenue, interest income, other income)
- Expenses (operating costs, materials, labor, utilities)

ACCOUNT_TYPE_1: 
Is this a child account? (Y/N): 
If yes, parent account name: 

ACCOUNT_TYPE_2: 
Is this a child account? (Y/N): 
If yes, parent account name: 

================================================================================
INSTRUCTIONS:
1. For each account above, enter the GnuCash account name you want to use
2. If it's a child account, answer Y and provide the parent account path
3. Use colons (:) to separate account levels for deep hierarchies
4. Review and consult your QuickBooks Desktop Chart of Accounts to help guide you

EXAMPLES - All accounts shall go under one of the 5 fundamental categories:

Assets Example:
  PETTY_CASH: Office Petty Cash
  Is this a child account? (Y/N): Y
  If yes, parent account name: Assets:Current Assets

Income Example:
  CONSULTING_FEES: Consulting Revenue
  Is this a child account? (Y/N): Y  
  If yes, parent account name: Income:Service Revenue

Expenses Example:
  OFFICE_SUPPLIES: Office Supplies
  Is this a child account? (Y/N): Y
  If yes, parent account name: Expenses:Office Expenses

PARSING CHECK: 
When you're done editing, make sure each account has ALL required fields filled in:
- Account name (after the colon)
- Child account answer (Y or N)
- Parent account name (if you answered Y)
Leave this section unchanged.
================================================================================
```

### 12.2 User Answer Parsing Specification

**Field Extraction Rules:**
- **Account Name**: Extract text after first colon and before newline, trim whitespace
- **Y/N Answer**: Scan line for first occurrence of [yYnN], case-insensitive matching
- **Parent Account**: Extract text after "parent account name:" colon, trim whitespace
- **Line Termination**: Double spaces or newline characters terminate field parsing
- **Validation**: Each field shall be non-empty after whitespace removal

**Parsing Algorithm:**
1. Split file content by line breaks
2. For each line containing ":", extract account type and user answer
3. For lines containing "Y/N", extract boolean response
4. For lines containing "parent account name", extract hierarchy path
5. Validate completeness before proceeding with mapping generation

### 12.2 File Lifecycle Management

**Workflow States:**
1. **Generation:** `accounts_mapping_questions.txt` created when unmapped types detected
2. **User Editing:** User completes questions in text editor
3. **Processing:** Pipeline parses completed file on restart
4. **Completion Check:** Validate all required types have mappings
5. **Conditional Archival:** Complete files renamed to `accounts_mapping_questions_v{number}.txt`, partial files preserved
6. **Integration:** Complete mappings merged into `accounts_mapping_specific.json`

**File Priority Sequence:**
- Questions file takes precedence over specific override file
- Complete mappings in questions file replace JSON config entries
- Mixed file states handled transparently with questions file priority

**File Naming Pattern:**
- Active questions: `accounts_mapping_questions.txt`
- Completed files: `accounts_mapping_questions_v001.txt`, `accounts_mapping_questions_v002.txt`, etc.
- Malformed files: `accounts_mapping_questions_error_v001.txt`