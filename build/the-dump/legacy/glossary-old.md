# Glossary of Terms

This glossary defines all key terms and concepts used in the Logical Flow Canonicalizer (LFC) process. Terms are referenced throughout LFC outputs using markdown links.

---

## [TOPOLOGICAL SORT](#topological-sort)
A deterministic ordering of modules or functions such that every dependency precedes its dependent. Used to ensure unambiguous execution flow in the LFD.

## [INTERFACE CONTRACT](#interface-contract)
A formal specification of function signatures, input/output types, and validation rules that must be satisfied at each module boundary. Also called a binding agreement in PRDs, governing validation logic.

## [VALIDATION](#validation)
The process of checking that all modules, dependencies, and orchestration rules conform to PRD and meta-file requirements. Includes error class and exit code enforcement. Validation rules may use schema (e.g., `accounts-validation.yaml`).

## [DISPATCH](#dispatch)
The act of routing data or control from the orchestrator (core) to a specific module based on a dispatch key or contract.

## [DISPATCH KEY](#dispatch-key)
A unique identifier used to route execution to the correct module, ensuring structured dispatch within the pipeline. Example: `!ACCNT` routes control to the accounts module.

## [MODULE](#module)
A self-contained unit of logic, typically corresponding to a domain (e.g., `accounts`), with its own entrypoint, validation, and dependencies. Modules are versioned and defined by PRDs and IR meta-files.

## [SUBMODULE](#submodule)
A component within a module (e.g., a Python file or class) that encapsulates a distinct aspect of the module’s logic. Example: `accounts_mapping` within the `accounts` module.

## [UTILITY](#utility)
A reusable, domain-agnostic component (e.g., `utils.logging`, `utils.error_handler`) that supports modules but does not contain domain-specific logic.

## [DEPENDENCY](#dependency)
A required relationship between modules, submodules, or utilities, as defined in meta-files and validated by PRDs.

## [PRD](#prd)
Product Requirements Document. The canonical source of operational, interface, and validation rules for all modules and utilities.

## [GOVERNANCE](#governance)
The set of structural, formatting, and compliance rules that all PRDs and outputs must follow, as defined in the governance model (see `prd-governance-model-v2.3.10.md`).

## [CANONICALIZATION](#canonicalization)
The process of converting ad hoc or implicit flows into a structured, validated, and reproducible sequence that aligns with meta-file definitions and PRD mandates.

## [ORCHESTRATION](#orchestration)
The coordination of module execution and inter-module communication to satisfy a system-level goal, governed by dependencies and contracts.

## [EXECUTION FLOW](#execution-flow)
The deterministic order in which modules and submodules are invoked, as defined by meta-files and enforced by PRDs.

## [EXECUTION HALT](#execution-halt)
A mandated stoppage of flow processing due to unresolved validation failure, dependency cycles, or governance violations. Output must include a halt report.

## [META-FILE](#meta-file)
A structured YAML or JSON file defining module relationships, dependencies, and logical ordering used by the LFC to construct the LFD.

## [IR](#ir)
Intermediate Representation. A structured YAML or JSON document that encodes the system’s modules, relationships, and orchestration rules for deterministic code generation.

## [VERSION RESOLUTION](#version-resolution)
The process of ensuring that all modules and dependencies are compatible and version-locked according to the rules in meta-files and PRDs.

## [LFD](#lfd)
Logical Flow Diagram. A directed acyclic graph rendered as Mermaid.js showing the validated execution order and dependencies between modules.

## [LFC](#lfc)
Logical Flow Canonicalizer. The system that reads meta-files and PRDs, performs validation, canonicalizes execution order, and generates deterministic artifacts.

## [ORCHESTRATOR](#orchestrator)
A core component responsible for managing execution flow, dispatching tasks, and coordinating modules. Defined in the PRD as a central control entity.

## [ENTRYPOINT](#entrypoint)
The designated callable function within a module that receives control during orchestration and is subject to strict input/output and contract validation.

## [HALT REPORT](#halt-report)
A required output (`lfc_halt_report.md`) when canonicalization fails, documenting the failure condition, affected components, and remediation guidance.

## [LOGGING](#logging)
A structured mechanism for tracking execution events, errors, and state transitions. Defined in `module-prd-logging-v1.0.4.md`, logging enforces compliance by maintaining traceability across pipeline stages.

---

All terms are referenced in [master_module_table.md](master_module_table.md), [lfd.md](lfd.md), [lfc-meta-files-manifest.md](lfc-meta-files-manifest.md), and [README.md](README.md).
