import os

class Config:
    def __init__(self):
        self.input_dir = None
        self.output_dir = None

    def load_config(self):
        # Load configuration from environment variables or a config file
        self.input_dir = os.environ.get('QBD_INPUT_DIR')
        self.output_dir = os.environ.get('GNUCASH_OUTPUT_DIR')

        # Create the output directory if it doesn't exist
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

        # Validate the configuration
        if not self.input_dir:
            raise ValueError("Input directory not specified")