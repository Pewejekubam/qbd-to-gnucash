import os
import logging
from config import Config
from utils.error_handler import handle_error
from list_converters.accounts import convert_accounts
from list_converters.payment_terms import convert_payment_terms
from list_converters.sales_tax_framework import process_sales_tax_framework

logging.info("Test log: Logging system is active.")

# -----------------------------------------------------------------------------
# CONFIGURATION INITIALIZATION
# -----------------------------------------------------------------------------

config = Config()

# -----------------------------------------------------------------------------
# FILE TYPE REGISTRY
# -----------------------------------------------------------------------------
# Each entry defines:
# - A QBD or virtual key
# - The conversion function
# - Any dependencies
# - The output file extension (csv, html, etc.)
# - The GnuCash-friendly output file name
# -----------------------------------------------------------------------------

file_type_registry = {
    '!ACCNT': {
        'description': 'Account file',
        'process_function': convert_accounts,
        'dependencies': [],
        'output_ext': 'csv',
        'output_name': 'accounts.csv'
    },
    '!TERMS': {
        'description': 'Payment Terms file',
        'process_function': convert_payment_terms,
        'dependencies': [],
        'output_ext': 'html',
        'output_name': 'terms.html'
    },
    '!SALESTAXCODE': {
        'description': 'Sales Tax Codes file',
        'process_function': None,
        'dependencies': [],
        'output_ext': None,
        'output_name': None
    },
    '!INVITEM': {
        'description': 'Sales Tax Items file',
        'process_function': None,
        'dependencies': [],
        'output_ext': None,
        'output_name': None
    },
    '!SALESTAX_FRAMEWORK': {
        'description': 'Combined tax code + item setup',
        'process_function': process_sales_tax_framework,
        'dependencies': ['!SALESTAXCODE', '!INVITEM'],
        'output_ext': 'html',
        'output_name': 'SalesTaxFramework.html'
    },
    '!CUST': {
        'description': 'Customer file (placeholder)',
        'process_function': None,
        'dependencies': [],
        'output_ext': 'csv',
        'output_name': 'Customers.csv'
    }
}

# -----------------------------------------------------------------------------
# FUNCTION: extract_keys_from_iif(file_path)
# PURPOSE: Normalize each header key (e.g., '!ACCNT'), ignore trailing labels
# -----------------------------------------------------------------------------

def extract_keys_from_iif(file_path):
    logging.debug("Entering extract_keys_from_iif function.")
    logging.debug(f"File path: {file_path}")
    keys_data = {}
    with open(file_path, 'r') as file:
        current_key = None
        for line in file:
            line = line.strip()
            if line.startswith('!'):
                normalized_key = line.split()[0]
                current_key = normalized_key
                if current_key not in keys_data:
                    keys_data[current_key] = []
            elif current_key:
                keys_data[current_key].append(line)
    logging.debug("Exiting extract_keys_from_iif function.")
    return keys_data

# -----------------------------------------------------------------------------
# FUNCTION: build_key_registry(iif_files)
# PURPOSE: Build a map of keys to the files in which they appear
# -----------------------------------------------------------------------------

def build_key_registry(iif_files):
    key_registry = {}
    for file_path in iif_files:
        keys_data = extract_keys_from_iif(file_path)
        for key in keys_data:
            if key not in key_registry:
                key_registry[key] = []
            key_registry[key].append(file_path)
    return key_registry

# -----------------------------------------------------------------------------
# FUNCTION: process_keys(key_registry)
# PURPOSE: Run each conversion function once all dependencies are satisfied
# -----------------------------------------------------------------------------

def process_keys(key_registry):
    print(f"\nDetected keys and associated files:")
    for key, files in key_registry.items():
        print(f"  {key}: {files}")

    processed = set()

    def can_process(key):
        deps = file_type_registry[key]['dependencies']
        return all(dep in processed for dep in deps)

    keys_to_process = list(file_type_registry.keys())

    while keys_to_process:
        for key in keys_to_process[:]:
            deps = file_type_registry[key]['dependencies']
            if not can_process(key):
                continue

            process_func = file_type_registry[key]['process_function']
            output_ext = file_type_registry[key].get('output_ext') or 'html'
            output_name = file_type_registry[key].get('output_name')

            # ---------------------------
            # VIRTUAL or MULTI-KEY case
            # ---------------------------
            if key not in key_registry and deps and process_func:
                if all(dep in key_registry for dep in deps):
                    print(f"\nProcessing virtual key {key} from dependencies {deps}...")

                    output_file = os.path.join(config.output_dir, output_name)

                    input_files = [key_registry[dep][0] for dep in deps]  # Use first file for each

                    if key == '!SALESTAX_FRAMEWORK':
                        process_func(input_files[0], input_files[1], output_file)

                    print(f"Processed {key} and wrote output to {output_file}")
                    processed.add(key)
                    keys_to_process.remove(key)
                continue

            # ---------------------------
            # NORMAL 1:1 case
            # ---------------------------
            if key in key_registry and process_func:
                for file_path in key_registry[key]:
                    print(f"\nProcessing {key} from {os.path.basename(file_path)}...")

                    output_file = os.path.join(config.output_dir, output_name)

                    if key == '!ACCNT':
                        baseline = os.path.join('mappings', 'account_mapping_baseline.json')
                        specific = os.path.join(config.output_dir, 'specific_account_mapping.json')

                        if not os.path.exists(baseline):
                            print(f"Missing baseline mapping for {key}. Skipping.")
                            continue

                        process_func(file_path, output_file, baseline, specific)
                    else:
                        process_func(file_path, output_file)

                    print(f"Processed {key} and wrote output to {output_file}")
                processed.add(key)
                keys_to_process.remove(key)

            if not process_func:
                print(f"\nSkipping {key}: no conversion function defined.")
                processed.add(key)
                keys_to_process.remove(key)

# -----------------------------------------------------------------------------
# FUNCTION: main()
# PURPOSE: Entrypoint — Load config, find files, and start processing
# -----------------------------------------------------------------------------

def main():
    try:
        # Remove any existing handlers first (especially if logging was initialized in imported modules)
        for handler in logging.root.handlers[:]:
            logging.root.removeHandler(handler)

        # Reconfigure logging to only show INFO and above
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )

        logging.debug("Starting main script execution.")
        logging.info("Logging system initialized. This is a test log message.")
        config.load_config()

        if not config.input_dir or not config.output_dir:
            raise ValueError("Both input_dir and output_dir must be set in the configuration.")

        print(f"Input directory: {config.input_dir}")
        print(f"Output directory: {config.output_dir}")

        if not os.path.exists(config.output_dir):
            os.makedirs(config.output_dir)

        iif_files = [
            os.path.join(config.input_dir, file_name)
            for file_name in os.listdir(config.input_dir)
            if file_name.lower().endswith('.iif')
        ]

        print(f"Found {len(iif_files)} IIF files")

        key_registry = build_key_registry(iif_files)

        process_keys(key_registry)

    except Exception as e:
        handle_error(e)

# -----------------------------------------------------------------------------
# SCRIPT ENTRY POINT
# -----------------------------------------------------------------------------

if __name__ == '__main__':
    main()
