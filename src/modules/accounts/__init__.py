"""Entry point for accounts processing pipeline."""

# Clean module interface - only expose the main pipeline function
from .accounts import run_accounts_pipeline

# Domain module follows PRD interface contract
__all__ = ['run_accounts_pipeline']