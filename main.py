import os
from config import Config
from utils.error_handler import handle_error
from list_converters.accounts import convert_accounts

config = Config()

def main():
    try:
        config.load_config()

        # Validate input and output directories
        if not config.input_dir or not config.output_dir:
            raise ValueError("Both input_dir and output_dir must be set in the configuration.")

        baseline_mapping_file = 'mappings/account_mapping_baseline.json'
        specific_mapping_file = os.path.join(config.output_dir, 'account_mapping_specific.json')

        print(f"Input directory: {config.input_dir}")
        print(f"Output directory: {config.output_dir}")

        # Ensure the output directory exists
        if not os.path.exists(config.output_dir):
            os.makedirs(config.output_dir)

        iif_files = [
            os.path.join(config.input_dir, file_name)
            for file_name in os.listdir(config.input_dir)
            if file_name.lower().endswith('.iif')
        ]

        print(f"Found {len(iif_files)} IIF files")

        for file_path in iif_files:
            print(f"Processing {file_path}")
            output_csv_path = os.path.join(config.output_dir, 'accounts.csv')
            convert_accounts(
                file_path,
                output_csv_path,
                baseline_mapping_file,
                specific_mapping_file
            )
            print(f"CSV output written to {output_csv_path}")

    except Exception as e:
        handle_error(e)

if __name__ == '__main__':
    main()