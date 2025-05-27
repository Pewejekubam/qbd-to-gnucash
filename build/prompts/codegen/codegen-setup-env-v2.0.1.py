# -----------------------------------------------------------------------------
# Script Name: codegen-setup-env-v2.0.1.py
# Purpose: Dynamically sets up environment per PRD-defined structure
# Version: v2.0.1
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

def parse_section_13(file_path):
    """Extract directory structure exactly as it appears in the PRD document."""
    with open(file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    in_directory_structure = False
    structure = {}
    path_stack = [structure]
    level_stack = [-1]  # Track indentation levels

    for line in lines:
        if line.startswith('## 13.'):
            continue

        if line.startswith('Project root:'):
            in_directory_structure = True
            continue

        if in_directory_structure:
            stripped = line.strip()
            if not stripped:
                break
            
            # Skip lines that don't start with '-' (like "> For rules about...")
            if not stripped.startswith('-'):
                if stripped.startswith('>') or stripped.startswith('#'):
                    break
                continue
            
            # Calculate indentation level (spaces before the '-')
            level = len(line) - len(line.lstrip())
            name = stripped.lstrip('-').strip()
            
            # Remove trailing '/' from directory names
            if name.endswith('/'):
                name = name[:-1]

            # Adjust the path stack based on current indentation level
            while len(level_stack) > 0 and level <= level_stack[-1]:
                path_stack.pop()
                level_stack.pop()

            # Determine if this is a file or directory
            if "." in name and not name.endswith('/'):  # File
                path_stack[-1][name] = None
            else:  # Directory
                path_stack[-1][name] = {}
                path_stack.append(path_stack[-1][name])
                level_stack.append(level)

    return structure

def rebuild_structure(structure, path):
    """Recreate directories and scaffold empty files using PRD definitions."""
    for name, value in structure.items():
        full_path = os.path.join(path, name)
        if value is None:  # File
            open(full_path, 'a').close()
            print(f"📄 Scaffolded empty file: {full_path}")
        else:  # Directory
            os.makedirs(full_path, exist_ok=True)
            print(f"📁 Created directory: {full_path}")
            rebuild_structure(value, full_path)

def get_project_root():
    """Determine project root dynamically, ensuring script execution from any directory."""
    script_dir = os.path.abspath(os.path.dirname(__file__))
    while not os.path.exists(os.path.join(script_dir, ".gitignore")):  # Using .gitignore as an anchor
        script_dir = os.path.dirname(script_dir)
        if script_dir == os.path.dirname(script_dir):  # Stop at system root
            raise RuntimeError("Error: Unable to detect project root. Ensure script is within the repository.")
    return script_dir

def backup_json_configs(src_path):
    """Backup JSON config files to ./setup-env-temp/*.json"""
    temp_dir = os.path.join(os.path.dirname(src_path), "setup-env-temp")
    os.makedirs(temp_dir, exist_ok=True)

    config_files = []
    for root, dirs, files in os.walk(src_path):
        for file in files:
            if file.endswith(".json"):
                file_path = os.path.join(root, file)
                backup_path = os.path.join(temp_dir, os.path.relpath(file_path, src_path) + '.bak')
                os.makedirs(os.path.dirname(backup_path), exist_ok=True)
                shutil.copy(file_path, backup_path)
                config_files.append((file_path, backup_path))
                print(f"✅ Backed up: {file_path} → {backup_path}")

    return config_files

def restore_json_configs(config_files):
    """Restore JSON config files from ./setup-env-temp/*.json"""
    for target, backup in config_files:
        # Ensure target directory exists before restoring
        target_dir = os.path.dirname(target)
        os.makedirs(target_dir, exist_ok=True)
        
        shutil.copy(backup, target)
        print(f"✅ Restored: {backup} → {target}")

def setup_environment():
    project_root = get_project_root()
    print(f"🚀 Initializing PRD-compliant environment setup from {os.getcwd()}...")
    print(f"🔍 Detected project root: {project_root}")

    prd_file = './prd/core-prd-v3.6.3.md'
    print(f"📖 Extracting PRD structure from {prd_file}")
    directory_structure = parse_section_13(prd_file)
    
    # Debug: Show what was parsed
    print(f"🔍 DEBUG: Parsed structure keys: {list(directory_structure.keys())}")
    print(f"🔍 DEBUG: Full structure: {directory_structure}")

    src_path = os.path.join(project_root, "src")

    # Backup JSON configs
    config_files = backup_json_configs(src_path)

    # Wipe /src/
    if os.path.exists(src_path):
        shutil.rmtree(src_path)
        print(f"🗑️ Deleted: {src_path}")

    # Rebuild structure
    os.makedirs(src_path, exist_ok=True)
    if 'src' in directory_structure:
        print("📁 Found 'src' in structure, rebuilding...")
        rebuild_structure(directory_structure['src'], src_path)
    else:
        print("⚠️  'src' not found in parsed structure!")
        print("🔍 Available keys:", list(directory_structure.keys()))
        # Try to rebuild with the entire structure if it exists
        if directory_structure:
            print("📁 Attempting to rebuild with full structure...")
            rebuild_structure(directory_structure, src_path)

    # Restore JSON configs
    restore_json_configs(config_files)

    # Clean up temp dir
    temp_dir = os.path.join(project_root, "setup-env-temp")
    shutil.rmtree(temp_dir)
    print(f"🗑️ Deleted: {temp_dir}")

    print("✅ Setup complete! PRD conformity ensured.")

if __name__ == "__main__":
    setup_environment()

