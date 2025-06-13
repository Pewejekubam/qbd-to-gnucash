"""Account data validation with text-based workflow support.

This module provides account record validation plus user-friendly text-based
workflow for handling unmapped account types.
"""

import logging
import os
import re
import json
from typing import Any, Dict, List, Optional

from utils.error_handler import ValidationError, MappingLoadError

def validate_accounts(accounts: List[Dict[str, str]], mapping: Dict[str, Any]) -> None:
    """Validate account records from IIF file.
    
    Args:
        accounts: List of account records from ACCNT section
        mapping: Account mapping configuration with valid account types
        
    Raises:
        ValidationError: If validation fails
    """
    seen_accounts = set()
    
    # Get valid account types from mapping configuration (config-driven)
    valid_types = set(mapping['account_types'].keys())
    
    for account in accounts:
        # Check required fields
        required_fields = ['NAME', 'ACCNTTYPE']
        missing = [f for f in required_fields if f not in account]
        if missing:
            raise ValidationError(f"Account missing required fields: {', '.join(missing)}")
            
        # Validate account name format - allow common business characters including periods, parentheses, and asterisks
        if not re.match(r"^[A-Za-z0-9*][A-Za-z0-9:_\-'&.()* ]*$", account['NAME']):
            raise ValidationError(f"Invalid account name format: {account['NAME']}")
            
        # Check for duplicates
        if account['NAME'] in seen_accounts:
            raise ValidationError(f"Duplicate account name: {account['NAME']}")
        seen_accounts.add(account['NAME'])
        
        # Validate account type using config-driven validation
        if account['ACCNTTYPE'] not in valid_types:
            raise ValidationError(
                f"Invalid account type: {account['ACCNTTYPE']} "
                f"(not found in mapping configuration). "
                f"Valid types: {', '.join(sorted(valid_types))}"
            )
    
    logging.info(f"Validated {len(accounts)} accounts using config-driven validation")


def generate_text_mapping_questions(unmapped_types: List[str], current_mapping: Dict[str, Any]) -> None:
    """Generate simple text file with mapping questions for user to answer.
    
    Args:
        unmapped_types: List of QBD account types needing mapping
        current_mapping: Current mapping configuration for reference
        
    Creates:
        output/accounts_mapping_questions.txt with simple questions format
    """
    try:
        # Use cross-platform path construction
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