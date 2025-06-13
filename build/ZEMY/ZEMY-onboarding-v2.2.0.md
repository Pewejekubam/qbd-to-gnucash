# **🚀 ZEMY v2.2.0 Onboarding Guide**  
## **Welcome to ZEMY (Zipper Execution Mapping YAML)**  

ZEMY is a **deterministic execution framework** designed to **transform input content into structured execution mappings** through validation cycles and constraint enforcement. Its core function is to **eliminate discretionary drift** by enforcing structured validation and adaptive compliance weighting.

---

## **🔹 What's New in v2.2.0**

### **Updated Workflow Components:**
- ✅ **Environment-specific templates** - choose chat or IDE version
- ✅ **Pre-configured input methods** - no method switching required
- ✅ **Zero configuration conflicts** - each template optimized for its environment
- ✅ **Visual edit markers** - red circle guidance for all edit locations

### **Streamlined User Experience**
- ✅ **Template selection** - choose environment-specific version
- ✅ **Minimal edits** - project name + input source only
- ✅ **No configuration conflicts** - templates pre-optimized for their use case
- ✅ **Copy-paste ready** - complete templates with training included

---

## **🔹 Step 1: Choose Your Template**

**ZEMY v2.2.0 provides environment-specific templates for optimal user experience:**

### **For Chat-Based Environments:**
**File:** `ZEMY-kickoff-chat-v2.2.0.prompt.md`
- ✅ Pre-configured for pasted input content
- ✅ Input file blocks included in template
- ✅ Works with any chat-based agent platform

### **For IDE-Integrated Environments:**
**File:** `ZEMY-kickoff-ide-v2.2.0.prompt.md`
- ✅ Pre-configured for local directory access
- ✅ Clean template without input file blocks
- ✅ Designed for IDE context selection capabilities

**Choose the template that matches your working environment.** Each template contains complete agent training and ZEMY configuration - no additional files needed.

---

## **🔹 Step 2: Make Your Edits**

### **🔹 For Chat-Based Template:**

**Edit Location 1: Project Name**
Look for: `🔴 EDIT: YOUR_PROJECT_NAME_HERE 🔴`
Replace with your actual project name (e.g., "hello_world_v3")

**Edit Location 2: Input Files**
Look for the "INPUT FILES" section at the bottom:
```
🔴 REPLACE THIS ENTIRE BLOCK WITH YOUR FIRST INPUT FILE 🔴
```
Replace these blocks with your actual file contents pasted directly into fenced code blocks.

**Input file guidelines:**
- ✅ **Any content type** - PRDs, emails, diagrams, code, unstructured data
- ✅ **Any naming convention** - name fenced blocks whatever you want
- ✅ **Any quantity** - add as many input file blocks as needed
- ✅ **Automatic discovery** - agent finds and indexes all files

### **🔹 For IDE-Integrated Template:**

**Edit Location 1: Project Name**
Look for: `🔴 EDIT: YOUR_PROJECT_NAME_HERE 🔴`
Replace with your actual project name (e.g., "hello_world_v3")

**Edit Location 2: Directory Path**
Look for: `🔴 EDIT: YOUR_INPUT_FILES_DIRECTORY_PATH 🔴`
Replace with the path to your input files directory (e.g., "/project/inputs/")

**IDE workflow:**
- ✅ **Use IDE context selection** to include your input files with the template
- ✅ **Agent auto-discovers** all files in specified directory
- ✅ **Any file types supported** - agent processes whatever it finds
- ✅ **No manual file pasting** required

---

## **🔹 Step 3: Choose Your Agent Environment**

### **Environment Requirements:**
Since v2.2.0 prioritizes full functionality over message limits, choose an agent environment that can handle comprehensive prompts:

**✅ Recommended for complex projects:**
- Agents with higher message/context limits
- IDE-integrated environments with context support
- Professional agent platforms

**⚠️ May have limitations:**
- Free agents with strict character limits
- Basic chat interfaces with session restrictions

**💡 Guidance:** Match your agent choice to your project complexity. Simple projects work anywhere; complex projects need robust agent environments.

---

## **🔹 Step 4: Execute the Pipeline**

