# QBD-to-GnuCash Intermediate Representation Schema **accounts Module**
# Version: v1.1.3
# Compatible Core PRD: v3.9.1
# Compatible Module PRD: v1.3.1

# 1. Core Interface Contract

# ## 1.1 Module Contract: accounts.py
# type: module
# name: accounts
# entry_point: run_accounts_pipeline
# dispatch_key: "!ACCNT"

# input_contract:
#   type: TypedDict
#   name: DispatchPayload
#   fields:
#     section: 
#       type: str
#       value: "!ACCNT"
#     records:
#       type: List[Dict[str, Any]]
#       description: List of parsed account records
#     input_path:
#       type: str
#       description: Original source file path
#     output_dir:
#       type: str
#       description: Target directory for outputs
#     log_path:
#       type: str
#       description: Log file path
#     mapping_config:
#       type: Dict[str, Any]
#       description: Account mapping configuration
#     extra_config:
#       type: Optional[Dict[str, Any]]
#       description: Additional configuration

# output_contract:
#   - type: File
#     format: CSV
#     path: "{output_dir}/accounts.csv"
#     schema: GnuCashAccountImport
#   - type: ExitCode
#     values:
#       0: Success
#       1: Critical failure
#       2: Validation errors
#   - type: LogFile
#     path: "{log_path}"
#     format: Structured

# 2. Interface Contracts

# ## 2.1 Public Interfaces

# ### run_accounts_pipeline
# ```python
# def run_accounts_pipeline(payload: DispatchPayload) -> None:
#     """Entry point for processing QBD !ACCNT list."""
# ```
# exceptions:
#   - IIFParseError: Dispatch validation failures (E0005)
#   - MappingLoadError: Mapping file issues (E0201)
#   - AccountsTreeError: Hierarchy construction failures (E0204)
#   - OutputWriteError: CSV generation issues (E0004)
#   - ValidationError: Final validation failures (E0301)
#   - HierarchyViolationError: Invalid parent/child relationships (E0302)
#   - MappingInconsistencyError: Mapping gaps or conflicts (E0303)

# ### load_mapping
# ```python
# def load_mapping(user_mapping_path: Optional[str] = None) -> Dict[str, Any]:
#     """Load and merge mapping files for QBD to GnuCash account types."""
# ```
# exceptions:
#   - MappingLoadError: Required files missing/unreadable (E0201)
#   - MappingInconsistencyError: Mapping schema or content errors (E0303)

# ### build_accounts_tree
# ```python
# def build_accounts_tree(records: List[Dict[str, Any]], mapping: Dict[str, Any]) -> Dict[str, Any]:
#     """Build and validate account hierarchy."""
# ```
# exceptions:
#   - AccountsTreeError: Invalid hierarchy (E0204)
#   - HierarchyViolationError: Cycles or orphaned nodes (E0302)

# ### run_validation_pass
# ```python
# def run_validation_pass(tree: Dict[str, Any], mapping: Dict[str, Any]) -> None:
#     """Final structure validation, AR/AP enforcement, circular reference detection."""
# ```
# exceptions:
#   - ValidationError: Final validation failures (E0301)
#   - HierarchyViolationError: Invalid parent/child relationships (E0302)

# ### export_accounts
# ```python
# def export_accounts(tree: Dict[str, Any], output_dir: str) -> None:
#     """GnuCash CSV file generation and output validation."""
# ```
# exceptions:
#   - OutputWriteError: CSV generation issues (E0004)

# 3. Data Structure Schemas

# ## 3.1 Account Record Schema
# ```typescript
# interface AccountRecord {
#   NAME: string;
#   ACCNTTYPE: string;
#   DESC?: string;
#   PARENT?: string;
#   BALANCE?: string;
#   TIMESTAMP?: string;
# }
# ```

# ## 3.2 Mapping File Schema
# ```json
# {
#   "$schema": "http://json-schema.org/draft-07/schema#",
#   "type": "object",
#   "properties": {
#     "account_types": {
#       "type": "object",
#       "additionalProperties": {
#         "type": "object",
#         "properties": {
#           "gnucash_type": {"type": "string"},
#           "hierarchy_path": {"type": "string"}
#         },
#         "required": ["gnucash_type", "hierarchy_path"]
#       }
#     },
#     "default_rules": {
#       "type": "object",
#       "additionalProperties": {"type": "string"}
#     }
#   },
#   "required": ["account_types", "default_rules"]
# }
# ```

