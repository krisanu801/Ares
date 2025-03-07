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
    from src.agents.data_scientist_agent import DataScientistAgent
except ImportError as e:
    print(f"ImportError: {e}.  Check that the project structure is correct and that the necessary files exist.")
    sys.exit(1)


class TestDataScientistAgent(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.dummy_config: Dict[str, Any] = {
            'gemini_api_key': 'TEST_API_KEY',
            'model_name': 'gemini-2.0-flash'
        }
        self.research_problem = "Investigate the impact of different fertilizer types on crop yield."
        self.hypotheses = [
            "Fertilizer A will increase crop yield more than Fertilizer B.",
            "The optimal fertilizer concentration is 100 kg/hectare."
        ]

    @patch('src.agents.data_scientist_agent.GeminiAPI.generate_content')
    def test_analyze_data_success(self, mock_generate_content):
        """Test successful data analysis."""
        mock_generate_content.return_value = "Analysis results: Fertilizer A shows a significant increase in crop yield."
        data_scientist = DataScientistAgent(config=self.dummy_config)
        analysis_results = data_scientist.analyze_data(self.research_problem, self.hypotheses)
        self.assertIn("Analysis results", analysis_results)

    @patch('src.agents.data_scientist_agent.GeminiAPI.generate_content')
    def test_analyze_data_empty_response(self, mock_generate_content):
        """Test data analysis with an empty response from Gemini API."""
        mock_generate_content.return_value = ""
        data_scientist = DataScientistAgent(config=self.dummy_config)
        analysis_results = data_scientist.analyze_data(self.research_problem, self.hypotheses)
        self.assertEqual(analysis_results, "")

    @patch('src.agents.data_scientist_agent.GeminiAPI.generate_content')
    def test_analyze_data_api_error(self, mock_generate_content):
        """Test data analysis when the Gemini API raises an exception."""
        mock_generate_content.side_effect = Exception("API Error")
        data_scientist = DataScientistAgent(config=self.dummy_config)
        analysis_results = data_scientist.analyze_data(self.research_problem, self.hypotheses)
        self.assertEqual(analysis_results, "")

    def test_initialization_missing_api_key(self):
        """Test DataScientistAgent initialization with a missing API key in the config."""
        with self.assertRaises(KeyError):
            DataScientistAgent(config={'model_name': 'gemini-2.0-flash'})


if __name__ == '__main__':
    unittest.main()