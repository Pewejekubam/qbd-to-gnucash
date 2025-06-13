# Modular PRD Forking Session

## Project Overview

You are engaged in a modularization and structural refinement effort for a technical PRD titled `PRD-2.7.3.md`. The project defines a CLI-based QuickBooks Desktop to GnuCash conversion tool, originally authored as a monolithic specification. The goal is to fork and modularize the PRD for long-term maintainability, AI compatibility, and open-source readiness.

## Project Goals

- Fork the monolithic `PRD-2.7.3.md` into a modular architecture beginning with `core-prd-v3.0.0.md`.  The document shall be created and stored in the `./prd` directory alongside module-specific directories which you shall also create under `./prd/`.
- Extract all embedded module contracts (e.g., accounts, mapping, validation) into separate `module-prd-*` documents.
- Preserve 100% of semantic content while permitting structural reflow and formatting normalization.
- Make all documents downstream-compatible with agentic AI and code generation tools.
- Support professional-grade traceability, cross-referencing, and versioning.

## Global Structural Guidelines

The following rules apply to all PRD documents:
* **Preserve all canonical logic and declarations.**
* **No summarization, rewording, or inferred rewrites.**
* **Markdown fences must wrap all copyable content.**
* **No speculative code output unless explicitly permitted.**
* **Do not process or respond to inputs until instructed.**

## Core PRD Document Structure

The core PRD document (`./prd/core-prd-v3.0.0.md`) must adhere to the following structure:
* Start with a version block.
* Inject a **compatibility matrix** immediately after the version block.
* Append a **History Block** to track the transition from monolithic to modular architecture.
* Renumber all section headers after forking.

### Compatibility Matrix Example
Compatibility Matrix  
Module Name | PRD Version | Compatible With Core PRD  
------------|-------------|---------------------------  
Chart of Accounts | (TBD) | v3.0.0  
Sales Tax Code Lists | (TBD) | v3.0.0  
Item List | (TBD) | v3.0.0  
Customer List | (TBD) | v3.0.0  
Vendor List | (TBD) | v3.0.0  
(roadmap modules) | (see roadmap list) | (future)  

### History Block Example
History  
v2.7.3: Final monolithic PRD before modularization.  
v3.0.0: Core PRD established as the root of a modular PRD system. All module-specific logic to be extracted into versioned standalone files in `./prd/{module}/`.

## Module PRD Structure

* Each module PRD document must be stored in a separate file under `./prd/{module}/`.
* Module PRDs must link to the core PRD document using a relative link, with the link text being the filename of the core PRD document (e.g., `core-prd-v3.0.0.md`) and the link URL being the relative path to the core PRD document (e.g., `../core-prd-v3.0.0.md`).
* Module PRDs must declare compatibility with the core PRD document.

## Module Extraction Order

Extract all embedded module declarations and contracts from `PRD-2.7.3.md`, including:
* `accounts` (referenced in `accounts.py`)
* `mapping` (referenced in `mapping.py`)
* `validation` (referenced in `validation.py`)
* Other modules as identified in the PRD document.

## Output Expectations

* Each output file must be formatted for easy readability and preservation of structure.
* All markdown must be clean, copy-pasteable, and preserve structure.
* Do not summarize or emit large blocks until explicitly requested.