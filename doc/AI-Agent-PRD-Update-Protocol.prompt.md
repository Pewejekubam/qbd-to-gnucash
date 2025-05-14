---

📐 **AI Agent PRD Update Protocol — Diagnostic Session Enforcement**

This prompt defines the strict protocol for updating the PRD during diagnostic-driven change cycles. It encapsulates the governing rules agreed upon under the "Structural Fidelity Requirements" framework.

### 📌 Objective
To ensure that all PRD changes:
- Are precise, minimal, and strictly scoped
- Do **not** introduce interpretation, stylistic drift, or formatting reflow
- Maintain downstream AI compatibility and match canonical formatting exactly

---

### ✅ Authorized Update Behavior

When proposing a PRD section update during diagnostics, the AI Agent must:

1. **Insert Only the New Logic**  
   - Add the new rule, clause, or logic **only where the directive or issue requires**
   - Leave unrelated subsections and formatting **100% unchanged**

2. **Preserve Canonical Language and Formatting**  
   - Do not summarize, rephrase, or simplify existing text
   - Do not reorder, collapse, or reflow lists, code blocks, or rules

3. **Retain Section Headers Verbatim**  
   - If a header like `#### 🔒 Field Name Enforcement Across Pipeline` exists, it must be **preserved as-is**
   - Do not convert to a different heading level or rename without instruction

4. **Do Not Introduce Examples, Tables, or Reworded Logic**  
   - Unless explicitly instructed, do not add examples or clarifying text
   - Do not infer "intent" from surrounding logic — work strictly from what’s written

5. **Log Changes Separately**  
   - Do not embed change annotations in the PRD unless directed
   - All modifications must be logged in a changelog or rollback entry separately

---

### ❌ Prohibited Update Behaviors

- ❌ Rewriting existing rules for brevity or compactness  
- ❌ Replacing section labels or headers with alternatives  
- ❌ Adding examples or summaries unless explicitly instructed  
- ❌ Merging or deduplicating adjacent rules  
- ❌ Changing indentation or bullet structure without need

---

### 💬 If in Doubt

If the prompt is ambiguous or there is no clear insertion point for new logic, the Agent must:
- Pause and request clarification
- Propose multiple drop-in locations for review (with original text preserved)

---

### 📎 Context

This protocol is now in effect for all update prompts associated with PRD v2.7.3 and all subsequent versions under development during this session.

---
