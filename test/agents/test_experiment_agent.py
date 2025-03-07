import sys
import os
import unittest
from unittest.mock import patch
from typing import Dict, Any, List

# Dynamically adjust sys.path to allow imports from the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# Local imports
try:
    from src.agents.experiment_agent import ExperimentAgent
except ImportError as e:
    print(f"ImportError: {e}.  Check that the project structure is correct and that the necessary files exist.")
    sys.exit(1)


class TestExperimentAgent(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.dummy_config: Dict[str, Any] = {
            'gemini_api_key': 'TEST_API_KEY',
            'model_name': 'gemini-2.0-flash'
        }
        self.hypotheses = [
            "Increasing the temperature will increase the reaction rate.",
            "Adding a catalyst will decrease the activation energy."
        ]
        self.data_analysis_results = "Existing data suggests a positive correlation between temperature and reaction rate, and the presence of a catalyst lowers the activation energy."

    @patch('src.agents.experiment_agent.GeminiAPI.generate_content')
    def test_run_simulation_success(self, mock_generate_content):
        """Test successful simulation run."""
        mock_generate_content.return_value = "Simulation results: Increasing the temperature by 10 degrees increased the reaction rate by 20%."
        experiment_agent = ExperimentAgent(config=self.dummy_config)
        simulation_results = experiment_agent.run_simulation(self.hypotheses, self.data_analysis_results)
        self.assertIn("Simulation results", simulation_results)

    @patch('src.agents.experiment_agent.GeminiAPI.generate_content')
    def test_run_simulation_empty_response(self, mock_generate_content):
        """Test simulation run with an empty response from Gemini API."""
        mock_generate_content.return_value = ""
        experiment_agent = ExperimentAgent(config=self.dummy_config)
        simulation_results = experiment_agent.run_simulation(self.hypotheses, self.data_analysis_results)
        self.assertEqual(simulation_results, "")

    @patch('src.agents.experiment_agent.GeminiAPI.generate_content')
    def test_run_simulation_api_error(self, mock_generate_content):
        """Test simulation run when the Gemini API raises an exception."""
        mock_generate_content.side_effect = Exception("API Error")
        experiment_agent = ExperimentAgent(config=self.dummy_config)
        simulation_results = experiment_agent.run_simulation(self.hypotheses, self.data_analysis_results)
        self.assertEqual(simulation_results, "")

    def test_initialization_missing_api_key(self):
        """Test ExperimentAgent initialization with a missing API key in the config."""
        with self.assertRaises(KeyError):
            ExperimentAgent(config={'model_name': 'gemini-2.0-flash'})


if __name__ == '__main__':
    unittest.main()