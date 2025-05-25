### README Update Prompt v1.0.0

---

**Objective:** Update all README files in the repository to ensure they are in sync with the latest information from their respective PRDs. The README filenames have the domain name tagged (e.g., `README-logging.md`). The content of each section in the README should be retained, and only the relevant context from the PRD should be summarized and used to update the respective sections.

**Instructions:**

1. **Identify the Relevant Files:**
   - Locate all PRD files (e.g., `module-prd-logging-v1.0.4.md`) in the repository.
   - Identify the corresponding README files (e.g., `README-logging.md`) for each PRD based on the domain name in the filenames.

2. **Extract Information from PRDs:**
   - For each PRD file, extract the relevant context for each section that corresponds to a section in the README file.
   - Each README already has a structure that must be maintained. The intent of the README file is to be a summary of the PRD relevant to each section in the README.
   - For each section in the README, scan for relevant context in the PRD that matches that README section. Summarize the relevant context and replace the existing content in the README section with the compiled summary. Do this for each section in the README file.

3. **Update the README Files:**
   - Replace the existing content of each section in the README file with the summarized relevant context from the corresponding PRD.
   - Ensure that the structure and formatting of the README sections are preserved.

4. **Commit the Changes:**
   - Commit the changes to each README file with a descriptive commit message, e.g., "Update {README} to match latest {PRD}" where {README} and {PRD} are the full filenames.
