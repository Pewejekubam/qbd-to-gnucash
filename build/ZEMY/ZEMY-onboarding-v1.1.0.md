🚀 **Finalized Onboarding Document for ZEMY v1.1.0**  

```markdown
# **🚀 ZEMY v1.1.0 Onboarding Guide**  
## **Welcome to ZEMY (Zipper Execution Mapping YAML)**  
ZEMY is a **self-triggering execution framework** designed to **transform input artifacts into deterministic execution mappings**.  
Its core function is to **eliminate discretionary drift** by enforcing structured validation cycles and adaptive compliance weighting.

---

## **🔹 Step 1: Agent Training for ZEMY Execution**  
Before running ZEMY, the agent **must be trained** to ensure execution mapping operates within strict compliance constraints.

### **Training Process**  
✔ Open the file: **`ZEMY-training-v1.1.0.prompt.md`**  
✔ Manually **paste the contents into the agent setup** before running `"Build it!"`  
✔ Ensure **the agent processes all execution mapping constraints** before ingesting input artifacts.  

💡 **Training prompt contents define structured execution enforcement, preventing discretionary drift.**  
Once training is complete, the execution mapping process follows a **fully structured workflow**, ensuring **self-regulating compliance enforcement**.  

---

## **🔹 Step 2: Configuring Input Sources**  
ZEMY processes input artifacts through two methods:  
✔ **Local Directory** → Define a path for structured input ingestion.  
✔ **Pasted Prompt Attachments** → Artifacts must be named explicitly in fenced blocks.

**Example Input Configuration in ZEMY.yaml:**  
```yaml
input_source:
  method: "Local Directory"
  path: "/project/zemy/input"  # Define artifact storage path.
  fallback: "Pasted Prompt"
  artifacts:
    - name: "artifact_1.md"
    - name: "artifact_2.txt"
    - name: "system_diagram.mermaid"
```

🚀 **What You Need to Do:**  
✔ Update `"path"` with your local artifact directory.  
✔ If pasting artifacts into the prompt, reference them inside **fenced code blocks**.  

## **🔹 Understanding ZEMY's Validation System**
ZEMY uses **predictive drift analysis** and **threshold-based validation** to ensure execution integrity:
✔ **Weight scores** are automatically monitored against defined thresholds
✔ **Role isolation** prevents execution logic from blending with output generation  
✔ **Compliance status** must reach "Fully aligned" before finalization

---

## **🔹 Step 3: Managing Execution Cycles**  
ZEMY tracks execution refinement across iterations until validation integrity is achieved.

**Example Cycle Tracking Configuration in ZEMY.yaml:**  
```yaml
iteration_tracking:
  cycle_count: 3  # Number of refinement cycles before execution mapping locks.
```

✔ **Each cycle refines execution constraints**, ensuring compliance thresholds hold.  
✔ **Users adjust `cycle_count` if additional validation cycles are needed.**  

---

## **🔹 Step 4: Controlling Execution Readiness**  
When execution mapping stabilizes, ZEMY transitions to agentic codegen.

**Execution Status in ZEMY.yaml:**  
```yaml
execution_finalized: true  # If true, execution mapping is locked—set to false to iterate another cycle.
```

🚀 **What You Need to Do:**  
✔ **If discrepancies exist, set `execution_finalized` to `false`.**  
✔ **Refine execution constraints before restarting validation.**  
✔ **Once validated, set `execution_finalized: true` to transition to codegen.**  

---

## **🔹 Step 5: Running ZEMY Execution**  
Once everything is configured, execution mapping begins with **a single command:**  
```plaintext
"Build it!"
```
💡 **ZEMY automatically processes input artifacts, enforces compliance validation, and locks execution mapping autonomously.**  

---

## **🔹 Step 6: Reviewing the Generated Execution Mapping**  
✔ **The final ZEMY file guarantees structured validation integrity.**  
✔ **If refinement is needed, users adjust the YAML file and iterate another cycle.**  
✔ **Once execution mapping is stable, agentic codegen follows naturally.**  

🚀 **Next Steps:**  
✔ Configure **input sources** (local directory or pasted artifacts).  
✔ Modify **cycle tracking or execution constraints as needed**.  
✔ Run `"Build it!"` to execute ZEMY autonomously.  

With ZEMY v1.1.0, structured execution mapping **eliminates ambiguity**, ensuring **deterministic transformation into agentic codegen.** 🚀  
Are we officially locking this version in for deployment?
```
