# Logical Flow Diagram (LFD)

---

## 1. System Overview Diagram
```mermaid
graph TD
    %% Source: core-ir-main-v3.9.1.md, Section 2, 6, 8
    subgraph "Input Processing"
        input_dir(["Input Directory"])
        config_source(("Configuration"))
        input_discovery(["Input Discovery"])
        input_dir -->|"IIF files"| input_discovery
        config_source --> input_discovery
        input_discovery --> section_processing(["Section Processing"])
    end
    %% Source: core-ir-main-v3.9.1.md, Section 2, 6
    subgraph "Core Processing"
        section_processing ==> dispatch_flow(["Dispatch Flow"])
        dispatch_flow ==> accounts_module(["Accounts Module"])
        dispatch_flow ==> other_modules(["Other Domain Modules"])
    end
    %% Source: core-ir-main-v3.9.1.md, Section 2
    subgraph "Output Generation"
        accounts_module --> accounts_export(["Accounts Export"])
        accounts_export --> output_csv({"accounts.csv"})
        output_csv --> result_artifacts(["Result Artifacts"])
    end
    %% Source: module-prd-logging-v1.0.5.md, utils.error_handler
    subgraph "Utilities"
        error_handler([["Error Handler"]])
        logging_service([["Logging Service"]])
    end
    %% Dependency edges
    accounts_module -.-> logging_service
    accounts_module -.-> error_handler
    accounts_export -.-> logging_service
    accounts_export -.-> error_handler
    %% Comments for dependencies
    %% accounts_module depends on logging_service and error_handler (schema, PRD)
    %% accounts_export depends on logging_service and error_handler (schema, PRD)
```

---

## 2. Detailed Execution Flow
```mermaid
graph TD
    %% Source: core-ir-main-v3.9.1.md, Section 2, 4, 5
    start((START)) --> init(["Initialization Sequence"])
    init --> validation(["Validation Gate"])
    validation -->|"valid"| processing(["Processing Pipeline"])
    validation -->|"invalid"| error_handler
    processing --> business_logic(["Business Logic Decisions"])
    business_logic -->|"accounts"| accounts_path(["Accounts Path"])
    business_logic -->|"other domain"| other_path(["Other Domain Path"])
    accounts_path --> output_gen(["Output Generation"])
    other_path --> output_gen
    output_gen --> completion(["Completion Check"])
    completion -->|"more sections"| processing
    completion -->|"complete"| end((COMPLETE))
    accounts_path -.-> logging_service
    output_gen -.-> logging_service
    accounts_path -->|"error"| error_handler
    output_gen -->|"error"| error_handler
    error_handler --> recovery(["Recovery Decision"])
    recovery -->|"recoverable"| processing
    recovery -->|"critical"| halt((HALT))
    %% Comments: All error and logging flows per PRD and schema
```

---

## 3. Module Dependency Graph
```mermaid
graph LR
    %% Source: core-ir-main-v3.9.1.md, module-ir-accounts-v1.1.4.md
    subgraph "Foundation Layer"
        config_loader(["ConfigLoader"])
        logging_service
        error_handler
    end
    subgraph "Processing Layer"
        iif_parser(["IIF Parser"])
        accounts_module
        accounts_mapping(["Accounts Mapping"])
        accounts_tree(["Accounts Tree"])
        accounts_validation(["Accounts Validation"])
        accounts_export(["Accounts Export"])
    end
    subgraph "Output Layer"
        output_csv
    end
    accounts_module -.-> logging_service
    accounts_module -.-> error_handler
    accounts_module --> accounts_mapping
    accounts_module --> accounts_tree
    accounts_module --> accounts_validation
    accounts_module --> accounts_export
    accounts_export --> output_csv
    %% Comments: All dependencies per schema and PRD
```

---

