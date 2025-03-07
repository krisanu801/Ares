import sys
import os
import logging
from typing import List, Dict, Any
from pubmed_parser import parse_medline_xml, parse_pubmed_paragraph

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


class PubmedRetriever:
    """
    Module for retrieving research papers from PubMed.
    """

    def __init__(self):
        """
        Initializes the PubmedRetriever.
        """
        logger.info("PubmedRetriever initialized.")

    def search_pubmed(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Searches PubMed for papers matching the given query.

        Args:
            query: The search query.
            max_results: The maximum number of results to return.  Note: PubMed API limits and requires handling.  This example uses a local XML file for demonstration.  A full implementation would require using the Entrez API with proper rate limiting and error handling.

        Returns:
            A list of dictionaries, where each dictionary represents a paper and contains its title, abstract, and PubMed ID.
        """
        try:
            # This is a placeholder.  A real implementation would use the Entrez API.
            # For demonstration purposes, we'll load data from a local XML file.
            # Replace 'pubmed_result.xml' with the path to your PubMed XML file.
            # You can obtain this XML file by searching PubMed and saving the results in XML format.

            # Example using a dummy XML file (replace with your actual file)
            xml_file = "data/pubmed_result.xml"  # Ensure this file exists or create a dummy one

            if not os.path.exists(xml_file):
                logger.warning("PubMed XML file not found. Returning empty list.  Please create a dummy file or implement Entrez API integration.")
                return []

            with open(xml_file, 'r', encoding='utf-8') as f:
                xml_data = f.read()

            parsed_results = parse_medline_xml(xml_data, year_info_only=False)

            results = []
            for i, paper in enumerate(parsed_results):
                if i >= max_results:
                    break
                paper_info = {
                    "title": paper.get('title', 'N/A'),
                    "abstract": paper.get('abstract', 'N/A'),
                    "pmid": paper.get('pmid', 'N/A')
                }
                results.append(paper_info)

            logger.info(f"Retrieved {len(results)} papers from PubMed (using local XML) for query: {query}")
            return results

        except FileNotFoundError:
            logger.error("PubMed XML file not found.  Please create a dummy file or implement Entrez API integration.")
            return []
        except Exception as e:
            logger.exception(f"Error searching PubMed: {e}")
            return []


if __name__ == "__main__":
    # Example Usage:
    # 1.  Create a dummy `data/pubmed_result.xml` file (or replace with a real PubMed XML file).
    # 2.  Run this script: `python src/knowledge_retrieval/pubmed_retriever.py`

    # Instantiate the PubmedRetriever
    pubmed_retriever = PubmedRetriever()

    # Define a search query
    search_query = "cancer immunotherapy"

    # Search PubMed
    papers = pubmed_retriever.search_pubmed(search_query, max_results=5)

    # Print the results
    print("PubMed Search Results:")
    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Abstract: {paper['abstract'][:200]}...")  # Print first 200 characters of abstract
        print(f"PMID: {paper['pmid']}")
        print("-" * 20)