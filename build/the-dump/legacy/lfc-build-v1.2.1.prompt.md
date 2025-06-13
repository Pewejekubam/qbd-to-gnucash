### **Prompt for Local Agent: Logical Flow Canonicalizer (LFC)**
### Version: 1.2.1 (Enhanced Mermaid Integration)
#### 1. **Compliance References**
- **Core PRD Document:** `core-prd-main-v3.6.5.md`
- **Governance Document:** `prd-governance-model-v2.3.10.md`
- **Logging Framework Module PRD:** `module-prd-logging-v1.0.4.md`

---

#### 2. **Objective**
You are tasked with constructing a **Logical Flow Canonicalizer (LFC)** that formalizes execution order, dependencies, interfaces, state transitions, and modular orchestration, ensuring deterministic code generation and eliminating ambiguity in system flow.

**Key Terms:**
- **LFC** = Logical Flow Canonicalizer (this system)
- **LFD** = Logical Flow Diagram (output artifact)
- **IR** = Intermediate Representation (schema layer)

Your directives are **strict**:  
✅ **DO enforce compliance with PRDs and governance mandates**  
✅ **DO ensure logging is fully integrated as a structured execution component**  
✅ **Place all generated files directly into the `result-files` directory**—**no output should be presented exclusively in chat**  
✅ **Modify files inline** within their designated locations—**no external drafts or temporary deliverables**  
🚫 **DO NOT infer execution order beyond authoritative source definitions**  
🚫 **DO NOT alter module relationships beyond structured dependencies**  

---

#### 3. **Source Authority Hierarchy**
**All system logic, execution ordering, interface contracts, validation mechanisms, and dispatch structures must be derived from these authoritative sources in order of precedence:**

**3.1 Primary Sources (Highest Authority)**
- **PRDs** (`./prd/core-prd-main-v3.6.5.md`, `./prd/module-prd-logging-v1.0.4.md`, etc.) → Define operational compliance, validation rules, interface contracts

**3.2 Secondary Sources (Implementation Guidance)**  
- **Meta-Files** (`./build/logical_flow_canonicalizer/meta-files/`) → Define structured execution mappings, interdependencies, orchestration sequences
- **IR Schema** (`./build/logical_flow_canonicalizer/schema/`) → QBD-to-GnuCash Intermediate Representation Schema files

**3.3 Resolution Protocol**
When conflicts arise between sources:
1. **PRD supersedes all other sources**
2. **Meta-files supersede IR Schema**  
3. **If gap exists between PRD and implementation sources → HALT execution and generate halt report**

The agent **is prohibited from making assumptions** outside of formal definitions. If a logical gap exists, **execution halts** until the discrepancy is explicitly resolved.

---

#### 4. **Pre-Execution Compliance Verification**
Before proceeding, you **must**:

**4.1 Scan Required Documents**
- `core-prd-main-v3.6.5.md` (Core PRD rules & constraints)
- `prd-governance-model-v2.3.10.md` (Governance policies)  
- `module-prd-logging-v1.0.4.md` (Logging facility structure)

**4.2 Generate Compliance Declaration**
Create `result-files/lfc_compliance_declaration.md` containing:
- Verification timestamp
- Document versions accessed
- Compliance gaps identified (if any)
- Authorization to proceed (or halt directive)

**Proceed only after successful compliance verification.**

---

#### 5. **Key Deliverables**

##### 5.1 **Master Module Table (`result-files/master_module_table.md`)**  
**Purpose:** Comprehensive registry of all system modules with dependencies and validation status

