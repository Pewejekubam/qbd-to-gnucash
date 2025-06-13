# Master Module Table

| Module Name         | Dependencies                                   | Entry Points                    | I/O Contracts                                                                 | Validation Status         | PRD Reference                                 | Codegen Template        |
|---------------------|------------------------------------------------|----------------------------------|-------------------------------------------------------------------------------|---------------------------|-----------------------------------------------|------------------------|
| core                | utils.error_handler, utils.logging             | run_conversion_pipeline, register_module, dispatch_to_module, log_and_exit | core_dispatch_payload_v1 (section, records, output_dir, extra_config)         | Validated (Core PRD 11.5, 11.6) | core-prd-main-v3.9.1.md#11.5, #11.6           | module.py.jinja        |
| utils.error_handler | None                                           | N/A                              | Exception classes, error codes (see Core PRD Section 14)                      | Validated (Core PRD 11.3.2)     | core-prd-main-v3.9.1.md#11.3.2                | module.py.jinja        |
| utils.logging       | utils.error_handler                            | setup_logging                    | Log file, log events, flush-safe logging                                      | Validated (Logging PRD 5, 6)    | module-prd-logging-v1.0.5.md#5, #6            | module.py.jinja        |
| modules.accounts    | utils.error_handler, utils.logging, accounts_mapping, accounts_validation, accounts_tree, accounts_export | run_accounts_pipeline             | core_dispatch_payload_v1 (section, records, output_dir, extra_config); CSV output; log file | Validated (Core PRD 11.5, 11.6; Module PRD 6.2) | core-prd-main-v3.9.1.md#11.5, #11.6; module-prd-accounts-v1.3.1.md#6.2 | module.py.jinja        |
| accounts_mapping    | None                                           | load_mapping                     | MappingFileSchema (JSON)                                                       | Validated (Module PRD)          | module-prd-accounts_mapping-v1.3.2.md         | function.py.jinja      |
| accounts_tree       | None                                           | build_accounts_tree              | Account hierarchy (Dict[str, Any])                                             | Validated (Module PRD)          | module-prd-accounts-v1.3.1.md                 | function.py.jinja      |
| accounts_validation | None                                           | run_validation_pass              | Validation rules, error classes                                                | Validated (Module PRD)          | module-prd-accounts_validation-v1.1.0.md      | function.py.jinja      |
| accounts_export     | None                                           | export_accounts                  | GnuCashAccountImport CSV, output validation                                    | Validated (Module PRD)          | module-prd-accounts-v1.3.1.md                 | function.py.jinja      |

- All modules accept `core_dispatch_payload_v1` schema as input where required.
- All entry points for domain modules follow `run_<domain>_pipeline(payload: Dict[str, Any]) -> bool` per Core PRD Section 11.6.
- All modules and interfaces validated against authoritative PRDs and schema.
- No schema entries lacking PRD validation detected.
- [Glossary](glossary.md#master-module-table) links technical terms.
