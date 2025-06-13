# 1.0 Prompt for Local Agent: Logical Flow Canonicalizer (LFC)

## 1.1 Version
Version: 1.3.0 (Enhanced Mermaid Integration)

## 1.2 Compliance References
- Core PRD Document: core-prd-main-v3.6.5.md
- Governance Document: prd-governance-model-v2.3.10.md
- Logging Framework Module PRD: module-prd-logging-v1.0.4.md

---

## 2.0 Objective
You are tasked with constructing a **Logical Flow Canonicalizer (LFC)** that formalizes execution order, dependencies, interfaces, state transitions, and modular orchestration, ensuring deterministic code generation and eliminating ambiguity in system flow.

### 2.1 Key Terms
- **LFC** = Logical Flow Canonicalizer (this system)
- **LFD** = Logical Flow Diagram (output artifact)
- **IR** = Intermediate Representation (schema layer)

### 2.2 Directives
✅ DO enforce compliance with PRDs and governance mandates  
✅ DO ensure logging is fully integrated as a structured execution component  
✅ Place all generated files directly into the `result-files` directory—no output should be presented exclusively in chat  
✅ Modify files inline within their designated locations—no external drafts or temporary deliverables  
🚫 DO NOT infer execution order beyond authoritative source definitions  
🚫 DO NOT alter module relationships beyond structured dependencies

---

## 3.0 Source Authority Hierarchy
All system logic, execution ordering, interface contracts, validation mechanisms, and dispatch structures must be derived from these authoritative sources in order of precedence:

### 3.1 Primary Sources (Highest Authority)
- PRDs (`./prd/core-prd-main-v3.6.5.md`, `./prd/module-prd-logging-v1.0.4.md`, etc.) → Define operational compliance, validation rules, interface contracts

### 3.2 Secondary Sources (Implementation Guidance)
- Meta-Files (`./build/logical_flow_canonicalizer/meta-files/`) → Define structured execution mappings, interdependencies, orchestration sequences
- IR Schema (`./build/logical_flow_canonicalizer/schema/`) → QBD-to-GnuCash Intermediate Representation Schema files

### 3.3 Resolution Protocol
When conflicts arise between sources:
1. PRD supersedes all other sources
2. Meta-files supersede IR Schema  
3. If gap exists between PRD and implementation sources → HALT execution and generate halt report

The agent is prohibited from making assumptions outside of formal definitions. If a logical gap exists, execution halts until the discrepancy is explicitly resolved.

---

## 4.0 Pre-Execution Compliance Verification

### 4.1 Scan Required Documents
Before proceeding, you must scan:
- `core-prd-main-v3.6.5.md` (Core PRD rules & constraints)
- `prd-governance-model-v2.3.10.md` (Governance policies)  
- `module-prd-logging-v1.0.4.md` (Logging facility structure)

### 4.2 Generate Compliance Declaration
Create `result-files/lfc_compliance_declaration.md` containing:
- Verification timestamp
- Document versions accessed
- Compliance gaps identified (if any)
- Authorization to proceed (or halt directive)

Proceed only after successful compliance verification.

---

## 5.0 Key Deliverables

### 5.1 Master Module Table (`result-files/master_module_table.md`)
**Purpose:** Comprehensive registry of all system modules with dependencies and validation status

**Requirements:**
- Derive from IR Schema in `./build/logical_flow_canonicalizer/schema/`
- Cross-validate against PRD specifications
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

### 5.2 Logical Flow Diagram (`result-files/lfd.md`)
**Purpose:** Comprehensive visual representation of system execution flow, dependencies, and all data transformations

**Requirements:**

#### 5.2.1 Node Coverage Mandates
- Appropriate Representation of Nodes: All schema-defined entities must be represented appropriately—their structure should reflect the nature of the data rather than force a one-to-one mapping to predefined Reference Diagram Formats.
- Implicit dependencies must be explicit: If a module uses logging, error handling, configuration, or any utility service, these must appear as dedicated nodes with edges showing the dependency relationship
- State transition nodes: Include nodes for different states of data processing (e.g., "Raw QBD Data", "Validated QBD Data", "Transformed Data", "GnuCash Output")
- Error and exception paths: Include nodes for error states, validation failures, and exception handling flows
- Configuration and runtime nodes: Include nodes for configuration loading, environment setup, and runtime initialization
- External system interfaces: Include nodes for any external system touchpoints (file system, databases, APIs, etc.)

