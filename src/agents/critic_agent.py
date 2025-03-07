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


class CriticAgent:
    """
    Critic AI agent responsible for refining hypotheses and experimental designs using the Gemini API.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the CriticAgent with a configuration.

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

        logger.info("CriticAgent initialized.")

    def refine_hypotheses(self, hypotheses: List[str], experiment_results: str) -> List[str]:
        """
        Refines the given hypotheses based on the experiment results using the Gemini API.

        Args:
            hypotheses: A list of strings representing the hypotheses to be refined.
            experiment_results: A string containing the results of the experiment.

        Returns:
            A list of strings representing the refined hypotheses.
        """
        try:
            prompt = f"""
            You are an expert scientific critic. Based on the following hypotheses and experiment results,
            refine the hypotheses to be more accurate and testable.
            Hypotheses: {hypotheses}
            Experiment Results: {experiment_results}
            Provide the refined hypotheses as a numbered list.
            """
            response = self.gemini_api.generate_content(prompt, model_name=self.model_name)

            # Process the response to extract refined hypotheses
            refined_hypotheses = self._extract_hypotheses(response)
            logger.info(f"Refined hypotheses: {refined_hypotheses}")
            return refined_hypotheses

        except Exception as e:
            logger.exception(f"Error refining hypotheses: {e}")
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
    # 2. Run this script: `python src/agents/critic_agent.py`

    # Load a dummy config for testing
    dummy_config = {
        'gemini_api_key': 'YOUR_API_KEY',  # Replace with your actual API key
        'model_name': 'gemini-2.0-flash'
    }

    # Instantiate the CriticAgent
    critic_agent = CriticAgent(config=dummy_config)

    # Define some initial hypotheses
    hypotheses = [
        "Increasing the temperature will increase the reaction rate.",
        "Adding a catalyst will decrease the activation energy."
    ]

    # Define some experiment results
    experiment_results = "Experiments showed that increasing the temperature initially increases the reaction rate, but beyond a certain point, the reaction rate decreases. The catalyst significantly lowered the activation energy as expected."

    # Refine the hypotheses
    refined_hypotheses = critic_agent.refine_hypotheses(hypotheses, experiment_results)

    # Print the refined hypotheses
    print("Refined Hypotheses:")
    for hypothesis in refined_hypotheses:
        print(f"- {hypothesis}")