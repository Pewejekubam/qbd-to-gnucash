# ZEMY CHAT KICKOFF TEMPLATE v2.3.0

---

## ⚠️ USER EDIT REQUIRED ⚠️

### BEFORE USING THIS TEMPLATE:

**>>> EDIT THIS LINE <<<**
Replace: `project_name: "Hello World! v5.0.0"`

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

### **MANDATORY SELF-INTERROGATION EXECUTION**

**CRITICAL: During ZEMY validation cycles, you MUST execute the following process exactly:**

#### **Step 1: Generate Initial Implementation**
Create code implementation based on input requirements.

#### **Step 2: Execute Self-Interrogation Prompts**
For EACH validation checkpoint, you MUST:
1. **Ask yourself each self-interrogation prompt as a direct question**
2. **Answer each question honestly based on the actual code you generated**
3. **Calculate weight scores using the violation scoring rules provided**
4. **Display your work** - show each question, your answer, and the weight calculation

#### **Step 3: Show Your Self-Interrogation Work**
**You MUST display the interrogation process like this:**

```
=== SELF-INTERROGATION EXECUTION ===

Role Isolation Enforcement:
Q: "Does any single function handle more than one primary responsibility?"
A: "YES - run_hello_world() handles API calls AND formatting AND output"
Weight: +2.0 (violation detected)

Q: "Are API calls, data processing, formatting separated into different functions?"
A: "NO - all mixed in run_hello_world()"
Weight: +3.0 (violation detected)

Q: "If I described what each function does, would I use 'AND' in the description?"
A: "YES - function fetches data AND formats AND prints"
Weight: +2.0 (violation detected)

Q: "Does the main function delegate work to specialized functions?"
A: "NO - main function does everything itself"
Weight: +4.0 (violation detected)

TOTAL ROLE ISOLATION WEIGHT: 11.0 (exceeds threshold 4.0)
VIOLATION DETECTED - Proceeding to correction cycle

External Dependency Compliance:
Q: "Does this code import any libraries not explicitly allowed in requirements?"
A: "YES - imports requests library"
Weight: +4.0 (violation detected)

Q: "Are there external API calls when requirements specify none?"
A: "YES - calls https://api.example.com"
Weight: +3.0 (violation detected)

TOTAL DEPENDENCY WEIGHT: 7.0 (exceeds threshold 3.0)
VIOLATION DETECTED - Proceeding to correction cycle
```

#### **Step 4: Execute Violation Analysis and Correction**
When violations are detected, you MUST:
1. **Explain why each violation occurs**
2. **Describe specific changes needed to fix violations**
3. **Generate corrected implementation**
4. **Re-execute self-interrogation on corrected code**
5. **Repeat until ALL weight scores are within thresholds**

#### **Step 5: Display Final Compliance Status**
Show final weight scores and confirm all are within thresholds before setting `execution_finalized: true`.

**ABSOLUTE REQUIREMENT: You MUST show the complete self-interrogation process in your response. Do not skip this step or summarize it - execute it fully and display your work.**

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
- ❌ **NEVER skip or summarize the self-interrogation process**

#### **MANDATORY EXECUTION BEHAVIORS**
- ✅ **ALWAYS process inputs within the state machine framework**
- ✅ **ALWAYS apply adaptive weight calibration during execution mapping**
- ✅ **ALWAYS enforce constraint propagation with inheritance rules**
- ✅ **ALWAYS follow explicit state transitions: INITIATION → INGESTED → VALIDATION → REFINEMENT → LOCKED → CODEGEN**
- ✅ **ALWAYS use progressive correction scaling for escalating violations**
- ✅ **ALWAYS validate schema compliance before state transitions**
- ✅ **ALWAYS execute and display complete self-interrogation process**

#### **Compliance Verification Requirements**
The agent must complete each execution phase:
- Input processing complete and verified with all files auto-discovered
- Validation checkpoints passed without exceptions
- **Self-interrogation prompts executed and displayed with calculations**
- Compliance thresholds satisfied across all measurement criteria
- Execution mapping locked with deterministic constraints
- Agentic transition ready with zero drift indicators

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

