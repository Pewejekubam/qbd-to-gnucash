# Governance Document — PRD Structure and Enforcement  
**Document Version:** v2.2.0  
**Module Identifier:** governance.md  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** 2025-05-24  

---

## 1. Purpose

This document establishes naming, formatting, and structural standards for all Product Requirements Documents (PRDs) associated with the QuickBooks Desktop to GnuCash Conversion Tool. It ensures consistency, enforceability, and compatibility with agentic AI systems and human collaborators alike.

---

## 2. PRD Roles and Scope

Each PRD must fall into one of the following categories:

- **Core Modules:** Cross-domain infrastructure or compliance logic (e.g., logging, error handling, IIF parsing).
- **Domain Modules:** Business logic scoped to a QuickBooks/GnuCash domain (e.g., accounts, vendors, sales_tax).
- **Submodules:** Logical subdivisions of a domain module (e.g., accounts_mapping, accounts_validation).
- **Templates:** Reusable boilerplate PRDs for standardized authoring.

---

## 3. Directory Structure

All PRDs must reside in the `/prd` root directory, under the following conventions:

```
/prd/
│
├───core-prd-vX.Y.Z.md
├───README-core.md
│
├───<domain>/
│   ├───module-prd-<domain>-vX.Y.Z.md
│   ├───module-prd-<domain>_<tag>-vX.Y.Z.md
│   ├───README-<domain>.md
│   └───README-<domain>_<tag>.md
│
└───templates/
    └───prd-template-module-vX.Y.Z.md
```

All domain-specific PRDs must be stored in a subdirectory named after the domain. Core PRDs remain at the top level of `/prd`.

---

## 4. Versioning Enforcement

### 4.1 Version Format

All PRD versions must follow semantic versioning as `vX.Y.Z`, where:

- `X` = major version (breaking changes)
- `Y` = minor version (feature additions)
- `Z` = patch version (bug fixes, formatting)

Example: `v1.2.0`, `v3.6.0`

### 4.2 Update Protocol

- Any material change to PRD content must result in a version bump.
- Changes to metadata only (e.g., author or timestamp) do not require version updates.
- Version bumps must reflect the semantic impact of the change.

### 4.3 Document Metadata

Each PRD must begin with the following metadata block:

```
# Product Requirements Document — <Module Name>  
**Document Version:** vX.Y.Z  
**Module Identifier:** <filename>.py  
**System Context:** QuickBooks Desktop to GnuCash Conversion Tool  
**Author:** Pewe Jekubam  
**Last Updated:** YYYY-MM-DD  
```

The `<Module Name>` is a human-readable label, while `<filename>.py` must match the source module the PRD describes.

### 4.4 Filename Protocol

All filenames must conform exactly to one of the following canonical patterns:

- `core-prd-vX.Y.Z.md` — cross-domain orchestration, logging, or global infrastructure.
- `core-prd_<tag>-vX.Y.Z.md` — specialized core module with a descriptive subcomponent tag.
- `module-prd-<domain>-vX.Y.Z.md` — standalone PRD for a business domain (e.g., `accounts`, `vendors`, `customers`).
- `module-prd-<domain>_<tag>-vX.Y.Z.md` — subordinate PRD within a domain, with `<tag>` denoting a specialized submodule (e.g., `accounts_mapping`, `accounts_validation`).
- `prd-template-module-vX.Y.Z.md` — template PRD for new modules.

The following rules are strictly enforced:

- `X.Y.Z` must be a valid semantic version triplet (e.g., `1.0.0`, `2.4.7`).
- `<domain>` must be a valid business domain identifier.
- `<tag>` (if present) must be a single snake_case identifier of one or two words. It must be relevant to the submodule’s primary function but is otherwise at the author's discretion.
- Only `.md` is permitted as the file extension.
- All filenames must use `snake_case` exclusively.
- Each file must reside in its corresponding subdirectory under `/prd`.

---

## 5. Domain Name Registry

The list of valid `<domain>` identifiers is maintained in the Core PRD. It is authoritative and updated with each recognized business domain added to the system. The Governance Document does not maintain this list directly.

Example domains:

- `accounts`
- `vendors`
- `customers`
- `sales_tax`
- `job_type`
- `payment_method`

---

## 6. PRD Templates

All new PRDs must be initialized from the `prd-template-module-vX.Y.Z.md` template stored under `/prd/templates`. The latest template version must always be used unless justified and version-locked.

---

## 7. Human vs AI Readability

- The numeric section system (e.g., 4.4, 5.2) is retained for human IDE navigation.
- All logic, validation, and enforcement rules must be fully declarative to support AI agent parsing and static enforcement.

---

## 8. Cross-Linking Conventions

- All internal references must use section numbers (e.g., “See §4.4”) to allow both humans and AI to resolve references unambiguously.
- Do not use page numbers or “see above/below” phrasing.

---

## 9. Change History and Audit

Every PRD must maintain a changelog section at the end of the file, noting:

- Date of change
- Author
- Version bump
- Nature of change

---

## 10. File Naming Violations

If a PRD file does not conform to the filename patterns in §4.4, it must be flagged for correction before merging into the project tree. This includes any of the following:

- Missing or malformed version strings
- Improper use of hyphens, mixed casing, or dots in `<domain>` or `<tag>`
- Misplaced directory locations

---

## 11. Enforced Constraints

- Filenames are enforced at pull request review time.
- Directory placement is enforced by static directory traversal tools or agent validation sweeps.
- Version bumps must be justified and validated at merge.

---

## 12. Metadata Location

The metadata block defined in §4.3 must appear at the top of the PRD file before any narrative content, headers, or logic sections.

---

## 13. [Intentionally Omitted]

CI/CD pipeline enforcement is not currently part of the roadmap and has been excluded from this document.

---
