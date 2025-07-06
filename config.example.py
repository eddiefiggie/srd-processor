"""
Example configuration file for the D&D SRD PDF to Markdown converter.
Copy this file to config.py and fill in your actual values.
"""

import os
from typing import Optional

# OpenAI API Configuration
OPENAI_API_KEY: Optional[str] = None  # Set your API key here or use environment variable

# OpenAI Model Configuration
OPENAI_MODEL = "gpt-4o-mini"  # You can change this to "gpt-4" for better quality but higher cost
OPENAI_MAX_TOKENS = 4000
OPENAI_TEMPERATURE = 0.1

# File Configuration
INPUT_PDF_FILE = "SRD_CC_v5.2.1.pdf"
RAW_TEXT_OUTPUT = "srd_raw_text.txt"
BASIC_MARKDOWN_OUTPUT = "srd_cleaned_output.md"
AI_ENHANCED_OUTPUT = "srd_ai_cleaned.md"

# Processing Configuration
ENABLE_AI_CLEANUP = True  # Set to False to disable AI cleanup by default
VERBOSE_LOGGING = True    # Set to False to reduce console output

# PDF Processing Configuration
DETECT_COLUMNS = True     # Whether to attempt column detection
PRESERVE_PAGE_MARKERS = True  # Whether to include <!-- Page X --> markers in output

def get_openai_api_key() -> str:
    """
    Get the OpenAI API key from environment variable or config.
    Raises ValueError if no API key is found.
    """
    if OPENAI_API_KEY:
        return OPENAI_API_KEY
    
    # Try environment variable as fallback
    env_key = os.getenv('OPENAI_API_KEY')
    if env_key:
        return env_key
    
    raise ValueError(
        "OpenAI API key not found. Please either:\n"
        "1. Set the OPENAI_API_KEY environment variable, or\n"
        "2. Set OPENAI_API_KEY in config.py"
    )

def validate_config() -> bool:
    """
    Validate that all required configuration is present.
    Returns True if valid, False otherwise.
    """
    try:
        get_openai_api_key()
        return True
    except ValueError:
        return False
