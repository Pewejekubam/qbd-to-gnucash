# Prompt for Local Agent: Logical Flow Canonicalizer (LFC)

## 1 Prompt Document Meta-Data
- Core IR Document: core-ir-main-v3.6.5.md
- Governance Document: prd-governance-model-v2.3.10.md
- Logging Framework Module PRD: module-prd-logging-v1.0.4.md
- QuickBooks Desktop to GnuCash Conversion Tool  
- Author: Pewe Jekubam (Development Engineer)  
- Module Identifier: lfc-build-v1.4.1.prompt.md
- Last Updated: 2025 06:05 12:38:00 CDT

---

## 2 Objective
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

## 3 Source Authority Hierarchy
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
3. If gap exists between PRD and implementation sources → HALT execution and generate execution report

The agent is prohibited from making assumptions outside of formal definitions. If a logical gap exists, execution halts until the discrepancy is explicitly resolved.

---

## 4 Pre-Execution Compliance Verification

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

## 5 Key Deliverables

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
- If an invalid edge type or node connector is detected, automatically correct it to the closest valid Mermaid syntax.

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

#### 5.2.14 Design Philosophy
These Reference Diagram Formats serve as adaptive guidance rather than rigid templates. They illustrate structural patterns and relationships that should be dynamically adjusted based on schema-defined requirements and system characteristics.

#### 5.2.15 Core Principles
- Schema-Driven Adaptation: Diagram structures should reflect actual schema relationships, not force predefined layouts
- Placeholder-Based Flexibility: Use placeholders for optional components that only appear when mandated by schema
- Contextual Optimization: Encourage diagrams that optimize for the specific system being modeled
- Compliance Preservation: Maintain strict alignment with PRDs and schema governance while allowing rendering flexibility

#### 5.2.16 Diagram Type Generation Requirements

- Each diagram must be generated with appropriate schema-driven content using the adaptive patterns below:

1. **System Overview Diagram** (`graph TD`) - High-level flow showing major phases and key decision points
2. **Detailed Execution Flow** (`graph TD`) - Complete step-by-step execution with all data flows and decision branches  
3. **Module Dependency Graph** (`graph LR`) - All static dependencies between modules, utilities, and artifacts
4. **Data Flow Diagram** (`graph TD`) - Focused on data transformation pipeline from input to output
5. **Error Flow Diagram** (`graph TD`) - Error propagation, exception handling, and recovery paths
6. **Configuration Flow Diagram** (`graph LR`) - Configuration loading and parameter distribution

#### 5.2.17 Adaptive Diagram Pattern Reference

##### 5.2.17.1 System Overview Diagram Pattern 
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

##### 5.2.17.2 Detailed Execution Flow Pattern
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

##### 5.2.17.3 Module Dependency Graph Pattern
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

##### 5.2.17.4 Data Flow Diagram Pattern
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

##### 5.2.17.5 Error Flow Diagram Pattern
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

##### 5.2.17.6 Configuration Flow Diagram Pattern
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
- `{OptionalExportConfig}`: Include only if schema defines export parameters
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


### 5.3 Glossary of Terms (`result-files/glossary.md`)

**Purpose:** Automatically derived glossary built from multiple project document and artifact sources

**Build Process:**
- Extract terminology from Master Module Table (`result-files/master_module_table.md`) - module names, relationships, interfaces
- Harvest terms from Logical Flow Diagram (`result-files/lfd.md`) - process steps, data flows, decision points  
- Pull definitions from schema files (`./build/logical_flow_canonicalizer/schema/*`) - data structures, validation rules, constraints   
- Mine PRDs (`- ../../../prd/*`) content for core and domain-specific terminology
- Cross-reference and deduplicate terms across all source artifacts

**Output Requirements:**
- Use consistent markdown anchor format: `#term-name`
- Include source attribution: each term notes which artifact(s) it originated from
- Maintain hierarchical organization reflecting the LFC structure
- Generate bidirectional linking preparation for build-map consumption

**Validation:**
- Ensure all technical terms from source artifacts are captured
- Verify no orphaned references in subsequent build-map (5.4)
- Confirm terminology consistency across all source materials

### 5.4 Build Map (`result-files/build_map.yaml`)
**Purpose:** Dependency-ordered sequence for agentic codegen execution

