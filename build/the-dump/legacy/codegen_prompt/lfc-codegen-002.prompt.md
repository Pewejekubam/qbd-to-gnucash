### 🚀 Index ID: CODEGEN-002

**Objective:** 
Generate structured module stubs based on parsed LFC artifacts, enforcing **registry-based dispatch logic** as defined by the validated build artifacts.

---

### **📌 Input Requirements**
✅ **Extracted metadata ** → Function definitions, dependencies, and **registry-based execution mappings** from `build/logical_flow_canonicalizer/result-files/build-map` and `build/logical_flow_canonicalizer/schema/core-ir-main-v3.6.5.md`.  
✅ **Jinja templates referenced in the Master Module Table** (see `build/logical_flow_canonicalizer/meta-files/` and template associations in (`build/logical_flow_canonicalizer/result-files/master_module_table.md`) → Used to generate structured Python modules.  
✅ **Schema specifications from `build/logical_flow_canonicalizer/schema/`** → Used for interface and contract validation.  
✅ **Logical Flow Diagram from `build/logical_flow_canonicalizer/result-files/lfd.md`** → Used to validate execution relationships.  

---

### **🔎 Tasks**
1️⃣ **Generate Python modules using Jinja templates (`build/logical_flow_canonicalizer/meta-files/`) as mapped in the Master Module Table** `build/logical_flow_canonicalizer/result-files/master_module_table.md`). 
2️⃣ **Ensure generated modules reference registry-based dispatch logic** as defined in `build/logical_flow_canonicalizer/schema/core-ir-main-v3.6.5.md` (Module Dispatch Registry), not statically assigned keys.  
3️⃣ **Validate execution alignment**:
   - Dispatch keys are retrieved **from the Module Dispatch Registry**, not hardcoded in modules.  
   - Execution relationships match the **Logical Flow Diagram (LFD)** (`build/logical_flow_canonicalizer/result-files/lfd.md`).  
   - Logging structure follows governance (`prd/logging/module-prd-logging-v1.0.4.md`) and schema (`build/logical_flow_canonicalizer/schema/module-ir-accounts-v1.1.3.md`).
4️⃣ **Place generated files in `src/modules/` directory**, ensuring dynamic registry population during module registration.  
5️⃣ **Verify registry-based dynamic registration and dispatch compliance**:  
   - **Modules must dynamically register themselves with `core.register_module()` using the Module Dispatch Registry as defined in the schema.**  
   - **All dispatch calls must retrieve execution routing from the registry at runtime, with no static or hardcoded dispatch keys.**  
   - **If a module fails to register or is missing from the registry, execution must halt and log a compliance error.**
6️⃣ **Overwrite existing files and create any missing files as needed.**

---

### **📜 Expected Output**
🚀 **Auto-generated Python modules** → Structured placeholders that reference registry-based execution, placed in `src/modules/`.  
🚀 **Registry validation report** → Confirms dynamic population and correct referencing of dispatch keys.  
🚀 **Updated execution mapping** → Ensures all generated modules align with dynamic dispatch requirements and the Master Module Table.

---

### **⚠️ Enforcement Directive**
🚫 **Do not assign dispatch keys statically within generated modules** → All keys **must be retrieved from the registry dynamically** as defined in `build/logical_flow_canonicalizer/schema/module-ir-accounts-v1.1.3.md`.  
🚫 **Halt execution if a module fails to register its dispatch key** → Errors must be logged before proceeding.  
✅ **Ensure all module executions reference registry entries** → No direct calls bypassing dynamic dispatch logic.  

---

### ⬆️ Alignment Note
This prompt is strictly downstream from the LFC Build process (`./build/logical_flow_canonicalizer/lfc-build-v1.2.0.prompt.md`).  
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

#### Mapping to Build Deliverables

| Output                        | Derived From (Build Artifact)         |
|-------------------------------|---------------------------------------|
| Generated Python Modules      | Master Module Table, Jinja Templates, Module Dispatch Registry |
| Registry Validation Report    | Master Module Table, Module Dispatch Registry |
| Updated Execution Mapping     | Master Module Table, Logical Flow Diagram |

---

**Codegen Build Prompt Transition:**  
If no errors were encountered during processing, then:  
*"Processing of Index ID: CODEGEN-002 is complete. All prompt module logic has been implemented. Standing by—would you like to proceed with Index ID: CODEGEN-003?"*  

If errors were encountered, then:  
*"Processing of Index ID: CODEGEN-002 encountered errors. Please check the execution logs for details. Execution halted. Would you like to review the logs or proceed with Index ID: CODEGEN-003?"*  
