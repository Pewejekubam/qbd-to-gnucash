I'll expand the guide to include specific prompt structures and key interaction points. Here's how you should engage with me for each phase:

# 🎯 IR-Based Build System Development Guide with Prompt Templates

## 📋 Milestone 1: IR Schema Definition

### Task 1.1: Core Schema Definition
**Initial Prompt Template**:
```
I'm starting the IR schema definition for the QBD-to-GnuCash converter. Please analyze core-prd-v3.6.3.md and define the basic system-ir.yaml structure that represents:
1. Core system components
2. Module relationships
3. Version binding rules
```

**202505271004 - Result:
```
I'll help you define the IR schema for the QBD-to-GnuCash converter. Let me first analyze the core PRD document to understand the system components and relationships. 

Based on the core PRD and governance model, I'll help you define the IR schema for the QBD-to-GnuCash converter. Let me create the schema that captures the core components, module relationships, and version binding rules.

Let me create a new `system-ir.yaml` file that follows the governance model and core PRD requirements. 

Made changes.



I've created a comprehensive IR schema that captures the system architecture based on the core PRD and governance model. Let me explain the key aspects:

1. **Core System Components**:
   - Defined core orchestrator with its interfaces and error handlers
   - Listed domain-agnostic utils (error_handler, iif_parser, logging)
   - Detailed the accounts module and its submodules with their versions

2. **Module Relationships**:
   - Captured core contracts used across modules (registration, dispatch, logging)
   - Defined dependencies between components
   - Specified module-specific relationships (e.g., accounts module dependencies)

3. **Version Binding Rules**:
   - Set current core (3.6.3) and governance (2.3.10) versions
   - Defined module compatibility requirements
   - Included validation rules for semantic versioning
   - Specified update protocol for version increments

The schema strictly follows the governance model's requirements:
- All components have explicit version numbers
- Module relationships are clearly defined
- Version binding follows semantic versioning rules
- Directory structure matches the core PRD

The IR schema will help enforce:
- Version compatibility between modules
- Proper dependency management
- Consistent interface contracts
- Governance model compliance

Would you like me to explain any specific part of the schema in more detail?
```

**Follow-up Prompt Template**:
```
Based on the initial IR schema, please generate the version resolution rules for:
1. Cross-module dependencies
2. Schema version compatibility
3. Interface contracts versioning
```

**20250527100850 - Result:
```
I'll help you generate the version resolution rules based on our system-ir.yaml schema. Let me create a new file specifically for version resolution rules. 

Made changes.



I've created comprehensive version resolution rules that build upon our system-ir.yaml. Let me explain each section:

1. **Cross-module Dependencies Resolution**:
   - Strict enforcement of version compatibility between modules
   - Direct dependency rules ensure major version alignment and minimum minor version requirements
   - Transitive dependency resolution with clear conflict resolution strategy
   - Specific version ranges for core and each module
   - Fallback and conflict resolution strategies defined

2. **Schema Version Compatibility**:
   - Clear rules for when to increment major/minor/patch versions for schema changes
   - Backward compatibility requirements (supports 2 versions back)
   - Automatic vs manual upgrade paths defined
   - Compatibility matrix between core and module versions
   - Migration rules for schema evolution

3. **Interface Contracts Versioning**:
   - Separate rules for public and internal interfaces
   - Clear versioning triggers for each change type (signature, return types, parameters)
   - Strong stability guarantees for public APIs
   - Deprecation policy with minimum notice periods
   - Version lock enforcement with specific exceptions for security/critical fixes

Key Features:
- All rules align with governance model v2.3.10
- Strong version lock enforcement with clear exceptions
- Automated validation at multiple stages (pre-commit, CI, release)
- Clear upgrade paths and compatibility requirements
- Comprehensive deprecation and breaking change policies

The rules ensure that:
1. Modules can't be used with incompatible versions of core or other modules
2. Schema changes are properly versioned and migrated
3. Interface changes follow strict semantic versioning
4. Breaking changes are clearly identified and managed

Would you like me to elaborate on any specific aspect of these rules?
```


### Task 1.2: Interface Contract Extraction
**Initial Prompt Template**:
```
Using the accounts module (module-prd-accounts-v1.1.1.md) as our first target, please:
1. Extract all interface contracts
2. Define the data structure schemas
3. Map the dependencies
This will serve as our template for other modules.
```