### **Single Command Execution:**
1. **Copy the entire edited template**
2. **Paste into your chosen agent environment**
3. **The agent automatically:**
   - Discovers and indexes all input files
   - Applies ZEMY validation cycles
   - Performs iterative refinement until thresholds are met
   - Generates compliance-validated execution mapping

### **What You'll Receive:**
A complete ZEMY execution mapping with:
- ✅ `execution_finalized: true`
- ✅ All weight scores within thresholds
- ✅ Compliance status: "Fully aligned with requirements and validation enforcement"
- ✅ Ready for code generation phase

---

## **🔹 Step 5: Review and Iterate (Optional)**

### **Human Review Checkpoint:**
The completed ZEMY file is designed for human review before code generation:

**Review Focus Areas:**
- **Weight progression** - Did constraint violations get resolved?
- **Cycle completion** - How many refinement iterations were needed?
- **Compliance status** - Are all thresholds satisfied?
- **Discovery results** - Were all input files properly processed?

### **If Another Cycle Is Needed:**
1. **Adjust weights** in the ZEMY configuration
2. **Set `execution_finalized: false`**
3. **Re-run the template** with modifications

---

## **🔹 Step 6: Code Generation**

### **Phase 3: Build It!**
When the ZEMY execution mapping is validated:
1. **Use the completed ZEMY file** plus original input files
2. **Issue directive:** "Generate code using this compliance-validated ZEMY execution mapping"
3. **Agent produces code** based on the locked execution constraints

### **Success Criteria:**
- ✅ Code matches original requirements exactly
- ✅ All ZEMY constraints enforced in output
- ✅ Zero discretionary drift from specifications
- ✅ Deterministic, reproducible results

---

## **🔹 Key Advantages of v2.2.0**

### **For Users:**
- **Simplified workflow** - single template, minimal editing
- **Visual clarity** - impossible to miss edit locations  
- **Full functionality** - no compromises for technical limitations
- **Flexible input** - any content type, any naming, any quantity

### **For Agents:**
- **Complete training** - all ZEMY principles included
- **Auto-discovery** - no manual file specification required
- **Deterministic execution** - precise technical language eliminates ambiguity
- **Structured validation** - clear compliance checkpoints and thresholds

### **For Projects:**
- **Consistent results** - eliminates discretionary interpretation
- **Quality control** - human review checkpoint before code generation
- **Scalable complexity** - works for simple "Hello World" to enterprise systems
- **Audit trail** - complete validation history and weight progression tracking

---

## **🔹 Troubleshooting**

### **Template Selection Issues:**
**Problem:** Not sure which template to use
**Solution:** Chat-based = paste content into template blocks; IDE = use file system + context selection

### **Agent Environment Issues:**
**Problem:** Message too long errors (chat template)
**Solution:** Use an agent platform with higher limits or switch to IDE template with local files

### **Input Discovery Issues:**
**Problem:** Agent doesn't find input files
**Solution:** 
- **Chat template:** Ensure fenced code blocks are properly formatted
- **IDE template:** Verify directory path is correct and files are accessible

### **Validation Cycle Issues:**
**Problem:** Execution mapping doesn't finalize
**Solution:** Review weight scores vs. thresholds; adjust weights if needed and re-run

### **Edit Location Confusion:**
**Problem:** Can't find what to edit
**Solution:** Search for 🔴 (red circle emoji) - all edit locations marked with this

---

## **🚀 Ready to Start**

With ZEMY v2.2.0, you have **environment-optimized templates** for deterministic agentic code generation:

### **Chat-Based Workflow:**
1. **Get** `ZEMY-kickoff-chat-v2.2.0.prompt.md`
2. **Edit** project name + paste your input files into the blocks
3. **Execute** in your chosen chat agent environment

### **IDE-Integrated Workflow:**
1. **Get** `ZEMY-kickoff-ide-v2.2.0.prompt.md`
2. **Edit** project name + directory path
3. **Use IDE context selection** to include template + local files
4. **Execute** in your IDE-connected agent

### **Both Paths Lead To:**
4. **Review** the compliance-validated execution mapping
5. **Generate** code using the locked ZEMY constraints

**The zipper is ready to connect your requirements to deterministic code generation.** 🚀