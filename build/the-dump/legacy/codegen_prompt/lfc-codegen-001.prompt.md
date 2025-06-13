### 🚀 Index ID: CODEGEN-001

**Objective:**  
Consume and verify LFC Build artifacts to extract execution-critical metadata and enforce dynamic, registry-based dispatch for code generation.

---

### 📌 Required Artifacts (from LFC Build)
- `build/logical_flow_canonicalizer/result-files/master_module_table.md` (Execution Metadata Registry)
- `build/logical_flow_canonicalizer/result-files/lfd.md` (Logical Flow Diagram)
- `build/logical_flow_canonicalizer/result-files/build_map.yaml` (Dependency-ordered sequence for agentic codegen execution)
- `build/logical_flow_canonicalizer/result-files/glossary.md` (Comprehensive Glossary)
- `build/logical_flow_canonicalizer/schema/core-ir-main-v3.6.5.md` (Module Dispatch Registry)
- `build/logical_flow_canonicalizer/schema/module-ir-accounts-v1.1.3.md` (Accounts Domain Module)

---

### 🔎 Tasks
✅ **Verify presence and completeness of all required artifacts.**  
✅ **Extract function definitions, dependencies, and registry assignments from the Master Module Table and Build Map.**  
✅ **Ensure all dispatch keys are resolved dynamically at runtime via the Module Dispatch Registry.**  
✅ **Ensure all dependency and compliance checks use the Execution Metadata Registry.**  
✅ **Halt execution and generate a halt report if any artifact or registry entry is missing, incomplete, or invalid.**

---

### ⚠️ Enforcement Directive
✅ **All codegen must use the validated, dynamic registries and metadata from the build process.**  
🚫 **Do not create, modify, or reinterpret registry entries or build artifacts.**  
🚫 **Do not rely on statically assigned dispatch keys.**  
🚫 **Halt if any artifact or registry entry is missing or invalid.**

---

### ⬆️ Alignment Note
This prompt is strictly downstream from the LFC Build process (`lfc-build-v1.4.1.prompt.md`).  
It must not proceed unless all required build artifacts are present and validated.

---

### Static vs Dynamic Registry Responsibilities

- **Static Registry (Code-Time/Compile-Time):**
  - The mapping of dispatch keys (e.g., section headers in input files) to modules is defined and maintained manually by the code maintainer.
  - This mapping is established at code generation time and is not modified at runtime.
  - No automatic or dynamic registration of new modules is supported.

- **Dynamic Dispatch (Runtime):**
  - At runtime, the system dynamically dispatches processing of input data (e.g., sections found in IIF files) by looking up the corresponding module in the static registry.
  - Only modules present in the static registry can be dispatched to.
  - If a dispatch key is found in the input that is not present in the static registry, the system logs a warning or error and skips or halts as per PRD.

**This distinction ensures that all code generation and runtime logic strictly follows the intended architecture and governance.**

---

**Codegen Build Prompt Transition:**  
If no errors were encountered during processing, then:  
*"Processing of Index ID: CODEGEN-001 is complete. All prompt module logic has been implemented. Standing by—would you like to proceed with Index ID: CODEGEN-002?"*  

If errors were encountered, then:  
*"Processing of Index ID: CODEGEN-001 encountered errors. Please check the execution logs for details. Execution halted. Would you like to review the logs or proceed with Index ID: CODEGEN-002?"*  
