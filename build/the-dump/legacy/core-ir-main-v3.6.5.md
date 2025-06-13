# QBD-to-GnuCash Intermediate Representation Schema **Main Dispatch**
# Version: v3.6.5
# Compatible Core PRD: v3.6.5
# Governance Model: v2.3.10

# 1. System Components
components:
  core:
    type: orchestrator
    version: "3.6.5"
    interfaces:
      - run_conversion_pipeline
      - register_module
      - dispatch_to_module
      - log_and_exit
    error_handlers:
      - RegistryKeyConflictError
      - ValidationError
    
  utils:
    common:
      - name: error_handler
        path: src/utils/error_handler.py
      - name: iif_parser
        path: src/utils/iif_parser.py
      - name: logging
        path: src/utils/logging.py
        version: "1.0.4"
        
  modules:
    accounts:
      version: "1.1.3"
      submodules:
        - name: accounts
          path: src/modules/accounts/accounts.py
        - name: accounts_mapping
          path: src/modules/accounts/accounts_mapping.py
          version: "1.0.8"
        - name: accounts_validation
          path: src/modules/accounts/accounts_validation.py
          version: "1.0.2"
        - name: accounts_tree
          path: src/modules/accounts/accounts_tree.py
        - name: accounts_export
          path: src/modules/accounts/accounts_export.py
      dispatch_key: "!ACCNT"
      dependencies:
        - utils.error_handler
        - utils.logging

# 2. Processing Pipeline
pipeline:
  input_discovery:
    directory: "./input/"
    file_pattern: "*.iif"  # case-insensitive
    subdirectories: false
    processing_model: "file-by-file"  # not batch
    
  section_processing:
    model: "streaming"  # parse section → dispatch section → next section
    ordering: "none"    # no ordering requirements within/across files
    error_handling: "fail-fast"  # unhandled exceptions fail pipeline
    
  dispatch_flow:
    - scan_input_directory
    - for_each_file:
        - parse_sections_streaming
        - for_each_section:
            - lookup_registered_module
            - if_registered: dispatch_to_module
            - if_unregistered: log_and_skip
    - pipeline_complete

# 3. Registry Architecture
registries:
  static_registry:
    description: "Compile-time mapping of dispatch keys to registered modules"
    populated_at: "code-time"
    managed_by: "main.py maintainer"
    structure:
      dispatch_key: module_reference
    example:
      "!ACCNT": "modules.accounts"
      
  discovery_tracking:
    description: "Runtime tracking of dispatch keys found in IIF files"
    populated_at: "runtime"
    managed_by: "iif_parser"
    purpose: "logging and audit"
    behavior:
      supported_key_found: "dispatch to module"
      unsupported_key_found: "log warning and skip"

# 4. Module Interface Contract
module_interface:
  required_function: "process_section"
  signature: |
    def process_section(payload: Dict[str, Any]) -> Any:
        """Process a section's records according to module domain logic.
        Args:
            payload (Dict[str, Any]): Canonical dispatch payload containing:
                - section (str): Section key (e.g., '!ACCNT')
                - records (List[Dict[str, Any]]): Parsed records from section
                - input_path (str): Path to source IIF file
                - output_dir (str): Target output directory
                - log_path (str): Logging configuration
                - mapping_config (Dict[str, Any]): Domain-specific mappings
                - extra_config (Dict[str, Any]): Additional configuration
        Returns:
            Any: Module-specific result (autonomous format)
        Raises:
            Module-specific exceptions as documented in module PRD
        """
  
  return_types: "autonomous"  # No standard return format enforced
  output_responsibility: "autonomous"  # Each module handles own output
  output_autonomy:
    - create_output_directories
    - define_file_naming_conventions  
    - perform_output_validation
    - handle_domain_specific_formats

# 5. Error Handling Model
error_handling:
  module_exceptions:
    handled_internally: "continue_pipeline"
    unhandled_bubbled: "fail_pipeline_fast"
  unregistered_sections: "log_and_skip"
  critical_errors: "log_and_exit"
  validation_errors: "module_autonomous"

# 6. Module Relationships
relationships:
  core_contracts:
    - module_registration:
        provider: core.register_module
        consumers: ["main.py"]
    - dispatch:
        provider: core.dispatch_to_module
        consumers: ["core.run_conversion_pipeline"]
    - logging:
        provider: utils.logging
        consumers: ["*"]
    - error_handling:
        provider: utils.error_handler
        consumers: ["*"]
        
  module_dependencies:
    accounts:
      - accounts_export
      - accounts_mapping
      - accounts_validation
      - accounts_tree

# 7. Version Binding Rules
version_rules:
  core_compatibility:
    current_core: "3.6.5"
    current_governance: "2.3.10"
    minimum_core: "3.6.0"
    
  module_compatibility:
    accounts:
      core: "3.6.5"
      logging: "1.0.4"
      internal:
        accounts: "1.1.3"
        accounts_mapping: "1.0.8"
        accounts_validation: "1.0.2"
        
  validation_rules:
    - rule: semantic_versioning
      pattern: "^v?\\d+\\.\\d+\\.\\d+$"
    - rule: version_lock
      enforce: true
      check_references: true
    - rule: governance_compliance
      model: "2.3.10"
      enforce: true
      
  update_protocol:
    - increment_major:
        conditions: ["breaking_changes", "interface_changes"]
    - increment_minor:
        conditions: ["feature_additions", "backwards_compatible"]
    - increment_patch:
        conditions: ["bug_fixes", "documentation"]

