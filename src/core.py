"""Core orchestration module with updated console and debug logging specification.

This module provides the central orchestration and dispatch functionality as specified 
in core-prd-main-v3.6.5.md with domain-tagged console and debug logging.
"""

import logging
import os
import sys
from datetime import datetime
from typing import Any, Dict, List

from utils.error_handler import ConversionError, RegistryKeyConflictError, FileNotFoundError as CustomFileNotFoundError
from utils.logging import (
    setup_logging, log_user_info, log_user_success, log_user_error, 
    log_technical_detail, log_module_registration, log_unregistered_module_key,
    log_file_processing_result, log_pipeline_summary, log_file_discovery,
    log_iif_parsing_summary, log_module_dispatch, log_module_success,
    log_sections_found, flush_logs
)
from utils.iif_parser import IIFParser

# Central module registry
_module_registry: Dict[str, Any] = {}

def run_conversion_pipeline(config: Dict[str, Any]) -> int:
    """Orchestrate the full conversion process with domain-tagged logging.
    
    Args:
        config (Dict[str, Any]): Configuration dictionary with iif_files list and directories.
        
    Returns:
        int: Exit code (0=success, 1=critical error, 2=validation error)
    """
    try:
        # Verify logging is set up (should be done by main.py)
        if not logging.getLogger().handlers:
            setup_logging()
            log_technical_detail("[CORE] Emergency logging setup completed")
            
        log_technical_detail("[CORE] Starting PRD compliant conversion pipeline")
        
        # Get all IIF files for content-based processing
        iif_files = config.get('iif_files', [])
        output_dir = config.get('output_dir', 'output')
        
        if not iif_files:
            log_user_error("[CORE] No IIF files provided for processing")
            log_technical_detail("[CORE] No IIF files provided in configuration")
            raise CustomFileNotFoundError("No IIF files provided in configuration")
        
        log_technical_detail(f"[CORE] Pipeline initiated - {len(iif_files)} IIF files, output directory: {output_dir}")
        
        # Verify all input files exist before processing
        for file_path in iif_files:
            if not os.path.exists(file_path):
                log_user_error(f"[CORE] Input file not found: {os.path.basename(file_path)}")
                log_technical_detail(f"[CORE] Input file not found: {file_path}")
                raise CustomFileNotFoundError(f"Input file not found: {file_path}")
        
        # Show discovered files to user with domain tagging
        log_user_info(f"[CORE] Discovered {len(iif_files)} IIF files for processing:")
        for file_path in iif_files:
            filename = os.path.basename(file_path)
            log_user_info(f"[CORE]   * {filename}")
        
        # Console: Pipeline initiation
        log_user_info("[CORE] Pipeline initiated")
        
        # Process each IIF file through content-based section detection
        total_sections_processed = 0
        unimplemented_sections_found = False
        
        for file_path in iif_files:
            filename = os.path.basename(file_path)
            log_technical_detail(f"[CORE] Begin content-based processing - {file_path}")
            
            # Parse IIF file to extract all module keys (PRD Section 13.4.2)
            try:
                log_technical_detail(f"[CORE] Initializing IIF parser for: {file_path}")
                parser = IIFParser(file_path)
                sections = parser.parse()
                
                # Count total records across all sections
                total_records = sum(len(records) for records in sections.values())
                log_iif_parsing_summary(file_path, len(sections), total_records)
                
                # Log discovered module keys (technical detail)
                section_names = list(sections.keys())
                log_sections_found(section_names)
                
                if not sections:
                    log_technical_detail(f"[CORE] No module keys found in file: {file_path}")
                    continue
                
            except Exception as e:
                log_user_error(f"[CORE] Failed to parse {filename} (see logs: parsing errors)")
                log_technical_detail(f"[CORE] IIF parsing failed - {file_path}: {str(e)}")
                raise
            
            # Track results for this file
            file_results = []
            
            # Dispatch each section to its registered module (PRD Section 13.4.3)
            for section_key, records in sections.items():
                if section_key in _module_registry:
                    log_module_dispatch(section_key, len(records))
                    
                    # Create simplified dispatch payload (core_dispatch_payload_v2)
                    payload = {
                        'section': section_key,
                        'records': records,
                        'output_dir': output_dir,
                        'extra_config': {}
                    }
                    
                    # Dispatch to registered module
                    try:
                        result = dispatch_to_module(_module_registry, section_key, payload)
                        if result:  # Boolean success
                            log_module_success(section_key, "processing completed successfully")
                            total_sections_processed += 1
                            
                            # Estimate output for user display
                            account_count = len(records)  # Record count estimate
                            file_results.append({
                                'module': section_key.lower(),
                                'output': f"{section_key.lower()}.csv",  # Standard output pattern
                                'count': account_count
                            })
                        else:
                            # Module returned FALSE (HALT condition) - use domain tagging with timestamp
                            timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]  # Millisecond precision
                            log_user_error(f"[{section_key.upper()}-PIPELINE] Module reports HALT. User action required. See debug log \"E0113\" around {timestamp}")
                            log_technical_detail(f"[CORE] E0113 Module returned False - {section_key}")
                        
                    except Exception as e:
                        log_user_error(f"[CORE] Module {section_key.lower()} failed for {filename} (see logs: module processing errors)")
                        log_technical_detail(f"[CORE] Module failed - {section_key} error: {str(e)}")
                        raise
                        
                else:
                    # Section found but no registered module (expected for unsupported sections)
                    unimplemented_sections_found = True
                    log_unregistered_module_key(section_key, len(records))
            
            # Show file processing results to user (only for successfully processed modules)
            if file_results:
                log_file_processing_result(file_path, len(sections), total_records, file_results)
        
        # Show final summary to user
        if total_sections_processed == 0:
            log_user_info("[CORE] No module key records were processed")
            log_user_info("[CORE] To process additional data types, register modules for the discovered module keys")
            log_technical_detail("[CORE] Available registered module keys: " + str(list(_module_registry.keys())))
            return 2  # Validation error - no processable content
        
        # Consolidated message for unimplemented data types
        if unimplemented_sections_found:
            log_user_info("[CORE] Some QBD data types are not yet implemented. See log file for details.")
        
        log_user_info(f"[CORE] Pipeline completed: {total_sections_processed} modules processed successfully from {len(iif_files)} files")
        
        # Flush logs before exit
        flush_logs()
        
        return 0
        
    except ConversionError as e:
        log_user_error(f"[CORE] Conversion failed (see logs: error details)")
        log_technical_detail(f"[CORE] Pipeline failed with conversion error - {str(e)} (exit code: {e.exit_code})")
        flush_logs()
        log_and_exit(str(e), e.exit_code)
        return e.exit_code
        
    except Exception as e:
        log_user_error(f"[CORE] Unexpected error occurred (see logs: error details)")
        log_technical_detail(f"[CORE] Pipeline failed with unexpected error - {str(e)}")
        flush_logs()
        log_and_exit(f"[CORE] Unexpected error: {str(e)}", 1)
        return 1

