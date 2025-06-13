# QBD to GnuCash Conversion Tool

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![PRD Governance](https://img.shields.io/badge/PRD-v2.7.0-green.svg)](prd/prd-governance-model-v2.7.0.md)
[![Core Architecture](https://img.shields.io/badge/Core-v3.9.1-blue.svg)](prd/core-prd-main-v3.9.1.md)

> **Enterprise-grade financial data migration from QuickBooks Desktop to GnuCash with intelligent mapping workflows and comprehensive audit trails.**

## 🚀 Overview

**QBD to GnuCash Conversion Tool** is a modular, command-line solution designed for professional migration of financial data from QuickBooks Desktop (QBD) to GnuCash. Built with enterprise requirements in mind, it features intelligent account mapping, user-guided workflows for unmapped data types, and comprehensive logging for audit compliance.

### Key Differentiators
- **🎯 Zero Data Loss:** Systematic preservation of all QuickBooks field data with source record tracking
- **🧠 Intelligent Mapping:** AI-compatible text-based workflow with QuickBooks path hints for unmapped accounts
- **📊 Enterprise Logging:** Domain-tagged console output with searchable debug logs for complete audit trails
- **🔧 Modular Architecture:** Extensible framework supporting multiple QuickBooks data domains
- **📋 PRD-Governed:** Agentic-compatible specifications enabling autonomous development and maintenance

---

## 📋 Table of Contents

- [Features](#-features)
- [Quick Start](#-quick-start)
- [Architecture](#-architecture)
- [Text-Based Mapping Workflow](#-text-based-mapping-workflow)
- [Console Logging System](#-console-logging-system)
- [Module Development](#-module-development)
- [File Structure](#-file-structure)
- [Requirements](#-requirements)
- [Contributing](#-contributing)
- [Documentation](#-documentation)
- [License](#-license)

---

## ✨ Features

### **Core Capabilities**
- **📁 Content-Based Processing:** Automatic detection and routing of QuickBooks data sections (ACCNT, CUST, TRNS, etc.)
- **🗺️ Intelligent Account Mapping:** Baseline configurations with user-guided mapping for unmapped account types
- **🔄 HALT Condition Management:** Graceful pipeline suspension for required user interactions
- **📈 GnuCash CSV Generation:** Direct output compatible with GnuCash import requirements
- **🏗️ Double-Entry Structure:** Proper accounting hierarchy construction with placeholder promotion

### **Enhanced User Experience**
- **🎨 Domain-Tagged Console Output:** Visual navigation with `[CORE]`, `[ACCOUNTS-PIPELINE]`, `[IIF-PARSER]` context tags
- **⚡ ASCII-Compliant Logging:** Universal terminal compatibility across all platforms
- **🔍 Searchable Error References:** Console messages coordinate with precise debug log locations
- **📝 QBD Path Hints:** Original QuickBooks account names provided for informed mapping decisions
- **🗂️ Generational File Management:** Automatic archiving of completed mapping sessions

### **Developer & Enterprise Features**
- **📚 PRD-Governed Architecture:** Complete specification-driven development with governance compliance
- **🤖 Agentic Compatibility:** Deterministic documentation enabling AI-assisted development
- **🛡️ Comprehensive Error Handling:** Structured exception management with standardized error codes
- **🔒 Domain Boundary Enforcement:** Strict separation of concerns preventing cross-module violations
- **📊 Audit Trail Compliance:** Complete processing history with structured metadata

---

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- QuickBooks Desktop IIF export files

### Installation
```bash
git clone https://github.com/Pewejekubam/qbd-to-gnucash.git
cd qbd-to-gnucash
```

### Basic Usage
1. **Export from QuickBooks Desktop:**
   - File → Utilities → Export → Lists to IIF Files
   - Select Chart of Accounts and export to `input/` directory

2. **Run the conversion:**
   ```bash
   python src/main.py
   ```

3. **Follow console guidance:**
   - Review discovered files and processing status
   - Complete any unmapped account mapping workflows
   - Verify generated CSV files in `output/` directory

4. **Import to GnuCash:**
   - File → Import → Import Accounts from CSV
   - Select generated `accounts.csv` file

### Example Console Output
```
[CORE] QBD to GnuCash Conversion Tool - Started
[CORE] Discovered 3 IIF files for processing:
[CORE]   * sample-qbd-accounts.IIF
[CORE]   * sample-qbd-customers.IIF
[CORE]   * sample-qbd-items.IIF
[CORE] Pipeline initiated
[ACCOUNTS-PIPELINE] Starting accounts processing with 106 records
[ACCOUNTS-MAPPING] Loaded and validated baseline mapping: 15 accounts
[ACCOUNTS-PIPELINE] Generated output file: output/accounts.csv (2847 bytes)
[ACCOUNTS-PIPELINE] Accounts processing completed successfully
[CORE] Pipeline completed: 1 modules processed successfully from 3 files
```

---

## 🏗️ Architecture

### **Modular Design Pattern**
```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Core Engine   │───▶│  Domain Modules  │───▶│  Output Files   │
│   (Dispatch)    │    │   (Processing)   │    │ (GnuCash CSV)   │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         │                       │                       │
         ▼                       ▼                       ▼
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   IIF Parser    │    │   Text Workflow  │    │   Audit Logs   │
│ (Content-Based) │    │ (User Guidance)  │    │(Debug Details)  │
└─────────────────┘    └──────────────────┘    └─────────────────┘
```

### **Core Components**

| Component | Purpose | Location |
|-----------|---------|----------|
| **Core Engine** | Orchestration, dispatch, and pipeline coordination | `src/core.py` |
| **Domain Modules** | Specialized processing for QBD data types | `src/modules/<domain>/` |
| **IIF Parser** | Content-based parsing of QuickBooks export files | `src/utils/iif_parser.py` |
| **Logging Framework** | Console guidance and debug audit trails | `src/utils/logging.py` |
| **Error Management** | Structured exception handling with error codes | `src/utils/error_handler.py` |

### **Data Flow Pipeline**
1. **Discovery:** Content-based detection of IIF files and section headers
2. **Parsing:** Extraction of structured data with field validation
3. **Dispatch:** Routing to appropriate domain modules via standardized payload
4. **Processing:** Domain-specific transformation with user interaction workflows
5. **Output:** GnuCash-compatible CSV generation with format validation
6. **Audit:** Complete logging with searchable references and error coordination

---

## 🗺️ Text-Based Mapping Workflow

### **Intelligent Unmapped Account Handling**

When the system encounters QuickBooks account types not in the baseline mapping, it initiates an intelligent workflow:

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Detection     │───▶│   Generation     │───▶│   User Edit     │
│ (Unmapped QBD)  │    │ (Questions File) │    │ (Account Paths) │
└─────────────────┘    └──────────────────┘    └─────────────────┘
         ▲                                               │
         │               ┌──────────────────┐           ▼
         └───────────────│   Processing     │◀──────────┘
                         │ (JSON + Archive) │
                         └──────────────────┘
```

### **Enhanced Features**

#### **QBD Path Hints Integration**
```
[MISC_LABOR_INCOME]
QuickBooks import path: Contractor Income
Enter the full GnuCash account path here: Income:Service Revenue:Labor
```

#### **Dual-File System**
- **`accounts_mapping_questions.txt`** — Clean workspace for user editing
- **`accounts_mapping_instructions.txt`** — Comprehensive reference with examples

#### **Advanced Validation**
- **ASCII Compliance:** Immediate HALT on non-ASCII characters with user guidance
- **Input Normalization:** Automatic cleanup of spacing and formatting
- **Partial Completion:** Progress preservation for continued editing sessions
- **Generational Archiving:** Completed files renamed to `accounts_mapping_questions_v###.txt`

### **Example Workflow Session**
```bash
# System detects unmapped accounts
[ACCOUNTS-UNMAPPED-PROCESSING] Found 3 unmapped accounts requiring user input
[ACCOUNTS-UNMAPPED-PROCESSING] Generated questions file: accounts_mapping_questions.txt and accounts_mapping_instructions.txt
[ACCOUNTS-UNMAPPED-PROCESSING] Edit the questions file and restart pipeline to continue
[ACCOUNTS-PIPELINE] Pipeline HALT: User action required for mapping completion

# User completes mapping and restarts
[ACCOUNTS-MAPPING] Successfully parsed 3 account mappings from questions file
[ACCOUNTS-MAPPING] Questions file renamed to accounts_mapping_questions_v001.txt
[ACCOUNTS-PIPELINE] Accounts processing completed successfully
```

---

## 📊 Console Logging System

### **Domain-Tagged Visual Navigation**

The logging system provides enterprise-grade audit capabilities with user-focused console guidance:

#### **Tagging Standards**
- **`[CORE]`** — Core orchestration and file discovery
- **`[{MODULE}-PIPELINE]`** — Domain-specific processing workflows
- **`[{MODULE}-{COMPONENT}]`** — Specialized component operations
- **Two-way radio format:** `[{called-party}-{calling-party}]` for cross-domain communication

#### **HALT Condition Coordination**
```bash
[CUSTOMERS-PIPELINE] Module reports HALT. User action required. See debug log "E0113" around 14:30:52.123
```

#### **Error Code Integration**
- **Console guidance:** User-friendly messaging with specific action requirements
- **Debug coordination:** Millisecond timestamps for precise verbose log navigation
- **Searchable references:** Error codes enable rapid issue diagnosis in verbose logs

### **Logging Philosophy**
- **User-Centric Design:** Each console message serves specific user understanding
- **Minimal but Helpful:** No verbose noise, every message provides value
- **Visual Scanning:** Domain tags enable quick navigation during complex processing
- **ASCII Compliance:** Universal terminal compatibility across all platforms

---

## 🔧 Module Development

### **Template-Driven Development**

New domain modules inherit complete specifications from the governance-compliant template:

```python
def run_customers_pipeline(payload: Dict[str, Any]) -> bool:
    """Standard entry point for customers domain processing."""
    # Template includes complete logging patterns
    log_user_info(f"[CUSTOMERS-PIPELINE] Starting customers processing with {len(payload['records'])} records")
    
    # Domain-specific processing logic
    # ...
    
    return True  # Success indication
```

### **Built-in Standards**
- **Interface Contracts:** Standardized `run_<domain>_pipeline(payload) -> bool` pattern
- **Logging Inheritance:** Console and debug patterns included in template
- **Error Handling:** Automatic integration with centralized error management
- **Domain Boundaries:** Strict separation enforcement with governance validation

### **Roadmap Modules**
- **🎯 Ready for Development:** customers, vendors, items, sales_tax
- **📝 Template Available:** [prd/prd-template-module-v3.7.0.md](prd/prd-template-module-v3.7.0.md)
- **🔧 Framework Support:** Complete infrastructure for autonomous development

---

## 📁 File Structure

```
qbd-to-gnucash/
├── 📂 input/                          # QuickBooks IIF export files
├── 📂 output/                         # Generated GnuCash CSV files & logs
├── 📂 prd/                           # Product Requirements Documents
│   ├── 📄 core-prd-main-v3.9.1.md          # Core architecture specification
│   ├── 📄 prd-governance-model-v2.7.0.md   # Governance framework
│   ├── 📄 prd-template-module-v3.7.0.md    # Module development template
│   ├── 📄 README-core.md                   # Architecture documentation
│   ├── 📂 accounts/                        # Accounts domain specifications
│   │   ├── 📄 module-prd-accounts-v1.3.2.md
│   │   ├── 📄 module-prd-accounts_mapping-v1.4.0.md
│   │   ├── 📄 module-prd-accounts_validation-v1.1.0.md
│   │   ├── 📄 README-accounts.md
│   │   ├── 📄 README-accounts_mapping.md
│   │   └── 📄 README-accounts_validation.md
│   └── 📂 logging/                         # Logging framework specs
│       ├── 📄 module-prd-logging-v1.0.5.md
│       └── 📄 README-logging.md
├── 📂 src/                           # Source code
│   ├── 📄 main.py                         # Application entry point
│   ├── 📄 core.py                         # Core orchestration engine
│   ├── 📂 modules/                        # Domain-specific modules
│   │   └── 📂 accounts/                   # Accounts processing domain
│   │       ├── 📄 accounts.py                  # Main accounts pipeline
│   │       ├── 📄 accounts_export.py           # GnuCash CSV generation
│   │       ├── 📄 accounts_mapping.py          # Mapping configuration & workflow
│   │       ├── 📄 accounts_mapping_baseline.json # Default mapping rules
│   │       ├── 📄 accounts_tree.py             # Hierarchy construction
│   │       └── 📄 accounts_validation.py       # Data validation
│   └── 📂 utils/                          # Cross-domain utilities
│       ├── 📄 error_handler.py               # Centralized exception management
│       ├── 📄 iif_parser.py                  # QuickBooks file parsing
│       └── 📄 logging.py                     # Logging framework
├── 📄 README.md                          # This file
└── 📄 LICENSE                            # MIT License
```

---

## 📋 Requirements

### **System Requirements**
- **Python:** 3.8 or higher
- **Memory:** 256MB minimum (typical datasets)
- **Storage:** 50MB for application + space for input/output files
- **Platform:** Windows, macOS, Linux (cross-platform compatible)

### **Input Requirements**
- **QuickBooks Desktop** IIF export files
- **UTF-8 encoding** with ASCII validation for user input
- **File access** to `input/` and `output/` directories

### **Dependencies**
- **Standard Library Only** — No external package dependencies
- **Self-Contained** — All functionality included in repository

---

## 🤝 Contributing

### **Development Standards**
- **PRD-Governed:** All changes must align with specification documents
- **Domain Boundaries:** Respect modular architecture and separation of concerns
- **Logging Compliance:** Follow established console and debug logging patterns
- **Agentic Compatible:** Maintain deterministic specifications for AI development

### **Contribution Process**
1. **Review PRDs:** Understand governance model and architectural patterns
2. **Follow Template:** Use module template for new domain development
3. **Test Workflows:** Verify text-based mapping and HALT condition handling
4. **Documentation:** Update relevant README files and specifications

### **Module Development Priority**
1. **customers** — Customer data import workflows
2. **vendors** — Vendor data import workflows  
3. **items** — Inventory item processing
4. **sales_tax** — Sales tax code management

---

## 📚 Documentation

### **Architecture & Governance**
- **[Core PRD v3.9.1](prd/core-prd-main-v3.9.1.md)** — Complete system architecture
- **[Governance Model v2.7.0](prd/prd-governance-model-v2.7.0.md)** — Development standards
- **[Module Template v3.7.0](prd/prd-template-module-v3.7.0.md)** — New module development guide
- **[Core Architecture README](prd/README-core.md)** — Console logging specification

### **Domain Modules**
- **[Accounts Module](prd/accounts/README-accounts.md)** — Chart of accounts processing
- **[Mapping Workflow](prd/accounts/README-accounts_mapping.md)** — Text-based mapping system
- **[Validation Framework](prd/accounts/README-accounts_validation.md)** — Data validation standards
- **[Logging Framework](prd/logging/README-logging.md)** — Centralized logging system

### **Technical Specifications**
- **[Interface Contracts](prd/core-prd-main-v3.9.1.md#11-system-architecture-and-workflow)** — API patterns and standards
- **[Error Handling](prd/core-prd-main-v3.9.1.md#14-authoritative-error-classes--error-code-table)** — Comprehensive error management
- **[Module Boundaries](prd/core-prd-main-v3.9.1.md#12-module-ownership-and-directory-boundaries)** — Development guidelines

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🎯 Project Status

| Component | Status | Version | Notes |
|-----------|--------|---------|-------|
| **Core Framework** | ✅ Complete | v3.9.1 | Production ready with full logging |
| **Accounts Module** | ✅ Complete | v1.3.2 | Text workflow, QBD hints, hierarchical processing |
| **Logging System** | ✅ Complete | v1.0.5 | Domain-tagged console & debug coordination |
| **Governance** | ✅ Complete | v2.7.0 | Agentic-compatible specifications |
| **Template System** | ✅ Complete | v3.7.0 | Logging patterns included |
| **Customers Module** | 🔄 Planned | - | Template-ready development |
| **Vendors Module** | 🔄 Planned | - | Template-ready development |
| **Items Module** | 🔄 Planned | - | Template-ready development |

---

<div align="center">

**Built with enterprise standards • Governed by comprehensive PRDs • Ready for autonomous development**

[📚 Documentation](prd/) • [🐛 Issues](https://github.com/Pewejekubam/qbd-to-gnucash/issues) • [💡 Feature Requests](https://github.com/Pewejekubam/qbd-to-gnucash/discussions)

</div>