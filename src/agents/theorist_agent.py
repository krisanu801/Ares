import sys
import os
import logging
from typing import List, Dict, Any

# Dynamically adjust sys.path to allow imports from the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Local imports
try:
    from src.utils.gemini_api import GeminiAPI
    from src.utils.logging_config import setup_logging
except ImportError as e:
    print(f"ImportError: {e}.  Check that the project structure is correct and that the necessary files exist.")
    sys.exit(1)


# Configure logging
setup_logging()
logger = logging.getLogger(__name__)


class TheoristAgent:
    """
    Theorist AI agent responsible for generating hypotheses using the Gemini API.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the TheoristAgent with a configuration.

        Args:
            config: A dictionary containing configuration parameters, including API keys.
        """
        try:
            self.gemini_api = GeminiAPI(api_key=config['gemini_api_key'])
            self.model_name = config.get('model_name', 'gemini-2.0-flash')  # Default model name
        except KeyError as e:
            logger.error(f"Missing configuration key: {e}")
            raise
        except Exception as e:
            logger.error(f"Error initializing GeminiAPI: {e}")
            raise

        logger.info("TheoristAgent initialized.")

    def generate_hypotheses(self, research_problem: str) -> List[str]:
        """
        Generates hypotheses based on the given research problem using the Gemini API.

        Args:
            research_problem: A string describing the research problem.

        Returns:
            A list of strings, where each string is a generated hypothesis.
        """
        try:
            prompt = f"""
            You are a brilliant scientist. Generate a few testable hypotheses for the following research problem:
            {research_problem}
            Provide the hypotheses as a numbered list.
            """
            response = self.gemini_api.generate_content(prompt, model_name=self.model_name)

            # Process the response to extract hypotheses
            hypotheses = self._extract_hypotheses(response)
            logger.info(f"Generated hypotheses: {hypotheses}")
            return hypotheses

        except Exception as e:
            logger.exception(f"Error generating hypotheses: {e}")
            return []

    def _extract_hypotheses(self, response: str) -> List[str]:
        """
        Extracts hypotheses from the Gemini API response.

        Args:
            response: The string response from the Gemini API.

        Returns:
            A list of hypotheses extracted from the response.
        """
        hypotheses = []
        try:
            lines = response.strip().split('\n')
            for line in lines:
                line = line.strip()
                if line and (line[0].isdigit() or line.startswith('-')):  # Check if the line starts with a number or a dash
                    # Remove numbering or bullet points
                    hypothesis = line.split(' ', 1)[1].strip() if len(line.split(' ', 1)) > 1 else line.strip()
                    hypotheses.append(hypothesis)
        except Exception as e:
            logger.error(f"Error extracting hypotheses from response: {e}")
        return hypotheses


if __name__ == "__main__":
    # Example Usage:
    # 1. Create a `configs/config.yaml` file with your Gemini API key.
    # 2. Run this script: `python src/agents/theorist_agent.py`

    # Load a dummy config for testing
    dummy_config = {
        'gemini_api_key': 'YOUR_API_KEY',  # Replace with your actual API key
        'model_name': 'gemini-2.0-flash'
    }

    # Instantiate the TheoristAgent
    theorist = TheoristAgent(config=dummy_config)

    # Define a research problem
    research_problem = "Investigate the impact of climate change on coral reef ecosystems."

    # Generate hypotheses
    hypotheses = theorist.generate_hypotheses(research_problem)

    # Print the generated hypotheses
    print("Generated Hypotheses:")
    for hypothesis in hypotheses:
        print(f"- {hypothesis}")