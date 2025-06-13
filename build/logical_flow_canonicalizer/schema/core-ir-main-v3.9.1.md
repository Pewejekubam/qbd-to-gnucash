# QBD-to-GnuCash Intermediate Representation Schema **Main Dispatch**
# Version: v3.9.1
# Compatible Core PRD: v3.9.1
# Governance Model: v2.7.0

# 1. System Components
components:
  core:
    type: orchestrator
    version: "3.9.1"
    interfaces:
      - run_conversion_pipeline
      - register_module
      - dispatch_to_module
      - log_and_exit
    error_handlers:
      - RegistryKeyConflictError
      - ValidationError
    interface_authority:
      source: core-prd-main-v3.9.1.md#115-interface-authority-precedence-rules
      precedence: authoritative
    
  utils:
    common:
      - name: error_handler
        path: src/utils/error_handler.py
        error_protocol: deterministic_implementation_per_core_prd_section_11_3_2
      - name: iif_parser
        path: src/utils/iif_parser.py
      - name: logging
        path: src/utils/logging.py
        version: "1.0.4"
        
  modules:
    accounts:
      version: "1.1.3"
      entry_point: run_accounts_pipeline
      entry_point_signature: "run_accounts_pipeline(payload: Dict[str, Any]) -> bool"
      payload_schema: core_dispatch_payload_v1
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
      dispatch_key: "ACCNT"
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
      "ACCNT": "modules.accounts"
      
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
  required_function: "run_<domain>_pipeline"
  signature: |
    def run_<domain>_pipeline(payload: Dict[str, Any]) -> bool:
        """Process a section's records according to module domain logic.
        Args:
            payload (Dict[str, Any]): Canonical dispatch payload containing:
                - section (str): Section key (e.g., 'ACCNT')
                - records (List[Dict[str, Any]]): Parsed records from section
                - output_dir (str): Target output directory
                - extra_config (Dict[str, Any]): Additional configuration
        Returns:
            bool: Success indication (True=success, False=failure)
        Raises:
            Module-specific exceptions as documented in module PRD
        """
  
  return_types: "bool"  # Boolean success indication
  output_responsibility: "autonomous"  # Each module handles own output
  output_autonomy:
    - create_output_directories
    - define_file_naming_conventions  
    - perform_output_validation
    - handle_domain_specific_formats
  interface_authority:
    source: core-prd-main-v3.9.1.md#115-interface-authority-precedence-rules
    compliance: "core_prd_section_11_3_1_authoritative"

# 5. Error Handling Model
error_handling:
  protocol: "deterministic_implementation"
  source: core-prd-main-v3.9.1.md#1132-exception-classes
  implementation_mapping:
    file_operations: ["E0101", "E0106", "E0108", "E0111"]
    data_validation: ["E0102", "E0107", "E1190"]
    parsing_operations: ["E0105", "E0109", "E0110"]
    export_operations: ["E0104", "E0112", "E1106"]
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
    current_core: "3.9.1"
    current_governance: "2.7.0"
    minimum_core: "3.9.0"
    
  module_compatibility:
    accounts:
      core: "3.9.1"
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
      model: "2.7.0"
      enforce: true
      
  update_protocol:
    - increment_major:
        conditions: ["breaking_changes", "interface_changes"]
    - increment_minor:
        conditions: ["feature_additions", "backwards_compatible"]
    - increment_patch:
        conditions: ["bug_fixes", "documentation"]

# 8. Dispatch Payload Schema
payload_schema:
  name: "core_dispatch_payload_v1"
  version: "1.0"
  source: core-prd-main-v3.9.1.md#1144-dispatch-payload-schema
  fields:
    section:
      type: "str"
      description: "QuickBooks header name (e.g., 'ACCNT')"
      required: true
    records:
      type: "List[Dict[str, Any]]"
      description: "Parsed records under the section header"
      required: true
    output_dir:
      type: "str"
      description: "Destination directory for processed output"
      required: true
    extra_config:
      type: "Dict[str, Any]"
      description: "Optional: Additional runtime parameters (may be empty)"
      required: false
      default: {}

# 9. Error Code Registry
# All error classes and codes for the system are governed by the canonical table
# in core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table
# Local codes are not duplicated here to ensure single-source-of-truth

error_code_ranges:
  core_errors: "E01xx"
  logging_errors: "E02xx"  
  accounts_domain: "E11xx"
  governance_violations: "E91xx"
  unknown_errors: "E99xx"

error_implementation_protocol:
  source: core-prd-main-v3.9.1.md#1132-exception-classes
  approach: "deterministic_pattern_matching"
  discretion: false
  enforcement: "protocol_driven_not_discretionary"

# 10. Module Boundary Enforcement
module_boundaries:
  source: core-prd-main-v3.9.1.md#121-enhanced-module-boundary-specification-matrix
  domain_specific_logic:
    location: "src/modules/<domain>/<domain>_*.py"
    naming: "domain_prefix_required"
  cross_domain_utilities:
    location: "src/utils/*.py"
    restriction: "truly_domain_agnostic_only"
  violations:
    enforcement: "governance_failure"
    correction: "required_before_codegen"

# 11. Module Entry Point Standards
entry_point_standards:
  source: core-prd-main-v3.9.1.md#116-module-entry-point-standards
  pattern: "run_<domain>_pipeline"
  signature: "run_<domain>_pipeline(payload: Dict[str, Any]) -> bool"
  parameter: "payload conforming to core_dispatch_payload_v1"
  return_type: "bool (success indication)"
  compliance: "mandatory_for_all_domain_modules"

# 12. Expected Log Events
# All required and expected log events for modules are governed by the
# centralized logging framework per module-prd-logging-v1.0.4.md
# Domain-specific log events should be defined in respective module PRDs

logging_requirements:
  console_output: "human_readable"
  log_file: "trace_with_file_function_chain"
  structure: "deterministic_and_flush_safe"
  metadata: "sufficient_for_auditing_and_debugging"

# 13. Governance Compliance
governance_compliance:
  affirmed: true
  reference: prd-governance-model-v2.7.0.md
  core_prd_version: "3.9.1"
  interface_authority_compliance: true
  entry_point_standardization: true
  error_implementation_protocol: true
  module_boundary_enforcement: true
  rationale: |
    This interface definition affirms compliance with the QBD-to-GnuCash governance model (v2.7.0), 
    including all structural, naming, and traceability requirements as specified in the authoritative 
    PRD and governance documentation. All interface specifications follow Core PRD Section 11.5 
    authority precedence rules.