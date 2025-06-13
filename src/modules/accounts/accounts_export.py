"""Account export to GnuCash CSV format.

UPDATED: Cross-platform path handling per Priority 1 decisions.
"""

import csv
import os
from typing import Any, Dict, List

from utils.error_handler import OutputWriteError
from utils.logging import logging

from .accounts_tree import AccountNode

def _flatten_tree(node: AccountNode, mapping: Dict[str, Any]) -> List[Dict[str, str]]:
    """Convert account tree to flat list of GnuCash accounts.
    
    Args:
        node: Root node of account tree
        mapping: Account mapping configuration
        
    Returns:
        List of dicts with GnuCash account fields matching expected CSV format
    """
    accounts = []
    
    def _process_node(node: AccountNode) -> None:
        if node.name != "Root":
            # Use the account's actual type as determined by the tree building process
            gnc_type = node.type
            
            # Remove "Root:" prefix from full_name for GnuCash compatibility
            clean_full_name = node.full_name
            if clean_full_name.startswith("Root:"):
                clean_full_name = clean_full_name[5:]  # Remove "Root:" prefix
            
            # Determine if this should be a placeholder account
            is_placeholder = 'F'  # Default to not placeholder
            
            # Fundamental accounting types should always be placeholders
            fundamental_types = {'Assets', 'Liabilities', 'Equity', 'Income', 'Expenses'}
            if node.name in fundamental_types:
                is_placeholder = 'T'
                logging.debug(f"Set placeholder=T for fundamental accounting type: {node.name}")
            else:
                # Use original placeholder status from source, or default to F
                is_placeholder = node.original_placeholder or 'F'
            
            # Create account record matching GnuCash CSV format exactly
            account = {
                'Type': gnc_type,
                'Full Account Name': clean_full_name,
                'Account Name': node.name,
                'Account Code': node.account_code,
                'Description': node.original_description,  # Preserved from source IIF
                'Account Color': node.original_color,      # Preserved from source IIF
                'Notes': node.original_notes,              # Preserved from source IIF
                'Symbol': mapping.get('default_commodity', 'USD'),
                'Namespace': 'CURRENCY',
                'Hidden': node.original_hidden or 'F',     # Use source or default
                'Tax Info': node.original_tax_info,        # Preserved from source IIF
                'Placeholder': is_placeholder              # Smart placeholder logic
            }
            accounts.append(account)
            
            logging.debug(f"Exported account '{node.name}' as type '{gnc_type}' with full name '{clean_full_name}'")
        
        # Process children
        for child in node.children:
            _process_node(child)
    
    _process_node(node)
    return accounts

def export_accounts(root: AccountNode, mapping: Dict[str, Any], output_dir: str = "output") -> None:
    """Export account hierarchy to GnuCash CSV format.
    
    Args:
        root: Root node of account tree
        mapping: Account mapping configuration
        output_dir: Directory for output file (from payload)
        
    Raises:
        ExportError: If export fails
    """
    try:
        # Convert tree to flat GnuCash format
        accounts = _flatten_tree(root, mapping)
        
        # Domain module controls output location - FIXED: Use payload output_dir
        output_path = os.path.join(output_dir, "accounts.csv")
        
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        
        # Write CSV file with exact GnuCash column headers
        fieldnames = [
            'Type', 'Full Account Name', 'Account Name', 'Account Code', 
            'Description', 'Account Color', 'Notes', 'Symbol', 'Namespace', 
            'Hidden', 'Tax Info', 'Placeholder'
        ]
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(accounts)
        
        logging.info(f"[EXPORT] Exported {len(accounts)} accounts to GnuCash-compatible CSV format")
        logging.debug(f"[EXPORT] Output file: {output_path} with {len(fieldnames)} columns")
        
    except (IOError, PermissionError, OSError) as e:
        raise OutputWriteError(f"Failed to write accounts CSV to {output_path}: {str(e)}")
    except (KeyError, ValueError) as e:
        raise OutputWriteError(f"CSV formatting error for {output_path}: {str(e)}")