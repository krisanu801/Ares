import sys
import os
import logging
import yaml
from typing import Dict, Any

# Dynamically adjust sys.path to allow imports from the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Local imports
try:
    from src.agents.theorist_agent import TheoristAgent
    from src.agents.data_scientist_agent import DataScientistAgent
    from src.agents.experiment_agent import ExperimentAgent
    from src.agents.critic_agent import CriticAgent
    from src.utils.logging_config import setup_logging
except ImportError as e:
    print(f"ImportError: {e}.  Check that the project structure is correct and that the necessary files exist.")
    sys.exit(1)


# Configure logging
setup_logging()
logger = logging.getLogger(__name__)


def load_config(config_path: str) -> Dict[str, Any]:
    """Loads configuration from a YAML file.

    Args:
        config_path: The path to the YAML configuration file.

    Returns:
        A dictionary containing the configuration.
    """
    try:
        with open(config_path, 'r') as f:
            config = yaml.safe_load(f)
        return config
    except FileNotFoundError:
        logger.error(f"Configuration file not found: {config_path}")
        raise
    except yaml.YAMLError as e:
        logger.error(f"Error parsing configuration file: {e}")
        raise


def main():
    """Main function to orchestrate the ARES system."""
    try:
        config = load_config("configs/config.yaml")

        # Initialize agents
        theorist = TheoristAgent(config=config)
        data_scientist = DataScientistAgent(config=config)
        experiment_agent = ExperimentAgent(config=config)
        critic = CriticAgent(config=config)

        # Example usage: Define a research problem
        research_problem = "create a nonconvex optimizer algorithm that humankind does not know about."
        logger.info(f"Research Problem: {research_problem}")

        # Theorist generates hypotheses
        hypotheses = theorist.generate_hypotheses(research_problem)
        logger.info(f"Generated Hypotheses: {hypotheses}")

        # Data Scientist analyzes existing data
        data_analysis_results = data_scientist.analyze_data(research_problem, hypotheses)
        logger.info(f"Data Analysis Results: {data_analysis_results}")

        # Experiment Agent designs and runs simulations
        experiment_results = experiment_agent.run_simulation(hypotheses, data_analysis_results)
        logger.info(f"Experiment Results: {experiment_results}")

        # Critic refines hypotheses based on results
        refined_hypotheses = critic.refine_hypotheses(hypotheses, experiment_results)
        logger.info(f"Refined Hypotheses: {refined_hypotheses}")

        logger.info("ARES system completed one iteration.")

    except Exception as e:
        logger.exception(f"An error occurred: {e}")


if __name__ == "__main__":
    main()

    # Example Usage:
    # 1. Ensure you have a `configs/config.yaml` file with necessary API keys and settings.
    # 2. Run the script: `python src/main.py`
    # 3. Check the logs for the output of each agent and the overall process.