# ## 3.3 GnuCash Account CSV Schema
# ```json
# {
#   "type": "object",
#   "properties": {
#     "account_type": {
#       "type": "string",
#       "enum": ["ASSET", "LIABILITY", "INCOME", "EXPENSE", "EQUITY"]
#     },
#     "full_name": {
#       "type": "string",
#       "pattern": "^[^:]+(?::[^:]+)*$"
#     },
#     "name": {"type": "string"},
#     "description": {"type": "string"},
#     "placeholder": {"type": "boolean"}
#   },
#   "required": ["account_type", "full_name", "name"]
# }
# ```

# 4. Dependencies Map

# ## 4.1 Direct Dependencies
# - accounts_mapping.py (v1.3.2):
#     - Purpose: Account type mapping, text-based workflow, unmapped type detection
#     - Interface: load_mapping
#     - Required by: run_accounts_pipeline
# - accounts_tree.py:
#     - Purpose: Account hierarchy construction, parent-child validation, type promotion
#     - Interface: build_accounts_tree
#     - Required by: run_accounts_pipeline
# - accounts_validation.py (v1.1.0):
#     - Purpose: Final validation, AR/AP enforcement, cycle detection
#     - Interface: run_validation_pass
#     - Required by: run_accounts_pipeline
# - accounts_export.py:
#     - Purpose: GnuCash CSV file generation, output validation
#     - Interface: export_accounts
#     - Required by: run_accounts_pipeline

# ## 4.2 Common Utilities
# - error_handler.py:
#   - Purpose: Exception definitions
#   - Classes: IIFParseError, MappingLoadError, AccountsTreeError, OutputWriteError, ValidationError, HierarchyViolationError, MappingInconsistencyError
#   - Required by: All modules
# - logging.py (v1.0.5):
#   - Purpose: Centralized logging
#   - Interface: setup_logging
#   - Required by: All modules

# ## 4.3 Configuration Files
# - accounts_mapping_baseline.json:
#   - Purpose: Default mappings
#   - Required by: accounts_mapping.py
#   - Schema: MappingFileSchema
# - accounts_mapping_specific.json:
#   - Purpose: User overrides (from text-based workflow)
#   - Required by: accounts_mapping.py
#   - Schema: MappingFileSchema

# 4.4 Error Code Reference
# All error classes and codes for this module are governed by the canonical table in core-prd-main-v3.9.1.md, Section 14: Authoritative Error Classes & Error Code Table. No ad-hoc or undocumented error classes are permitted.

# 4.5 Expected Log Events Reference
# All required and expected log events for this module are governed by the canonical expected_log_events block in system-ir-v2.2.1.yaml (section: expected_log_events), and Logging Framework PRD v1.0.5 Section 6. Local log event duplication is avoided to ensure traceability, single-source-of-truth, and PRD/governance compliance.

# 5. Validation Rules
# 5.1 Input Validation
# - Valid QuickBooks account types
# - One AR and one AP root account; duplicates trigger errors
# - No orphaned children or circular hierarchies
# - Required fields non-null
# 5.2 Mapping Rules
# - All keys resolve to known GnuCash types
# - Default rules for unmapped types (placeholder accounts inserted and logged)
# - Valid hierarchy paths
# 5.3 Output Rules
# - Valid GnuCash CSV format
# - Unique account paths
# - Proper placeholder flags
# - Output integrity verified

# 6. Version Compatibility
# compatible_versions:
#   core_prd: "3.9.1"
#   governance_model: "2.7.0"
#   logging_module: "1.0.5"
#   mapping_module: "1.3.2"
#   validation_module: "1.1.0"
#   python: ">=3.8"

# governance_compliance:
#   affirmed: true
#   reference: prd-governance-model-v2.7.0.md
#   rationale: |
#     This interface definition affirms compliance with the QBD-to-GnuCash governance model (v2.7.0), including all structural, naming, and traceability requirements as specified in the authoritative PRD and governance documentation.