def register_module(registry: Dict[str, Any], key: str, module: Any) -> None:
    """Register a domain module with the core registry for dispatching input sections.
    
    Args:
        registry (Dict[str, Any]): The central registry mapping section keys to modules.
        key (str): The unique section key (e.g., 'ACCNT', 'CUST', 'VEND').
        module (Any): The module function implementing the required interface.
        
    Raises:
        RegistryKeyConflictError: If the key is already registered.
    """
    if key in registry:
        raise RegistryKeyConflictError(f"Registry key already exists: {key}")
    
    log_module_registration(key)
    registry[key] = module

def dispatch_to_module(registry: Dict[str, Any], section_key: str, payload: Dict[str, Any]) -> bool:
    """Dispatch simplified payload to the appropriate domain module for processing.
    
    Args:
        registry (Dict[str, Any]): The central registry mapping section keys to modules.
        section_key (str): The section key identifying the domain (e.g., 'ACCNT').
        payload (Dict[str, Any]): Simplified payload conforming to core_dispatch_payload_v2.
        
    Returns:
        bool: True for successful completion, False for failure.
        
    Raises:
        KeyError: If the section_key is not registered.
        Exception: For module-specific processing errors.
    """
    if section_key not in registry:
        log_technical_detail(f"[CORE] Module key not registered: {section_key}")
        raise KeyError(f"Module key not registered: {section_key}")
    
    log_technical_detail(f"[CORE] Module dispatch initiated - {section_key}")
    
    try:
        module_func = registry[section_key]
        result = module_func(payload)
        log_technical_detail(f"[CORE] Module dispatch completed - {section_key}")
        return result
        
    except Exception as e:
        log_technical_detail(f"[CORE] Module dispatch failed - {section_key}: {str(e)}")
        raise

def log_and_exit(message: str, code: int = 1) -> None:
    """Log a critical error message and exit the process with the specified code.
    
    Args:
        message (str): The error message to log (should include error code).
        code (int, optional): Exit code (default: 1).
        
    Raises:
        SystemExit: Always raised to terminate the process.
    """
    log_technical_detail(f"[CORE] System exit requested - {message} (exit code: {code})")
    
    # Ensure all logs are flushed before exit (PRD requirement)
    flush_logs()
    
    sys.exit(code)

# Convenience function to register with the global registry
def register_global_module(key: str, module: Any) -> None:
    """Register a module with the global registry using module key.
    
    Args:
        key (str): Module key (e.g., 'ACCNT', 'CUST', 'VEND') - WITHOUT exclamation mark
        module (Any): Module processing function
    """
    register_module(_module_registry, key, module)

def get_global_registry() -> Dict[str, Any]:
    """Get the global module registry."""
    return _module_registry