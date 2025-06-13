Kick-off the ZEMY pipeline given the following inputs:
- 

````PRD
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
````

```IR
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