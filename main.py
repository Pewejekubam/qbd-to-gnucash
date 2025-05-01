import os
from config import Config
from utils.error_handler import handle_error

config = Config()

def main():
    try:
        config.load_config()

        print(f"Input directory: {config.input_dir}")
        print(f"Output directory: {config.output_dir}")

        # Identify the IIF files to process
        iif_files = []
        for file_name in os.listdir(config.input_dir):
            if file_name.lower().endswith('.iif'):
                iif_files.append(os.path.join(config.input_dir, file_name))

        print(f"Found {len(iif_files)} IIF files")

        # Process each IIF file
        for file_path in iif_files:
            print(f"Processing {file_path}")

            # Determine the list type based on the file name or contents
            list_type = determine_list_type(file_path)

            # Call the corresponding list converter module
            if list_type == 'accounts':
                from list_converters.accounts import convert_accounts
                convert_accounts(file_path, os.path.join(config.output_dir, 'accounts.csv'))
                print(f"Converted {file_path} to accounts.csv")

    except Exception as e:
        handle_error(e)

def determine_list_type(file_path):
    # Determine the list type based on the file name or contents
    # For now, let's assume the list type is based on the file name
    file_name = os.path.basename(file_path)
    if file_name.lower().startswith('qbd-chart-of-accounts'):
        return 'accounts'
    # Add more list types as needed

if __name__ == '__main__':
    main()