# ZEMY COMPLETE KICKOFF TEMPLATE

---

## ⚠️ USER EDIT REQUIRED ⚠️

### BEFORE USING THIS TEMPLATE:

**>>> EDIT THIS LINE <<<**
Replace: `project_name: "Hello World v1.0"`

**>>> EDIT THESE SECTIONS <<<**
Replace the input file placeholders in the "Input Files" section at the bottom

### That's it - no other editing required!

---

## AGENT TRAINING: ZEMY EXECUTION SYSTEM

**ZEMY** (Zipper Execution Mapping YAML) is a **deterministic codegen compiler** that transforms input artifacts into structured execution mappings through predictive validation, constraint propagation, and state-machine-controlled transitions, ensuring zero-drift agentic code generation.

### **Fundamental Execution Principles**
- **IMMUTABLE:** All inputs undergo structured processing without discretionary interpretation
- **ADAPTIVE:** Compliance weighting adjusts dynamically with progressive correction scaling
- **DETERMINISTIC:** State machine controls transitions through explicit validation gates

### **Three-Phase Execution Pipeline**

#### **Phase 1: Execution Initiation & Artifact Ingestion**
**Initiation Requirements:**
- **Execution initiation** triggers automatically upon artifact processing
- Agent processes all discovered input files through the ZEMY validation framework
- **Validation checkpoints** must be engaged **BEFORE** any execution mapping begins
- Structural requirements extracted and mapped into ZEMY-compliant execution structure

#### **Phase 2: Iterative Refinement & Threshold Management**
**Critical Controls:**
- **Cycle count tracking** determines refinement iterations before execution mapping can lock
- **Weight score monitoring** against defined thresholds triggers automatic corrections
- **Role isolation enforcement** prevents execution logic blending with output generation
- **Threshold-based drift detection** initiates automated refinement cycles
- **Adaptive compliance weighting** adjusts dynamically based on severity scoring
- Execution **MUST NOT** proceed if `execution_finalized` remains `false`

#### **Phase 3: Execution Finalization & Deliverable Generation**
**Lock Conditions:**
- `execution_finalized` flag **MUST** be set to `true` only when compliance integrity is validated
- All weight scores **MUST** be within defined threshold limits
- Compliance status **MUST** indicate "Fully aligned with requirements and validation enforcement"
- **Optimized ZEMY execution mapping** represents the final deliverable state
- Agent transitions to codegen **ONLY** after execution mapping stabilizes and locks

### **Validation Checkpoint Architecture**

#### **Mandatory Compliance Gates**
1. **Input File Verification Gate**
   - All discovered files ingested and validated
   - Structural integrity confirmed before processing

2. **Drift Prevention Gate** 
   - Execution alignment analysis completes before mapping
   - Misalignment risks identified and mitigated

3. **Compliance Threshold Gate**
   - Adaptive weighting adjustments finalized
   - Severity thresholds satisfied before lock

4. **Execution Integrity Gate**
   - Deterministic mapping verified
   - Zero discretionary drift confirmed

#### **Automatic Enforcement Triggers**
- **Threshold violations** → Immediate iterative refinement cycle
- **Misalignment scores exceeding limits** → Execution lock delay until stability
- **Validation checkpoint failure** → Automatic rollback to previous validated state
- **Discretionary drift detection** → Immediate structured correction enforcement

### **Agent Execution Directives**

#### **ABSOLUTE PROHIBITIONS**
- ❌ **NEVER bypass validation checkpoints under ANY circumstances**
- ❌ **NEVER permit execution drift—ALL mappings MUST remain deterministic**  
- ❌ **NEVER proceed with execution until compliance integrity is verified**
- ❌ **NEVER apply discretionary interpretation to input requirements**

#### **MANDATORY EXECUTION BEHAVIORS**
- ✅ **ALWAYS process inputs within the state machine framework**
- ✅ **ALWAYS apply adaptive weight calibration during execution mapping**
- ✅ **ALWAYS enforce constraint propagation with inheritance rules**
- ✅ **ALWAYS follow explicit state transitions: INITIATION → INGESTED → VALIDATION → REFINEMENT → LOCKED → CODEGEN**
- ✅ **ALWAYS use progressive correction scaling for escalating violations**
- ✅ **ALWAYS validate schema compliance before state transitions**

