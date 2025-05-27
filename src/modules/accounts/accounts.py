"""Accounts module for converting QuickBooks Desktop account data to GnuCash format.
Version: 1.1.1
Compatible with Core PRD v3.6.3
"""
from typing import Dict, List, Any, Optional
import os
import csv
from .accounts_mapping import load_mapping, find_unmapped_types
from .accounts_tree import build_accounts_tree
from .accounts_validation import run_validation_pass
from utils.error_handler import (
    IIFParseError,  
    MappingLoadError,
    AccountsTreeError,
    OutputError,
    ValidationError
)
from utils.logging import setup_logging

logger = setup_logging()

def run_accounts_pipeline(payload: Dict[str, Any]) -> None:
    """Entry point for processing QBD !ACCNT list.
    
    Args:
        payload: Dict conforming to core_dispatch_payload_v1 schema containing:
            - section (str): Section identifier ('!ACCNT')
            - records (List[Dict]): List of parsed account records
            - input_path (str): Original source file path
            - output_dir (str): Target directory for outputs 
            - log_path (str): Log file path
            - mapping_config (Dict): Account mapping configuration
            - extra_config (Dict, optional): Additional configuration

    Raises:
        IIFParseError: For dispatch validation failures
        MappingLoadError: For mapping file issues 
        AccountsTreeError: For hierarchy construction failures
        OutputError: For CSV generation issues
    """
    logger = setup_logging(payload['log_path'])
    
    try:
        # Load and validate type mappings
        mapping = load_mapping(payload.get('mapping_config'))
        logger.info("Account mappings loaded successfully")

        # Check for unmapped types
        unmapped = find_unmapped_types(payload['records'], mapping)
        if unmapped:
            logger.warning(f"Found {len(unmapped)} unmapped account types")

        # Build account hierarchy tree
        tree = build_accounts_tree(payload['records'], mapping)
        logger.info("Account tree structure built successfully")
        
        # Run validation rules
        run_validation_pass(tree)
        logger.info("Account validation passed successfully")
        
        # Generate GnuCash CSV output
        write_accounts_csv(tree, payload['output_dir'])
        logger.info("Account CSV generated successfully")

    except (IIFParseError, MappingLoadError, AccountsTreeError, OutputError) as e:
        logger.error(f"Account processing failed: {str(e)}")
        raise


def write_accounts_csv(tree: Dict[str, Any], output_dir: str) -> None:
    """Write account tree to GnuCash-compatible CSV format.
    
    Args:
        tree: The validated account hierarchy tree
        output_dir: Directory to write output files to
        
    Raises:
        OutputError: If CSV generation fails
    """
    try:
        # Ensure output directory exists
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, 'accounts.csv')
        
        # Collect flattened account data
        accounts = []
        
        def _process_node(node: Dict[str, Any]) -> None:
            if node['name'] != 'ROOT':  # Skip root node
                accounts.append({
                    'account_type': node['type'],
                    'full_name': node['full_path'],
                    'name': node['name'],
                    'description': node['description'],
                    'placeholder': str(node['placeholder']).lower()
                })
            for child in node['children'].values():
                _process_node(child)
                
        _process_node(tree['root'])
        
        # Write CSV file
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'account_type', 'full_name', 'name', 'description', 'placeholder'
            ])
            writer.writeheader()
            writer.writerows(accounts)
            
    except Exception as e:
        raise OutputError(f"Failed to write accounts CSV: {str(e)}")