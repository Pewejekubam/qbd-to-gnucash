"""Account mapping configuration loader with embedded schema validation.

UPDATED: Cross-platform path handling and embedded schema validation per Priority 1 decisions.
"""

import json
import os
from typing import Dict, Any, List, Optional

from utils.error_handler import MappingLoadError, OutputWriteError
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

def generate_text_mapping_questions(unmapped_accounts: List[str], records: List[Dict[str, Any]], output_dir: str) -> None:
    """Generate user-friendly questions file for unmapped accounts with QBD path hints.
    
    Args:
        unmapped_accounts: List of QBD accounts needing mapping
        records: List of account records from QBD for path lookup
        output_dir: Directory for output file
        
    Raises:
        OutputWriteError: If questions file cannot be created
    """
    try:
        # Use cross-platform path construction
        questions_path = os.path.join(output_dir, "accounts_mapping_questions.txt")
        instructions_path = os.path.join(output_dir, "accounts_mapping_instructions.txt")
        
        # Create clean questions file with QBD path hints
        questions_content = "Where should these accounts go in GnuCash?\n\n"
        
        # Create lookup for QBD account data
        qbd_accounts = {record.get('ACCNTTYPE', ''): record for record in records}
        
        for qbd_account in unmapped_accounts:
            questions_content += f"[{qbd_account}]\n"
            
            # Add QBD path hint if available
            if qbd_account in qbd_accounts:
                record = qbd_accounts[qbd_account]
                # Build QBD path from available fields
                qbd_path_parts = []
                if record.get('PARENT'):
                    qbd_path_parts.append(record.get('PARENT'))
                if record.get('NAME'):
                    qbd_path_parts.append(record.get('NAME'))
                
                if qbd_path_parts:
                    qbd_path = ':'.join(qbd_path_parts)
                    questions_content += f"QuickBooks import path: {qbd_path}\n"
            
            questions_content += f"Enter the full GnuCash account path here: \n\n"
        
        # Add separator and minimal instructions
        questions_content += """================================================================================
WARNING: ASCII only (A-Z, 0-9, basic punctuation). Special characters cause failure.
REQUIREMENT: Must start with Assets | Liabilities | Equity | Income | Expenses

Enter full account path using colons: "Income:Service Revenue:Labor"
See accounts_mapping_instructions.txt for examples and detailed help.
"""
        
        # Create detailed instructions file
        instructions_content = """DETAILED MAPPING INSTRUCTIONS FOR GNUCASH ACCOUNT CONVERSION

ABOUT THIS PROCESS:
This maps QuickBooks accounts not in the baseline configuration.
Complete accounts_mapping_questions.txt and restart the pipeline to:
1. Process your mappings and validate them
2. Generate accounts.csv for GnuCash import  
3. Rename questions file to accounts_mapping_questions_v###.txt

THE 5 FUNDAMENTAL ACCOUNTING TYPES:
All account paths must start with one of these:
- Assets: bank accounts, receivables, inventory, equipment, cash
- Liabilities: payables, loans, credit cards, accrued expenses
- Equity: owner's equity, retained earnings, capital contributions
- Income: sales, service revenue, interest income, other income
- Expenses: operating costs, materials, labor, utilities, supplies

ACCOUNT PATH EXAMPLES:

Assets:
  PETTY_CASH: Assets:Current Assets:Petty Cash
  CHECKING: Assets:Current Assets:Checking Account

Income:
  CONSULTING_FEES: Income:Service Revenue:Consulting
  MISC_LABOR_INCOME: Income:Labor Revenue

Expenses:
  OFFICE_SUPPLIES: Expenses:Office:Supplies
  UTILITIES: Expenses:Utilities:Electric

HIERARCHY RULES:
- Use colons to separate levels: "Category:Subcategory:Account"
- Top level must be Assets, Liabilities, Equity, Income, or Expenses
- Keep names descriptive but concise
- Match your QuickBooks Chart of Accounts structure when possible

COMPLETION CHECKLIST:
- Enter account name in brackets
- Enter full account path starting with one of the 5 accounting types
- Save file and restart pipeline when complete

Consult your QuickBooks Desktop Chart of Accounts for guidance.
"""
        
        # Write both files
        os.makedirs(output_dir, exist_ok=True)
        
        with open(questions_path, 'w', encoding='utf-8') as f:
            f.write(questions_content)
            
        with open(instructions_path, 'w', encoding='utf-8') as f:
            f.write(instructions_content)
        
        logging.info(f"[ACCOUNTS-UNMAPPED-PROCESSING] Generated questions file: accounts_mapping_questions.txt and accounts_mapping_instructions.txt")
        logging.info(f"[ACCOUNTS-UNMAPPED-PROCESSING] Edit the questions file and restart pipeline to continue")
        logging.info(f"[ACCOUNTS-UNMAPPED-PROCESSING] Pipeline HALT: User action required")
        
    except Exception as e:
        raise OutputWriteError(f"Failed to generate mapping questions file: {str(e)}")

