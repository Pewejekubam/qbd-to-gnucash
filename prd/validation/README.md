# Validation Module

## Overview
This module performs final-stage cross-domain verification of all parsed and transformed data before output is emitted. It ensures data consistency, mapping completeness, hierarchy integrity, and conformance with GnuCash import requirements. All validation errors are raised in structured form and logged in compliance with centralized logging policy.

## File Structure
- `module-prd-validation-v1.0.1.md` — PRD for the validation module
- `validation.py` — Validation logic
- `README.md` — This file

## Design Reference
This module is governed by [module-prd-validation-v1.0.1.md](./module-prd-validation-v1.0.1.md)

## Key Contracts or Responsibilities
- Perform global validation checks on processed module data
- Enforce data integrity, mapping completeness, and hierarchy correctness
- Raise and log structured validation errors
- Ensure no unhandled errors exit the pipeline

## Exceptions & Logging
- Exceptions: `ValidationError` (see PRD §7)
- Logging: All validation errors and process exits are logged per [logging/module-prd-logging-v1.0.4.md](../logging/module-prd-logging-v1.0.4.md)

---
Changelog: v1.0.1 — README created for PRD and governance model compliance (2025-05-23)
