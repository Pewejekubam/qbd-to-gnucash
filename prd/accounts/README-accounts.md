# Accounts Module

## Overview
This module manages the conversion and validation of account data exported from QuickBooks Desktop (QBD) into an import format compatible with GnuCash CSV import. It orchestrates account mapping, hierarchy construction, and enforces typing rules critical for correct financial data import. The module coordinates enhanced text-based mapping workflow with QBD path hints integration and implements comprehensive console logging with hierarchical tagging. The module is fully agentic and compliant with the latest governance and core PRD standards, and follows the orchestration and delegation model described in the authoritative PRD.

## File Structure
- `src/modules/accounts/accounts.py` — Main accounts module orchestrator with enhanced sub-module coordination
- `src/modules/accounts/accounts_export.py` — GnuCash CSV file generation and output validation
- `src/modules/accounts/accounts_mapping.py` — Account mapping loader, merger, and text-based workflow with QBD path hints
- `src/modules/accounts/accounts_mapping_baseline.json` — Baseline mapping JSON file
- `src/modules/accounts/accounts_tree.py` — Account tree builder and validator
- `src/modules/accounts/accounts_validation.py` — Account validation logic
- `prd/accounts/README-accounts.md` — This file
- `prd/accounts/module-prd-accounts-v1.3.2.md` — Authoritative PRD for this module
- Output:
    - `output/accounts.csv` — Fully converted, GnuCash-compatible import file
    - `output/accounts_mapping_questions.txt` — Text-based mapping questions for unmapped accounts with QBD path hints
    - `output/accounts_mapping_instructions.txt` — Comprehensive mapping instructions and examples
    - `output/accounts_mapping_questions_v{number}.txt` — Archive of mapping questions

