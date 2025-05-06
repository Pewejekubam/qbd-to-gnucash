import os
from config import Config
from utils.error_handler import handle_error
from list_converters.accounts import convert_accounts

config = Config()

def main():
    try:
        config.load_config()

        baseline_mapping_file = 'mappings/account_mapping_baseline.json'
        specific_mapping_file = os.path.join(config.output_dir, 'account_mapping_specific.json')

        print(f"Input directory: {config.input_dir}")
        print(f"Output directory: {config.output_dir}")

        iif_files = [
            os.path.join(config.input_dir, file_name)
            for file_name in os.listdir(config.input_dir)
            if file_name.lower().endswith('.iif')
        ]

        print(f"Found {len(iif_files)} IIF files")

        for file_path in iif_files:
            print(f"Processing {file_path}")
            convert_accounts(
                file_path,
                os.path.join(config.output_dir, 'accounts.csv'),
                baseline_mapping_file,
                specific_mapping_file
            )

    except Exception as e:
        handle_error(e)

if __name__ == '__main__':
    main()