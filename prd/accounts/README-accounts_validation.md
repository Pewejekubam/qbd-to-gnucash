# Validation Module

## Overview
This module performs final-stage cross-domain verification of all parsed and transformed data before output is emitted. It ensures data consistency, mapping completeness, hierarchy integrity, and conformance with GnuCash import requirements. All validation errors are raised in structured form and logged in compliance with centralized logging policy. The module is fully compliant with the latest governance and core PRD standards, and follows the validation and error handling model described in the authoritative PRD.

## File Structure
- `src/modules/accounts/accounts_validation.py` — Account validation logic
- `prd/accounts/README-accounts_validation.md` — This file
- `prd/accounts/module-prd-accounts_validation-v1.1.0.md` — Authoritative PRD for this module

## Design Reference
This module is governed by [Validation Module PRD v1.1.0](./module-prd-accounts_validation-v1.1.0.md) and follows the [Governance Model PRD v2.7.0 Section 2](../prd-governance-model-v2.7.0.md#2-structural-rules-and-document-standards). All interface contracts, error handling, and logging are aligned with [Core PRD v3.9.1 Section 7.3](../core-prd-main-v3.9.1.md#73-logging-strategy) and [Logging Framework PRD v1.0.5 Section 5](../logging/module-prd-logging-v1.0.5.md#5-interface--integration).

## Key Responsibilities
- Perform global validation checks on processed module data
- Enforce data integrity, mapping completeness, and hierarchy correctness
- Raise and log structured validation errors
- Ensure no unhandled errors exit the pipeline
- Ensure all validation and error handling is compliant with the authoritative error code table

## Exceptions & Logging
- Exceptions: `ValidationError`, `HierarchyViolationError`, `MappingInconsistencyError` (see [Validation Module PRD v1.1.0 Section 6.2](./module-prd-accounts_validation-v1.1.0.md#62-error-classes--exit-codes))
- Logging: All validation errors and process exits are logged per [Logging Framework PRD v1.0.5 Section 6](../logging/module-prd-logging-v1.0.5.md#6-validation--error-handling) and [Core PRD v3.9.1 Section 14](../core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table)

## Revision History
| Version | Date       | Author | Summary                           |
|---------|------------|--------|-----------------------------------|
| v1.1.0  | 2025-06-11 | PJ     | README updated to match PRD v1.1.0 and fully aligned with latest PRD-driven changes |
