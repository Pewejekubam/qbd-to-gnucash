# Product Requirements Document — Mapping Module  

**Document Version:** v1.1.0
**Module Identifier:** module-prd-accounts_mapping-v1.1.0.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-06-11  
**Compatible Core PRD:** core-prd-main-v3.9.1.md  
**Governance Model:** prd-governance-model-v2.7.0.md  

---

## 1. Scope
Loads, merges, and validates account type mapping files. Provides lookup services for resolving QBD types to GnuCash account types and hierarchy paths. Manages text-based mapping workflow for unmapped account types requiring user interaction.

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

#### 3.2.4 Text-Based Mapping Workflow
- Detects presence of `accounts_mapping_questions.txt` file
- Parses completed questions file with structure validation
- Generates user-friendly questions file for unmapped account types
- Manages generational file naming
- Integrates user responses into specific mapping configuration
- Coordinates HALT conditions for user interaction requirements

#### 3.2.5 Version-Locked Core PRD Reference  
- Aligns with [Core PRD v3.9.1 Section 6.5.1](../core-prd-main-v3.9.1.md#651-processing-rules)
- Coordinates with [accounts PRD v1.3.1 Section 4.2](../accounts/module-prd-accounts-v1.3.1.md#42-core-module-behavior-accountspy) for text workflow orchestration

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

#### load_mapping  
- **Arguments:** `user_mapping_path: Optional[str]`  
- **Return Type:** `Dict[str, Any]`  
- **Exceptions:** `MappingLoadError`  
- **Description:** Loads and merges mapping files for QBD to GnuCash account types.  

#### find_unmapped_types  
- **Arguments:** `records: List[Dict[str, Any]]`, `mapping: Dict[str, Any]`  
- **Return Type:** `List[str]`  
- **Exceptions:** None  
- **Description:** Returns a list of unmapped QBD account types.  

#### generate_text_mapping_questions
- **Arguments:** `unmapped_types: List[str]`, `output_path: str`
- **Return Type:** `None`
- **Exceptions:** `OutputWriteError`
- **Description:** Creates user-friendly questions file for unmapped account types. Generates structured questions with instructions for user completion.
- **Side Effects:** Creates `accounts_mapping_questions.txt` in specified output directory
- **Log Patterns:**
  ```
  [WARN] [MAPPING] Found {count} unmapped account types requiring user input:
  [WARN] [MAPPING]   - {account_type}
  [INFO] [MAPPING] Generated questions file: accounts_mapping_questions.txt
  [INFO] [MAPPING] Edit the file and restart pipeline to continue
  [HALT] User action required
  ```

#### parse_text_mapping_file
- **Arguments:** `questions_file_path: str`
- **Return Type:** `Dict[str, Any]`
- **Exceptions:** `MappingLoadError`
- **Description:** Parses completed questions file into JSON mapping structure. Validates file structure and user responses for completeness and format compliance.
- **Side Effects:** Renames processed file to generational format
- **Log Patterns:**
  ```
  [INFO] [MAPPING] Found questions file: accounts_mapping_questions.txt
  [INFO] [MAPPING] Parsing questions file
  [INFO] [MAPPING] Successfully parsed {count} account mappings
  [INFO] [MAPPING] File renamed to accounts_mapping_questions_v{number}.txt
  [INFO] [MAPPING] Generated mappings saved to accounts_mapping_specific.json
  ```
- **Error Patterns:**
  ```
  [ERROR] [MAPPING] File appears corrupted or severely malformed
  [INFO] [MAPPING] File renamed to accounts_mapping_questions_v{number}.txt
  [INFO] [MAPPING] Recommend deleting or renaming the processed file and restarting pipeline
  [HALT] Processing stopped
  ```

### 5.2 Dependencies  
- [Logging Framework module PRD v1.0.4](../logging/module-prd-logging-v1.0.4.md)  
- [Core PRD v3.9.1 Section 7.3: Logging Strategy](../core-prd-main-v3.9.1.md#73-logging-strategy)  

---

## 6. Validation & Error Handling

### 6.1 Validation Rules
- Input mapping files shall follow expected schema with JSON validation
- Text questions file structure validation (format compliance, not business logic)
- All lookups shall use exact QBD keys
- User responses shall include required fields (account name, parent indication)
- Generated mappings shall conform to baseline schema structure

### 6.2 Error Classes & Exit Codes  
- The error classes and exit codes for this module are defined in the authoritative registry in [Core PRD v3.9.1 Section 14: Authoritative Error Classes & Error Code Table](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table). All errors shall be raised and logged in compliance with the centralized logging module requirements. No ad-hoc or undocumented error classes are permitted.

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

### 8.2 Upstream/Downstream Impacts
Changes to this module may affect other modules that rely on the mapping functionality. Text workflow integration affects accounts.py orchestration and user interaction patterns.

---

## 9. Non-Functional Requirements
- Text workflow files shall be human-readable and editable with standard text editors
- File operations shall be atomic to prevent corruption during user editing
- Error messages shall provide clear guidance for user recovery actions

---

## 10. Example Calls for Public Functions/Classes

### 10.1 load_mapping

```python
# Normal case
mapping = load_mapping('output/accounts_mapping_specific.json')
# Edge case: missing file
try:
    mapping = load_mapping('output/missing.json')
except MappingLoadError as e:
    print(e)
```

### 10.2 Text Workflow Integration

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

### 10.3 Complete Workflow Example

```python
# Full text-based mapping workflow
def process_mapping_with_text_workflow(records, output_dir):
    # Load existing mappings
    mapping = load_mapping(f'{output_dir}/accounts_mapping_specific.json')
    
    # Check for existing questions file
    questions_file = f'{output_dir}/accounts_mapping_questions.txt'
    if os.path.exists(questions_file):
        try:
            user_mappings = parse_text_mapping_file(questions_file)
            # Update mapping with user responses
            mapping.update(user_mappings)
        except MappingLoadError as e:
            print(f"Parse error: {e}")
            return False
    
    # Detect remaining unmapped types
    unmapped = find_unmapped_types(records, mapping)
    if unmapped:
        generate_text_mapping_questions(unmapped, output_dir)
        return False  # HALT for user input
    
    return True  # Continue processing
```

---

## 11. Appendix (Optional)

### 11.1 Text Questions File Format

**Generated Format:**
```
Where should these accounts go in GnuCash?

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
4. Save this file and restart the pipeline to continue processing
================================================================================
```

**User Completion Example:**
```
Where should these accounts go in GnuCash?

MISC_LABOR_INCOME: Labor Income
Is this a child account? (Y/N): Y
If yes, parent account name: Income:Consulting

EQUIPMENT: Office Equipment
Is this a child account? (Y/N): N
If yes, parent account name: 
```

### 11.2 File Lifecycle Management

**Workflow States:**
1. **Generation:** `accounts_mapping_questions.txt` created when unmapped types detected
2. **User Editing:** User completes questions in text editor
3. **Processing:** Pipeline parses completed file on restart
4. **Archival:** Processed file renamed to `accounts_mapping_questions_v{number}.txt`
5. **Integration:** User mappings merged into `accounts_mapping_specific.json`

**File Naming Pattern:**
- Active questions: `accounts_mapping_questions.txt`
- Processed files: `accounts_mapping_questions_v001.txt`, `accounts_mapping_questions_v002.txt`, etc.