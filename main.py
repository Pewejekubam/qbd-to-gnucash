import os
from config import Config
from utils.error_handler import handle_error
from list_converters.accounts import convert_accounts

# Initialize configuration object
config = Config()

def main():
    """
    Main function to orchestrate the conversion of QuickBooks IIF files to GnuCash-compatible CSV files.
    
    Steps:
    1. Load configuration settings.
    2. Validate input and output directories.
    3. Identify IIF files in the input directory.
    4. Process each IIF file and generate a corresponding CSV file.

    Raises:
        ValueError: If input or output directories are not set.
    """
    try:
        # Load configuration settings (e.g., input/output directories)
        config.load_config()

        # Validate that input and output directories are set
        if not config.input_dir or not config.output_dir:
            raise ValueError("Both input_dir and output_dir must be set in the configuration.")

        # Define paths for baseline and specific mapping files
        baseline_mapping_file = 'mappings/account_mapping_baseline.json'
        specific_mapping_file = os.path.join(config.output_dir, 'account_mapping_specific.json')

        print(f"Input directory: {config.input_dir}")
        print(f"Output directory: {config.output_dir}")

        # Ensure the output directory exists
        if not os.path.exists(config.output_dir):
            os.makedirs(config.output_dir)

        # Identify all IIF files in the input directory
        iif_files = [
            os.path.join(config.input_dir, file_name)
            for file_name in os.listdir(config.input_dir)
            if file_name.lower().endswith('.iif')
        ]

        print(f"Found {len(iif_files)} IIF files")

        # Process each IIF file
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
        # Handle any errors that occur during processing
        handle_error(e)

if __name__ == '__main__':
    # Entry point for the script
    main()