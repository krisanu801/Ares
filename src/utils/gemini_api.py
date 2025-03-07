import sys
import os
import logging
from typing import Optional

# Dynamically adjust sys.path to allow imports from the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Local imports
try:
    from src.utils.logging_config import setup_logging
except ImportError as e:
    print(f"ImportError: {e}.  Check that the project structure is correct and that the necessary files exist.")
    sys.exit(1)

# Configure logging
setup_logging()
logger = logging.getLogger(__name__)

try:
    import google.generativeai as genai
except ImportError:
    logger.error("google-generative-ai library not found. Please install it: pip install google-generative-ai")
    sys.exit(1)


class GeminiAPI:
    """
    Wrapper for interacting with the Gemini API.
    """

    def __init__(self, api_key: str):
        """
        Initializes the GeminiAPI with the given API key.

        Args:
            api_key: The Gemini API key.
        """
        try:
            genai.configure(api_key=api_key)
            self.api_key = api_key
            logger.info("Gemini API configured successfully.")
        except Exception as e:
            logger.error(f"Error configuring Gemini API: {e}")
            raise

    def generate_content(self, prompt: str, model_name: str = 'gemini-2.0-flash') -> str:
        """
        Generates content using the Gemini API.

        Args:
            prompt: The prompt to send to the API.
            model_name: The name of the Gemini model to use (default: 'gemini-2.0-flash').

        Returns:
            The generated content as a string.
        """
        try:
            model = genai.GenerativeModel(model_name)
            response = model.generate_content(prompt)
            logger.info(f"Generated content using model: {model_name}")
            return response.text
        except Exception as e:
            logger.exception(f"Error generating content: {e}")
            return ""


if __name__ == "__main__":
    # Example Usage:
    # 1. Create a `configs/config.yaml` file with your Gemini API key.
    # 2. Run this script: `python src/utils/gemini_api.py`

    # Replace with your actual API key
    dummy_api_key = "YOUR_API_KEY"

    # Instantiate the GeminiAPI
    gemini_api = GeminiAPI(api_key=dummy_api_key)

    # Define a prompt
    prompt = "Write a short poem about the stars."

    # Generate content
    generated_content = gemini_api.generate_content(prompt)

    # Print the generated content
    print("Generated Content:")
    print(generated_content)