The markdown-formatted Product Requirements Document (PRD) #file:PRD-2.7.1.md  that includes embedded update directives for integrating new logic.

Your task is to:

1. **Integrate the updates** precisely where directed within the PRD.
2. **Maintain the original structure, formatting, verbosity, and logical boundaries** of the document — do not reflow, deduplicate, or reformat beyond what is explicitly allowed.
3. **Produce an updated PRD** with:
   - The new version number applied as appropriate (e.g., v2.7).
   - A **rollback-ready changelog** that captures each modification made, by section and reason.
   - Optional: Inline version tags like `<!-- v2.7 update applied -->` may be included for traceability.


---

### 💡 Notes for AI Interpreter

- **Do not alter** sections or paragraphs without explicit directives, even if improvements seem obvious.
- Changes are **surgical and local** unless otherwise instructed.
- All embedded formatting — bolding, headers, bullet structure — is **intentional and must be preserved**.
- Redundancy is **not accidental**; do not collapse repeated logic or remove mirrored rules unless explicitly told to.
- The resulting changelog must allow **section-level rollback** or diff inspection.
- A machine-readable changelog (e.g., JSON or tabular format) may optionally be requested afterward.
