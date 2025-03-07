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


class ExperimentAgent:
    """
    Experiment AI agent responsible for designing and running simulations and experiments using the Gemini API.
    """

    def __init__(self, config: Dict[str, Any]):
        """
        Initializes the ExperimentAgent with a configuration.

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

        logger.info("ExperimentAgent initialized.")

    def run_simulation(self, hypotheses: List[str], data_analysis_results: str) -> str:
        """
        Designs and runs a simulation based on the given hypotheses and data analysis results using the Gemini API.

        Args:
            hypotheses: A list of strings representing the hypotheses to be tested.
            data_analysis_results: A string containing the results of the data analysis.

        Returns:
            A string containing the simulation results.
        """
        try:
            prompt = f"""
            You are an expert in designing and running scientific simulations.
            Based on the following hypotheses and data analysis results, design and run a simulation to test the hypotheses.
            Hypotheses: {hypotheses}
            Data Analysis Results: {data_analysis_results}
            Provide a detailed description of the simulation setup, parameters, and the expected results.
            Also, provide the actual simulation results.
            """
            response = self.gemini_api.generate_content(prompt, model_name=self.model_name)
            logger.info(f"Simulation results: {response}")
            return response

        except Exception as e:
            logger.exception(f"Error running simulation: {e}")
            return ""


if __name__ == "__main__":
    # Example Usage:
    # 1. Create a `configs/config.yaml` file with your Gemini API key.
    # 2. Run this script: `python src/agents/experiment_agent.py`

    # Load a dummy config for testing
    dummy_config = {
        'gemini_api_key': 'YOUR_API_KEY',  # Replace with your actual API key
        'model_name': 'gemini-2.0-flash'
    }

    # Instantiate the ExperimentAgent
    experiment_agent = ExperimentAgent(config=dummy_config)

    # Define some hypotheses
    hypotheses = [
        "Increasing the temperature will increase the reaction rate.",
        "Adding a catalyst will decrease the activation energy."
    ]

    # Define some data analysis results
    data_analysis_results = "Existing data suggests a positive correlation between temperature and reaction rate, and the presence of a catalyst lowers the activation energy."

    # Run the simulation
    simulation_results = experiment_agent.run_simulation(hypotheses, data_analysis_results)

    # Print the simulation results
    print("Simulation Results:")
    print(simulation_results)