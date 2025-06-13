# Change Request CR-003: Module Console Logging Standards

**Document Version:** CR-003-v1.0.0  
**Change Request ID:** CR-003  
**Target Document:** Module PRD Template (All Future Module PRDs)  
**Author:** Development Team  
**Date:** 2025-06-12  
**Status:** Draft  

---

## 1. Overview
Establish standardized console logging conventions for module PRDs to ensure consistent user experience across horizontal module scaling while preserving domain autonomy and separation of concerns.

---

## 2. Rationale
- **Horizontal Scaling:** Prepare for future modules (sales_tax, customers, vendors, etc.) with consistent console output patterns
- **User Experience:** Provide scannable, hierarchical console logs that clearly show processing flow
- **Domain Autonomy:** Maintain module control over their specific console messaging without core infrastructure changes
- **Pattern Consistency:** Create "soft standards" that guide without constraining module innovation

---

## 3. Proposed Changes

### 3.1 New Section Addition to Module PRD Template
Add new section **"Console Logging Standards"** after existing **"Logging & Observability"** section:

#### Console Logging Standards
This module shall follow established console logging conventions to maintain consistency across the conversion tool while preserving domain-specific autonomy.

**Hierarchical Tag Convention:**
- `[DOMAIN]` - Main module orchestration and entry point logging
- `[DOMAIN-SUBFUNCTION]` - Sub-function processing within the domain
- `[PIPELINE]` - Reserved for core pipeline-level messaging (not used by modules)

**Implementation Requirements:**
- All console logging shall use centralized logging functions (`log_user_info()`, `log_user_error()`, etc.)
- Modules control their own tag content and sub-function breakdown
- Tags shall be included in message content, not enforced by core infrastructure
- Sub-function naming reflects domain-specific processing phases

**Examples for [DOMAIN] Module:**
```
[DOMAIN] Starting [domain] processing with X records
[DOMAIN-MAPPING] Loaded baseline mapping: X types
[DOMAIN-VALIDATION] Validation completed - X records validated  
[DOMAIN-EXPORT] Generated output file: [domain].csv (X bytes)
```

**Tag Naming Guidelines:**
- Use UPPERCASE for domain names
- Use descriptive sub-function names (MAPPING, VALIDATION, EXPORT, etc.)
- Maintain consistency within module but allow domain-specific variations
- Keep tags concise for console readability

### 3.2 Implementation Notes
- **No Core Changes Required:** Uses existing centralized logging infrastructure
- **Domain Flexibility:** Modules determine their own sub-function breakdown
- **Scalability:** Pattern applies to any future module without modification
- **PRD Compliance:** Maintains separation of concerns and centralized logging requirements

---

## 4. Impact Assessment

### 4.1 Affected Components
- **Module PRD Template:** Add new console logging standards section
- **Future Module PRDs:** Implement console logging conventions per template
- **Existing Module PRDs:** Optional alignment with new standards during routine updates

### 4.2 Non-Affected Components
- **Core PRD:** No changes required - already compliant with centralized logging
- **Governance Model:** No changes required
- **Logging Framework PRD:** No changes required
- **Core Infrastructure:** No code changes needed

### 4.3 Benefits
- **Consistent User Experience:** Scannable, hierarchical console output across all modules
- **Developer Guidance:** Clear pattern for implementing console logging in new modules
- **Maintainability:** Standardized approach without architectural coupling
- **Future-Proofing:** Scales horizontally to any number of future modules

---

## 5. Implementation Timeline
- **Phase 1:** Update Module PRD Template with console logging standards section
- **Phase 2:** Apply standards to next module development (sales_tax)
- **Phase 3:** Optional alignment of existing modules during routine PRD updates

---

## 6. Approval Requirements
- **Technical Review:** Validate approach maintains separation of concerns
- **PRD Governance:** Ensure compliance with existing governance standards
- **Module Domain Experts:** Confirm approach supports domain autonomy requirements

---

## 7. References
- **Core PRD v3.9.1 Section 7.3:** Logging Strategy requirements
- **Logging Framework PRD v1.0.5:** Centralized logging compliance
- **Governance Model v2.7.0:** PRD structural requirements and change control