#### 5.2.2 Recommended Edge Guidelines (Adaptive Reference Format)
- Data Flow Edges: Solid arrows `-->` (e.g., `A --> B`) indicate data movement between modules.
- Control Flow Edges: Thick arrows `==>` (e.g., `A ==> B`) define execution order, orchestration, and process transitions.
- Dependency Edges: Dashed arrows `-.->` (e.g., `A -.-> B`) represent logical dependencies, imports, and required services.
- Error/Exception Edges: Dotted arrows `..>` (e.g., `A ..> B`) show error propagation, exception handling, and failure states.
- Configuration Edges: Dash-dot arrows `-.-` (e.g., `A -.- B`) are for configuration loading, parameter passing, and setup dependencies.
- Validation Edges: Double arrows `<-->` (e.g., `A <--> B`) define bidirectional validation, feedback loops, and confirmation flows.
- Conditional Edges: Labels on edges using `-->|condition|` or `==>|condition|` (e.g., `A --|on success|--> B`) indicate flow triggers.
- Text on Edges: Edge labels should be applied only where Mermaid syntax supports them. If an edge type does not allow labels, use separate annotations or descriptive nodes instead.

#### 5.2.3 Guidance for Syntax Compliance
- Labels should be applied only to edge types that allow them in Mermaid.js.
- Where labels are unsupported, add descriptive comments or reference nodes to maintain clarity.
- Before finalizing diagrams, verify edge syntax validity to avoid enforcement errors.

#### 5.2.4 Guidance for Adaptive Structure
- These edge definitions serve as recommendations to align visualization with schema logic.
- Use these as a reference—not strict templates—to ensure diagrams reflect actual relationships.
- Adjust formatting dynamically based on structural requirements, avoiding rigid replication.

// Reference: https://mermaid.js.org/syntax/flowchart.html

#### 5.2.5 Edge Labels (Required)

- **All edges must include descriptive labels** explaining what flows through them
- **Labels are only allowed** on `-->` and `---` connectors in Mermaid
- For other edge types (`==>`, `-.->`, `..>`, `-.-`), use **comments** instead of labels

**Labeling Guidelines:**

- **Data edges**: use `-->` with labels (e.g., `-->|QBD Account List|`)
- **Control flow edges**: use `-->` with trigger condition labels (e.g., `-->|after validation|`)
- **Dependency edges**: use `-.->` without labels; annotate with `%%` comments
- **Configuration and error edges**: use appropriate connectors and document meaning with comments

**Syntax-Safe Examples:**

```mermaid
A -->|QBD Account List| B           %% Data flow with label
A -->|after validation| C          %% Control flow with trigger
D -.-> E                           %% Dependency (no label allowed)
%% D depends on E for logging service
F ..> G                            %% Error propagation
%% F passes exception to G
H -.- I                            %% Configuration flow
%% H loads config used by I
```

#### 5.2.6 Source Reference Comments
- For every node and edge, include a Mermaid comment (`%%`) referencing the authoritative source (PRD, meta-file, or schema) that defines or requires it. Example:
  - `%% Source: schema/module-ir-accounts-v1.1.3.md`
  - `%% Source: prd/module-prd-logging-v1.0.4.md`
- For complex or composite nodes, include all relevant sources.
- Place these comments immediately before the relevant Mermaid line for traceability and auditing.

#### 5.2.7 Syntax Validation and Automated Correction
- All Mermaid diagrams must be validated for syntax correctness using a Mermaid parser before being written to result files.
- If an invalid edge type or node connector is detected, automatically correct it to the closest valid Mermaid syntax and log the correction in the diagram quality report.
- Any syntax errors or corrections must be documented in the diagram quality validation report.

#### 5.2.8 Required Diagram Hierarchy
1. System Overview Diagram (`graph TD`): High-level flow showing major phases and key decision points
2. Detailed Execution Flow (`graph TD`): Complete step-by-step execution with all data flows and decision branches
3. Module Dependency Graph (`graph LR`): All static dependencies between modules, utilities, and artifacts
4. Data Flow Diagram (`graph TD`): Focused on data transformation pipeline from input to output
5. Error Flow Diagram (`graph TD`): Error propagation, exception handling, and recovery paths
6. Configuration Flow Diagram (`graph LR`): Configuration loading and parameter distribution

#### 5.2.9 Cross-Diagram Consistency
- Nodes appearing in multiple diagrams must use identical names and styling
- All relationships shown in one diagram must be consistent with others
- No diagram should contradict information in another diagram