def get_next_generational_number(output_dir: str, base_name: str, suffix: str = "") -> int:
    """Get next available generational number for file naming.
    
    Args:
        output_dir: Directory to check for existing files
        base_name: Base filename without version number
        suffix: Optional suffix (e.g., "error" for error files)
        
    Returns:
        Next available version number
    """
    if suffix:
        pattern = f"{base_name}_{suffix}_v"
    else:
        pattern = f"{base_name}_v"
    
    existing_numbers = []
    
    if os.path.exists(output_dir):
        for filename in os.listdir(output_dir):
            if filename.startswith(pattern) and filename.endswith('.txt'):
                # Extract number from filename like "base_v001.txt" or "base_error_v001.txt"
                try:
                    number_part = filename[len(pattern):filename.rfind('.txt')]
                    existing_numbers.append(int(number_part))
                except ValueError:
                    continue
    
    return max(existing_numbers, default=0) + 1

def parse_text_mapping_file(questions_file_path: str) -> Dict[str, Any]:
    """Parse user-completed text mapping file with full account paths and convert to JSON structure.
    
    Args:
        questions_file_path: Path to completed questions file
        
    Returns:
        Dict containing account_types mappings in baseline schema format
        
    Raises:
        MappingLoadError: If text file cannot be parsed or has invalid format
    """
    if not os.path.exists(questions_file_path):
        raise MappingLoadError(f"Questions file not found: {questions_file_path}")
    
    try:
        # ASCII validation with immediate HALT on first non-ASCII detection
        with open(questions_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Line-by-line ASCII scanning with immediate HALT
        lines = content.split('\n')
        for line_num, line in enumerate(lines, 1):
            for char_pos, char in enumerate(line):
                # Character range validation: printable characters (32-126)
                if ord(char) < 32 or ord(char) > 126:
                    logging.error(f"[ACCOUNTS-MAPPING] Non-ASCII characters detected in questions file - please re-edit using standard ASCII characters only")
                    raise MappingLoadError(f"Non-ASCII character detected at line {line_num}, position {char_pos + 1}: '{char}' (ASCII {ord(char)}). Please use only standard ASCII characters.")
        
        account_mappings = {}
        
        # Split content into sections (before instructions)
        if "================================================================================" in content:
            questions_section = content.split("================================================================================")[0]
        else:
            questions_section = content
        
        # Parse each account block with simplified format
        i = 0
        
        while i < len(lines):
            line = lines[i].strip()
            
            # Look for account name line (contains brackets)
            if line.startswith('[') and line.endswith(']'):
                qbd_account = line[1:-1].strip()  # Remove brackets
                
                if qbd_account:  # Valid account name
                    # Look for full account path in next lines
                    full_path = ""
                    
                    # Check next few lines for full account path
                    for j in range(i + 1, min(i + 3, len(lines))):
                        if lines[j].strip().startswith('Enter the full GnuCash account path here'):
                            path_parts = lines[j].split(':', 1)
                            if len(path_parts) == 2:
                                # Normalize spaces around colons and strip whitespace
                                full_path = path_parts[1].strip().replace(' : ', ':').replace(': ', ':').replace(' :', ':')
                    
                    if full_path:
                        # Validate that path starts with one of the 5 fundamental accounting types
                        valid_categories = ['Assets', 'Liabilities', 'Equity', 'Income', 'Expenses']
                        path_root = full_path.split(':')[0].strip()
                        
                        if path_root not in valid_categories:
                            raise MappingLoadError(f"Account path '{full_path}' must start with one of: {', '.join(valid_categories)}")
                        
                        # Infer GnuCash type from full path
                        gnucash_type = infer_gnucash_type(full_path)
                        
                        account_mappings[qbd_account] = {
                            "gnucash_type": gnucash_type,
                            "destination_hierarchy": full_path
                        }
                        
                        logging.debug(f"[ACCOUNTS-UNMAPPED-PROCESSING] Parsed: {qbd_account} -> {gnucash_type} at {full_path}")
            
            i += 1
        
        if not account_mappings:
            raise MappingLoadError("No valid account mappings found in questions file. Please fill in the account names and full account paths.")
        
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
        
        logging.info(f"[ACCOUNTS-MAPPING] Successfully parsed {len(account_mappings)} account mappings from questions file")
        return result
        
    except Exception as e:
        logging.error(f"[ACCOUNTS-MAPPING] Failed to parse questions file: {str(e)}")
        raise MappingLoadError(f"Failed to parse questions file: {str(e)}")

def infer_gnucash_type(full_path: str) -> str:
    """Infer GnuCash account type from full account path.
    
    Args:
        full_path: Full account path like "Assets:Current Assets:Checking" or "Expenses:Office:Supplies"
        
    Returns:
        Appropriate GnuCash account type
    """
    path_parts = full_path.split(':')
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

def is_questions_file_completed(questions_file_path: str) -> bool:
    """Check if questions file has been completed by user.
    
    Args:
        questions_file_path: Path to questions file
        
    Returns:
        True if file appears to have user input, False otherwise
    """
    try:
        with open(questions_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Simple check: if file contains filled-in answers
        lines = content.split('\n')
        for line in lines:
            # Look for completed account names or full paths
            if (line.startswith('Enter the full GnuCash account path here') and 
                ':' in line and line.split(':', 1)[1].strip()):
                return True
        
        return False
        
    except Exception:
        return False

def load_mapping(user_mapping_path: Optional[str] = None) -> Dict[str, Any]:
    """Load account mapping configuration with integrated text-based workflow.
    
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
        
        logging.debug(f"[ACCOUNTS-MAPPING] Loading baseline mapping from: {baseline_path}")
        
        if not os.path.exists(baseline_path):
            raise MappingLoadError(f"Baseline mapping file not found: {baseline_path}")
        
        with open(baseline_path, 'r', encoding='utf-8') as f:
            mapping = json.load(f)
        
        # Validate baseline mapping against schema
        baseline_errors = validate_mapping_schema(mapping, baseline_path)
        if baseline_errors:
            raise MappingLoadError(f"Baseline mapping validation failed: {'; '.join(baseline_errors)}")
        
        logging.info(f"[ACCOUNTS-MAPPING] Loaded and validated baseline mapping: {len(mapping.get('account_types', {}))} accounts")
        
        # Check for text-based mapping workflow (Priority 1)
        questions_path = os.path.join("output", "accounts_mapping_questions.txt")
        override_path = user_mapping_path or os.path.join("output", "accounts_mapping_specific.json")
        
        if os.path.exists(questions_path):
            if is_questions_file_completed(questions_path):
                try:
                    logging.info(f"[ACCOUNTS-MAPPING] Found completed questions file, processing user mappings")
                    
                    # Parse text file and convert to JSON
                    text_mapping = parse_text_mapping_file(questions_path)
                    
                    # Save as specific file for future use
                    with open(override_path, 'w', encoding='utf-8') as f:
                        json.dump(text_mapping, f, indent=2, ensure_ascii=False)
                    
                    # Merge with baseline
                    if 'account_types' in text_mapping:
                        mapping['account_types'].update(text_mapping['account_types'])
                        logging.info(f"[ACCOUNTS-MAPPING] Successfully parsed {len(text_mapping['account_types'])} account mappings from questions file")
                        
                        # Generate generational filename and rename processed file
                        next_version = get_next_generational_number("output", "accounts_mapping_questions")
                        processed_path = os.path.join("output", f"accounts_mapping_questions_v{next_version:03d}.txt")
                        os.rename(questions_path, processed_path)
                        logging.info(f"[ACCOUNTS-MAPPING] Questions file renamed to accounts_mapping_questions_v{next_version:03d}.txt")
                    
                    logging.info(f"[ACCOUNTS-MAPPING] Text-based mapping workflow completed successfully")
                    return mapping
                    
                except Exception as e:
                    logging.error(f"[ACCOUNTS-MAPPING] File appears corrupted or severely malformed")
                    # Rename with error suffix for user inspection
                    next_version = get_next_generational_number("output", "accounts_mapping_questions", "error")
                    error_path = os.path.join("output", f"accounts_mapping_questions_error_v{next_version:03d}.txt")
                    os.rename(questions_path, error_path)
                    logging.info(f"[ACCOUNTS-MAPPING] Questions file renamed to accounts_mapping_questions_error_v{next_version:03d}.txt")
                    raise MappingLoadError(f"Failed to parse questions file: {str(e)}")
            else:
                # File exists but incomplete - signal HALT needed
                logging.info(f"[ACCOUNTS-MAPPING] Questions file contains incomplete mappings")
                logging.info(f"[ACCOUNTS-MAPPING] Complete all account mappings and restart pipeline")
                return None  # Signal HALT condition to caller
        
        # Load existing specific file if present (Priority 2)
        if os.path.exists(override_path):
            logging.info(f"[ACCOUNTS-MAPPING] Found mapping overrides file: {override_path}")
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
                    logging.info(f"[ACCOUNTS-MAPPING] Applied {len(specific['account_types'])} account type overrides")
                    
                if 'default_rules' in specific:
                    mapping['default_rules'].update(specific['default_rules'])
                    override_count += len(specific['default_rules'])
                    logging.info(f"[ACCOUNTS-MAPPING] Applied {len(specific['default_rules'])} default rule overrides")
                
                if override_count > 0:
                    logging.info(f"[ACCOUNTS-MAPPING] Configuration customization: {override_count} total overrides applied from user file")
                else:
                    logging.warning(f"Override file exists but contains no valid overrides: {override_path}")
                    
            except json.JSONDecodeError as e:
                logging.error(f"[E0107] Override file contains invalid JSON: {override_path} - {str(e)}")
                raise MappingLoadError(f"Override file contains invalid JSON: {str(e)}")
            except (KeyError, TypeError) as e:
                logging.error(f"[E0107] Override file structure error: {override_path} - {str(e)}")
                raise MappingLoadError(f"Override file structure error: {str(e)}")
        
        logging.info("[ACCOUNTS-MAPPING] No user override file found - using baseline configuration")
        logging.debug(f"[ACCOUNTS-MAPPING] To customize mappings, create: {override_path}")
        
        # Final validation of merged configuration
        final_errors = validate_mapping_schema(mapping, "merged_configuration")
        if final_errors:
            raise MappingLoadError(f"Final merged configuration validation failed: {'; '.join(final_errors)}")
        
        logging.info(f"[ACCOUNTS-MAPPING] Account mapping configuration ready - {len(mapping['account_types'])} types mapped and validated")
        return mapping
        
    except (IOError, json.JSONDecodeError) as e:
        logging.error(f"[E1101] Failed to load account mapping configuration: {str(e)}")
        raise MappingLoadError(f"Failed to load account mapping configuration: {str(e)}")

def find_unmapped_types(records: List[Dict[str, Any]], mapping: Dict[str, Any]) -> List[str]:
    """Find QBD accounts that are not mapped in the configuration.
    
    Args:
        records: List of account records from !ACCNT section
        mapping: Account mapping configuration
        
    Returns:
        List of unmapped QBD account strings
    """
    mapped_types = set(mapping.get('account_types', {}).keys())
    record_types = set(record.get('ACCNTTYPE', '') for record in records)
    unmapped = record_types - mapped_types
    
    if unmapped:
        logging.info(f"[ACCOUNTS-UNMAPPED-PROCESSING] Found {len(unmapped)} unmapped accounts requiring user input")
        logging.debug(f"[ACCOUNTS-MAPPING] Mapped types available: {sorted(mapped_types)}")
    else:
        logging.debug("[ACCOUNTS-MAPPING] All accounts are properly mapped")
    
    return sorted(unmapped)