#### 5.4.1 Input
- **IR Schema (`./build/logical_flow_canonicalizer/schema/*`)**
- **Meta-Files (`./build/logical_flow_canonicalizer/meta-files/`)**
- **Logical Flow Diagram (`./build/logical_flow_canonicalizer/result-files/lfd.md`)**
- **Master Module Table (`result-files/master_module_table.md`)**

#### 5.4.2 Output
- **YAML Build Map**: A structured YAML file that outlines the order of module generation, dependencies, interface contracts, validation checkpoints, and rollback points.

#### 5.4.3 Steps
1. **Parse the Schema Definition**:
   - Extract the list of components, their dependencies, and interface contracts from the schema.
   - Identify the core orchestrator, utility modules, and specific modules like `accounts`.
2. **Generate Topological Order**:
   - Use the logical flow diagram to determine the correct order of module generation based on dependencies.
   - Implement a topological sort to ensure that all dependencies are resolved before a module is generated.
3. **Create Module Definitions**:
   - For each module, define its template, dependencies, interface contracts, validation checkpoints, and rollback points.
   - Ensure that each module's dependencies are correctly listed and validated.
4. **Build Interface Validation Matrix**:
   - Create a matrix that lists pairs of modules and their interface contracts, along with the validation status.
   - Include all necessary interfaces and their validation checkpoints.
5. **Output the Build Map**:
   - Format the generated data into a YAML structure.
   - Ensure that the YAML file is well-structured and easy to read.

#### 5.4.4 Example Output
```yaml
# build_map.yaml
build_map:
  purpose: Dependency-ordered sequence for agentic codegen execution
  phases:
    - name: Phase 1: Foundation Modules
      modules:
        - name: utils.error_handler
          template: meta-files/module.py.jinja
          dependencies: []
          interface_contracts:
            - ../schema/core-ir-main-v3.6.5.md
          validation_checkpoint: Post-generation interface verification
          rollback_point: Log error and skip further processing
        - name: utils.logging
          template: meta-files/module.py.jinja
          dependencies:
            - utils.error_handler
          interface_contracts:
            - ../../../prd/logging/module-prd-logging-v1.0.4.md
          validation_checkpoint: Interface alignment with utils.error_handler
          rollback_point: Log error and skip further processing
    - name: Phase 2: Core Orchestration
      modules:
        - name: core
          template: meta-files/module.py.jinja
          dependencies:
            - utils.error_handler
            - utils.logging
          interface_contracts:
            - ../schema/core-ir-main-v3.6.5.md
          validation_checkpoint: Post-generation interface verification
          rollback_point: Log error and skip further processing
    - name: Phase 3: Accounts Processing
      modules:
```
---

## 6 Execution Flow

Execute workflow in strict sequential order according to the header sequence, where each step's successful completion is a prerequisite for proceeding to the next, ensuring a deterministic and validated outcome.

---

## 7 Quality Assurance

### 7.1 Validation Checkpoints
- All timestamps must be in the ISO 8601 Timestamp UTC format
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

### 7.2 File Integrity
- Each generated file must include generation timestamp
- Cross-references between files must be validated
- Mermaid diagrams must render without syntax errors
- All click events and internal links must resolve correctly

### 7.3 Diagram-Specific Quality Checks
- Every node in dependency graph must have at least one edge (unless entry/exit point)
- Every data transformation must be represented in data flow diagram
- Every error condition must be represented in error flow diagram
- Every configuration parameter must be represented in configuration flow diagram
- All subgraphs must contain logically related components
- All edge labels must be descriptive and accurate

---

## 8 Error Handling

### 8.1 Graceful Degradation
If partial execution is possible, generate available outputs and document limitations in execution report.

### 8.2 Halt Conditions
- PRD compliance failure
- Circular dependency detection  
- Missing critical meta-files
- Schema-PRD conflict resolution failure
- Build map topological sort failure
- Interface contract misalignment
- Template-to-module mapping conflicts

### 8.3 Recovery Guidance
All execution  reports must include specific, actionable steps for resolution, including:
- Which schema elements are missing from diagrams
- Which PRD requirements lack diagram representation
- Which diagram syntax errors need correction
- Which cross-diagram inconsistencies need resolution

---

## 9. Execution Authorization
This prompt authorizes LFC execution under the constraints and requirements specified above. Begin with compliance verification and proceed systematically through all deliverables.