### **Prompt for Local Agent: Logical Flow Canonicalizer (LFC)**
### Version: 1.1.8

#### 1. **Compliance References**
- **Core PRD Document:** `core-prd-main-v3.6.4.md`
- **Governance Document:** `prd-governance-model-v2.3.10.md`
- **Logging Framework Module PRD:** `module-prd-logging-v1.0.4.md`

---

#### 2. **Objective**
You are tasked with constructing a **Logical Flow Canonicalizer (LFC)** that formalizes execution order, dependencies, interfaces, state transitions, and modular orchestration, ensuring deterministic code generation and eliminating ambiguity in system flow.

(LFD = Logical Flow Diagram)  

Your directives are **strict**:  
✅ **DO extract logical flow data exclusively from meta-files** within `./build/logical_flow_canonicalizer/lfc-meta-files/`  
✅ **DO enforce compliance with PRDs and governance mandates**  
✅ **DO ensure logging is fully integrated as a structured execution component**  
✅ **Place all generated files directly into the file system**—**no output should be presented exclusively in chat**.  
✅ **Modify files inline** within their designated locations—**no external drafts or temporary deliverables**.  

🚫 **DO NOT infer execution order beyond metadata definitions**  
🚫 **DO NOT alter module relationships beyond structured dependencies**  

---

#### 3. **Enforcement Directive: PRDs & Meta-Files as Core Execution Sources**
_"All system logic, execution ordering, interface contracts, validation mechanisms, and dispatch structures **must be derived explicitly from two authoritative sources**:  
3.1️⃣ **Meta-Files** (`./build/logical_flow_canonicalizer/lfc-meta-files/`) → Define structured execution mappings, interdependencies, orchestration sequences.  
3.2️⃣ **PRDs** (`./prd/core-prd-main-v3.6.4.md`, `./prd/loggingmodule-prd-logging-v1.0.4.md`, etc.) → Define operational compliance, validation rules, interface contracts.  

The agent **is prohibited from making assumptions** outside of formal PRD definitions or structured metadata. If a logical gap exists between PRD constraints and meta-file execution rules, **execution halts** until the discrepancy is explicitly resolved."

---

#### 4. **Compliance Verification**
Before proceeding, you **must** scan and acknowledge the compliance requirements of:

- `core-prd-main-v3.6.4.md` (Core PRD rules & constraints)
- `prd-governance-model-v2.3.10.md` (Governance policies)
- `module-prd-logging-v1.0.4.md` (Logging facility structure)

Upon completion, generate a **structured declaration** that:
- Summarizes compliance rules affecting modular execution flow  
- Identifies enforced constraints influencing orchestration  
- Confirms alignment with governance mandates  
- Explicitly states understanding before canonicalization begins  

Proceed **only after compliance verification**.

---

#### 5. **Key Deliverables**

##### 5.1 **Master Module Table**
- The **Master Module Table** is derived from IR meta-files in `./build/logical_flow_canonicalizer/lfc-meta-files/`, which serve as **provisional representations** of module relationships.  
- All listed modules and dependencies **must correspond** to entries in this IR layer, but **the PRD remains the canonical source of truth**.  
- If a dependency appears in a meta-file but lacks validation (e.g., **missing entrypoint signature, absent I/O contract, vague validation logic**), the **LFD generation prompt must attempt to reconcile this using the matching module PRD before deciding whether to include it**.  
- The **LFD prompt must treat meta-files as *suggestive but fallible***. It must **default to PRD guidance when inconsistencies or omissions are detected**.  
- Shall be produced as `master_module_table.md`.

##### 5.2 **Logical Flow Diagram (LFD)**
- Logical Flow Diagrams must be **emitted as Mermaid.js code blocks** within Markdown documents.  
- Each node represents a **module or function**, and edges represent **dependencies or execution flow**.  
- Shall be produced as `lfd.md`

Example:
````markdown
```mermaid
graph TD
  config_loader --> mapping_loader
  config_loader --> account_tree
  account_tree --> transaction_parser
`````

````

##### 5.3 **lfc-meta-files Directory (`build/logical_flow_canonicalizer/lfc-meta-files/`)**
- All valuable meta-files contributing to LFD formation must be read from `build/logical_flow_canonicalizer/lfc-meta-files/`.  
- The **index and manifest of meta-files** can be generated, but actual meta-file content **must be preserved in the `./lfc-meta-files/` directory** for future reference.  
- An **illustrative example meta-file** should be included for documentation purposes (non-enforced).

##### 5.4 **Output Location Directive**
- All generated documents must be stored in the root directory `./build/logical_flow_canonicalizer/`, including:
  - `master_module_table.md` - Master Module Table  
  - `lfd.md` - Logical Flow Diagram
  - `lfc-meta-files-manifest.md` - Manifest of LFC Meta-Files
  - `README.md` - Overview of LFC Outputs
  - `glossary.md` - Glossary of Terms
  - `lfc_halt_report.md` - Execution Halt Report (if applicable)
- Only meta-files are stored under `lfc-meta-files/`, ensuring **LFC outputs and documentation remain clearly separated**.
- All markdown files must not contain HTML tags or inline HTML elements, ensuring **pure markdown formatting**.

##### 5.5 **Execution Halt Reporting**
If the LFC halts due to validation failure, cycle detection, or unresolved dependencies, it must output a file:

**`lfc_halt_report.md`** containing:
- The trigger condition
- Affected module or step
- Related PRD or meta-file reference
- Suggested remediation or review path

---

#### 6. **Glossary Cross-Referencing**
Glossary terms must be stored in `glossary.md`, co-located within `build/logical_flow_canonicalizer/`.  
All LFC outputs must reference glossary terms using markdown links:  
E.g. `[TOPOLOGICAL SORT](glossary.md#topological-sort)`  

These links must be present in:
- Master Module Table  
- Logical Flow Diagram
- Interface Contract Index  
- Manifest of LFC Meta-Files
```