**20250527102018 - Result:
```
I'll help you analyze the accounts module and extract the required information. Let me first look at the accounts module PRD. 

Made changes.



I've created a comprehensive interface definition for the accounts module that can serve as a template for other modules. Let me explain the key aspects:

1. **Interface Contracts**:
   - Core module contract with entry point (`run_accounts_pipeline`)
   - Input/output contracts using TypeScript/JSON Schema
   - Public interface definitions with full type annotations
   - Exception handling specifications
   - Clear input/output path contracts

2. **Data Structure Schemas**:
   - Account Record schema (TypeScript interface)
   - Mapping File schema (JSON Schema)
   - GnuCash CSV output schema (JSON Schema)
   - All with required/optional fields clearly marked

3. **Dependencies Map**:
   - Direct module dependencies with versions
   - Common utility dependencies
   - Configuration file dependencies
   - Clear purpose and interfaces for each dependency

Key Features:
- Strict version compatibility requirements
- Clear validation rules at each stage
- Input/output formats
- Error handling contracts
- Path and configuration management

This template:
1. Follows PRD governance model v2.3.10
2. Maps to core PRD v3.6.3 requirements
3. Provides clear interfaces for agentic processing
4. Maintains separation of concerns

Would you like me to:
1. Explain any specific part in more detail?
2. Show how this template can be adapted for other modules?
3. Add any additional aspects to the interface definition?
```

## 📋 Milestone 2: Validation Framework

### Task 2.1: PRD Validator
**Initial Prompt Template**:
```
Based on prd-governance-model-v2.3.10.md, please create a validation ruleset that:
1. Verifies PRD structure compliance
2. Validates cross-references
3. Checks version compatibility
Start with the core validator class structure.
```

**20250527103117 - Result:
```
Summarized conversation historyI'll help you create a validation ruleset based on the governance model. First, I'll check the governance model document to understand the requirements. Summarized conversation historyI'll help create a validation ruleset based on the PRD governance model. Let me first search for the governance model content to understand the requirements. 

Based on the search results, I'll create a PRD validator that enforces the governance model rules. The validator should:

1. Check file naming and location according to Section 5.4
2. Validate PRD structure and formatting per Sections 2 and 4
3. Check version declaration and changelog format per Section 5
4. Validate cross-references per Section 8

Let me create the validator: 

Made changes.



I've created a PRD validator that implements the rules from the governance model. Here are the key features:

1. File Naming & Location Validation:
- Enforces correct PRD types (module, core, governance)
- Validates domain names against the authoritative list
- Checks file location in proper directory structure
- Enforces filename format rules

2. Structure Validation:
- Requires horizontal rule separators between major sections
- Validates sequential section numbering
- Checks subsection hierarchy 
- Enforces correct header formatting

3. Version Handling:
- Validates semantic version format
- Ensures version consistency between filename and metadata
- Checks changelog format and chronological ordering
- Validates version declarations in cross-references

4. Cross-Reference Validation:
- Requires relative paths for internal references
- Validates reference targets exist
- Supports http(s) URLs for external references
- Ensures proper link formatting

5. Error Types:
- `ValidationError` - Base class for all validation errors
- `StructuralError` - For document structure issues
- `ReferenceError` - For cross-reference problems
- `VersionError` - For version-related violations

The validator can be used by calling `validate_prd()` with a path to a PRD file, which will return a list of validation errors if any are found.

Should I add any test cases to verify the validation rules?
```


**20250527111111 - Result
```
I agree we should implement a minimal test suite as a safety net. The focus should be on critical validation paths that could cause system-wide issues if they fail. Let me create a minimal but effective test suite for both validators. 

Made changes.

Made changes.

Made changes.



I've created a minimal but effective test suite that focuses on critical validation paths:

1. Schema Validator Tests (`test_schema_validator.py`):
- JSON Schema validation
- TypeScript interface validation
- Schema extraction accuracy
- Error message clarity

2. PRD Validator Tests (`test_prd_validator.py`):
- PRD structure validation
- Version number validation
- Section numbering
- Cross-reference validation
- Metadata field validation
- Domain name validation
- Error message clarity

3. Test Utilities (`test_utils.py`):
- Common test setup utilities 
- Test data templates
- Helper functions

Key test coverage:
1. Schema Accuracy:
- Valid/invalid JSON Schema detection
- Valid/invalid TypeScript interface detection
- Property type validation
- Required field validation

2. Dependency Resolution:
- Cross-reference validation
- Version compatibility checking
- Path resolution testing

3. Governance Compliance:
- Structure verification
- Version format validation
- Metadata requirements
- Domain validation

4. Error Handling:
- Clear error messages
- Proper error classification
- Error location reporting

The test suite is minimal but covers the most critical paths that could cause issues if they fail. Would you like me to:

1. Add more test cases for specific scenarios?
2. Add integration tests between the two validators?
3. Move on to documenting the validation framework?
```

