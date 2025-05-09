import os
from dotenv import load_dotenv

class Config:
    def __init__(self):
        # Initialize paths as None; they will be loaded in load_config()
        self.input_dir = None
        self.output_dir = None

    def load_config(self):
        """
        Loads configuration values for the input and output directories.
        Priority:
        1. Environment variables (set in shell or via .env file)
        2. Hardcoded fallback paths (from known good working PS session)
        """

        # Load environment variables from .env file (if it exists)
        load_dotenv()

        # Attempt to load input and output directories from the environment
        self.input_dir = os.environ.get('QBD_INPUT_DIR')
        self.output_dir = os.environ.get('GNUCASH_OUTPUT_DIR')

        # ---------------------------------------------------------------------
        # Fallback: use known working values if env variables are not set
        # These values match the paths from your working PowerShell session
        # ---------------------------------------------------------------------
        if not self.input_dir:
            print("Warning: QBD_INPUT_DIR not set. Using fallback path.")
            self.input_dir = r"C:\git-root\qbd-to-gnucash\input"

        if not self.output_dir:
            print("Warning: GNUCASH_OUTPUT_DIR not set. Using fallback path.")
            self.output_dir = r"C:\git-root\qbd-to-gnucash\output"

        # ---------------------------------------------------------------------
        # Ensure the output directory exists. Create it if needed.
        # ---------------------------------------------------------------------
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
            print(f"Created output directory: {self.output_dir}")

        # ---------------------------------------------------------------------
        # Final validation: raise if input directory doesn't exist
        # ---------------------------------------------------------------------
        if not os.path.exists(self.input_dir):
            raise ValueError(f"Input directory does not exist: {self.input_dir}")