#### 5.2.10 Advanced Mermaid Requirements
- Subgraphs: Group related modules into logical subsystems (e.g., `subgraph "QBD Processing"`)
- Node Styling: Use different shapes for different node types:
  - `[Module Name]` for processing modules
  - `(Configuration)` for config nodes  
  - `{Result File}` for output artifacts
  - `[[Utility Service]]` for shared services
  - `((Decision Point))` for branching logic
- Conditional Styling: Use different colors/styles for different phases or error states
- Click Events: Include click handlers for nodes to reference documentation (e.g., `click ModuleName "schema.md#module-name"`)

#### 5.2.11 Mandatory Content Coverage
- All PRD-defined interfaces: Every interface contract mentioned in PRDs must appear as edges
- All meta-file orchestration: Every orchestration sequence in meta-files must be visualized
- All template relationships: Every Jinja template and its target modules must be connected
- All validation points: Every validation step mentioned in schemas must appear as nodes/edges
- All error conditions: Every error condition defined in PRDs must have corresponding error flow paths
- All configuration dependencies: Every configuration parameter usage must be shown as dependency edges
- All result artifacts: Every output file, log entry, or data structure must be represented as nodes

#### 5.2.12 Diagram Completeness Validation
- Schema Contract Verification: For every input/output declared in IR Schema, verify corresponding edges exist in diagrams
- Orphan Detection: Identify any nodes with no incoming or outgoing edges (unless they are true entry/exit points)
- Dead End Analysis: Flag any nodes that receive data but produce no output (unless they are true sinks like log files)
- Circular Dependency Detection: Identify and document any circular dependencies in the dependency graph
- Interface Gap Detection: Verify that every module interface contract has corresponding edges showing data flow
- Template Coverage Verification: Ensure every Jinja template referenced in meta-files has corresponding nodes in the diagrams

#### 5.2.13 Validation Against Dependencies
- Every module's declared dependencies and I/O contracts in the Master Module Table and IR schema must be reflected as edges in the Mermaid dependency graph.
- After diagram generation, cross-check all dependencies and I/O contracts listed in the Master Module Table and IR schema against the edges in the Mermaid dependency graph. Flag or halt if any declared dependency or contract is missing.

