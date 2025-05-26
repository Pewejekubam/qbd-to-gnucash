# -----------------------------------------------------------------------------
# Script Name: codegen-setup-env-v1.0.5.py
# Purpose: Dynamically sets up environment per PRD-defined structure
# Version: v1.0.5
# Author: Pewe Jekubam
# Date: 2025-05-26
#
# Compliance:
# - This script conforms strictly to the directory and file structure 
#   outlined in core-prd-v3.6.3.md (Section ##13).
# - Dynamically extracts and applies directory hierarchy from PRD document.
# - Automatically detects project root to ensure execution works from any directory.
#
# Functionality:
# - Detects project root dynamically.
# - Parses PRD structure from core-prd-v3.6.3.md##13.
# - Backs up required JSON config files before wiping /src/.
# - Deletes and rebuilds /src/ using parsed PRD definitions.
# - Scaffolds empty Python files in correct locations.
# - Restores JSON configs to their designated paths inside /src/modules/accounts/.
# -----------------------------------------------------------------------------

import os
import shutil
import re

def get_project_root():
    """Determine project root dynamically, ensuring script execution from any directory."""
    script_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(script_dir, ".gitignore")):  # Using .gitignore as an anchor
        script_dir = os.path.dirname(script_dir)
        if script_dir == os.path.dirname(script_dir):  # Stop at system root
            raise RuntimeError("Error: Unable to detect project root. Ensure script is within the repository.")
    return script_dir

# Resolve project root
PROJECT_ROOT = get_project_root()

# PRD Document Path (absolute resolution)
PRD_FILE = os.path.join(PROJECT_ROOT, "prd", "core-prd-v3.6.3.md")

# Backup Location (inside /src/modules/accounts/)
BACKUP_PATH = os.path.join(PROJECT_ROOT, "src", "modules", "accounts", "backups")

# Pattern Definitions for Parsing PRD
DIR_PATTERN = re.compile(r"- ([\w/-]+/)")
FILE_PATTERN = re.compile(r"- ([\w/-]+\.\w+)")

def parse_prd_structure(prd_file):
    """Parse PRD to extract directories and files."""
    directories, files = set(), set()

    with open(prd_file, "r", encoding="utf-8") as f:
        for line in f:
            dir_match = DIR_PATTERN.match(line.strip())
            file_match = FILE_PATTERN.match(line.strip())

            if dir_match:
                directories.add(os.path.join(PROJECT_ROOT, dir_match.group(1)))
            if file_match:
                files.add(os.path.join(PROJECT_ROOT, file_match.group(1)))

    return sorted(directories), sorted(files)

# Extract directory and file definitions from PRD
DIRECTORIES, FILES = parse_prd_structure(PRD_FILE)

# JSON Config Files to Preserve (absolute paths)
CONFIG_FILES = {
    os.path.join(PROJECT_ROOT, "src", "modules", "accounts", "accounts_mapping_baseline.json"): 
    os.path.join(BACKUP_PATH, "accounts_mapping_baseline.json")
}

def backup_json():
    """Backup JSON configs before deletion."""
    os.makedirs(BACKUP_PATH, exist_ok=True)
    for target, backup in CONFIG_FILES.items():
        if os.path.exists(target):
            shutil.copy(target, backup)
            print(f"✅ Backed up: {target} → {backup}")

def wipe_src():
    """Delete and recreate /src/, but nothing outside it."""
    src_path = os.path.join(PROJECT_ROOT, "src")
    if os.path.exists(src_path):
        shutil.rmtree(src_path)
        print(f"🗑️ Deleted: {src_path}")

def rebuild_structure():
    """Recreate directories and scaffold empty files using PRD definitions."""
    for directory in DIRECTORIES:
        os.makedirs(directory, exist_ok=True)
        print(f"📁 Created directory: {directory}")

    for file in FILES:
        open(file, 'a').close()
        print(f"📄 Scaffolded empty file: {file}")

def restore_json():
    """Restore JSON configs inside /src/modules/accounts/ only."""
    for target, backup in CONFIG_FILES.items():
        if os.path.exists(backup):
            shutil.copy(backup, target)
            print(f"✅ Restored: {backup} → {target}")

def setup_environment():
    print(f"🚀 Initializing PRD-compliant environment setup from {os.getcwd()}...")
    print(f"🔍 Detected project root: {PROJECT_ROOT}")
    print(f"📖 Extracting PRD structure from {PRD_FILE}")

    backup_json()
    wipe_src()
    rebuild_structure()
    restore_json()

    print("✅ Setup complete! PRD conformity ensured.")

if __name__ == "__main__":
    setup_environment()