# 8. Logging Protocols (PRD v3.6.5, agentic-compliant)
# logging_protocols:
#   metadata_fields:
#     - name: file_or_key
#       required: true
#       description: Full path or logical section key associated with the log event.
#     - name: line_or_record_ref
#       required: false
#       description: Line number or record identifier, if applicable.
#     - name: processing_step
#       required: true
#       description: Logical step (e.g., discovery, dispatch, validation).
#     - name: expected_vs_actual
#       required: false
#       description: When applicable, describes a validation mismatch.
#     - name: registry_context
#       required: false
#       description: Registry or module context if the log relates to a namespaced processing unit.
#
#   severity_matrix:
#     E0101:
#       name: FileNotFoundError
#       description: Required input file is missing or unreadable
#       module: core, all
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E0102:
#       name: ValidationError
#       description: Input or output data fails schema or contract validation
#       module: core, all
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E0103:
#       name: RegistryKeyConflictError
#       description: Duplicate registry key detected during module registration
#       module: core
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E0104:
#       name: OutputWriteError
#       description: Output file cannot be written (permissions, disk full, etc.)
#       module: core, all
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E0105:
#       name: IIFParseError
#       description: Raised when .IIF file parsing fails or input is malformed.
#       module: core, all
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E0106:
#       name: ConfigFileNotFoundError
#       description: Required config file is missing or unreadable
#       module: core, all
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E0107:
#       name: ConfigValidationError
#       description: Config file fails schema or semantic validation
#       module: core, all
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E0108:
#       name: InputDirectoryNotFoundError
#       description: Input directory is missing or inaccessible
#       module: core
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E0109:
#       name: InputFileFormatError
#       description: Input file is not a valid IIF or expected format
#       module: core, all
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E0110:
#       name: SectionHeaderNotFoundError
#       description: No recognizable section headers found in input file
#       module: core, all
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E0111:
#       name: OutputDirectoryNotFoundError
#       description: Output directory missing or cannot be created
#       module: core, all
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E0112:
#       name: OutputFormatError
#       description: Output file fails post-write validation
#       module: core, all
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E0113:
#       name: PipelineHaltError
#       description: Unexpected halt not covered by other error classes
#       module: core
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E0201:
#       name: LoggingError
#       description: Logging subsystem failed to record a required event
#       module: logging
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E0202:
#       name: LogFileWriteError
#       description: Log file cannot be written
#       module: logging
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E0203:
#       name: LogFormatError
#       description: Log entry fails to serialize or is malformed
#       module: logging
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1101:
#       name: MappingLoadError
#       description: Mapping file missing, unreadable, or invalid schema
#       module: accounts_mapping
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1102:
#       name: UnmappedAccountTypeError
#       description: QBD account type not mapped and no default rule applies
#       module: accounts_mapping
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1103:
#       name: MappingRuleError
#       description: Mapping config contains invalid or ambiguous rules
#       module: accounts_mapping
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1104:
#       name: MappingAmbiguityError
#       description: Multiple mapping rules match a single input
#       module: accounts_mapping
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1105:
#       name: UnmappedFieldError
#       description: Required field in input has no mapping and no default
#       module: accounts_mapping, all
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1106:
#       name: ExportOperationError
#       description: Failure during export logic
#       module: accounts_export, all
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1110:
#       name: TreeConstructionError
#       description: Account tree cannot be constructed due to missing/circular refs
#       module: accounts, accounts_tree
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1111:
#       name: AccountsTreeError
#       description: Raised when account hierarchy is invalid (e.g., cycles, orphan nodes, etc).
#       module: accounts_tree
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1190:
#       name: DomainValidationError
#       description: Domain-specific validation failed
#       module: all domain modules
#       severity: error
#       exit_code: 2
#       logging_action: log_error
#     E1191:
#       name: DomainDependencyError
#       description: Required domain dependency missing or failed to load
#       module: all domain modules
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E9101:
#       name: GovernanceViolationError
#       description: Detected violation of PRD/governance rules
#       module: core, all
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#     E9999:
#       name: UnknownError
#       description: Unclassified error
#       module: all
#       severity: critical
#       exit_code: 1
#       logging_action: log_and_exit
#
#   expected_log_events:
#     - event: mapping_load_error
#       trigger: On failure to load or parse mapping file
#       severity: error
#       logging_action: log_error
#       error_code: E1101
#     - event: unmapped_account_type
#       trigger: On encountering an account type with no mapping and no default
#       severity: error
#       logging_action: log_error
#       error_code: E1102
#     - event: mapping_rule_error
#       trigger: On invalid or ambiguous mapping rules
#       severity: error
#       logging_action: log_error
#       error_code: E1103
#     - event: mapping_ambiguity
#       trigger: On multiple mapping rules matching a single input
#       severity: error
#       logging_action: log_error
#       error_code: E1104
#     - event: unmapped_field
#       trigger: On required field in input with no mapping and no default
#       severity: error
#       logging_action: log_error
#       error_code: E1105
#     - event: export_operation_error
#       trigger: On failure during account export logic
#       severity: error
#       logging_action: log_error
#       error_code: E1106
#     - event: tree_construction_error
#       trigger: On failure to construct account tree due to missing/circular refs
#       severity: error
#       logging_action: log_error
#       error_code: E1110
#     - event: accounts_tree_error
#       trigger: On invalid account hierarchy (cycles, orphan nodes, etc.)
#       severity: error
#       logging_action: log_error
#       error_code: E1111
#     - event: domain_validation_error
#       trigger: On domain-specific validation failure
#       severity: error
#       logging_action: log_error
#       error_code: E1190
#     - event: domain_dependency_error
#       trigger: On required domain dependency missing or failed to load
#       severity: critical
#       logging_action: log_and_exit
#       error_code: E1191
#
#   rules:
#     enforce_module_logging:
#       description: All modules must use `utils.logging`. No ad hoc logging is permitted.
#       violation_code: L0001
#       severity: critical
#       exit_code: 1