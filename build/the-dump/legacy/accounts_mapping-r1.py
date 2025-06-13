"""Account mapping configuration loader with embedded schema validation.

UPDATED: Cross-platform path handling and embedded schema validation per Priority 1 decisions.
"""

import json
import os
from typing import Dict, Any, List, Optional

from utils.error_handler import MappingLoadError
from utils.logging import logging

def validate_mapping_schema(mapping_data: Dict[str, Any], file_path: str) -> List[str]:
    """Validate mapping data against embedded schema.
    
    Args:
        mapping_data: Parsed mapping configuration
        file_path: File path for error reporting
        
    Returns:
        List of validation error messages (empty if valid)
    """
    errors = []
    
    # Define embedded schema for validation
    MAPPING_SCHEMA = {
        "type": "object",
        "required": ["account_types", "default_rules"],
        "properties": {
            "account_types": {
                "type": "object",
                "additionalProperties": {
                    "type": "object",
                    "required": ["gnucash_type", "destination_hierarchy"],
                    "properties": {
                        "gnucash_type": {
                            "type": "string",
                            "enum": ["ASSET", "LIABILITY", "EQUITY", "INCOME", "EXPENSE", 
                                   "RECEIVABLE", "PAYABLE", "CASH", "BANK", "STOCK", 
                                   "MUTUAL", "CREDIT", "ROOT", "TRADING"]
                        },
                        "destination_hierarchy": {
                            "type": "string",
                            "minLength": 1,
                            "pattern": "^[^:]*(?::[^:]+)*$"  # Valid hierarchy format
                        }
                    },
                    "additionalProperties": False
                }
            },
            "default_rules": {
                "type": "object",
                "additionalProperties": {
                    "type": "string"
                }
            }
        },
        "additionalProperties": True  # Allow metadata fields
    }
    
    # Validate top-level structure
    if not isinstance(mapping_data, dict):
        errors.append(f"{file_path}: Root must be a JSON object")
        return errors
    
    # Check required fields
    for field in MAPPING_SCHEMA["required"]:
        if field not in mapping_data:
            errors.append(f"{file_path}: Missing required field '{field}'")
    
    # Validate account_types structure
    account_types = mapping_data.get("account_types", {})
    if not isinstance(account_types, dict):
        errors.append(f"{file_path}: 'account_types' must be an object")
    else:
        valid_gnucash_types = set(MAPPING_SCHEMA["properties"]["account_types"]["additionalProperties"]["properties"]["gnucash_type"]["enum"])
        
        for qbd_type, config in account_types.items():
            if not isinstance(config, dict):
                errors.append(f"{file_path}: Account type '{qbd_type}' must be an object")
                continue
            
            # Check required fields for each account type
            for required_field in ["gnucash_type", "destination_hierarchy"]:
                if required_field not in config:
                    errors.append(f"{file_path}: Account type '{qbd_type}' missing required field '{required_field}'")
                elif not isinstance(config[required_field], str):
                    errors.append(f"{file_path}: Account type '{qbd_type}' field '{required_field}' must be a string")
                elif not config[required_field].strip():
                    errors.append(f"{file_path}: Account type '{qbd_type}' field '{required_field}' cannot be empty")
            
            # Validate gnucash_type enum
            gnucash_type = config.get("gnucash_type", "").upper()
            if gnucash_type and gnucash_type not in valid_gnucash_types:
                errors.append(f"{file_path}: Account type '{qbd_type}' has invalid gnucash_type '{gnucash_type}'. Valid types: {sorted(valid_gnucash_types)}")
            
            # Validate hierarchy format
            hierarchy = config.get("destination_hierarchy", "")
            if hierarchy:
                # Check for invalid characters
                invalid_chars = ['/', '\\', '<', '>', '|', '"', '*', '?']
                for char in invalid_chars:
                    if char in hierarchy:
                        errors.append(f"{file_path}: Account type '{qbd_type}' hierarchy contains invalid character '{char}'")
                
                # Check for double colons or starting/ending colons
                if '::' in hierarchy:
                    errors.append(f"{file_path}: Account type '{qbd_type}' hierarchy contains double colons '::'")
                if hierarchy.startswith(':') or hierarchy.endswith(':'):
                    errors.append(f"{file_path}: Account type '{qbd_type}' hierarchy cannot start or end with ':'")
    
    # Validate default_rules structure
    default_rules = mapping_data.get("default_rules", {})
    if not isinstance(default_rules, dict):
        errors.append(f"{file_path}: 'default_rules' must be an object")
    else:
        for rule_key, rule_value in default_rules.items():
            # FIXED: Allow both string and object values in default_rules
            if isinstance(rule_value, str):
                # Simple string rule (legacy format)
                continue
            elif isinstance(rule_value, dict):
                # Complex object rule (current baseline format)
                # Validate object structure similar to account_types
                if 'gnucash_type' in rule_value and 'destination_hierarchy' in rule_value:
                    if not isinstance(rule_value['gnucash_type'], str) or not rule_value['gnucash_type'].strip():
                        errors.append(f"{file_path}: Default rule '{rule_key}' gnucash_type must be non-empty string")
                    if not isinstance(rule_value['destination_hierarchy'], str) or not rule_value['destination_hierarchy'].strip():
                        errors.append(f"{file_path}: Default rule '{rule_key}' destination_hierarchy must be non-empty string")
                else:
                    errors.append(f"{file_path}: Default rule '{rule_key}' object must have 'gnucash_type' and 'destination_hierarchy' fields")
            else:
                errors.append(f"{file_path}: Default rule '{rule_key}' must be either a string or an object with gnucash_type/destination_hierarchy")
    
    return errors