**20250527111649 - Result
```
I'll create comprehensive documentation for the validation framework, focusing on both the PRD and schema validators. 

Made changes.

Made changes.



I've created comprehensive documentation for the validation framework:

1. README.md:
- Full framework overview
- Component descriptions
- Usage examples
- Error types
- Testing information
- Best practices
- Troubleshooting guide
- Future enhancements

2. `quickstart.py`:
- Ready-to-use example code
- Common validation scenarios
- Pretty result printing
- Directory validation support
- Command-line interface

The documentation covers:

1. Core Components:
- PRD Validator
- Schema Validator
- Test Framework

2. Usage Patterns:
- Single file validation
- Directory validation
- Schema validation
- Error handling

3. Rules & Requirements:
- Document structure
- Version enforcement
- Domain rules
- Dependencies
- AI agent compliance
- Governance authority

4. Practical Guidance:
- Best practices
- Common issues
- Troubleshooting steps
- Example code

Would you like me to:
1. Add more examples to the documentation?
2. Create additional usage scenarios?
3. Move on to the next development task?
```


**Implementation Prompt**:
```
Let's implement the first validation component for [specific aspect].
Requirements:
1. [List specific requirements]
2. [Error handling approach]
3. [Expected validation outputs]
```

**20250527103726 - Result:
```
Based on the governance model's requirements and dependencies, I recommend we start with implementing the Version Validation component first. This is because version compatibility is foundational to the entire PRD system and is referenced by other validation rules. Let me propose specific requirements:

Let's implement the Version Validation component:

Requirements:
1. Version Format Validation:
   - Version must follow vX.Y.Z format (from §5.1)
   - All components (X,Y,Z) must be integers ≥ 0 (from §5.4.3)
   - Version must be consistent between filename and metadata (from §5.1)

2. Version Compatibility:
   - Module PRDs must declare compatible core PRD version (from §7.2)
   - Cross-version references require explicit version-lock (from §8.2)
   - Module versions must be appropriate for their changes (from §5.2)

3. Version Update Rules:
   - Major (X) for backward-incompatible changes
   - Minor (Y) for backward-compatible additions
   - Patch (Z) for backward-compatible fixes

Error Handling Approach:
- Use `VersionError` for all version-related violations
- Provide specific error messages identifying the exact rule violation
- Include both the invalid value and expected format in error messages
- Return all version-related errors, not just the first one found

Expected Validation Outputs:
1. Success: Empty list of errors
2. Failure: List of `VersionError` instances with:
   - Error message explaining the violation
   - Location of the error (filename vs metadata)
   - Expected vs actual version format
   - Related PRD version for compatibility errors

Let me implement this component by enhancing the version validation in our existing validator: 

Let me enhance the version validation by adding version compatibility checks and semantic versioning enforcement: 
````

````


Made changes.



I've enhanced the version validation with the following additions:

1. Enhanced `PRDVersion` class:
   - Stricter version format validation
   - Added compatibility checking method
   - Better error messages with expected format

2. Added `PRDReferenceInfo` class to track referenced PRDs and their versions

3. Added new validation methods:
   - `validate_version_compatibility()`: Ensures module PRDs declare and maintain compatibility with core PRD
   - `validate_version_references()`: Verifies all cross-references use version locking
   - `validate_semantic_versioning()`: Enforces semantic versioning rules for version increments

4. Improved error handling:
   - Maintains a list of errors instead of failing on first error
   - More detailed error messages with context
   - Groups related version errors

5. Added helper methods:
   - `_get_changelog_versions()`: Extracts version history
   - `_get_changelog_summary()`: Gets changelog entry for version validation
   - `is_module_prd()`: Determines if file is a module PRD

The validator now enforces these key rules from the governance model:
- Version format must be vX.Y.Z with non-negative integers
- Module PRDs must declare compatible core PRD version
- Cross-references must use version locking
- Version increments must follow semantic versioning rules
- Breaking changes must be documented for major version bumps
- New features must be documented for minor version bumps

Would you like me to:
1. Add test cases to verify these validation rules?
2. Add more specific version compatibility checks?
3. Move on to implementing another validation component?
```