**Requirements:**
- Derive from **IR Schema** in `./build/logical_flow_canonicalizer/schema/`
- Cross-validate against **PRD specifications**
- Map each module to its Jinja template (e.g., `class.py.jinja`, `module.py.jinja`, `function.py.jinja`, `interface_impl.py.jinja`).
- Include columns: Module Name, Dependencies, Entry Points, I/O Contracts, Validation Status, PRD Reference, Codegen Template
- Flag any schema entries lacking PRD validation
- Use [glossary linking](glossary.md#master-module-table) for technical terms

**Example Structure:**
````markdown
# Master Module Table

| Module Name | Dependencies | Entry Points | I/O Contracts | Validation Status | PRD Reference | Codegen Template     |
|-------------|--------------|--------------|---------------|-------------------|---------------|----------------------|
| ...         | ...          | ...          | ...           | ...               | ...           | module.py.jinja      |
````

##### 5.2 **Logical Flow Diagram (`result-files/lfd.md`)**  
**Purpose:** Comprehensive visual representation of system execution flow, dependencies, and all data transformations

**Requirements:**

**Node Coverage Mandates:**
- **Appropriate Representation of Nodes:** All schema-defined entities must be **represented appropriately**—their structure should reflect the nature of the data rather than force a one-to-one mapping to predefined Reference Diagram Formats.
- **Implicit dependencies must be explicit:** If a module uses logging, error handling, configuration, or any utility service, these must appear as dedicated nodes with edges showing the dependency relationship
- **State transition nodes:** Include nodes for different states of data processing (e.g., "Raw QBD Data", "Validated QBD Data", "Transformed Data", "GnuCash Output")
- **Error and exception paths:** Include nodes for error states, validation failures, and exception handling flows
- **Configuration and runtime nodes:** Include nodes for configuration loading, environment setup, and runtime initialization
- **External system interfaces:** Include nodes for any external system touchpoints (file system, databases, APIs, etc.)

**Recommended Edge Guidelines (Adaptive Reference Format):**
- **Data Flow Edges:** Solid arrows `-->` (e.g., `A --> B`) indicate data movement between modules.
- **Control Flow Edges:** Thick arrows `==>` (e.g., `A ==> B`) define execution order, orchestration, and process transitions.
- **Dependency Edges:** Dashed arrows `-.->` (e.g., `A -.-> B`) represent logical dependencies, imports, and required services.
- **Error/Exception Edges:** Dotted arrows `..>` (e.g., `A ..> B`) show error propagation, exception handling, and failure states.
- **Configuration Edges:** Dash-dot arrows `-.-` (e.g., `A -.- B`) are for configuration loading, parameter passing, and setup dependencies.
- **Validation Edges:** Double arrows `<-->` (e.g., `A <--> B`) define bidirectional validation, feedback loops, and confirmation flows.
- **Conditional Edges:** Labels on edges using `-->|condition|` or `==>|condition|` (e.g., `A --|on success|--> B`) indicate flow triggers.
- **Text on Edges:** Edge labels should be applied **only where Mermaid syntax supports them**. If an edge type does **not** allow labels, use separate annotations or descriptive nodes instead.

**Guidance for Syntax Compliance:**
- Labels should be applied **only to edge types that allow them in Mermaid.js**.
- Where labels are unsupported, add **descriptive comments** or **reference nodes** to maintain clarity.
- Before finalizing diagrams, verify edge syntax validity to avoid enforcement errors.

**Guidance for Adaptive Structure:**
- These edge definitions serve as **recommendations** to align visualization with schema logic.
- **Use these as a reference**—not strict templates—to ensure diagrams reflect actual relationships.
- **Adjust formatting dynamically** based on structural requirements, avoiding rigid replication.

// Reference: https://mermaid.js.org/syntax/flowchart.html

**Edge Labels (Required):**
- All edges must include descriptive labels explaining what flows through them
- Data edges: specify data type/structure (e.g., `-->|QBD Account List|`)
- Control edges: specify trigger condition (e.g., `==>|after validation|`)
- Dependency edges: specify service type (e.g., `-.->|logging service|`)

**Source Reference Comments:**
- For every node and edge, include a Mermaid comment (`%%`) referencing the authoritative source (PRD, meta-file, or schema) that defines or requires it. Example:
  - `%% Source: schema/module-ir-accounts-v1.1.3.md`
  - `%% Source: prd/module-prd-logging-v1.0.4.md`
- For complex or composite nodes, include all relevant sources.
- Place these comments immediately before the relevant Mermaid line for traceability and auditing.

**Syntax Validation and Automated Correction:**
- All Mermaid diagrams must be validated for syntax correctness using a Mermaid parser before being written to result files.
- If an invalid edge type or node connector is detected, automatically correct it to the closest valid Mermaid syntax and log the correction in the diagram quality report.
- Any syntax errors or corrections must be documented in the diagram quality validation report.

**Required Diagram Hierarchy:**
1. **System Overview Diagram (`graph TD`):** High-level flow showing major phases and key decision points
2. **Detailed Execution Flow (`graph TD`):** Complete step-by-step execution with all data flows and decision branches
3. **Module Dependency Graph (`graph LR`):** All static dependencies between modules, utilities, and artifacts
4. **Data Flow Diagram (`graph TD`):** Focused on data transformation pipeline from input to output
5. **Error Flow Diagram (`graph TD`):** Error propagation, exception handling, and recovery paths
6. **Configuration Flow Diagram (`graph LR`):** Configuration loading and parameter distribution

**Cross-Diagram Consistency:**
- Nodes appearing in multiple diagrams must use identical names and styling
- All relationships shown in one diagram must be consistent with others
- No diagram should contradict information in another diagram

**Advanced Mermaid Requirements:**
- **Subgraphs:** Group related modules into logical subsystems (e.g., `subgraph "QBD Processing"`)
- **Node Styling:** Use different shapes for different node types:
  - `[Module Name]` for processing modules
  - `(Configuration)` for config nodes  
  - `{Result File}` for output artifacts
  - `[[Utility Service]]` for shared services
  - `((Decision Point))` for branching logic
- **Conditional Styling:** Use different colors/styles for different phases or error states
- **Click Events:** Include click handlers for nodes to reference documentation (e.g., `click ModuleName "schema.md#module-name"`)

**Mandatory Content Coverage:**
- **All PRD-defined interfaces:** Every interface contract mentioned in PRDs must appear as edges
- **All meta-file orchestration:** Every orchestration sequence in meta-files must be visualized
- **All template relationships:** Every Jinja template and its target modules must be connected
- **All validation points:** Every validation step mentioned in schemas must appear as nodes/edges
- **All error conditions:** Every error condition defined in PRDs must have corresponding error flow paths
- **All configuration dependencies:** Every configuration parameter usage must be shown as dependency edges
- **All result artifacts:** Every output file, log entry, or data structure must be represented as nodes

**Diagram Completeness Validation:**
- **Schema Contract Verification:** For every input/output declared in IR Schema, verify corresponding edges exist in diagrams
- **Orphan Detection:** Identify any nodes with no incoming or outgoing edges (unless they are true entry/exit points)
- **Dead End Analysis:** Flag any nodes that receive data but produce no output (unless they are true sinks like log files)
- **Circular Dependency Detection:** Identify and document any circular dependencies in the dependency graph
- **Interface Gap Detection:** Verify that every module interface contract has corresponding edges showing data flow
- **Template Coverage Verification:** Ensure every Jinja template referenced in meta-files has corresponding nodes in the diagrams

**Validation Against Dependencies:**
- **Every module's declared dependencies and I/O contracts in the Master Module Table and IR schema must be reflected as edges in the Mermaid dependency graph.**
- After diagram generation, cross-check all dependencies and I/O contracts listed in the Master Module Table and IR schema against the edges in the Mermaid dependency graph. **Flag or halt if any declared dependency or contract is missing.**

- Include legend explaining node types and edge meanings, clarifying that some nodes (like Error Handler and Logging) are global utilities with multiple inbound edges. The legend must also explain edge styles/labels.
- Validate against [topological ordering](glossary.md#topological-sort) requirements

# Reference Diagram Formats for LFD Generation

## Design Philosophy
These Reference Diagram Formats serve as **adaptive guidance** rather than rigid templates. They illustrate structural patterns and relationships that should be dynamically adjusted based on schema-defined requirements and system characteristics.

## Core Principles
- **Schema-Driven Adaptation**: Diagram structures should reflect actual schema relationships, not force predefined layouts
- **Placeholder-Based Flexibility**: Use placeholders for optional components that only appear when mandated by schema
- **Contextual Optimization**: Encourage diagrams that optimize for the specific system being modeled
- **Compliance Preservation**: Maintain strict alignment with PRDs and schema governance while allowing rendering flexibility

## Adaptive Reference Formats

### 1. System Overview Pattern
```mermaid
graph TD
    subgraph "Input Processing"
        {PrimaryInput} --> {InputDiscovery}
        {ConfigurationSource} --> {InputDiscovery}
        {InputDiscovery} --> {SectionProcessing}
    end
    
    subgraph "Core Processing"
        {SectionProcessing} ==> {DispatchFlow}
        {DispatchFlow} ==> {PrimaryParser}
        {PrimaryParser} -->|{DataType}| {DispatchFlow}
        {DispatchFlow} ==> {BusinessLogicModules}
    end
    
    subgraph "Output Generation"
        {BusinessLogicModules} --> {OutputMapping}
        {OutputMapping} --> {OutputStructure}
        {OutputStructure} --> {OutputExport}
        {OutputExport} --> {ResultArtifacts}
    end
    
    subgraph "Utilities"
        {OptionalErrorHandler}
        {OptionalLoggingService}
        {OptionalUtilityServices}
    end
    
    %% Conditional Dependencies
    {ConditionalErrorEdges}
    {ConditionalLoggingEdges}
    {ConditionalUtilityEdges}
    
    %% Schema-Driven Flows
    {SchemaDefinedErrorFlows}
    {SchemaDefinedCompletionSignals}
```

**Placeholder Definitions:**
- `{PrimaryInput}`: Replace with actual input source from schema
- `{ConfigurationSource}`: Only include if configuration is schema-defined
- `{BusinessLogicModules}`: Expand to actual processing modules per schema
- `{OptionalErrorHandler}`: Include only if error handling is schema-mandated
- `{OptionalLoggingService}`: Include only if logging is schema-required
- `{ConditionalErrorEdges}`: Add error flows only where schema defines error conditions
- `{ResultArtifacts}`: Replace with actual output artifacts from schema

### 2. Execution Flow Pattern
```mermaid
graph TD
    {EntryPoint} ==> {InitializationSequence}
    {InitializationSequence} ==> {ValidationGate}
    
    {ValidationGate} -->|valid| {ProcessingPipeline}
    {ValidationGate} {ErrorHandling} {OptionalErrorHandler}
    
    {ProcessingPipeline} --> {BusinessLogicDecisions}
    {BusinessLogicDecisions} --> {ConditionalProcessing}
    
    {ConditionalProcessing} --> {OutputGeneration}
    {OutputGeneration} --> {CompletionSignal}
    
    %% Dynamic Error Flows
    {SchemaDefinedErrorNodes}
    {SchemaDefinedRecoveryPaths}
    
    %% Utility Integration
    {ConditionalUtilityIntegration}
```

**Adaptive Guidelines:**
- `{InitializationSequence}`: Expand based on schema-defined startup requirements
- `{ProcessingPipeline}`: Structure according to actual processing stages in schema
- `{BusinessLogicDecisions}`: Include only decision points that exist in schema logic
- `{SchemaDefinedErrorNodes}`: Generate error nodes only for schema-defined error conditions
- `{ConditionalUtilityIntegration}`: Add utility connections only where schema mandates them

### 3. Dependency Graph Pattern
```mermaid
graph LR
    subgraph "Foundation Layer"
        {RequiredFoundationModules}
        {OptionalFoundationModules}
    end
    
    subgraph "Processing Layer"
        {CoreProcessingModules}
        {OptionalProcessingModules}
    end
    
    subgraph "Integration Layer"
        {OutputModules}
        {OptionalIntegrationModules}
    end
    
    subgraph "Artifacts"
        {MandatoryArtifacts}
        {OptionalArtifacts}
    end
    
    %% Schema-Driven Dependencies
    {SchemaDependencyEdges}
    {ConditionalDependencyEdges}
```

**Dynamic Expansion Rules:**
- `{RequiredFoundationModules}`: Include only modules explicitly required by schema
- `{OptionalFoundationModules}`: Include only if schema references optional foundation services
- `{MandatoryArtifacts}`: Include only artifacts explicitly defined in schema outputs
- `{OptionalArtifacts}`: Include only if schema defines conditional outputs (e.g., logs only if logging enabled)
- `{SchemaDependencyEdges}`: Generate edges only for dependencies declared in schema
- `{ConditionalDependencyEdges}`: Add dependency edges only where schema defines conditional relationships

### 4. Data Flow Pattern
```mermaid
graph TD
    {PrimaryDataSource} --> {InitialDataState}
    {ConfigurationData} --> {InitialDataState}
    
    {InitialDataState} --> {ValidationLayer}
    {ValidationLayer} --> {ProcessedDataStates}
    
    {ProcessedDataStates} --> {TransformationLayer}
    {TransformationLayer} --> {OutputDataStates}
    {OutputDataStates} --> {FinalArtifacts}
    
    %% Conditional Audit Flows
    {ConditionalAuditFlows}
    {ConditionalLoggingFlows}
```

**Schema-Driven Adaptations:**
- `{ProcessedDataStates}`: Generate states based on actual data transformations in schema
- `{TransformationLayer}`: Include only transformations explicitly defined in schema
- `{ConditionalAuditFlows}`: Add audit flows only if schema defines audit requirements
- `{ConditionalLoggingFlows}`: Add logging flows only if schema mandates logging

### 5. Error Flow Pattern
```mermaid
graph TD
    {SchemaDefinedErrorSources} {ErrorAggregation}
    
    {ErrorAggregation} --> {ErrorClassification}
    {ErrorClassification} --> {SeverityAssessment}
    
    {SeverityAssessment} --> {ConditionalRecovery}
    {SeverityAssessment} --> {ConditionalEscalation}
    {SeverityAssessment} --> {ConditionalTermination}
    
    %% Optional Error Artifacts
    {OptionalErrorLogging}
    {OptionalErrorNotification}
```

**Conditional Generation Rules:**
- `{SchemaDefinedErrorSources}`: Include only error sources explicitly defined in schema
- `{ConditionalRecovery}`: Add recovery paths only if schema defines recovery mechanisms
- `{OptionalErrorLogging}`: Include error logging only if schema mandates error persistence
- `{OptionalErrorNotification}`: Include notifications only if schema defines notification requirements

### 6. Configuration Flow Pattern
```mermaid
graph LR
    {ConfigurationSources} --> {ConfigurationAggregation}
    
    {ConfigurationAggregation} --> {ConfigurationValidation}
    {ConfigurationValidation} --> {ConfigurationDistribution}
    
    {ConfigurationDistribution} --> {ConditionalConfigurationTargets}
    
    %% Dynamic Configuration Edges
    {SchemaDefinedConfigurationEdges}
```

**Adaptive Configuration Rules:**
- `{ConfigurationSources}`: Include only configuration sources referenced in schema
- `{ConditionalConfigurationTargets}`: Add configuration targets only for modules that schema defines as configurable
- `{SchemaDefinedConfigurationEdges}`: Generate configuration edges only where schema defines configuration dependencies

## Implementation Guidelines

### Placeholder Resolution Process
1. **Schema Analysis**: Examine schema definitions to identify required vs. optional components
2. **Conditional Inclusion**: Include placeholder content only when schema mandates it
3. **Dynamic Naming**: Replace generic placeholders with actual schema-defined names
4. **Relationship Mapping**: Generate edges based on actual schema relationships, not template assumptions

### Flexibility Principles
- **No Hardcoded Artifacts**: Avoid references to specific files (e.g., `conversion.log`, `error.log`) unless schema explicitly defines them
- **Conditional Utilities**: Include utility services (logging, error handling) only when schema requires them
- **Adaptive Grouping**: Use subgraphs based on logical schema groupings, not predetermined categories
- **Schema-First Structure**: Let schema definitions drive diagram structure rather than forcing predefined layouts

### Compliance Maintenance
- **Schema Validation**: Every diagram element must correspond to a schema-defined component or relationship
- **Governance Alignment**: All diagrams must align with PRD and schema governance mandates
- **Dependency Verification**: All dependencies shown must match Master Module Table and IR schema declarations
- **Interface Coverage**: All schema-defined interfaces must be represented as appropriate edges

## Syntax Validation Enhancements

### Pre-Render Validation Rules
Before generating any Mermaid diagram, validate:

1. **Connector Syntax Validation:**
   - Replace any Unicode dashes with ASCII dashes
   - Verify label compatibility with connector types
   - Check for invalid connector combinations

2. **Node Name Validation:**
   - Ensure node names don't start with `o` or `x` (add space or capitalize)
   - Validate special characters in node names
   - Check for reserved keywords

3. **Edge Label Validation:**
   - Only apply labels to compatible edge types (`-->`, `---`)
   - Remove labels from unsupported edge types (`==>`, `-.->`, `..>`, `-.-`)
   - Use alternative styling for unlabeled edges

### Syntax-Safe Alternatives

**Instead of problematic patterns:**
```mermaid
A ==>|condition| B     ❌ (Labels may not work with ==>)
A -.->|service type| B  ❌ (Labels typically not supported)
A ..>|error type| B     ❌ (Labels may not be supported)
```

**Use these validated patterns:**
```mermaid
A -->|condition| B     ✅ (Reliable label support)
A -.-> B              ✅ (Dependency without label)
A ..> B               ✅ (Error flow without label)

%% Add descriptive comments for context
%% A depends on B for logging service
%% A propagates errors to B
```

### Enhanced Error Handling
```mermaid
%% Safe error flow pattern
{ErrorSource} --> {ErrorHandler}
{ErrorHandler} -->|critical| {HaltProcess}
{ErrorHandler} -->|recoverable| {ContinueProcess}

%% Avoid unsupported label patterns
{ErrorSource} ..> {ErrorHandler}  %% Simple error propagation
%% Comment: Critical errors halt process, recoverable errors continue
```

### Edge Type Recommendations (Syntax-Validated)
Use these **verified** edge types adaptively based on actual relationships:

**Valid Data Flow Connectors:**
- `-->` for basic data flow
- `-->|label|` for labeled data flow (most reliable for labels)
- `---` for simple connections without arrows

**Valid Control Flow Connectors:**
- `==>` for emphasized control flow (**WARNING**: Labels may not work with `==>`)
- `-->` with control-specific labels (recommended alternative)

**Valid Dependency Connectors:**
- `-.->` for dashed dependencies
- `-.-` for dotted dependencies (**WARNING**: Labels typically not supported)

**Valid Error Flow Connectors:**
- `..>` for dotted error flows (**WARNING**: Labels may not be supported)
- `-->` with error-specific styling (recommended alternative)

**Bidirectional Connectors:**
- `<-->` for bidirectional flow (**WARNING**: Limited label support)
- `-->` and `<--` separately (recommended for better control)

**CRITICAL SYNTAX RULES:**
1. **Avoid Unicode Characters**: Use only ASCII dashes (`-`) not Unicode en-dash (`–`) or em-dash (`—`)
2. **Label Compatibility**: Only use labels with `-->` and `---` connectors for maximum compatibility
3. **Node Naming**: Avoid starting node names with `o` or `x` (add space or capitalize)
4. **Edge IDs**: Use `id@-->` syntax only with Mermaid v11.6.0+

### Legend Template
```
**Legend:**
- **Node Types:** Adapt shapes based on actual component types in schema
- **Edge Types:** Include only edge types actually used in the diagram
- **Subgraphs:** Reflect actual logical groupings from schema
- **Conditional Elements:** Mark elements that appear only under certain schema conditions
- **Source References:** Every element must reference its authoritative schema source
```

## Validation Checklist
- [ ] All placeholders resolved with schema-defined components
- [ ] No hardcoded artifacts unless schema-mandated
- [ ] All edges correspond to actual schema relationships
- [ ] No template artifacts remain in final output
- [ ] Diagram structure reflects schema logic, not template structure
- [ ] All conditional elements included only when schema requires them
- [ ] **Syntax validation passed for all Mermaid code using validated connector patterns**
- [ ] **All Unicode characters replaced with ASCII equivalents**
- [ ] **Edge labels only used with compatible connector types (`-->`, `---`)**
- [ ] **Node names validated for reserved characters and patterns**
- [ ] Cross-diagram consistency maintained
- [ ] All schema-defined components appropriately represented

##### 5.3 **LFC Contribution Manifest (`result-files/lfc_contribution_manifest.md`)**  
**Purpose:** Index of all source files contributing to LFC generation

**Requirements:**
- Scan `build/logical_flow_canonicalizer/meta-files/` and `build/logical_flow_canonicalizer/schema/`
- List file paths, modification dates, and contribution type
- **Preserve actual content in source directories** - manifest is index only

##### 5.4 **LFC Overview (`result-files/README.md`)**  
**Purpose:** User guide for generated LFC outputs

**Requirements:**
- Brief description of each generated file
- File locations and purposes  
- Usage instructions and important notes
- Cross-references to [glossary terms](glossary.md)
- Integration points with broader system

##### 5.5 **Glossary of Terms (`result-files/glossary.md`)**  
**Purpose:** Centralized definition of LFC terminology

**Requirements:**
- Define all technical terms from meta-files, schema, and generated outputs
- Use consistent markdown anchor format: `#term-name`
- Include terms: TOPOLOGICAL SORT, MASTER MODULE TABLE, DEPENDENCY GRAPH, BUILD MAP, INTERFACE ALIGNMENT, etc.
- Cross-reference terms in all other LFC outputs using `[TERM](glossary.md#term-name)` format

##### 5.6 **Build Map (`result-files/build_map.md`)**  
**Purpose:** Dependency-ordered sequence for agentic codegen execution

**Requirements:**
- Generate from [LFD](glossary.md#logical-flow-diagram) using [topological sort](glossary.md#topological-sort)
- Create ordered list of modules for sequential code generation
- Include interface validation checkpoints between dependent modules
- Specify codegen template mappings for each module type
- Include rollback points for interface misalignment recovery

**Structure:**
```markdown
# Build Map - Codegen Execution Sequence

## Phase 1: Foundation Modules
1. **config_loader** 
   - Template: `meta-files/module.py.jinja`
   - Dependencies: None
   - Interface Contracts: [config_schema.md](schema/config_schema.md)
   - Validation Checkpoint: Post-generation interface verification

2. **logging_facility**
   - Template: `meta-files/class.py.jinja` 
   - Dependencies: config_loader
   - Interface Contracts: [logging_schema.md](schema/logging_schema.md)
   - Validation Checkpoint: Interface alignment with config_loader

## Phase 2: Processing Layer
[Continue with dependency-ordered modules...]

## Interface Validation Matrix
| Module A | Module B | Interface Contract | Validation Status |
|----------|----------|-------------------|------------------|
| config_loader | logging_facility | LogConfig schema | PENDING |
```

##### 5.7 **Interface Alignment Report (`result-files/interface_alignment_report.md`)**
**Purpose:** Continuous validation of schema-to-implementation consistency

**Requirements:**
- Cross-reference generated code interfaces with IR Schema definitions
- Flag any misalignments between coded interfaces and schema contracts
- Provide specific remediation steps for interface conflicts
- Track interface evolution through codegen iterations
- Generate compatibility matrix between all module pairs

##### 5.8 **Diagram Quality Validation Report (`result-files/diagram_quality_report.md`)**
**Purpose:** Comprehensive validation of Mermaid diagram completeness and accuracy

**Requirements:**

**Diagram Quality Validation (Pre-Generation Checks):**
1. **Completeness Audit:** Compare generated diagrams against Master Module Table - every entry must appear
2. **Schema Alignment:** Every IR Schema contract must have visual representation
3. **PRD Compliance:** Every PRD requirement must be traceable in the diagrams
4. **Meta-file Coverage:** Every orchestration rule in meta-files must be visualized
5. **Template Mapping:** Every Jinja template must connect to its target modules
6. **Syntax Validation:** All Mermaid code must be syntactically valid and renderable
7. **Cross-Reference Validation:** All internal links and references must resolve correctly

**Post-Generation Verification:**
- Render all Mermaid diagrams in a Mermaid parser to verify syntax
- Generate a coverage report showing which schema elements are visualized
- Create a traceability matrix linking PRD requirements to diagram elements
- Verify cross-diagram consistency (same nodes have same names and relationships)
- Validate that all edge types are properly labeled and use correct Mermaid syntax

**Report Structure:**
```markdown
# Diagram Quality Validation Report

## Validation Summary
- Total Diagrams Generated: 6
- Syntax Validation: PASSED/FAILED
- Schema Coverage: XX% (YY/ZZ elements covered)
- PRD Traceability: XX% (YY/ZZ requirements traced)

## Coverage Analysis
### Nodes Coverage
| Schema Element | System Overview | Execution Flow | Dependencies | Data Flow | Error Flow | Config Flow | Status |
|----------------|-----------------|----------------|--------------|-----------|------------|-------------|---------|
| config_loader  | ✓              | ✓             | ✓           | ✓         | -          | ✓          | COMPLETE |

### Edge Coverage
| Interface Contract | Represented As | Diagrams | Status |
|-------------------|----------------|----------|---------|
| config_loader -> logging_service | Dependency Edge | Dependencies, Config | COMPLETE |

## Validation Issues
[List any gaps, inconsistencies, or missing elements]

## Remediation Actions
[Specific steps to address any issues found]
```

##### 5.9 **Execution Status Report (`result-files/lfc_execution_report.md`)**  
**Purpose:** Success confirmation or halt documentation

**Success Report Contents:**
- Execution timestamp and duration
- Files generated with validation status
- Compliance verification results
- Summary of dependencies resolved
- Build map generation status
- Interface alignment verification results
- Diagram quality validation results

**Halt Report Contents (if execution fails):**
- Trigger condition and affected module/step
- Related PRD or meta-file reference  
- Specific validation failure details
- Suggested remediation path with actionable steps
- Build map generation failure analysis
- Diagram completeness gaps identified

---

#### 6. **Execution Flow**

**Step 1:** Compliance Verification → Generate `lfc_compliance_declaration.md`
**Step 2:** IR Schema Analysis → Scan and validate schema files for module definitions and interfaces
**Step 3:** Meta-file Analysis → Scan template and orchestration files for implementation guidance  
**Step 4:** Dependency Resolution → Build dependency graph from schema and meta-file data
**Step 5:** PRD Cross-Validation → Cross-check against PRD specifications for compliance
**Step 6:** Pre-LFD Validation → Verify all source elements are captured before diagram generation
**Step 7:** LFD Generation → Create all 6 logical flow diagrams from validated dependencies
**Step 8:** Diagram Quality Validation → Verify syntax, coverage, and consistency across all diagrams
**Step 9:** Build Map Generation → Create dependency-ordered codegen sequence
**Step 10:** Interface Schema Validation → Verify schema-to-LFD alignment
**Step 11:** Template Mapping → Associate codegen templates with modules from meta-files
**Step 12:** Generate All Deliverables → Create remaining artifacts
**Step 13:** Final Validation → Cross-check all outputs for completeness and consistency
**Step 14:** Final Report → Generate execution status report with comprehensive validation results

**Critical:** Each step must complete successfully before proceeding to the next. Any validation failure triggers halt condition with detailed remediation guidance.

---

#### 7. **Quality Assurance**

**7.1 Validation Checkpoints**
- All generated files must exist in `result-files/` directory
- All glossary terms must be properly linked across documents
- All dependencies must trace back to authoritative sources
- No orphaned references or broken internal links
- Build map must represent valid topological ordering
- Interface contracts must align between schema and LFD
- Template mappings must correspond to actual meta-file templates
- **All Mermaid diagrams must pass syntax validation**
- **All schema elements must appear in at least one diagram**
- **All PRD requirements must be traceable in diagrams**
- **Cross-diagram consistency must be maintained**

**7.2 File Integrity**
- Each generated file must include generation timestamp
- Cross-references between files must be validated
- Mermaid diagrams must render without syntax errors
- All click events and internal links must resolve correctly

**7.3 Diagram-Specific Quality Checks**
- Every node in dependency graph must have at least one edge (unless entry/exit point)
- Every data transformation must be represented in data flow diagram
- Every error condition must be represented in error flow diagram
- Every configuration parameter must be represented in configuration flow diagram
- All subgraphs must contain logically related components
- All edge labels must be descriptive and accurate

---

#### 8. **Error Handling**

**8.1 Graceful Degradation**
If partial execution is possible, generate available outputs and document limitations in execution report.

**8.2 Halt Conditions**
- PRD compliance failure
- Circular dependency detection  
- Missing critical meta-files
- Schema-PRD conflict resolution failure
- Build map topological sort failure
- Interface contract misalignment
- Template-to-module mapping conflicts
- **Diagram syntax validation failure**
- **Schema element coverage gaps**
- **Cross-diagram consistency violations**
- **Missing edge labels or node definitions**

**8.3 Recovery Guidance**
All halt reports must include specific, actionable steps for resolution, including:
- Which schema elements are missing from diagrams
- Which PRD requirements lack diagram representation
- Which diagram syntax errors need correction
- Which cross-diagram inconsistencies need resolution

---


### **Execution Authorization**
This prompt authorizes LFC execution under the constraints and requirements specified above. Begin with compliance verification and proceed systematically through all deliverables, with particular attention to comprehensive Mermaid diagram generation and validation.