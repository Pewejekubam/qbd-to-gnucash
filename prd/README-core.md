# PRD Index: QBD to GnuCash Conversion Tool

## Overview
This directory contains the Product Requirements Documents (PRDs) governing the architecture, modules, and compliance of the QBD to GnuCash Conversion Tool. Each PRD is versioned, agentic-compatible, and maintained under PRD Governance Model v2.7.0 for deterministic LFC artifact generation.

## Current Document Structure

### Core Architecture
- `core-prd-main-v3.9.1.md` — Core product requirements and system architecture
- `prd-governance-model-v2.7.0.md` — Governance framework and compliance rules
- `prd-template-module-v3.7.0.md` — Standardized template for domain module PRDs

### Domain Modules
- `accounts/module-prd-accounts-v1.1.3.md` — Accounts domain module
- `accounts/module-prd-accounts_mapping-v1.0.8.md` — Account type mapping subsystem
- `accounts/module-prd-accounts_validation-v1.0.2.md` — Account validation subsystem
- `logging/module-prd-logging-v1.0.4.md` — Centralized logging framework

## LFC Build Specifications

### Entry Point Pattern
All domain modules implement standardized entry points:
```
Function: run_<domain>_pipeline(payload: Dict[str, Any]) -> bool
Schema: core_dispatch_payload_v1 (section, records, output_dir, extra_config)
Return: Boolean success indication
```

### Error Implementation Protocol
Error codes mapped deterministically per Core PRD Section 14:
- File operations → E01xx range
- Domain-specific → E11xx range (accounts), E12xx (customers), etc.
- Protocol-driven implementation, no discretionary decisions

### Module Boundary Matrix
Domain logic placement follows Core PRD Section 12.1 decision matrix:
- Domain-specific: `src/modules/<domain>/<domain>_*.py`
- Cross-domain utilities: `src/utils/*.py`
- No CLI argument processing permitted

## Interface Authority Hierarchy
Per Core PRD Section 11.5:
1. Core PRD Section 11.3.1: Cross-module patterns (authoritative)
2. Module PRD Section 6.2: Domain implementations (compliant)
3. Conflict resolution: Core PRD supersedes module PRDs

## Dispatch Payload Schema
```json
{
  "section": "string",
  "records": "array", 
  "output_dir": "string",
  "extra_config": "object"
}
```

## Output Structure
All domain modules output to `output/` directory:
- `output/accounts.csv` — GnuCash account import
- `output/qbd-to-gnucash.log` — Centralized processing log
- Additional domain-specific outputs as defined in module PRDs

## Governance Compliance
- All PRDs follow immutable section headers per Governance v2.7.0
- Inter-PRD references use format: `[Document vX.Y.Z Section N: Title](path)`
- Version-locked dependencies prevent specification drift
- Sequential section numbering without gaps

## Dependencies
Core system dependencies:
- Python 3.8+ runtime environment
- No external libraries beyond standard Python distribution
- File I/O limited to `input/` and `output/` directories
- No CLI argument processing or user interaction

## Module Development
New domain modules use `prd-template-module-v3.7.0.md`:
- Follow Core PRD Section 11.6 entry point standards
- Implement Core PRD Section 14 error codes deterministically
- Comply with Core PRD Section 12.1 boundary specifications
- Reference authoritative Core PRD interface patterns

## File Processing Pipeline
1. Core discovers `.IIF` files in `input/` directory
2. Core parses section headers (ACCNT, CUST, TRNS, etc.)
3. Core dispatches payload to appropriate domain module
4. Domain module processes payload and generates output
5. All processing logged to centralized log file

## Validation Framework
- Input validation: core_dispatch_payload_v1 schema compliance
- Output validation: GnuCash CSV import format compliance
- Error validation: Authoritative error code implementation
- Interface validation: Core PRD Section 11.5 authority compliance

## CR-2025-002 Enhancements
Recent governance precision improvements:
- Interface authority precedence rules eliminate specification conflicts
- Module entry point standardization ensures consistent integration
- Enhanced boundary matrices prevent cross-domain violations
- Deterministic error implementation protocol for agentic compatibility

## Horizontal Scaling Readiness
Framework prepared for roadmap modules:
- sales_tax domain module development
- items domain module development  
- customers domain module development
- vendors domain module development

All roadmap modules will follow established patterns without specification conflicts.

## Revision History
| Version | Date       | Author | Summary                           |
|---------|------------|--------|-----------------------------------|
| v3.9.1  | 2025-06-11 | PJ     | README updated for PRD v3.9.1, new module PRDs, clarified compliance and interface authority |

---

**Document Governance:** PRD Governance Model v2.7.0  
**Last Updated:** 2025-06-11  
**Compatibility:** Core PRD v3.9.1, LFC artifact generation, autonomous codegen processes