def generate_text_mapping_questions(unmapped_types: List[str], current_mapping: Dict[str, Any]) -> None:
    """Generate simple text file with mapping questions for user to answer.
    
    Args:
        unmapped_types: List of QBD account types needing mapping
        current_mapping: Current mapping configuration for reference
        
    Creates:
        output/accounts_mapping_questions.txt with simple questions format
    """
    try:
        # FIXED: Use cross-platform path construction
        questions_path = os.path.join("output", "accounts_mapping_questions.txt")
        
        # Create simple text questions format
        questions_content = "Where should these accounts go in GnuCash?\n\n"
        
        for qbd_type in unmapped_types:
            questions_content += f"{qbd_type}: \n"
            questions_content += f"Is this a child account? (Y/N): \n"
            questions_content += f"If yes, parent account name: \n\n"
        
        # Add educational footer
        questions_content += """================================================================================
INSTRUCTIONS:

1. For each account above, enter the GnuCash account name you want to use
2. If it's a child account, answer Y and provide the parent account path
3. Use colons (:) to separate account levels for deep hierarchies

EXAMPLES:
  Simple: 
    Account: Bank Fees
    Parent: Expenses

  Multi-level:
    Account: Contractor
    Parent: Income:Landscaping:Labor

ACCOUNT CATEGORIES:
- Assets (bank accounts, receivables, inventory)
- Liabilities (payables, loans, credit cards)  
- Equity (owner's equity, retained earnings)
- Income (sales, service revenue, other income)
- Expenses (operating costs, materials, labor)

PARSING CHECK: 
When you're done editing, make sure each account has BOTH fields filled in.
Leave this section unchanged.
================================================================================
"""
        
        # Write questions file
        os.makedirs("output", exist_ok=True)
        with open(questions_path, 'w', encoding='utf-8') as f:
            f.write(questions_content)
        
        logging.info(f"[MAPPING] Generated mapping questions file: {questions_path}")
        logging.info(f"[MAPPING] User action: Edit the questions file and run conversion again")
        logging.info(f"[MAPPING] Found {len(unmapped_types)} unmapped types: {unmapped_types}")
        
    except Exception as e:
        logging.warning(f"[MAPPING] Failed to generate mapping questions file: {str(e)}")

