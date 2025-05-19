"""
IIF to GnuCash Converter CLI Entrypoint
- Dispatches to list converter modules based on IIF section key (currently only !ACCNT)
- Sets up logging and handles structured errors
"""
import sys
import logging
from utils.error_handler import IIFParseError, MappingLoadError, AccountTreeError
from modules import accounts
import os

def setup_logging(log_path):
    logging.basicConfig(
        filename=log_path,
        filemode='w',
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s'
    )

def main():
    # Hardcoded paths as per PRD (no CLI arguments allowed)
    iif_path = os.path.join('input', 'sample-qbd-accounts.IIF')
    output_csv = os.path.join('output', 'accounts.csv')
    log_path = os.path.join('output', 'qbd-to-gnucash.log')
    mapping_diff_path = os.path.join('output', 'accounts_mapping_diff.json')
    user_mapping = None  # No user mapping file supported in this mode

    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    os.makedirs(os.path.dirname(log_path), exist_ok=True)

    setup_logging(log_path)
    logging.info("Starting conversion: %s", iif_path)
    try:
        logging.info("Dispatching to !ACCNT handler")
        accounts.run_accounts_pipeline(
            iif_path=iif_path,
            mapping_path=user_mapping,
            csv_path=output_csv,
            log_path=log_path,
            mapping_diff_path=mapping_diff_path
        )
        logging.info("Conversion complete: %s", output_csv)
        logging.shutdown()  # Ensure log is flushed before exit
        sys.exit(0)
    except (IIFParseError, MappingLoadError, AccountTreeError) as e:
        logging.error("%s: %s", type(e).__name__, str(e))
        logging.shutdown()  # Ensure log is flushed before exit
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(getattr(e, 'exit_code', 1))
    except SystemExit as e:
        logging.shutdown()  # Ensure log is flushed before exit
        raise
    except Exception as e:
        logging.exception("Unhandled exception")
        logging.shutdown()  # Ensure log is flushed before exit
        print(f"Fatal error: {e}", file=sys.stderr)
        sys.exit(99)

if __name__ == "__main__":
    main()
