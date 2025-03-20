"""Configuration management for the PDF analyzer."""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path('.env')
load_dotenv(dotenv_path=env_path)

# OpenAI Configuration
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Logging Configuration
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# PDF Processing Configuration
MAX_PDF_SIZE_MB = int(os.getenv('MAX_PDF_SIZE_MB', '10'))
ALLOW_IMAGES = os.getenv('ALLOW_IMAGES', 'true').lower() == 'true'

def validate_config():
    """Validate required configuration values."""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY environment variable is not set. "
            "Please check your .env file or environment variables."
        )

# Validate configuration on import
validate_config()