def parse_text_mapping_file() -> Dict[str, Any]:
    """Parse user-completed text mapping file and convert to JSON structure.
    
    Returns:
        Dict containing account_types mappings in baseline schema format
        
    Raises:
        MappingLoadError: If text file cannot be parsed or has invalid format
    """
    questions_path = os.path.join("output", "accounts_mapping_questions.txt")
    
    if not os.path.exists(questions_path):
        raise MappingLoadError(f"Questions file not found: {questions_path}")
    
    try:
        account_mappings = {}
        
        with open(questions_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Split content into sections (before instructions)
        if "================================================================================" in content:
            questions_section = content.split("================================================================================")[0]
        else:
            questions_section = content
        
        # Parse each account block
        lines = questions_section.split('\n')
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for account name line (contains colon and account name)
            if ':' in line and not line.startswith('Is this') and not line.startswith('If yes'):
                account_parts = line.split(':', 1)
                if len(account_parts) == 2:
                    qbd_type = account_parts[0].strip()
                    account_name = account_parts[1].strip()
                    
                    if account_name:  # User filled in account name
                        # Look for child account question
                        is_child = False
                        parent_account = ""
                        
                        # Check next few lines for child account info
                        for j in range(i + 1, min(i + 4, len(lines))):
                            if lines[j].strip().startswith('Is this a child account'):
                                child_parts = lines[j].split(':', 1)
                                if len(child_parts) == 2:
                                    is_child_answer = child_parts[1].strip().upper()
                                    is_child = is_child_answer.startswith('Y')
                            elif lines[j].strip().startswith('If yes, parent account name'):
                                parent_parts = lines[j].split(':', 1)
                                if len(parent_parts) == 2:
                                    parent_account = parent_parts[1].strip()
                        
                        # Build destination hierarchy
                        if is_child and parent_account:
                            destination_hierarchy = f"{parent_account}:{account_name}"
                        else:
                            destination_hierarchy = account_name
                        
                        # Infer GnuCash type from parent category
                        gnucash_type = infer_gnucash_type(destination_hierarchy)
                        
                        account_mappings[qbd_type] = {
                            "gnucash_type": gnucash_type,
                            "destination_hierarchy": destination_hierarchy
                        }
                        
                        logging.debug(f"[MAPPING] Parsed: {qbd_type} -> {gnucash_type} at {destination_hierarchy}")
            
            i += 1
        
        if not account_mappings:
            raise MappingLoadError("No valid account mappings found in questions file. Please fill in the account names and child account information.")
        
        # Create complete mapping structure
        result = {
            "account_types": account_mappings,
            "default_rules": {
                "unmapped_accounts": {
                    "gnucash_type": "EXPENSE",
                    "destination_hierarchy": "Expenses:Uncategorized"
                }
            }
        }
        
        logging.info(f"[MAPPING] Successfully parsed {len(account_mappings)} account mappings from questions file")
        return result
        
    except Exception as e:
        logging.error(f"[MAPPING] Failed to parse questions file: {str(e)}")
        raise MappingLoadError(f"Failed to parse questions file: {str(e)}")

def infer_gnucash_type(destination_hierarchy: str) -> str:
    """Infer GnuCash account type from destination hierarchy path.
    
    Args:
        destination_hierarchy: Full account path like "Assets:Checking" or "Expenses:Office"
        
    Returns:
        Appropriate GnuCash account type
    """
    path_parts = destination_hierarchy.split(':')
    root_category = path_parts[0].strip().lower()
    
    # Map root categories to GnuCash types
    category_mapping = {
        'assets': 'ASSET',
        'asset': 'ASSET',
        'liabilities': 'LIABILITY', 
        'liability': 'LIABILITY',
        'equity': 'EQUITY',
        'income': 'INCOME',
        'expenses': 'EXPENSE',
        'expense': 'EXPENSE'
    }
    
    gnucash_type = category_mapping.get(root_category, 'EXPENSE')  # Default to EXPENSE
    
    # Special cases for specific account names
    account_name = path_parts[-1].strip().lower()
    if 'receivable' in account_name:
        gnucash_type = 'RECEIVABLE'
    elif 'payable' in account_name:
        gnucash_type = 'PAYABLE'
    
    return gnucash_type

def load_mapping(user_mapping_path: Optional[str] = None) -> Dict[str, Any]:
    """Load account mapping configuration with text-based workflow support.
    
    Args:
        user_mapping_path: Optional path to user override mapping file
        
    Returns:
        Dict containing validated account mapping rules and settings
        
    Raises:
        MappingLoadError: If mapping files cannot be loaded or fail validation
    """
    try:
        # Load baseline mappings from module directory
        baseline_path = os.path.join(os.path.dirname(__file__), 'accounts_mapping_baseline.json')
        
        logging.debug(f"[MAPPING] Loading baseline mapping from: {baseline_path}")
        
        if not os.path.exists(baseline_path):
            raise MappingLoadError(f"Baseline mapping file not found: {baseline_path}")
        
        with open(baseline_path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        # Validate baseline mapping against schema
        baseline_errors = validate_mapping_schema(mapping, baseline_path)
        if baseline_errors:
            raise MappingLoadError(f"Baseline mapping validation failed: {'; '.join(baseline_errors)}")
        
        logging.info(f"[MAPPING] Loaded and validated baseline mapping: {len(mapping.get('account_types', {}))} account types")
        
        # Check for text-based mapping workflow
        questions_path = os.path.join("output", "accounts_mapping_questions.txt")
        override_path = user_mapping_path or os.path.join("output", "accounts_mapping_specific.json")
        
        # Priority 1: Check if user has completed text questions file
        if os.path.exists(questions_path):
            try:
                # Check if questions file has been filled out
                with open(questions_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Simple check: if file contains filled-in answers
                if ':' in content and any(line.strip().endswith(': Y') or line.strip().endswith(': N') for line in content.split('\n')):
                    logging.info(f"[MAPPING] Found completed questions file, processing user mappings")
                    
                    # Parse text file and convert to JSON
                    text_mapping = parse_text_mapping_file()
                    
                    # Save as specific file for future use
                    with open(override_path, 'w', encoding='utf-8') as f:
                        json.dump(text_mapping, f, indent=2, ensure_ascii=False)
                    
                    # Merge with baseline
                    if 'account_types' in text_mapping:
                        mapping['account_types'].update(text_mapping['account_types'])
                        logging.info(f"[MAPPING] Applied {len(text_mapping['account_types'])} account type mappings from questions file")
                        
                        # Archive processed questions file
                        processed_path = os.path.join("output", "accounts_mapping_questions_processed.txt")
                        os.rename(questions_path, processed_path)
                        logging.info(f"[MAPPING] Questions file processed and archived as: {processed_path}")
                    
                    logging.info(f"[MAPPING] Text-based mapping workflow completed successfully")
                    return mapping
                    
            except Exception as e:
                logging.warning(f"[MAPPING] Failed to process questions file: {str(e)}")
                # Fall through to normal specific file handling
        
        # Priority 2: Load existing specific file if present
        if os.path.exists(override_path):
            logging.info(f"[MAPPING] Found mapping overrides file: {override_path}")
            try:
                with open(override_path, 'r', encoding='utf-8') as f:
                    specific = json.load(f)
                
                # Validate user override file against schema
                validation_errors = validate_mapping_schema(specific, override_path)
                if validation_errors:
                    logging.error(f"[E1107] Mapping override file has validation errors:")
                    for error in validation_errors:
                        logging.error(f"  - {error}")
                    raise MappingLoadError(f"Override file validation failed: {len(validation_errors)} errors found. See log for details.")
                
                override_count = 0
                # Merge specific overrides into baseline
                if 'account_types' in specific:
                    mapping['account_types'].update(specific['account_types'])
                    override_count += len(specific['account_types'])
                    logging.info(f"[MAPPING] Applied {len(specific['account_types'])} account type overrides")
                    
                if 'default_rules' in specific:
                    mapping['default_rules'].update(specific['default_rules'])
                    override_count += len(specific['default_rules'])
                    logging.info(f"[MAPPING] Applied {len(specific['default_rules'])} default rule overrides")
                
                if override_count > 0:
                    logging.info(f"[MAPPING] Configuration customization: {override_count} total overrides applied from user file")
                else:
                    logging.warning(f"Override file exists but contains no valid overrides: {override_path}")
                    
            except json.JSONDecodeError as e:
                logging.error(f"[E0107] Override file contains invalid JSON: {override_path} - {str(e)}")
                raise MappingLoadError(f"Override file contains invalid JSON: {str(e)}")
            except (KeyError, TypeError) as e:
                logging.error(f"[E0107] Override file structure error: {override_path} - {str(e)}")
                raise MappingLoadError(f"Override file structure error: {str(e)}")
        else:
            logging.info("[MAPPING] No user override file found - using baseline configuration")
            logging.debug(f"[MAPPING] To customize mappings, create: {override_path}")
        
        # Final validation of merged configuration
        final_errors = validate_mapping_schema(mapping, "merged_configuration")
        if final_errors:
            raise MappingLoadError(f"Final merged configuration validation failed: {'; '.join(final_errors)}")
        
        logging.info(f"[MAPPING] Account mapping configuration ready - {len(mapping['account_types'])} types mapped and validated")
        return mapping
        
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"[E1101] Failed to load account mapping configuration: {str(e)}")
        raise MappingLoadError(f"Failed to load account mapping configuration: {str(e)}")

def find_unmapped_types(records: List[Dict[str, Any]], mapping: Dict[str, Any]) -> List[str]:
    """Find QBD account types that are not mapped in the configuration.
    
    Args:
        records: List of account records from !ACCNT section
        mapping: Account mapping configuration
        
    Returns:
        List of unmapped QBD account type strings
    """
    mapped_types = set(mapping.get('account_types', {}).keys())
    record_types = set(record.get('ACCNTTYPE', '') for record in records)
    unmapped = record_types - mapped_types
    
    if unmapped:
        logging.warning(f"[E1102] Found {len(unmapped)} unmapped account types: {sorted(unmapped)}")
        logging.debug(f"[MAPPING] Mapped types available: {sorted(mapped_types)}")
        
        # Generate text-based mapping questions for user configuration
        generate_text_mapping_questions(sorted(unmapped), mapping)
    else:
        logging.debug("[MAPPING] All account types are properly mapped")
    
    return sorted(unmapped)