- Include legend explaining node types and edge meanings, clarifying that some nodes (like Error Handler and Logging) are global utilities with multiple inbound edges. The legend must also explain edge styles/labels.
- Validate against [topological ordering](glossary.md#topological-sort) requirements

### 5.3 Reference Diagram Formats for LFD Generation

#### 5.3.1 Design Philosophy
These Reference Diagram Formats serve as adaptive guidance rather than rigid templates. They illustrate structural patterns and relationships that should be dynamically adjusted based on schema-defined requirements and system characteristics.

#### 5.3.2 Core Principles
- Schema-Driven Adaptation: Diagram structures should reflect actual schema relationships, not force predefined layouts
- Placeholder-Based Flexibility: Use placeholders for optional components that only appear when mandated by schema
- Contextual Optimization: Encourage diagrams that optimize for the specific system being modeled
- Compliance Preservation: Maintain strict alignment with PRDs and schema governance while allowing rendering flexibility

#### 5.3.3 Mandatory Diagram Requirements

The following **6 diagrams are required** for every LFD output. Each diagram must be generated with appropriate schema-driven content using the adaptive patterns below:

1. **System Overview Diagram** (`graph TD`) - High-level flow showing major phases and key decision points
2. **Detailed Execution Flow** (`graph TD`) - Complete step-by-step execution with all data flows and decision branches  
3. **Module Dependency Graph** (`graph LR`) - All static dependencies between modules, utilities, and artifacts
4. **Data Flow Diagram** (`graph TD`) - Focused on data transformation pipeline from input to output
5. **Error Flow Diagram** (`graph TD`) - Error propagation, exception handling, and recovery paths
6. **Configuration Flow Diagram** (`graph LR`) - Configuration loading and parameter distribution

#### 5.3.4 Adaptive Reference Formats
##### 1. System Overview Diagram Pattern 
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

##### 2. Detailed Execution Flow Pattern
**Purpose:** Complete step-by-step execution with all data flows and decision branches

```mermaid
graph TD
    start_node((START)) --> {InitializationSequence}
    {InitializationSequence} --> {ValidationGate}
    
    {ValidationGate} -->|valid| {ProcessingPipeline}
    {ValidationGate} -->|invalid| {ErrorHandler}
    
    {ProcessingPipeline} --> {BusinessLogicDecisions}
    {BusinessLogicDecisions} -->|condition_a| {ProcessingPathA}
    {BusinessLogicDecisions} -->|condition_b| {ProcessingPathB}
    
    {ProcessingPathA} --> {OutputGeneration}
    {ProcessingPathB} --> {OutputGeneration}
    {OutputGeneration} --> {CompletionCheck}
    
    {CompletionCheck} -->|more_sections| {ProcessingPipeline}
    {CompletionCheck} -->|complete| end_node((COMPLETE))
    
    %% Error flows with syntax-safe patterns
    {ProcessingPathA} -->|error| {ErrorHandler}
    {ProcessingPathB} -->|error| {ErrorHandler}
    {OutputGeneration} -->|error| {ErrorHandler}
    
    {ErrorHandler} --> {RecoveryDecision}
    {RecoveryDecision} -->|recoverable| {ProcessingPipeline}
    {RecoveryDecision} -->|critical| halt_node((HALT))
    
    %% Utility connections (no labels on dashed lines)
    {ProcessingPathA} -.-> {OptionalLoggingService}
    {ProcessingPathB} -.-> {OptionalLoggingService}
    {OutputGeneration} -.-> {OptionalLoggingService}
```

**Syntax-Safe Adaptations:**
- Use `-->|label|` for all labeled connections
- Avoid labels on `-.->` (dependency) edges
- Use descriptive node names instead of single letters
- Include START/COMPLETE/HALT control nodes where schema requires them
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

##### 3. Module Dependency Graph Pattern
**Purpose:** All static dependencies between modules, utilities, and artifacts

```mermaid
graph LR
    subgraph "Foundation Layer"
        config_loader[{ConfigLoader}]
        {OptionalLoggingService}
        {OptionalErrorHandler}
    end
    
    subgraph "Processing Layer"
        {InputProcessor}
        {BusinessLogicModules}
        {ValidationModule}
    end
    
    subgraph "Output Layer"
        {OutputProcessors}
        {ReportGenerators}
    end
    
    subgraph "Artifacts"
        {MandatoryOutputs}
        {OptionalArtifacts}
    end
    
    %% Foundation dependencies (no labels on dashed edges)
    {InputProcessor} -.-> config_loader
    {InputProcessor} -.-> {OptionalLoggingService}
    {InputProcessor} -.-> {OptionalErrorHandler}
    
    %% Processing dependencies
    {BusinessLogicModules} --> {InputProcessor}
    {BusinessLogicModules} -.-> {OptionalLoggingService}
    {ValidationModule} --> {InputProcessor}
    
    %% Output dependencies
    {OutputProcessors} --> {BusinessLogicModules}
    {OutputProcessors} --> {ValidationModule}
    {ReportGenerators} --> {BusinessLogicModules}
    
    %% Artifact generation
    {OutputProcessors} --> {MandatoryOutputs}
    {ReportGenerators} --> {OptionalArtifacts}
    {OptionalLoggingService} --> {OptionalLogFiles}
```

**Syntax-Safe Adaptations:**
- Use `[Module Name]` for processing modules
- Use `{Placeholder}` for schema-driven components
- No labels on `-.->` dependency edges
- Use descriptive comments instead of edge labels for dependencies
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

##### 4. Data Flow Diagram Pattern
**Purpose:** Focused on data transformation pipeline from input to output

```mermaid
graph TD
    {PrimaryDataSource} --> {RawDataState}
    {ConfigurationData} --> {RawDataState}
    
    {RawDataState} --> {ParsedDataState}
    {ParsedDataState} --> {ValidatedDataState}
    {ValidatedDataState} --> {ProcessedDataStates}
    
    {ProcessedDataStates} --> {TransformedDataA}
    {ProcessedDataStates} --> {TransformedDataB}
    {ProcessedDataStates} --> {TransformedDataC}
    
    {TransformedDataA} --> {OutputFormatA}
    {TransformedDataB} --> {OutputFormatB}
    {TransformedDataC} --> {OutputFormatC}
    
    {OutputFormatA} --> {FinalArtifactA}
    {OutputFormatB} --> {FinalArtifactB}
    {OutputFormatC} --> {FinalArtifactC}
    
    %% Audit flows (use comments for context)
    {ParsedDataState} -.-> {OptionalAuditLog}
    {ValidatedDataState} -.-> {OptionalAuditLog}
    {TransformedDataA} -.-> {OptionalAuditLog}
    
    %% Schema-driven data states
    %% Replace {ProcessedDataStates} with actual data structures from schema
    %% Replace {TransformedData*} with actual transformation outputs
    %% Replace {FinalArtifact*} with schema-defined output files
```

**Schema-Driven Adaptations:**
- `{ProcessedDataStates}`: Expand to actual data structures from IR schema
- `{TransformedData*}`: Replace with actual transformation outputs
- `{FinalArtifact*}`: Use schema-defined output artifacts
- Audit flows only included if schema mandates auditing
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

##### 5. Error Flow Diagram Pattern
**Purpose:** Error propagation, exception handling, and recovery paths

```mermaid
graph TD
    {SchemaDefinedErrorSource1} --> error_aggregator[Error Aggregator]
    {SchemaDefinedErrorSource2} --> error_aggregator
    {SchemaDefinedErrorSource3} --> error_aggregator
    {OptionalAdditionalErrorSources} --> error_aggregator
    
    error_aggregator --> error_classifier[Error Classifier]
    error_classifier --> severity_assessor{Assess Severity}
    
    severity_assessor -->|critical| critical_handler[Critical Error Handler]
    severity_assessor -->|recoverable| recovery_handler[Recovery Handler]  
    severity_assessor -->|warning| warning_handler[Warning Handler]
    
    critical_handler --> halt_process((HALT EXECUTION))
    
    recovery_handler --> recovery_attempt{Recovery Attempt}
    recovery_attempt -->|success| continue_process[Continue Processing]
    recovery_attempt -->|failure| escalate_error[Escalate Error]
    
    warning_handler --> continue_process
    escalate_error --> user_intervention{User Intervention Required?}
    user_intervention -->|yes| pause_execution((PAUSE FOR INPUT))
    user_intervention -->|no| halt_process
    
    continue_process --> main_flow_return[Return to Main Flow]
    
    %% Optional error logging (no labels on dashed lines)
    error_classifier -.-> {OptionalErrorLog}
    critical_handler -.-> {OptionalErrorLog}
    recovery_handler -.-> {OptionalErrorLog}
    
    %% Optional notifications
    escalate_error -.-> {OptionalNotificationSystem}
```

**Conditional Generation Rules:**
- `{SchemaDefinedErrorSource*}`: Include only error sources defined in schema
- Recovery paths only generated if schema defines recovery mechanisms
- Logging connections only if schema mandates error persistence
- Notification systems only if schema defines alerting requirements
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

##### 6. Configuration Flow Diagram Pattern
**Purpose:** Configuration loading and parameter distribution

```mermaid
graph LR
    config_file({ConfigFile}) --> config_loader[Configuration Loader]
    env_vars({EnvironmentVariables}) --> config_loader
    {OptionalConfigSources} --> config_loader
    
    config_loader --> config_validator[Configuration Validator]
    config_validator --> config_distributor[Configuration Distributor]
    
    config_distributor --> app_config[Application Config]
    config_distributor --> {OptionalLoggingConfig}
    config_distributor --> {OptionalMappingConfig}
    config_distributor --> {OptionalExportConfig}
    
    %% Configuration consumption (no labels on dash-dot lines)
    app_config -.- {InputProcessor}
    app_config -.- {ValidationModule}
    
    {OptionalLoggingConfig} -.- {OptionalLoggingService}
    {OptionalMappingConfig} -.- {BusinessLogicModules}
    {OptionalExportConfig} -.- {OutputProcessors}
    
    %% Error handling for configuration
    config_validator -->|invalid_config| config_error_handler[Config Error Handler]
    config_error_handler --> config_error_resolution{Error Resolution}
    config_error_resolution -->|use_defaults| config_distributor
    config_error_resolution -->|halt| halt_config((HALT))
```

**Adaptive Configuration Rules:**
- `{OptionalConfigSources}`: Include only additional config sources from schema
- `{OptionalLoggingConfig}`: Include only if schema defines logging configuration
- `{OptionalMappingConfig}`: Include only if schema defines mapping parameters
- Configuration target connections only for modules that schema defines as configurable
- Error handling only if schema defines configuration validation requirements
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

## 6.0 Implementation Guidelines

### 6.1 Placeholder Resolution Process
1. Schema Analysis: Examine schema definitions to identify required vs. optional components
2. Conditional Inclusion: Include placeholder content only when schema mandates it
3. Dynamic Naming: Replace generic placeholders with actual schema-defined names
4. Relationship Mapping: Generate edges based on actual schema relationships, not template assumptions

### 6.2 Flexibility Principles
- No Hardcoded Artifacts: Avoid references to specific files (e.g., `conversion.log`, `error.log`) unless schema explicitly defines them
- Conditional Utilities: Include utility services (logging, error handling) only when schema requires them
- Adaptive Grouping: Use subgraphs based on logical schema groupings, not predetermined categories
- Schema-First Structure: Let schema definitions drive diagram structure rather than forcing predefined layouts

### 6.3 Compliance Maintenance
- Schema Validation: Every diagram element must correspond to a schema-defined component or relationship
- Governance Alignment: All diagrams must align with PRD and schema governance mandates
- Dependency Verification: All dependencies shown must match Master Module Table and IR schema declarations
- Interface Coverage: All schema-defined interfaces must be represented as appropriate edges

## 7.0 Syntax Validation Enhancements

### 7.1 Pre-Render Validation Rules
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

### 7.2 Syntax-Safe Alternatives

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

### 7.3 Enhanced Error Handling
```mermaid
%% Safe error flow pattern
{ErrorSource} --> {ErrorHandler}
{ErrorHandler} -->|critical| {HaltProcess}
{ErrorHandler} -->|recoverable| {ContinueProcess}

%% Avoid unsupported label patterns
{ErrorSource} ..> {ErrorHandler}  %% Simple error propagation
%% Comment: Critical errors halt process, recoverable errors continue
```

### 7.4 Edge Type Recommendations (Syntax-Validated)
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

### 7.5 Legend Template (Required for All Diagrams)
```
**Legend:**
- **Node Types:** 
  - `[Module Name]` for processing modules
  - `(Configuration)` for config sources  
  - `{Artifact File}` for output files
  - `[[Service Name]]` for utility services
  - `((Control Point))` for start/end/decision points
  - `{Placeholder}` for schema-driven components

- **Edge Types:** 
  - `-->` data flow (with labels supported)
  - `-->|label|` labeled data flow
  - `-.->` dependencies (no labels - use comments)
  - `-.-` configuration flow (no labels - use comments)  
  - `<-->` bidirectional validation (limited label support)

- **Subgraphs:** Logical groupings based on schema-defined relationships
- **Conditional Elements:** Components that appear only when schema mandates them
- **Source References:** Every element references authoritative schema source via comments
- **Syntax Validation:** All diagrams validated against Mermaid.js syntax before output
```

## 8.0 Validation Checklist
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

##### 8.1 Success Report Contents
- Execution timestamp and duration
- Files generated with validation status
- Compliance verification results
- Summary of dependencies resolved
- Build map generation status
- Interface alignment verification results
- Diagram quality validation results

##### 8.2 Halt Report Contents (if execution fails)
- Trigger condition and affected module/step
- Related PRD or meta-file reference  
- Specific validation failure details
- Suggested remediation path with actionable steps
- Build map generation failure analysis
- Diagram completeness gaps identified

---

## 9.0 Execution Flow

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

## 10.0 Quality Assurance

### 10.1 Validation Checkpoints
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

### 10.2 File Integrity
- Each generated file must include generation timestamp
- Cross-references between files must be validated
- Mermaid diagrams must render without syntax errors
- All click events and internal links must resolve correctly

### 10.3 Diagram-Specific Quality Checks
- Every node in dependency graph must have at least one edge (unless entry/exit point)
- Every data transformation must be represented in data flow diagram
- Every error condition must be represented in error flow diagram
- Every configuration parameter must be represented in configuration flow diagram
- All subgraphs must contain logically related components
- All edge labels must be descriptive and accurate

---

## 11.0 Error Handling

### 11.1 Graceful Degradation
If partial execution is possible, generate available outputs and document limitations in execution report.

### 11.2 Halt Conditions
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

### 11.3 Recovery Guidance
All halt reports must include specific, actionable steps for resolution, including:
- Which schema elements are missing from diagrams
- Which PRD requirements lack diagram representation
- Which diagram syntax errors need correction
- Which cross-diagram inconsistencies need resolution

---


### **Execution Authorization**
This prompt authorizes LFC execution under the constraints and requirements specified above. Begin with compliance verification and proceed systematically through all deliverables, with particular attention to comprehensive Mermaid diagram generation and validation.