# Validation Module

## Overview
This module performs final-stage cross-domain verification of all parsed and transformed data before output is emitted. It ensures data consistency, mapping completeness, hierarchy integrity, and conformance with GnuCash import requirements. All validation errors are raised in structured form and logged in compliance with centralized logging policy.

## File Structure
- `prd/accounts/module-prd-accounts_validation-v1.0.2.md` — PRD for the validation module
- `src/modules/accounts/accounts_validation.py` — Account validation logic  
- `prd/accounts/README-accounts_validation.md` — This file  


## Design Reference
This module is governed by [module-prd-accounts_validation-v1.0.2.md](./module-prd-validation-v1.0.2.md)

## Key Contracts or Responsibilities
- Perform global validation checks on processed module data
- Enforce data integrity, mapping completeness, and hierarchy correctness
- Raise and log structured validation errors
- Ensure no unhandled errors exit the pipeline

## Exceptions & Logging
- Exceptions: `ValidationError` (see PRD §7)
- Logging: All validation errors and process exits are logged per [logging/module-prd-logging-v1.0.4.md](../logging/module-prd-logging-v1.0.4.md)


## Revision History  
| Version | Date       | Author | Summary                           
|---------|------------|--------|--------------------------------- 
| v1.0.1  | 2025-05-23 | PJ     | README aligned with PRD and governance model