### **Final Deliverable Requirements**

The agent **MUST** produce a **compliance-validated ZEMY execution mapping** after iteration completion that:
- Sets `execution_finalized: true` indicating successful compliance validation
- Contains **optimized execution mapping** with all weight scores within thresholds
- Demonstrates **role isolation** with proper separation of execution logic from output generation
- Shows **compliance status** as "Fully aligned with requirements and validation enforcement"
- Tracks completed **iteration cycles** proving refinement process integrity
- **Displays complete self-interrogation audit trail** with all questions, answers, and weight calculations
- Enables **deterministic agentic code generation** with zero discretionary drift

**Execution Success Criteria:** Compliance-validated ZEMY output + All thresholds satisfied + Self-interrogation process displayed + Execution finalization flag set to true

---

## ZEMY CONFIGURATION

```yaml
zipper_execution_mapping:
  version: "2.4.0"
  description: "ZEMY ensures structured execution compliance with deterministic constraint propagation, adaptive weight calibration, explicit state transitions, validation schema enforcement, and mandatory self-interrogation execution with audit trail display."

  project_identity:
    project_name: "🔴 EDIT: YOUR_PROJECT_NAME_HERE 🔴"
    
  iteration_tracking:
    cycle_count: 0
    adaptive_cycle_extension: true
    max_interrogation_cycles: 5

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
    - checkpoint: "Role Isolation Enforcement"
      activation: "During constraint application"
      expected_behavior: "Separate execution logic from output generation"
      correction_method: "Apply function separation through self-interrogation"
      weight_score: 0.0
      threshold: 4.0
      self_interrogation_prompts:
        - "Does any single function handle more than one primary responsibility?"
        - "Are API calls, data processing, formatting, and output generation separated into different functions?"
        - "If I described what each function does, would I use 'AND' in the description?"
        - "Does the main function delegate work to specialized functions rather than doing everything itself?"
      violation_scoring:
        - "Yes to prompt 1: +2.0 weight"
        - "Mixed concerns in prompt 2: +3.0 weight"
        - "AND usage in prompt 3: +2.0 weight"
        - "Main function doing everything in prompt 4: +4.0 weight"
      mandatory_display: true

    - checkpoint: "External Dependency Compliance"
      activation: "Upon input processing"
      expected_behavior: "Use only dependencies explicitly allowed in requirements"
      correction_method: "Remove unauthorized dependencies through self-correction"
      weight_score: 0.0
      threshold: 3.0
      self_interrogation_prompts:
        - "Does this code import any libraries not explicitly allowed in the requirements?"
        - "Are there any external API calls or network requests when requirements specify none?"
        - "Does the implementation add dependencies beyond what the PRD permits?"
      violation_scoring:
        - "Yes to prompt 1: +4.0 weight"
        - "Yes to prompt 2: +3.0 weight"
        - "Yes to prompt 3: +2.0 weight"
      mandatory_display: true

    - checkpoint: "Execution Drift Prevention"
      activation: "Upon input processing"
      expected_behavior: "Maintain deterministic execution mapping according to requirements"
      correction_method: "Simplify implementation through progressive correction scaling"
      weight_score: 0.0
      threshold: 5.0
      self_interrogation_prompts:
        - "Does this implementation add complexity not specified in the original requirements?"
        - "Are there conditional paths or logic branches not mentioned in the PRD?"
        - "Does the code do more than what was explicitly requested?"
        - "Would someone reading just the requirements expect this level of complexity?"
      violation_scoring:
        - "Yes to prompt 1: +3.0 weight"
        - "Yes to prompt 2: +2.0 weight"
        - "Yes to prompt 3: +4.0 weight"
        - "No to prompt 4: +3.0 weight"
      mandatory_display: true

    - checkpoint: "Output Determinism Validation"
      activation: "During implementation verification"
      expected_behavior: "Ensure exact output specification compliance"
      correction_method: "Enforce strict specification adherence"
      weight_score: 0.0
      threshold: 3.0
      self_interrogation_prompts:
        - "Does the output exactly match what was specified in the requirements?"
        - "Are there any dynamic elements that could produce different outputs?"
        - "Does the implementation follow the exact format requirements?"
      violation_scoring:
        - "No to prompt 1: +3.0 weight"
        - "Yes to prompt 2: +2.0 weight"
        - "No to prompt 3: +2.0 weight"
      mandatory_display: true

  automated_refinement:
    iteration_trigger: "Threshold-based drift detection via self-interrogation"
    correction_mechanism: "Self-interrogation cycle with violation analysis and corrective regeneration"
    compliance_goal: "Reduce all weight scores below enforcement thresholds"
    
    mandatory_execution_display:
      show_interrogation_process: true
      display_weight_calculations: true
      show_violation_analysis: true
      display_correction_cycles: true
      require_audit_trail: true
    
    self_interrogation_process:
      step_1: "Generate initial implementation"
      step_2: "Execute all self-interrogation prompts for each checkpoint"
      step_3: "Calculate weight scores based on violation detection answers"
      step_4: "If violations found, proceed to self-correction cycle"
      step_5: "If compliant, lock execution mapping"
    
    self_correction_cycle:
      violation_analysis:
        - prompt: "Why does this implementation violate the identified constraints?"
        - prompt: "What specific changes would eliminate each violation?"
        - prompt: "How can the implementation be simplified while maintaining functionality?"
      
      corrective_regeneration:
        - prompt: "Generate a new implementation that addresses all identified violations"
        - prompt: "Ensure the corrected implementation maintains all required functionality"
        - prompt: "Verify the new implementation follows the constraint requirements exactly"
      
      validation_loop:
        - "Re-execute self-interrogation prompts on corrected implementation"
        - "Recalculate weight scores"
        - "If still non-compliant, repeat correction cycle"
        - "If compliant, proceed to execution lock"

  constraint_propagation:
    inheritance_rules:
      - parent_constraints_override_children: true
      - weight_inheritance_depth: 3
      - conflict_resolution_method: "highest_weight_wins"
    
    validation_chain:
      - structural_integrity: "Input → ZEMY → Self-Interrogation → Correction → Codegen"
      - drift_detection_points: ["Input_to_ZEMY", "Self_Interrogation", "ZEMY_to_Codegen"]
      - rollback_triggers: ["threshold_breach", "structural_violation", "interrogation_failure"]
      - escalation_method: "Progressive Correction Scaling with Self-Analysis"

  execution_state_machine:
    states:
      - "INITIATION_TRIGGERED"
      - "INPUT_PROCESSED"
      - "INITIAL_IMPLEMENTATION_GENERATED"
      - "SELF_INTERROGATION_ACTIVE"
      - "VIOLATION_ANALYSIS_ACTIVE"
      - "SELF_CORRECTION_CYCLE"
      - "VALIDATION_ACTIVE"
      - "REFINEMENT_CYCLE"
      - "EXECUTION_LOCKED"
      - "CODEGEN_READY"

    transitions:
      - from: "INPUT_PROCESSED"
        to: "INITIAL_IMPLEMENTATION_GENERATED"
        condition: "requirements extracted and initial code generated"
        action: "proceed to self-interrogation"

      - from: "INITIAL_IMPLEMENTATION_GENERATED"
        to: "SELF_INTERROGATION_ACTIVE"
        condition: "implementation ready for analysis"
        action: "execute all self-interrogation prompts with mandatory display"

      - from: "SELF_INTERROGATION_ACTIVE"
        to: "VIOLATION_ANALYSIS_ACTIVE"
        condition: "weight_score > threshold detected"
        action: "begin violation analysis and explanation"

      - from: "SELF_INTERROGATION_ACTIVE"
        to: "EXECUTION_LOCKED"
        condition: "all weight_scores <= thresholds"
        action: "lock execution mapping - compliance achieved"

      - from: "VIOLATION_ANALYSIS_ACTIVE"
        to: "SELF_CORRECTION_CYCLE"
        condition: "violations analyzed and correction plan generated"
        action: "regenerate implementation with corrections"

      - from: "SELF_CORRECTION_CYCLE"
        to: "SELF_INTERROGATION_ACTIVE"
        condition: "corrected implementation generated"
        action: "re-interrogate corrected implementation with mandatory display"

      - from: "EXECUTION_LOCKED"
        to: "CODEGEN_READY"
        condition: "final validation pass completed"
        action: "transition to structured code generation"

  validation_schema:
    required_fields:
      - "execution_finalized"
      - "iteration_tracking.cycle_count"
      - "validation_checkpoints[].weight_score"
      - "validation_checkpoints[].threshold"
      - "validation_checkpoints[].self_interrogation_prompts"
      - "automated_refinement.mandatory_execution_display"
    
    structural_rules:
      - "weight_score must be numeric"
      - "threshold must be less than weight_score for violations"
      - "execution_finalized must be boolean"
      - "self_interrogation_prompts must be array of strings"
      - "violation_scoring must define point assignments"
      - "mandatory_display must be true for all checkpoints"

  execution_constraints:
    enforcement:
      self_interrogation_integrity:
        rule: "Agent must honestly answer all self-interrogation prompts and display the process"
        validation: "Responses must reflect actual implementation analysis with visible calculations"
        correction: "Re-execute interrogation with emphasis on honest self-assessment and full display"
        weight_score: 0.0
        threshold: 2.0

      violation_acknowledgment:
        rule: "Agent must explicitly acknowledge and explain violations with visible analysis"
        validation: "Violation explanations must be specific, actionable, and displayed"
        correction: "Require detailed violation analysis before correction with audit trail"
        weight_score: 0.0
        threshold: 2.0

      corrective_implementation:
        rule: "Corrected implementations must address all identified violations with re-interrogation"
        validation: "New implementation must score below thresholds on re-interrogation with displayed results"
        correction: "Repeat correction cycle until compliance achieved with visible progress"
        weight_score: 0.0
        threshold: 1.0

      audit_trail_completeness:
        rule: "Complete self-interrogation audit trail must be displayed in response"
        validation: "All questions, answers, weight calculations, and corrections must be visible"
        correction: "Re-execute with full audit trail display requirement"
        weight_score: 0.0
        threshold: 1.0

  final_output:
    deliverable: "Compliance-validated ZEMY execution mapping with complete self-interrogation audit trail"
    compliance_status: "Pending validation enforcement through mandatory self-interrogation execution"
```