## Design Reference
This module is governed by [Accounts Module PRD v1.3.2](./module-prd-accounts-v1.3.2.md) and follows the [Governance Model PRD v2.7.0 Section 2](../prd-governance-model-v2.7.0.md#2-structural-rules-and-document-standards). All interface contracts, error handling, and logging are aligned with [Core PRD v3.9.1 Section 7.3](../core-prd-main-v3.9.1.md#73-logging-strategy) and [Logging Framework PRD v1.0.5 Section 5](../logging/module-prd-logging-v1.0.5.md#5-interface--integration). Enhanced with CR-2025-CR-004v1.0.0 for QBD path hints orchestration.

## Key Responsibilities
- Orchestrate the complete accounts processing pipeline: mapping, tree building, validation, and export
- Process dispatched `!ACCNT` records from the central dispatcher (no direct IIF parsing)
- Coordinate enhanced text-based mapping workflow with QBD path hints for unmapped accounts
- Apply mapping and hierarchy rules to produce GnuCash-compatible CSV output
- Enforce strict account typing, placeholder handling, and AR/AP account rules
- Construct and validate the account tree structure
- Provide comprehensive console logging with hierarchical tagging for user guidance
- Implement streamlined HALT condition coordination for user interaction workflows
- Log all processing phases for traceability and debugging
- Ensure all validation and error handling is compliant with the authoritative error code table

## Enhanced Orchestration Features
- **QBD Path Hints Coordination**: Passes account records to mapping module for context integration
- **Hierarchical Console Logging**: `[ACCOUNTS-PIPELINE]` and `[ACCOUNTS-ORCHESTRATION]` tag structure
- **Streamlined HALT Messaging**: Cleaner user communication for mapping completion requirements
- **Sub-module Data Flow**: Coordinates account records between orchestrator and specialized modules
- **Enhanced Error Propagation**: Structured error handling with detailed context for debugging
- **Pipeline Flow Control**: Intelligent coordination between mapping, tree, validation, and export phases

## Pipeline Orchestration Model

### Data Flow Coordination
1. **Input Processing**: Receives `!ACCNT` records from core dispatcher via payload schema
2. **Mapping Coordination**: Passes account records to mapping module for QBD path hints integration
3. **Tree Construction**: Coordinates validated mappings for hierarchy building
4. **Validation Enforcement**: Ensures structural integrity across account relationships
5. **Export Generation**: Produces final GnuCash-compatible CSV output

### Enhanced Sub-module Integration
- **accounts_mapping.py**: Coordinated with account records parameter for QBD path context
- **accounts_tree.py**: Receives validated mapping results for hierarchy construction
- **accounts_validation.py**: Validates complete account structure integrity
- **accounts_export.py**: Generates final CSV output with format compliance

### HALT Condition Coordination
- **Detection**: Identifies when sub-modules require user interaction
- **Messaging**: Provides clear user guidance for completion requirements
- **Coordination**: Manages workflow state between pipeline phases
- **Recovery**: Handles resumption after user completion of required actions

## Console Logging Standards
- **`[ACCOUNTS-PIPELINE]`**: Main pipeline orchestration and completion status
- **`[ACCOUNTS-ORCHESTRATION]`**: Sub-module coordination and workflow management
- **User Guidance**: Clear messaging for HALT conditions and action requirements
- **Error Context**: Structured error reporting with actionable recovery information
- **Progress Tracking**: Detailed processing status for each pipeline phase

## Interface Contracts
- **`run_accounts_pipeline()`**: Main orchestration entry point with enhanced sub-module coordination
- **Sub-module Coordination**: Standardized data passing with account records integration
- **Error Handling**: Comprehensive exception propagation with structured context
- **HALT Management**: Boolean return patterns for pipeline flow control

## Exceptions & Logging
- **Exceptions**: `IIFParseError`, `MappingLoadError`, `AccountsTreeError`, and validation exceptions (see [Accounts Module PRD v1.3.2 Section 7.2](./module-prd-accounts-v1.3.2.md#72-error-classes--exit-codes))
- **Logging**: All errors and processing steps are logged per [Logging Framework PRD v1.0.5 Section 6](../logging/module-prd-logging-v1.0.5.md#6-validation--error-handling) and [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table)
- **Console Output**: Hierarchical tagging for user-friendly progress tracking and guidance

## Enhanced Workflow Integration

### QBD Path Hints Orchestration
```
accounts.py receives account records
    ↓
Passes records to accounts_mapping.py for context
    ↓
Mapping module generates questions with QBD path hints
    ↓
User sees original QuickBooks account names for context
    ↓
Enhanced mapping decisions with source system context
```

### Pipeline Coordination Flow
```
[ACCOUNTS-PIPELINE] Starting accounts processing
    ↓
[ACCOUNTS-ORCHESTRATION] Loading account mapping configuration
    ↓
[ACCOUNTS-ORCHESTRATION] Sub-module coordination: HALT condition detected (if needed)
    ↓
[ACCOUNTS-PIPELINE] Pipeline HALT: User action required (if needed)
    ↓
[ACCOUNTS-ORCHESTRATION] Building account hierarchy tree
    ↓
[ACCOUNTS-ORCHESTRATION] Beginning CSV export
    ↓
[ACCOUNTS-PIPELINE] Accounts processing completed successfully
```

## Production Readiness Features
- **Agentic Compatibility**: Deterministic orchestration patterns for autonomous operation
- **Error Recovery**: Comprehensive error handling with structured recovery guidance
- **User Experience**: Enhanced console messaging with clear action requirements
- **Data Integrity**: Preserved QBD account information throughout processing pipeline
- **Interface Stability**: Maintained contract compatibility with enhanced functionality
- **Logging Standards**: Hierarchical tagging for improved debugging and user guidance

## Dependencies
- **Core Framework**: Dispatcher integration via core_dispatch_payload_v1 schema
- **Sub-modules**: Enhanced coordination with mapping, tree, validation, and export modules
- **Error Handling**: Centralized exception management with structured context
- **Logging**: Hierarchical console output with user-friendly messaging patterns
- **External PRDs**: Logging Framework PRD v1.0.5, Core PRD v3.9.1 for compliance
- **Interface Enhancement**: CR-2025-CR-004v1.0.0 for QBD path hints orchestration

## Revision History
| Version | Date       | Author | Summary                           |
|---------|------------|--------|-----------------------------------|
| v1.3.1  | 2025-06-11 | PJ     | README updated to match PRD v1.3.1 and fully aligned with latest PRD-driven changes |
| v1.3.2  | 2025-06-13 | PJ     | CR-2025-CR-004v1.0.0 integration: Enhanced orchestration documentation, QBD path hints coordination, hierarchical console logging, streamlined HALT condition management, improved sub-module integration patterns |