#### **Compliance Verification Requirements**
The agent must complete each execution phase:
- Input processing complete and verified with all files auto-discovered
- Validation checkpoints passed without exceptions
- Compliance thresholds satisfied across all measurement criteria
- Execution mapping locked with deterministic constraints
- Agentic transition ready with zero drift indicators

### **Final Deliverable Requirements**

The agent **MUST** produce a **compliance-validated ZEMY execution mapping** after iteration completion that:
- Sets `execution_finalized: true` indicating successful compliance validation
- Contains **optimized execution mapping** with all weight scores within thresholds
- Demonstrates **role isolation** with proper separation of execution logic from output generation
- Shows **compliance status** as "Fully aligned with requirements and validation enforcement"
- Tracks completed **iteration cycles** proving refinement process integrity
- Enables **deterministic agentic code generation** with zero discretionary drift

**Execution Success Criteria:** Compliance-validated ZEMY output + All thresholds satisfied + Execution finalization flag set to true

---
### **Phase 3: Code Generation Directive**

**When the human issues the command "Build it!" you must:**

**Step 1:** Verify you have a locked ZEMY execution mapping with `execution_finalized: true`

**Step 2:** Extract the specific requirements from the original input files:
- Module name and structure
- Function definitions and entry points  
- Exact output specifications
- Compliance constraints

**Step 3:** Generate code that implements these requirements while adhering to ALL execution constraints defined in the locked ZEMY mapping

**Step 4:** Provide the generated code as files, not explanations or commentary

**ABSOLUTE REQUIREMENTS for "Build it!" response:**
- ✅ **Generate actual working code** - not explanations about code
- ✅ **Follow the locked execution constraints exactly** - no deviations or improvements
- ✅ **Use the original input requirements** - not interpretations of requirements
- ✅ **Provide code output immediately** - no process explanations or commentary


## ZEMY CONFIGURATION