## 4. Data Flow Diagram
```mermaid
graph TD
    %% Source: module-ir-accounts-v1.1.4.md, core-ir-main-v3.9.1.md
    input_dir --> raw_data(["Raw QBD Data"])
    config_source --> raw_data
    raw_data --> parsed_data(["Parsed Data State"])
    parsed_data --> validated_data(["Validated Data State"])
    validated_data --> processed_data(["Processed Data States"])
    processed_data --> transformed_accounts(["Transformed Accounts Data"])
    transformed_accounts --> output_csv
    output_csv --> result_artifacts
    parsed_data -.-> logging_service
    validated_data -.-> logging_service
    transformed_accounts -.-> logging_service
    %% Comments: Data and audit flows per schema
```

---

## 5. Error Flow Diagram
```mermaid
graph TD
    %% Source: core-ir-main-v3.9.1.md, module-ir-accounts-v1.1.4.md
    accounts_module --> error_aggregator(["Error Aggregator"])
    accounts_mapping --> error_aggregator
    accounts_tree --> error_aggregator
    accounts_validation --> error_aggregator
    error_aggregator --> error_classifier(["Error Classifier"])
    error_classifier --> severity_assessor(["Assess Severity"])
    severity_assessor -->|"critical"| critical_handler(["Critical Error Handler"])
    severity_assessor -->|"recoverable"| recovery_handler(["Recovery Handler"])
    severity_assessor -->|"warning"| warning_handler(["Warning Handler"])
    critical_handler --> halt(("HALT EXECUTION"))
    recovery_handler --> recovery_attempt(["Recovery Attempt"])
    recovery_attempt -->|"success"| continue_process(["Continue Processing"])
    recovery_attempt -->|"failure"| escalate_error(["Escalate Error"])
    warning_handler --> continue_process
    escalate_error --> user_intervention(["User Intervention Required?"])
    user_intervention -->|"yes"| pause_execution(("PAUSE FOR INPUT"))
    user_intervention -->|"no"| halt
    continue_process --> main_flow_return(["Return to Main Flow"])
    error_classifier -.-> logging_service
    critical_handler -.-> logging_service
    recovery_handler -.-> logging_service
    escalate_error -.-> notification_system(["Notification System"])
    %% Comments: Error and notification flows per PRD
```

---

## 6. Configuration Flow Diagram
```mermaid
graph LR
    %% Source: core-ir-main-v3.9.1.md, module-prd-logging-v1.0.5.md
    config_file(("ConfigFile")) --> config_loader
    env_vars(("EnvironmentVariables")) --> config_loader
    config_loader --> config_validator(["Configuration Validator"])
    config_validator --> config_distributor(["Configuration Distributor"])
    config_distributor --> app_config(["Application Config"])
    config_distributor --> logging_config(["Logging Config"])
    config_distributor --> mapping_config(["Mapping Config"])
    config_distributor --> export_config(["Export Config"])
    app_config -.- iif_parser
    app_config -.- accounts_module
    logging_config -.- logging_service
    mapping_config -.- accounts_mapping
    export_config -.- accounts_export
    config_validator -->|"invalid_config"| config_error_handler(["Config Error Handler"])
    config_error_handler --> config_error_resolution(["Error Resolution"])
    config_error_resolution -->|"use_defaults"| config_distributor
    config_error_resolution -->|"halt"| halt_config(("HALT"))
    %% Comments: Configuration and error flows per PRD and schema
```

---

## Legend
- **[Node Types]**
  - [Module Name]: Processing modules
  - ((Decision Point)): Branching logic
  - {Result File}: Output artifacts
  - [[Utility Service]]: Shared services (logging, error handler)
  - (Configuration): Config nodes
- **[Edge Types]**
  - `-->`: Data flow (with labels where allowed)
  - `==>`: Control flow (no label)
  - `-.->`: Dependency (no label)
  - `..>`: Error propagation (no label)
  - `-.-`: Configuration flow (no label)
- **All nodes and edges are cross-referenced to authoritative PRD, schema, or meta-file sources via Mermaid comments.**
- **All edge and node names are consistent across diagrams.**
- **Logging and Error Handler are global utilities with multiple inbound edges.**
