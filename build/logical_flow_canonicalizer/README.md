
## LFC IR/Meta File Naming Scheme
All LFC-generated intermediate representation (IR) and meta documentation files follow a strict, scalable naming convention for clarity, traceability, and governance compliance:
```
<type>-ir-<domain>[_<tag>]-v<MAJOR>.<MINOR>.<PATCH>.md
```
Where:
- `<type>`: `core` or `module` (corresponds to system/core or a specific module)
- `<domain>`: a valid domain name as defined in the PRD Governance Model (see Section 3, Domain Index Protocol)
- `<tag>`: optional, for submodules or extensions (must be lowercase and snake_case)
- `<MAJOR>.<MINOR>.<PATCH>`: version number matching the referenced PRD

**Examples:**
- `core-ir-main-v3.6.5.md` (IR distillation of `core-prd-main-v3.6.5.md`)
- `module-ir-accounts-v1.1.3.md` (IR distillation of `module-prd-accounts-v1.1.3.md`)
- `module-ir-accounts_mapping-v1.0.8.md` (IR for the accounts mapping submodule)

This scheme ensures:
- Clear distinction from canonical PRDs (using `ir` instead of `prd` in the identifier)
- Scalability for future modules and submodules
- Direct traceability to the authoritative PRD version through consistent naming patterns
- Full alignment with governance structure while maintaining processing clarity## Usage Notes
- All outputs are Markdown and reference [GOVERNANCE](glossary.md#governance) and [PRD](glossary.md#prd) terms as required.
- Glossary links are embedded throughout for clarity and compliance.
- If `lfc_halt_report.md` exists, review and resolve the issues before proceeding with further canonicalization or code generation.

---

For more details, see the [LFC Prompt](lfc-build-v1.1.9.prompt.md) and referenced PRDs.
