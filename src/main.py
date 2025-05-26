# Agentic affirmation: This script is compliant with PRD v3.6.3 and Governance Document v2.3.10.
"""
Main entry point for QBD to GnuCash conversion tool (Chart of Accounts only).
Handles CLI, logging, error handling, and pipeline orchestration per PRD v3.6.3.
"""
import sys
import os
import argparse
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))
from utils.logging import get_logger, flush_logs
from utils.error_handler import (
    IIFParseError, MappingLoadError, AccountsTreeError, ValidationError, OutputError
)
from modules.accounts.accounts import run_accounts_pipeline


def parse_args():
    parser = argparse.ArgumentParser(
        description="Convert QuickBooks Desktop .IIF Chart of Accounts to GnuCash-compatible CSV."
    )
    parser.add_argument("-i", "--input", required=True, help="Path to QBD .IIF file (Chart of Accounts export)")
    parser.add_argument("-o", "--output", required=True, help="Path to output CSV file")
    parser.add_argument("--log", default="output/qbd-to-gnucash.log", help="Path to log file")
    return parser.parse_args()


def main():
    args = parse_args()
    logger = get_logger(args.log)
    try:
        logger.info("Starting QBD to GnuCash conversion pipeline.")
        run_accounts_pipeline(args.input, args.output, logger=logger)
        logger.info("Pipeline completed successfully.")
        flush_logs(logger)
        sys.exit(0)
    except ValidationError as ve:
        logger.error(f"Validation error: {ve}")
        flush_logs(logger)
        sys.exit(2)
    except (IIFParseError, MappingLoadError, AccountsTreeError, OutputError) as ce:
        logger.critical(f"Critical error: {ce}")
        flush_logs(logger)
        sys.exit(1)
    except Exception as e:
        logger.critical(f"Unhandled exception: {e}", exc_info=True)
        flush_logs(logger)
        sys.exit(1)

if __name__ == "__main__":
    main()

# Example usage:
#   python -m src.main -i input/sample-qbd-accounts.IIF -o output/accounts.csv
# All logs written to output/qbd-to-gnucash.log by default.