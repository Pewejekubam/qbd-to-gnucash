## MAPPING DIFF PROCESS - FULL IMPLEMENTATION DISCOVERED

### **COMPLETE WORKFLOW IDENTIFIED:**

#### **TEXT-BASED MAPPING QUESTIONS SYSTEM:**

**Function:** `generate_text_mapping_questions()`
**Output:** `output/accounts_mapping_questions.txt`
**Format:** Super easy-to-edit text file with guided questions

**Example Output:**
```
Where should these accounts go in GnuCash?

PETTY_CASH: 
Is this a child account? (Y/N): 
If yes, parent account name: 

INVENTORY: 
Is this a child account? (Y/N): 
If yes, parent account name: 

================================================================================
INSTRUCTIONS:
1. For each account above, enter the GnuCash account name you want to use
2. If it's a child account, answer Y and provide the parent account path
3. Use colons (:) to separate account levels for deep hierarchies
================================================================================
```

#### **COMPLETE WORKFLOW:**

1. **Detection:** `find_unmapped_types()` identifies missing mappings
2. **Generation:** Creates `accounts_mapping_questions.txt` with simple Q&A format
3. **User Editing:** User fills in account names and hierarchy info
4. **Processing:** `parse_text_mapping_file()` converts text answers to JSON
5. **Integration:** `load_mapping()` merges user answers into baseline config
6. **Archival:** Processed file moved to `_processed.txt` to prevent re-processing

### **PRD SPECIFICATION GAP:**

**Missing from Module PRDs:**
- Text-based workflow documentation
- `generate_text_mapping_questions()` function specification
- `parse_text_mapping_file()` function specification
- User workflow instructions
- File lifecycle management (questions → processed → specific.json)

**RECOMMENDATION:** Add comprehensive text-based mapping workflow specification to accounts_mapping PRD