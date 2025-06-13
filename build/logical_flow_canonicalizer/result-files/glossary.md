# Glossary

## Master Module Table Terms
- **core**: The orchestrator module responsible for pipeline execution and module dispatch. (Source: core-prd-main-v3.9.1.md)
- **utils.error_handler**: Utility for exception classes and error code management. (Source: core-prd-main-v3.9.1.md, Section 14)
- **utils.logging**: Centralized logging utility for all modules. (Source: module-prd-logging-v1.0.5.md)
- **modules.accounts**: Domain module for QBD Accounts section processing. (Source: module-ir-accounts-v1.1.4.md)
- **accounts_mapping**: Submodule for mapping QBD account types to GnuCash. (Source: module-ir-accounts-v1.1.4.md)
- **accounts_tree**: Submodule for account hierarchy construction. (Source: module-ir-accounts-v1.1.4.md)
- **accounts_validation**: Submodule for validation of account data and structure. (Source: module-ir-accounts-v1.1.4.md)
- **accounts_export**: Submodule for exporting GnuCash-compatible CSV. (Source: module-ir-accounts-v1.1.4.md)

## Logical Flow Diagram Terms
- **Input Discovery**: Process of locating and identifying input files. (Source: core-ir-main-v3.9.1.md)
- **Section Processing**: Streaming and dispatching of QBD sections. (Source: core-ir-main-v3.9.1.md)
- **Dispatch Flow**: The logic for routing parsed sections to the correct module. (Source: core-ir-main-v3.9.1.md)
- **Business Logic Modules**: Modules that implement domain-specific processing. (Source: core-ir-main-v3.9.1.md)
- **Output Mapping/Export**: Transformation and output of processed data. (Source: module-ir-accounts-v1.1.4.md)
- **Error Handler**: Utility for error aggregation and handling. (Source: core-prd-main-v3.9.1.md)
- **Logging Service**: Utility for structured, flush-safe logging. (Source: module-prd-logging-v1.0.5.md)

## Schema Terms
- **core_dispatch_payload_v1**: Canonical payload schema for all module entry points. (Source: core-ir-main-v3.9.1.md)
- **MappingFileSchema**: JSON schema for account mapping files. (Source: module-ir-accounts-v1.1.4.md)
- **GnuCashAccountImport**: Output CSV schema for GnuCash import. (Source: module-ir-accounts-v1.1.4.md)

## PRD Authority Terms
- **Interface Authority Precedence**: Core PRD Section 11.5, which governs interface contract resolution. (Source: core-prd-main-v3.9.1.md)
- **Module Entry Point Standard**: Core PRD Section 11.6, which mandates `run_<domain>_pipeline` signature. (Source: core-prd-main-v3.9.1.md)
- **Module Boundary Matrix**: Core PRD Section 12.1, which defines placement of logic and utilities. (Source: core-prd-main-v3.9.1.md)

## Additional Terms
- **Topological Sort**: Dependency-ordered sequence for codegen. (Source: glossary.md#topological-sort)
- **Result Artifacts**: Output files or data structures produced by modules. (Source: module-ir-accounts-v1.1.4.md)

---

All terms are cross-referenced to their authoritative source. No orphaned references detected. Terminology is consistent across all artifacts and diagrams.
