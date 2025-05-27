# 📝 Prompts Directory Overview

This `./prompts` directory serves as the **central repository for AI-generated development prompts**, managing structured execution across code generation, auditing, and workflow orchestration. Each subdirectory houses prompts designed for specific phases of the AI-assisted build and review process.

## 📂 Directory Structure

The directory is divided into **four primary categories**:

### 🔹 `codegen/`
Prompts responsible for **AI-assisted code generation**. These guide the agent through structured builds, scaffolding, and iterative development phases.

Example prompts:
- `codegen-build-v2.1.7.prompt.md` → Defines phased code generation for modular development.
- `codegen-setup-env-v1.0.0.py` → Ensures PRD-compliant environment setup before execution.

### 🔹 `audit/`
AI-driven compliance checks to ensure generated code follows **PRD governance, maintainability rules, and structured validation**.

Example prompts:
- `full-code-audit-v1.0.0.prompt.md` → Performs a comprehensive review of AI-generated outputs.
- `full-prd-audit-v1.1.0.prompt.md` → Cross-checks build compliance with PRD definitions.

### 🔹 `workflow/`
Execution control and **process orchestration prompts** that manage AI-agent interactions for structured development.

Example prompts:
- `begin_ai_chat_session_prompt.md` → Establishes AI session directives and scope.
- `3-phase-build-v1.1.0.prompt.md` → Defines multi-phase agent-driven execution strategies.

### 🔹 `legacy/`
Archived versions of prompts no longer actively used but retained for **historical reference and evolution tracking**.

Example contents:
- Older phased build prompts (`phased-build-v2.1.4.prompt.md`)
- Deprecated PRD governance models (`prd-governance-model-v2.3.4.md`)

## ⚡ Best Practices for Using Prompts
- **Maintain versioning** ➝ Version numbers ensure clarity in iterative development.
- **Categorize appropriately** ➝ Store prompts in their respective subdirectories to maintain workflow integrity.
- **Review before execution** ➝ Ensure prompts align with current PRD and development goals before applying them.

---

This structure ensures **prompt-driven development stays modular, organized, and scalable**. If new workflow improvements emerge, prompts can be **iteratively refined and versioned** while keeping the AI-driven build process tightly governed.

