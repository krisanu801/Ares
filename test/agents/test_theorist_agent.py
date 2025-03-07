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
    from src.agents.theorist_agent import TheoristAgent
except ImportError as e:
    print(f"ImportError: {e}.  Check that the project structure is correct and that the necessary files exist.")
    sys.exit(1)


class TestTheoristAgent(unittest.TestCase):

    def setUp(self):
        """Set up for test methods."""
        self.dummy_config: Dict[str, Any] = {
            'gemini_api_key': 'TEST_API_KEY',
            'model_name': 'gemini-2.0-flash'
        }
        self.research_problem = "Investigate the effects of novel materials on solar cell efficiency."

    @patch('src.agents.theorist_agent.GeminiAPI.generate_content')
    def test_generate_hypotheses_success(self, mock_generate_content):
        """Test successful hypothesis generation."""
        mock_generate_content.return_value = "1. Hypothesis 1\n2. Hypothesis 2"
        theorist = TheoristAgent(config=self.dummy_config)
        hypotheses = theorist.generate_hypotheses(self.research_problem)
        self.assertEqual(len(hypotheses), 2)
        self.assertEqual(hypotheses[0], "Hypothesis 1")
        self.assertEqual(hypotheses[1], "Hypothesis 2")

    @patch('src.agents.theorist_agent.GeminiAPI.generate_content')
    def test_generate_hypotheses_empty_response(self, mock_generate_content):
        """Test hypothesis generation with an empty response from Gemini API."""
        mock_generate_content.return_value = ""
        theorist = TheoristAgent(config=self.dummy_config)
        hypotheses = theorist.generate_hypotheses(self.research_problem)
        self.assertEqual(len(hypotheses), 0)

    @patch('src.agents.theorist_agent.GeminiAPI.generate_content')
    def test_generate_hypotheses_api_error(self, mock_generate_content):
        """Test hypothesis generation when the Gemini API raises an exception."""
        mock_generate_content.side_effect = Exception("API Error")
        theorist = TheoristAgent(config=self.dummy_config)
        hypotheses = theorist.generate_hypotheses(self.research_problem)
        self.assertEqual(len(hypotheses), 0)

    def test_initialization_missing_api_key(self):
        """Test TheoristAgent initialization with a missing API key in the config."""
        with self.assertRaises(KeyError):
            TheoristAgent(config={'model_name': 'gemini-2.0-flash'})

    def test_extract_hypotheses_numbered_list(self):
        """Test extracting hypotheses from a numbered list response."""
        response = "1. Hypothesis A\n2. Hypothesis B\n3. Hypothesis C"
        theorist = TheoristAgent(config=self.dummy_config)
        hypotheses = theorist._extract_hypotheses(response)
        self.assertEqual(hypotheses, ["Hypothesis A", "Hypothesis B", "Hypothesis C"])

    def test_extract_hypotheses_bullet_points(self):
        """Test extracting hypotheses from a bullet point list response."""
        response = "- Hypothesis X\n- Hypothesis Y\n- Hypothesis Z"
        theorist = TheoristAgent(config=self.dummy_config)
        hypotheses = theorist._extract_hypotheses(response)
        self.assertEqual(hypotheses, ["Hypothesis X", "Hypothesis Y", "Hypothesis Z"])

    def test_extract_hypotheses_mixed_format(self):
        """Test extracting hypotheses from a mixed format response."""
        response = "1. Hypothesis P\n- Hypothesis Q\n2. Hypothesis R"
        theorist = TheoristAgent(config=self.dummy_config)
        hypotheses = theorist._extract_hypotheses(response)
        self.assertEqual(hypotheses, ["Hypothesis P", "Hypothesis Q", "Hypothesis R"])

    def test_extract_hypotheses_empty_lines(self):
        """Test extracting hypotheses with empty lines in the response."""
        response = "1. Hypothesis M\n\n2. Hypothesis N\n"
        theorist = TheoristAgent(config=self.dummy_config)
        hypotheses = theorist._extract_hypotheses(response)
        self.assertEqual(hypotheses, ["Hypothesis M", "Hypothesis N"])

    def test_extract_hypotheses_no_numbering(self):
        """Test extracting hypotheses when there's no numbering or bullet points."""
        response = "Hypothesis 1\nHypothesis 2"
        theorist = TheoristAgent(config=self.dummy_config)
        hypotheses = theorist._extract_hypotheses(response)
        self.assertEqual(hypotheses, []) # Should return empty list as it cannot reliably extract

if __name__ == '__main__':
    unittest.main()