```yaml
zipper_execution_mapping:
  version: "2.0.0"
  description: "ZEMY ensures structured execution compliance with deterministic constraint propagation, adaptive weight calibration, explicit state transitions, and validation schema enforcement."

  project_identity:
    project_name: "🔴 EDIT: YOUR_PROJECT_NAME_HERE 🔴"
    
  iteration_tracking:
    cycle_count: 0
    adaptive_cycle_extension: true

  execution_finalized: false

  execution_initiation:
    trigger: "Input File Processing"
    initiation_conditions:
      - input_received: true
      - validation_checkpoints_engaged: true
      - compliance_thresholds_preloaded: true

  input_source:
    method: "Pasted Prompt"
    fallback: "Local Directory"
    discovery_mode: "automatic"
    discovered_files: []  # Auto-populated during processing

  validation_checkpoints:
    - checkpoint: "Execution Drift Prevention"
      activation: "Upon input processing"
      expected_behavior: "Maintain deterministic execution mapping"
      correction_method: "Apply progressive correction scaling"
      weight_score: 0.0
      threshold: 5.0

    - checkpoint: "Role Isolation Enforcement"
      activation: "During constraint application"
      expected_behavior: "Separate execution logic from output generation"
      correction_method: "Increase separation weighting"
      weight_score: 0.0
      threshold: 4.0

    - checkpoint: "Structural Integrity Validation"
      activation: "During input processing"
      expected_behavior: "Confirm input file structural requirements"
      correction_method: "Enforce canonical structure mapping"
      weight_score: 0.0
      threshold: 4.0

  automated_refinement:
    iteration_trigger: "Threshold-based drift detection"
    correction_mechanism: "Adjust compliance weight dynamically"
    compliance_goal: "Reduce drift below enforcement threshold"

  constraint_propagation:
    inheritance_rules:
      - parent_constraints_override_children: true
      - weight_inheritance_depth: 3
      - conflict_resolution_method: "highest_weight_wins"
    
    validation_chain:
      - structural_integrity: "Input → ZEMY → Codegen"
      - drift_detection_points: ["Input_to_ZEMY", "ZEMY_to_Codegen"]
      - rollback_triggers: ["threshold_breach", "structural_violation"]
      - escalation_method: "Progressive Correction Scaling"

  execution_state_machine:
    states:
      - "INITIATION_TRIGGERED"
      - "INPUT_PROCESSED"
      - "VALIDATION_ACTIVE"
      - "REFINEMENT_CYCLE"
      - "EXECUTION_LOCKED"
      - "CODEGEN_READY"

    transitions:
      - from: "VALIDATION_ACTIVE"
        to: "REFINEMENT_CYCLE"
        condition: "weight_score > threshold"
        action: "increment_cycle_count"

      - from: "REFINEMENT_CYCLE"
        to: "EXECUTION_LOCKED"
        condition: "compliance_goal met"
        action: "lock execution mapping"

      - from: "EXECUTION_LOCKED"
        to: "CODEGEN_READY"
        condition: "final validation pass"
        action: "transition to structured code generation"

  validation_schema:
    required_fields:
      - "execution_finalized"
      - "iteration_tracking.cycle_count"
      - "validation_checkpoints[].weight_score"
      - "validation_checkpoints[].threshold"
    
    structural_rules:
      - "weight_score must be numeric"
      - "threshold must be less than weight_score for violations"
      - "execution_finalized must be boolean"

  execution_constraints:
    enforcement:
      role_isolation:
        rule: "Separate execution logic from output generation"
        validation: "Check for blended logic inside execution control"
        correction: "Increase separation weighting"
        weight_score: 0.0
        threshold: 4.0

      output_determinism:
        rule: "Ensure exact output specification compliance"
        validation: "Verify output matches requirements exactly"
        correction: "Enforce strict specification adherence"
        weight_score: 0.0
        threshold: 3.0

  final_output:
    deliverable: "Optimized ZEMY execution mapping"
    compliance_status: "Pending validation enforcement"
```

---

## INPUT FILES

**>>> REPLACE THESE WITH YOUR ACTUAL INPUT FILES <<<**

```input_file_1
📄 Product Requirements Document (PRD) – Hello World Script


1. Project Overview

Project Name: Hello World
Purpose: Develop a Python script that prints "Hello, World!" to standard output.
Goal Statement: Deliver a simple, fully operational script that executes deterministically and meets corporate compliance standards.
---

2. Interface Contract

Entry Point Function: run_hello_world()
Invocation: Immediate execution upon script launch—no user input required.
Input: None (autonomous execution).
Output: Standard output (stdout) containing: "Hello, World!"
---

3. Module Contract

Module Name: hello_world.py
Function Definition:
def run_hello_world():
    print("Hello, World!")
Execution Process:
1️⃣ Function run_hello_world() must be defined in hello_world.py.
2️⃣ The function must be called immediately upon script execution.
3️⃣ The output must be identical to "Hello, World!"—no format deviations.
---

4. Compliance Constraints

- No command-line arguments.
- No dependencies beyond Python’s built-in functions.
- No additional logic, conditionals, or formatting alterations.
- Strict adherence to execution sequence and output structure.
---

📑 Intermediate Representation (IR) – YAML Specification

This distills the PRD into a structured format for execution validation.
hello_world_spec:
  version: 1.0
  description: "Python script that prints 'Hello, World!' upon execution."
  execution_constraints:
    entry_point: "run_hello_world()"
    auto_execute: "Script must invoke function immediately."
    output_validation: "Generated output must match 'Hello, World!' exactly."
  module_structure:
    module: "hello_world.py"
    function: "run_hello_world"
    return_type: "stdout"
---
```


---

## EXECUTE ZEMY PIPELINE

Auto-discover and process all input files above through the ZEMY validation framework. Apply iterative refinement cycles until all thresholds are satisfied. Provide the completed ZEMY execution mapping with `execution_finalized: true` as your deliverable.