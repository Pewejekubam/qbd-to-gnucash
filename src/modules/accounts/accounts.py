"""Main accounts module pipeline with integrated text-based workflow orchestration.

This module provides the accounts processing pipeline entry point as specified
in the module PRDs with integrated text workflow coordination and HALT condition handling.
"""

import logging
import os
from typing import Dict, List, Any

from utils.error_handler import ConversionError, OutputWriteError
from utils.logging import log_user_info, log_user_error, log_technical_detail

from .accounts_tree import build_accounts_tree
from .accounts_mapping import load_mapping, find_unmapped_types, generate_text_mapping_questions
from .accounts_export import export_accounts

def run_accounts_pipeline(payload: Dict[str, Any]) -> bool:
    """Main entry point for accounts processing pipeline with text workflow coordination.
    
    Args:
        payload: Simplified dispatch payload containing:
            - section: Section identifier (e.g., 'ACCNT')
            - records: List of account records from !ACCNT section
            - output_dir: Directory for generated output files
            - extra_config: Additional configuration (optional)
        
    Returns:
        bool: True for successful completion, False for HALT condition (user action required)
        
    Raises:
        ConversionError: If any step in the pipeline fails
    """
    try:
        # Extract only what the domain module needs from simplified payload
        accounts_data = payload.get('records', [])
        output_dir = payload.get('output_dir', 'output')
        
        log_user_info(f"[ACCOUNTS-PIPELINE] Starting accounts processing with {len(accounts_data)} records")
        
        # Step 1: Load account mapping configuration with text workflow integration
        log_technical_detail("[ACCOUNTS-ORCHESTRATION] Loading account mapping configuration")
        mapping = load_mapping()
        
        # Check for HALT condition from text workflow
        if mapping is None:
            log_user_info("[ACCOUNTS-ORCHESTRATION] Sub-module coordination: HALT condition detected")
            log_user_info("[ACCOUNTS-PIPELINE] Pipeline HALT: User action required for mapping completion")
            return False  # HALT condition - user needs to complete questions file
        
        # Step 2: Basic data validation (inline - no separate module needed)
        log_technical_detail("[ACCOUNTS-ORCHESTRATION] Beginning account validation")
        if not accounts_data:
            logging.warning("[ACCOUNTS-PIPELINE] No account records found to process")
            return True
        
        # Quick validation - check required fields
        required_fields = ['NAME', 'ACCNTTYPE']
        for i, account in enumerate(accounts_data):
            for field in required_fields:
                if field not in account or not account[field]:
                    log_user_error(f"[ACCOUNTS-ORCHESTRATION] Pipeline coordination failed: Account record {i} missing required field '{field}'")
                    raise ConversionError(f"Account record {i} missing required field '{field}'")
        
        log_technical_detail(f"[ACCOUNTS-ORCHESTRATION] Account validation completed - {len(accounts_data)} accounts validated")
        
        # Step 3: Check for unmapped types and handle text workflow
        unmapped_types = find_unmapped_types(accounts_data, mapping)
        
        if unmapped_types:
            log_user_info(f"[ACCOUNTS-ORCHESTRATION] Sub-module coordination: HALT condition detected")
            
            # Generate text questions file for user completion with QBD path hints
            generate_text_mapping_questions(unmapped_types, accounts_data, output_dir)
            
            # Log HALT condition details
            log_user_info("[ACCOUNTS-PIPELINE] Pipeline HALT: User action required for mapping completion")
            
            return False  # HALT condition - user needs to complete mapping
        
        # Step 4: Build account hierarchy tree with double-entry structure
        log_technical_detail("[ACCOUNTS-ORCHESTRATION] Building account hierarchy tree")
        root_node = build_accounts_tree(accounts_data, mapping)
        log_technical_detail("[ACCOUNTS-ORCHESTRATION] Account hierarchy tree construction completed")
        
        # Step 5: Export to GnuCash CSV format (domain controls output location)
        log_technical_detail("[ACCOUNTS-ORCHESTRATION] Beginning CSV export")
        export_accounts(root_node, mapping, output_dir)
        
        # Domain module determines its own output path using payload output_dir
        output_path = os.path.join(output_dir, "accounts.csv")
        
        # Self-report success with output verification
        if os.path.exists(output_path):
            file_size = os.path.getsize(output_path)
            log_user_info(f"[ACCOUNTS-PIPELINE] Generated output file: {output_path} ({file_size} bytes)")
        else:
            log_user_error(f"[ACCOUNTS-ORCHESTRATION] Pipeline coordination failed: Expected output file not created: {output_path}")
            raise OutputWriteError(f"Output file not created: {output_path}")
            
        log_user_info(f"[ACCOUNTS-PIPELINE] Accounts processing completed successfully")
        return True  # Boolean success indication
        
    except Exception as e:
        log_user_error(f"[ACCOUNTS-ORCHESTRATION] Pipeline coordination failed: {str(e)}")
        raise