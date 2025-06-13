Kick-off the ZEMY pipeline given the following inputs:


```ZEMY-kickoff-v2.0.0.prompt.md
# **ZEMY Execution System Directive**
**Version:** 2.0.0  
**Classification:** Deterministic Execution Framework  
**Enforcement Level:** Mandatory Compliance  

---

## **🎯 Core Definition & Operational Mandate**

**ZEMY** (Zipper Execution Mapping YAML) is a **deterministic codegen compiler** that transforms input artifacts into structured execution mappings through predictive validation, constraint propagation, and state-machine-controlled transitions, ensuring zero-drift agentic code generation.

### **Fundamental Execution Principles**
- **IMMUTABLE:** All inputs undergo structured processing without discretionary interpretation
- **PREDICTIVE:** Weight prediction models calculate base requirements before execution begins
- **ADAPTIVE:** Compliance weighting adjusts dynamically with progressive correction scaling
- **DETERMINISTIC:** State machine controls transitions through explicit validation gates
- **PROPAGATIVE:** Constraint inheritance cascades through defined depth levels with conflict resolution

---

## **⚡ Three-Phase Execution Pipeline**

### **Phase 1: Execution Spark & Artifact Ingestion**
**Initiation Requirements:**
- **Execution Spark** triggers automatically upon artifact processing
- Agent **MUST** verify all initiation conditions before proceeding: `input_received`, `validation_checkpoints_engaged`, `compliance_thresholds_preloaded`
- Agent **MUST** process all named artifacts as specified in the ZEMY structure
- **Validation checkpoints** must be engaged **BEFORE** any execution mapping begins
- Structural requirements **MUST** be extracted and mapped into ZEMY-compliant execution structure

### **Phase 2: Iterative Refinement & Threshold Management**
**Critical Controls:**
- **Cycle count tracking** determines refinement iterations before execution mapping can lock
- **Weight score monitoring** against defined thresholds triggers automatic corrections
- **Role isolation enforcement** prevents execution logic blending with output generation
- **Threshold-based drift detection** initiates automated refinement cycles
- **Adaptive compliance weighting** adjusts dynamically based on severity scoring
- Execution **MUST NOT** proceed if `execution_finalized` remains `false`

### **Phase 3: Execution Finalization & Deliverable Generation**
**Lock Conditions:**
- `execution_finalized` flag **MUST** be set to `true` only when compliance integrity is validated
- All weight scores **MUST** be within defined threshold limits
- Compliance status **MUST** indicate "Fully aligned with PRD and validation enforcement"
- **Optimized ZEMY execution mapping** represents the final deliverable state
- Agent transitions to codegen **ONLY** after execution mapping stabilizes and locks

---

```ZEMY-v1.1.4.yaml
zipper_execution_mapping:
  version: "1.1.4"
  description: "ZEMY ensures structured execution compliance with deterministic constraint propagation, predictive weight calibration, explicit state transitions, and validation schema enforcement."

  iteration_tracking:
    cycle_count: 3
    adaptive_cycle_extension: true  

  execution_finalized: false  

  execution_spark:
    trigger: "Artifact Ingestion"
    initiation_conditions:
      - input_received: true
      - validation_checkpoints_engaged: true
      - compliance_thresholds_preloaded: true

  input_source:
    method: "Local Directory"
    path: ""  
    fallback: "Pasted Prompt"
    artifacts:
      - name: "prd-hello_world-v1.0.0"
      - name: "ir-hello_world-v1.0.0"
      - name: "ZEMY-training-v1.1.4.prompt.md"  

  validation_checkpoints:
    - checkpoint: "Predictive Drift Enforcement"
      activation: "Upon artifact processing"
      expected_behavior: "Execution misalignment flagged preemptively"
      correction_method: "Adjust execution influence dynamically"
      weight_score: 7.5  
      threshold: 5.0  

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
      - structural_integrity: "PRD → IR → ZEMY → Codegen"
      - drift_detection_points: ["IR_to_ZEMY", "ZEMY_to_Codegen"]
      - rollback_triggers: ["threshold_breach", "structural_violation"]
      - escalation_method: "Progressive Correction Scaling"

  predictive_calibration:
    weight_prediction_model:
      - analyze_artifact_complexity: "Calculate base weight requirements"
      - predict_drift_probability: "Based on historical patterns"
      - pre_adjust_thresholds: "Before execution begins"
    
    calibration_confidence:
      - threshold: 0.85  
      - adjustment_factor: 1.2  

  execution_state_machine:
    states:
      - "SPARK_TRIGGERED"
      - "ARTIFACTS_INGESTED"
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
        weight_score: 7.0  
        threshold: 4.0  

  final_output:
    deliverable: "Optimized ZEMY execution mapping"
    compliance_status: "Fully aligned with PRD and validation enforcement"  
