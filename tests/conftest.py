# Agentic affirmation: This file is compliant with PRD v3.6.3 and Governance Document v2.3.10.
"""
Pytest configuration to add src/ to sys.path for module resolution.
"""
import sys
import os

SRC_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))
if SRC_PATH not in sys.path:
    sys.path.insert(0, SRC_PATH)
