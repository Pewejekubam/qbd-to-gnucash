import sys
import logging
from utils.error_handler import (
    IIFParseError, MappingLoadError, AccountTreeError, RegistryKeyConflictError, UnregisteredKeyError
)

# Registry for dispatching handlers by IIF key
dispatch_registry = {}

def register_handler(key, handler):
    if key in dispatch_registry:
        raise RegistryKeyConflictError(f"Key already registered: {key}")
    dispatch_registry[key] = handler

def dispatch(key, *args, **kwargs):
    if key not in dispatch_registry:
        raise UnregisteredKeyError(f"No handler registered for key: {key}")
    return dispatch_registry[key](*args, **kwargs)


def main():
    import os
    # Ensure output and log directories exist
    os.makedirs('output', exist_ok=True)
    os.makedirs('intermediate', exist_ok=True)

    logging.basicConfig(
        filename='output/qbd-to-gnucash.log',
        level=logging.INFO,
        format='%(asctime)s [%(levelname)s] %(module)s.%(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    logging.info("Starting qbd-to-gnucash CLI tool")
    try:
        # Config/env/CLI arg parsing
        QBD_INPUT_PATH = os.getenv('QBD_INPUT_PATH', 'input/sample-qbd-accounts.IIF')
        GNC_OUTPUT_PATH = os.getenv('GNC_OUTPUT_PATH', 'output/accounts.csv')
        MAPPING_BASELINE_PATH = os.getenv('MAPPING_BASELINE_PATH', 'registry/mapping/account_mapping_baseline.json')
        MAPPING_SPECIFIC_PATH = os.getenv('MAPPING_SPECIFIC_PATH', 'output/accounts_mapping_specific.json')
        MAPPING_DIFF_PATH = os.getenv('MAPPING_DIFF_PATH', 'output/accounts_mapping_diff.json')

        # CLI arg override for input file
        if len(sys.argv) > 1:
            QBD_INPUT_PATH = sys.argv[1]
        logging.info(f"Input file: {QBD_INPUT_PATH}")
        logging.info(f"Output CSV: {GNC_OUTPUT_PATH}")
        logging.info(f"Mapping baseline: {MAPPING_BASELINE_PATH}")
        logging.info(f"Mapping specific: {MAPPING_SPECIFIC_PATH}")
        logging.info(f"Mapping diff: {MAPPING_DIFF_PATH}")

        from modules.accounts import process_accounts
        register_handler('!ACCNT', process_accounts)
        # Only !ACCNT supported in MVP
        csv_rows = dispatch('!ACCNT', QBD_INPUT_PATH, MAPPING_BASELINE_PATH, MAPPING_SPECIFIC_PATH, GNC_OUTPUT_PATH, MAPPING_DIFF_PATH)
        logging.info("Processing complete.")

        # Check for unmapped types (diff file written)
        if os.path.exists(MAPPING_DIFF_PATH):
            import json
            with open(MAPPING_DIFF_PATH, 'r', encoding='utf-8') as f:
                diff_data = json.load(f)
            if diff_data:
                logging.error(f"Unmapped account types detected. See {MAPPING_DIFF_PATH}.")
                print(f"Unmapped account types detected. See {MAPPING_DIFF_PATH}.")
                sys.exit(2)
        print(f"Accounts CSV written to {GNC_OUTPUT_PATH}.")
    except (IIFParseError, MappingLoadError, AccountTreeError) as e:
        logging.error(f"Critical error: {e}")
        print(f"Error: {e}")
        sys.exit(1)
    except SystemExit as e:
        raise e
    except Exception as e:
        logging.exception("Unhandled exception")
        print(f"Unhandled error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
