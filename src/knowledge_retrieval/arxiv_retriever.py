import sys
import os
import logging
import arxiv
from typing import List, Dict, Any

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


class ArxivRetriever:
    """
    Module for retrieving research papers from ArXiv.
    """

    def __init__(self):
        """
        Initializes the ArxivRetriever.
        """
        logger.info("ArxivRetriever initialized.")

    def search_arxiv(self, query: str, max_results: int = 10) -> List[Dict[str, str]]:
        """
        Searches ArXiv for papers matching the given query.

        Args:
            query: The search query.
            max_results: The maximum number of results to return.

        Returns:
            A list of dictionaries, where each dictionary represents a paper and contains its title, abstract, and URL.
        """
        try:
            search = arxiv.Search(
                query=query,
                max_results=max_results,
                sort_by=arxiv.SortCriterion.Relevance
            )
            results = []
            for result in search.results():
                paper_info = {
                    "title": result.title,
                    "abstract": result.summary,
                    "url": result.pdf_url
                }
                results.append(paper_info)
            logger.info(f"Retrieved {len(results)} papers from ArXiv for query: {query}")
            return results
        except Exception as e:
            logger.exception(f"Error searching ArXiv: {e}")
            return []


if __name__ == "__main__":
    # Example Usage:
    # 1. Run this script: `python src/knowledge_retrieval/arxiv_retriever.py`

    # Instantiate the ArxivRetriever
    arxiv_retriever = ArxivRetriever()

    # Define a search query
    search_query = "quantum computing"

    # Search ArXiv
    papers = arxiv_retriever.search_arxiv(search_query, max_results=5)

    # Print the results
    print("ArXiv Search Results:")
    for paper in papers:
        print(f"Title: {paper['title']}")
        print(f"Abstract: {paper['abstract'][:200]}...")  # Print first 200 characters of abstract
        print(f"URL: {paper['url']}")
        print("-" * 20)