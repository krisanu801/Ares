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


class DataScientistAgent:
    """
    Data Scientist AI agent responsible for data analysis and interpretation using the Gemini API.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the DataScientistAgent with a configuration.

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

        logger.info("DataScientistAgent initialized.")

    def analyze_data(self, research_problem: str, hypotheses: List[str]) -> str:
        """
        Analyzes existing data related to the research problem and hypotheses using the Gemini API.

        Args:
            research_problem: A string describing the research problem.
            hypotheses: A list of strings representing the hypotheses to be analyzed.

        Returns:
            A string containing the analysis results.
        """
        try:
            prompt = f"""
            You are an expert data scientist. Analyze the following research problem and hypotheses,
            and provide insights based on existing knowledge and data.
            Research Problem: {research_problem}
            Hypotheses: {hypotheses}
            Provide a detailed analysis of the hypotheses in relation to the research problem.
            """
            response = self.gemini_api.generate_content(prompt, model_name=self.model_name)
            logger.info(f"Data analysis results: {response}")
            return response

        except Exception as e:
            logger.exception(f"Error analyzing data: {e}")
            return ""


if __name__ == "__main__":
    # Example Usage:
    # 1. Create a `configs/config.yaml` file with your Gemini API key.
    # 2. Run this script: `python src/agents/data_scientist_agent.py`

    # Load a dummy config for testing
    dummy_config = {
        'gemini_api_key': 'YOUR_API_KEY',  # Replace with your actual API key
        'model_name': 'gemini-2.0-flash'
    }

    # Instantiate the DataScientistAgent
    data_scientist = DataScientistAgent(config=dummy_config)

    # Define a research problem
    research_problem = "Investigate the impact of different fertilizer types on crop yield."

    # Define some hypotheses
    hypotheses = [
        "Fertilizer A will increase crop yield more than Fertilizer B.",
        "The optimal fertilizer concentration is 100 kg/hectare."
    ]

    # Analyze the data
    analysis_results = data_scientist.analyze_data(research_problem, hypotheses)

    # Print the analysis results
    print("Data Analysis Results:")
    print(analysis_results)