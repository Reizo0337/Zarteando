import os
from dotenv import load_dotenv

# Load environment variables before importing modules that might use them
load_dotenv()

from diagnostics import print_diagnostics

if __name__ == "__main__":
    print_diagnostics()