**20250527104715 - Result:
```
Based on the key validation requirements from the governance model, let's implement the Structural Validation component next, focusing on strict section formatting and numbering rules from §2 Structural Rules.

Looking at the current code, we already have basic structural validation, but it needs to be enhanced to handle:
1. Stricter header format validation
2. Subsection depth validation
3. Horizontal rule placement validation
4. Section immutability verification

Let me enhance the structural validation: 
```


Made changes.


```


I apologize for the formatting issue. Let me fix that and add a few more structural validation methods: 
````

````


Made changes.



I've enhanced the structural validation with more comprehensive checks based on §2 of the governance model. Key improvements:

1. Section Header Formatting (§2.1):
   - Major sections must follow `## N. Title` format
   - Subsections must follow `### N.M Title` format
   - Subsubsections must follow `#### N.M.P Title`
   - Titles must start with capital letter
   - Sequential numbering enforcement

2. Section Delimiters (§2.3):
   - Horizontal rules must delimit major sections
   - No consecutive horizontal rules
   - Proper section opening/closing
   - No stray horizontal rules

3. Section Numbering (§2.1):
   - Strict sequential numbering enforcement
   - Proper subsection hierarchy
   - No skipped numbers
   - Proper parent-child relationships

4. Content Rules (§2.2 & §4):
   - No HTML tags (except special tooling tags)
   - Proper title capitalization
   - Proper section structure

The validator now splits these concerns into separate methods for better organization and adds more detailed error messages.

Would you like me to:
1. Add test cases for these structural rules?
2. Add more specific content validation rules?
3. Move on to implementing the next validation component?
```

**20250527105458 - Result
```
Let me check the governance model to see what other validation requirements we need to implement: Summarized conversation historyLet me search through the governance model to check for any validation rules we haven't implemented yet. 

Based on the search results, I notice we haven't implemented validation for several important rules from the governance model. Here are the key areas that need to be added:

1. AI Agent Compliance (Section 9):
- Validate that interface definitions use only acceptable formats (TypedDict, JSON Schema, strict enums)
- Check for explicit exception types, exit codes and validation suites
- Validate deterministic logging with no heuristic assumptions

2. Update Discipline (Section 6):
- Validate targeted edits only modify intended logic 
- Check that insertions occur in correct semantic locations
- Verify renumbering consistency across sections

3. Domain Validation (Section 3.1):
- Validate that all domain names use snake_case 
- Verify domains match the authoritative list
- Check for properly capitalized names

Let me add these validation rules. I'll start with the domain validation since it's foundational: 
````

````


Made changes.



Now I'll add validation for update discipline rules: 
````

````


Made changes.



I've added validation for the remaining key sections from the governance model:

1. Domain Validation (Section 3):
- Added `VALID_DOMAINS` constant with the authoritative domain list
- Added `validate_domain_name()` to check:
  - snake_case format
  - Domain exists in authorized list
  - Proper filename format

2. Update Discipline Validation (Section 6):
- Added `validate_update_discipline()` which performs:
  - `_validate_targeted_edits()` - Checks changelog for broad/untargeted changes
  - `_validate_ordered_insertion()` - Verifies sections are in logical order
  - `_validate_renumbering_consistency()` - Ensures no gaps in numbering

3. AI Agent Compliance (Section 9):
- Added interface validation in `_validate_interface_definitions()`
  - Checks for TypedDict, JSON Schema, or strict enums
  - Flags non-compliant interface definitions
- Added error contract validation in `_validate_error_contracts()`
  - Verifies presence of exit codes
  - Verifies exception definitions
  - Checks for explicit error contracts

These validations are now integrated into the main `validate_all()` method. The validator will check:

1. Structural requirements (already implemented)
2. Version controls (already implemented)  
3. Domain rules (newly added)
4. Update discipline (newly added)
5. AI agent compliance (newly added)

The validator should now fully enforce all governance rules from sections 2-9 of the governance model.

Should I add any additional validation rules from other sections of the governance model?
```

**2025055759 - Result
```
I'll search through the remaining sections of the governance model to identify any validation rules we haven't implemented yet. 

Based on the search results, there are three remaining sections from the governance model that need additional validation rules:

1. Governance Authority (Section 10):
- Validation of precedence order (governance > core > module)
- Enforcement of no governance overrides without formal revision

2. Compliance Enforcement (Section 11):
- AI agent affirmation checking
- Human validation requirements
- Invalidation trigger handling