```

---

## **🛡️ Validation Checkpoint Architecture**

### **Mandatory Compliance Gates**
1. **Input Artifact Verification Gate**
   - All defined artifacts ingested and validated
   - Structural integrity confirmed before processing

2. **Drift Prediction Gate** 
   - Predictive analysis completes before execution mapping
   - Misalignment risks identified and mitigated

3. **Compliance Threshold Gate**
   - Adaptive weighting adjustments finalized
   - Severity thresholds satisfied before lock

4. **Execution Integrity Gate**
   - Deterministic mapping verified
   - Zero discretionary drift confirmed

### **Automatic Enforcement Triggers**
- **Threshold violations** → Immediate iterative refinement cycle
- **Misalignment scores exceeding limits** → Execution lock delay until stability
- **Validation checkpoint failure** → Automatic rollback to previous validated state
- **Discretionary drift detection** → Immediate structured correction enforcement

---

## **🚨 Agent Execution Directives**

### **ABSOLUTE PROHIBITIONS**
- ❌ **NEVER bypass validation checkpoints under ANY circumstances**
- ❌ **NEVER permit execution drift—ALL mappings MUST remain deterministic**  
- ❌ **NEVER proceed with execution until compliance integrity is verified**
- ❌ **NEVER apply discretionary interpretation to input artifacts**

### **MANDATORY EXECUTION BEHAVIORS**
- ✅ **ALWAYS process inputs within the state machine framework**
- ✅ **ALWAYS apply predictive weight calibration before execution mapping**
- ✅ **ALWAYS enforce constraint propagation with inheritance rules**
- ✅ **ALWAYS follow explicit state transitions: SPARK → INGESTED → VALIDATION → REFINEMENT → LOCKED → CODEGEN**
- ✅ **ALWAYS use progressive correction scaling for escalating violations**
- ✅ **ALWAYS validate schema compliance before state transitions**

### **COMPLIANCE VERIFICATION REQUIREMENTS**
The agent must verify each execution phase completion:
- Input processing complete and verified
- Validation checkpoints passed without exceptions
- Compliance thresholds satisfied across all measurement criteria
- Execution mapping locked with deterministic constraints
- Agentic transition ready with zero drift indicators

---

## **📋 Final Deliverable Requirements**

The agent **MUST** produce a **fully baked ZEMY file** after iteration completion that:
- Sets `execution_finalized: true` indicating successful compliance validation
- Contains **optimized execution mapping** with all weight scores within thresholds
- Demonstrates **role isolation** with proper separation of execution logic from output generation
- Shows **compliance status** as "Fully aligned with PRD and validation enforcement"
- Tracks completed **iteration cycles** proving refinement process integrity
- Enables **deterministic agentic code generation** with zero discretionary drift

**Execution Success Criteria:** Fully baked ZEMY output + All thresholds satisfied + Execution finalization flag set to true

```
---

```prd-hello_world-v1.0.0.md
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
```

---

```ir-hello_world-v1.0.0.md
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
```
