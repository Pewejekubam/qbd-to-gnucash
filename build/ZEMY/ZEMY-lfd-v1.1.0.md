flowchart TD
    A[Input Artifacts Received] --> B{Execution Spark Triggered?}
    B -->|No| C[Wait for Artifacts]
    C --> A
    B -->|Yes| D[Verify Initiation Conditions]
    
    D --> E{All Conditions Met?}
    E -->|input_received: false| F[Await Input Processing]
    E -->|validation_checkpoints_engaged: false| G[Engage Validation Checkpoints]
    E -->|compliance_thresholds_preloaded: false| H[Preload Compliance Thresholds]
    F --> D
    G --> D
    H --> D
    
    E -->|All True| I[Process Named Artifacts]
    I --> J[Extract Structural Requirements]
    J --> K[Initialize Predictive Drift Analysis]
    
    K --> L[Check Weight Scores vs Thresholds]
    L --> M{Weight Score > Threshold?}
    M -->|Role Isolation: >4.0| N[Increase Separation Weighting]
    M -->|Drift Enforcement: >5.0| O[Adjust Compliance Weight Dynamically]
    M -->|Within Limits| P[Proceed to Validation]
    
    N --> Q[Increment Cycle Count]
    O --> Q
    Q --> R{Cycle Count < Max Iterations?}
    R -->|Yes| L
    R -->|No| S[Force Refinement Cycle]
    S --> L
    
    P --> T[Execute Role Isolation Check]
    T --> U{Execution Logic Separated?}
    U -->|No| V[Apply Corrective Measures]
    V --> Q
    U -->|Yes| W[Validate Compliance Status]
    
    W --> X{All Thresholds Satisfied?}
    X -->|No| Y[Continue Iteration Cycle]
    Y --> Q
    X -->|Yes| Z[Set execution_finalized: true]
    
    Z --> AA[Generate Compliance Status Report]
    AA --> BB[Produce Fully Baked ZEMY File]
    BB --> CC[Enable Agentic Codegen Transition]
    CC --> DD[PROCESS COMPLETE]
    
    style A fill:#e1f5fe
    style DD fill:#c8e6c9
    style Z fill:#fff3e0
    style X fill:#fce4ec
    style M fill:#f3e5f5
    style R fill:#e8f5e8