3. Metadata Requirements:
- Validation of all required metadata fields
- Check for unresolved placeholders

Let me implement these remaining validation rules: 
````

````


Made changes.



I've added three new validation methods to handle the remaining requirements from the governance model:

1. `validate_metadata()`: 
- Checks for all required metadata fields
- Verifies no unresolved placeholders remain
- Additional fields required for module PRDs
- Ensures metadata matches template format

2. `validate_governance_authority()`:
- Enforces the precedence order (governance > core > module)
- Prevents governance overrides without formal revision
- Checks for proper precedence declaration in extensions
- Validates against attempts to bypass governance rules

3. `validate_compliance_requirements()`:
- Validates AI agent compliance affirmation
- Checks for required validation requirements sections
- Ensures all required validation types are present
- Enforces human validation requirements

The validator now fully implements all requirements from the governance model sections 1-12, including:
- Structural rules (§2)
- Domain validation (§3)
- Formatting protocols (§4)
- Version enforcement (§5)
- Update discipline (§6)
- Modular PRD definition (§7)
- Dependencies (§8)
- AI agent compliance (§9)
- Governance authority (§10)
- Compliance enforcement (§11)
- Numbering example validation (§12)

All validation errors will trigger document invalidation as required by §11.3.

Would you like me to add test cases to verify these validation rules?
```



### Task 2.2: Schema Validator
**Initial Prompt Template**:
```
Using the schema definitions from Milestone 1, please create:
1. The base schema validator structure
2. Type checking rules
3. Interface contract validation logic
Focus on the core validation engine first.
```

## 📋 Milestone 3: IR Generator Development

### Task 3.1: PRD Parser Development
**Initial Prompt Template**:
```
Let's develop the PRD parser component. Please analyze:
1. The PRD markdown structure
2. Interface definition patterns
3. Cross-reference formats
And provide the initial parser class structure.
```

**Implementation Prompts Series**:
```yaml
Stage 1:
  Focus: "Base parser implementation for PRD sections"
  Validation: "Section extraction accuracy"

Stage 2:
  Focus: "Interface contract extraction"
  Validation: "Contract completeness"

Stage 3:
  Focus: "Dependency resolution"
  Validation: "Graph completeness"
```

### Task 3.2: IR Builder Component
**Initial Prompt Template**:
```
Based on our parser output, let's create the IR builder that:
1. Assembles parsed components
2. Resolves version dependencies
3. Generates the complete IR
Please provide the core builder structure.
```

## 📋 Milestone 4: Code Generation Engine

### Task 4.1: Template Engine
**Initial Prompt Template**:
```
Using accounts.py as our reference implementation, please design:
1. The template structure for module generation
2. Code block templates
3. Output formatting rules
Focus on maintaining our current code style and patterns.
```

**Component Prompts**:
```yaml
Template Definition:
  Request: "Create the base template for [module type]"
  Context: [Specific requirements/patterns]

Code Generation:
  Request: "Implement generator for [component]"
  Validation: [Expected output format]
```

### Task 4.2: Module Generator
**Initial Prompt Template**:
```
Let's create the module generator using accounts.py as our prototype.
Please design:
1. The module generation pipeline
2. Test generation system
3. Documentation generator
```

## 📋 Milestone 5: Integration and Testing

### Task 5.1: System Integration
**Initial Prompt Template**:
```
We're ready to integrate components. Please provide:
1. Integration pipeline structure
2. Checkpoint system design
3. Component interaction patterns
Start with the high-level integration architecture.
```

### Task 5.2: Validation Suite
**Final Implementation Prompt**:
```
Let's implement the end-to-end validation suite that:
1. Verifies full system operation
2. Validates all checkpoints
3. Generates compliance reports
```

# 🔄 Key Interaction Points

For each component, use this meta-prompt structure:
```yaml
Task:
  Component: [Specific component name]
  Stage: [Development stage]
  Context: [Current state/requirements]
  
Request:
  Action: [Specific action needed]
  Input: [Required resources]
  Expected_Output: [Desired outcome]
  
Validation:
  Criteria: [Success metrics]
  Tests: [Required validations]
  Acceptance: [Pass/fail conditions]
```

# 📊 Progress Tracking Prompt
Use this after each major component:
```yaml
Status_Update:
  Component: [Component name]
  Progress: [Percentage complete]
  Blockers: [Current issues]
  Next_Steps: [Immediate actions needed]
```

Would you like me to elaborate on any specific prompt structure or provide an example of how to use one of these templates for a specific task?