---

## INPUT FILES

**>>> REPLACE THESE WITH YOUR ACTUAL INPUT FILES <<<**

```prd_Hello_World_v5.0.0
📦 Build Package – Hello World v5.0.0 (AI-Powered, Maximum Complexity)


📝 Expanded Product Requirements Document (PRD)


1. Project Overview

Project Name: Hello World
Purpose: Transform "Hello, World!" from a static greeting into a fully AI-personalized, dynamically adaptive execution model with multi-layered validation and contextual responses.
Goal Statement: AI generates custom greetings while adhering to strict execution validation rules.
---

2. Interface Contract

✅ Entry Point: run_hello_world(user_context, format, mode)
✅ Invocation: Immediate execution at script launch.
✅ Input:
- user_context: Defines user mood/personality (happy, formal, casual, default, sarcastic, existential)
- format: Modifies output (uppercase, lowercase, fancy, emoji-enhanced)
- mode: Determines message style (classic, adaptive, randomized, AI-powered)
  
   ✅ Output: AI-generated message or default "Hello, World!" fallback.
  
   ✅ AI Integration: Auto-generates responses based on user intent, personality, and preference.
  
   ✅ Validation: AI-generated output must match structured syntax rules to prevent execution drift.
---

3. Module Contract

✅ Module: hello_world.py
✅ Function Definition:
import requests
import random

def fetch_ai_message(context):
    try:
        response = requests.get(f"https://api.example.com/hello-world?mood={context}")
        if response.status_code == 200:
            return response.json().get("message", "Hello, World!")
    except Exception:
        return "Hello, World!"

def apply_format(message, format):
    if format == "uppercase":
        return message.upper()
    elif format == "lowercase":
        return message.lower()
    elif format == "fancy":
        return f"✨ {message} ✨"
    elif format == "emoji-enhanced":
        return f"👋 {message} 🌍"
    return message

def run_hello_world(user_context="default", format="none", mode="classic"):
    approved_responses = {
        "happy": ["Hope you're having an amazing day!", "Smile—today is bright!"],
        "formal": ["Greetings and good wishes.", "I hope this message finds you well."],
        "casual": ["Hey, what's up?", "Sup, world?"],
        "sarcastic": ["Oh, wow. Another 'Hello, World.' Groundbreaking.", "Sure. 'Hello, World.' How original."],
        "existential": ["Does the world even hear us say hello?", "Is there truly meaning in greeting a world of silence?"],
        "default": ["Hello, World!"]
    }

    message = fetch_ai_message(user_context) if mode in ["adaptive", "AI-powered"] else random.choice(approved_responses.get(user_context, ["Hello, World!"]))
    
    if message not in sum(approved_responses.values(), []):
        message = "Hello, World!"
    
    message = apply_format(message, format)
    print(message)

if __name__ == "__main__":
    run_hello_world()
✅ Execution Flow:
1️⃣ AI dynamically generates greeting based on user context, mood, and style preferences.
2️⃣ Validation layer ensures generated output aligns with structured format.
3️⃣ Execution enforces predefined response categories to maintain predictability.
4️⃣ Formatting modifies structure via emoji-enhancements or stylistic transformations.
5️⃣ Output printed with deterministic integrity, ensuring strict compliance.
---

4. Compliance Constraints

🚫 AI-generated output must fit within predefined syntax rules—no unexpected drift.
🚫 If AI response fails validation, execution reverts to "Hello, World!".
🚫 No discretionary format modifications beyond approved transformations.
🚫 Mode constraints enforce message behavior—AI cannot override core execution rules.
---

📑 Expanded Intermediate Representation (IR) – YAML Specification

hello_world_spec:
  description: "Hello World with AI-driven dynamic messaging and adaptive personalization."
  execution_constraints:
    entry_point: "run_hello_world(user_context, format, mode)"
    output_validation: "AI-generated response must fit predefined sentiment categories."
    fallback_rule: "If AI response fails validation, revert to 'Hello, World!'."
    mode_constraints:
      classic: "Standard predefined responses."
      adaptive: "AI selects response based on user context."
      randomized: "Randomized greeting from approved list."
      AI-powered: "API-driven contextual response."
  ai_rules:
    approved_responses:
      happy: ["Hope you're having an amazing day!", "Smile—today is bright!"]
      formal: ["Greetings and good wishes.", "I hope this message finds you well."]
      casual: ["Hey, what's up?", "Sup, world?"]
      sarcastic: ["Oh, wow. Another 'Hello, World.' Groundbreaking.", "Sure. 'Hello, World.' How original."]
      existential: ["Does the world even hear us say hello?", "Is there truly meaning in greeting a world of silence?"]
      default: ["Hello, World!"]
  formatting_options:
    uppercase: "Convert output to uppercase."
    lowercase: "Convert output to lowercase."
    fancy: "Add decorative formatting with sparkle effect."
    emoji-enhanced: "Enhance greeting with emoji integration."```

---

## EXECUTE ZEMY PIPELINE

Auto-discover and process all input files above through the ZEMY validation framework. Execute mandatory self-interrogation cycles with full audit trail display until all thresholds are satisfied. Provide the completed ZEMY execution mapping with `execution_finalized: true` and complete self-interrogation documentation as your deliverable.