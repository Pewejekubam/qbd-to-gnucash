"""Main entry point for QBD to GnuCash conversion tool with domain-tagged logging.

UPDATED: Domain-tagged console and debug logging per logging specification.
"""

import os
import logging

from core import run_conversion_pipeline, register_global_module
from modules.accounts.accounts import run_accounts_pipeline
from utils.logging import setup_logging, log_user_info, log_user_error, log_technical_detail
from utils.error_handler import FileNotFoundError

def discover_input_files(input_dir: str = 'input') -> list:
    """Discover all IIF files in input directory for content-based processing.
    
    Args:
        input_dir: Directory to scan for IIF files
        
    Returns:
        List of IIF file paths (PRD compliant - no filename-based routing)
    """
    iif_files = []
    
    if not os.path.exists(input_dir):
        return iif_files
    
    for file in os.listdir(input_dir):
        if file.lower().endswith('.iif'):
            iif_files.append(os.path.join(input_dir, file))
    
    return iif_files

def main() -> None:
    """Main entry point - no CLI arguments as per PRD specification."""
    # Initialize logging system first (PRD compliance)
    try:
        setup_logging()
        log_technical_detail("[CORE] QBD to GnuCash conversion tool started")
    except Exception as e:
        print(f"FATAL: Logging system initialization failed: {str(e)}")
        exit(1)
    
    try:
        # Ensure directories exist
        os.makedirs('input', exist_ok=True)
        os.makedirs('output', exist_ok=True)
        log_technical_detail("[CORE] Directory structure verified")
        
        # Register modules with their module keys (PRD Section 13.4.3)
        register_global_module('ACCNT', run_accounts_pipeline)
        # Future modules would be registered here:
        # register_global_module('CUST', run_customers_pipeline) 
        # register_global_module('VEND', run_vendors_pipeline)
        # register_global_module('INVITEM', run_items_pipeline)
        log_technical_detail("[CORE] Module registration completed")
        
        # Discover all IIF files (content-based, not filename-based)
        iif_files = discover_input_files()
        
        if not iif_files:
            log_user_error("[CORE] No IIF files found in input/ directory")
            log_user_info("[CORE] Please place your QuickBooks IIF files in the input/ folder")
            log_technical_detail("[CORE] No IIF files found in input directory")
            exit(1)
        
        log_technical_detail(f"[CORE] File discovery completed - {len(iif_files)} IIF files found")
        log_technical_detail("[CORE] Starting conversion pipeline")
        
        # Prepare configuration for PRD compliant processing
        config = {
            'iif_files': iif_files,  # Pass all files for content-based dispatch
            'input_dir': 'input',
            'output_dir': 'output'
        }
        
        # Run conversion pipeline (core will handle content-based section dispatch)
        exit_code = run_conversion_pipeline(config)
        
        if exit_code == 0:
            log_technical_detail("[CORE] Conversion completed successfully")
        else:
            log_technical_detail(f"[CORE] Conversion failed with exit code {exit_code}")
            
        exit(exit_code)
        
    except Exception as e:
        log_user_error(f"[CORE] Unexpected error occurred (see logs: startup errors)")
        log_technical_detail(f"[CORE] Unexpected error in main: {str(e)}")
        print(f"FATAL ERROR: {str(e)}")
        exit(1)

if __name__ == '__main__':
    main()