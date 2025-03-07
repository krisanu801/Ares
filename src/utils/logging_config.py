import sys
import os
import logging
import logging.config
import yaml
from typing import Dict, Any

# Dynamically adjust sys.path to allow imports from the project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)


def setup_logging(default_path: str = 'configs/logging.yaml', default_level: int = logging.INFO, env_key: str = 'LOG_CFG') -> None:
    """
    Setup logging configuration.

    Args:
        default_path: Path to the logging configuration file (YAML).
        default_level: Default logging level if no configuration file is found.
        env_key: Environment variable key for specifying the logging configuration file path.
    """
    path = os.getenv(env_key, default_path)
    if path and os.path.exists(path):
        try:
            with open(path, 'r') as f:
                config = yaml.safe_load(f)
            logging.config.dictConfig(config)
        except Exception as e:
            logging.basicConfig(level=default_level)
            logging.error(f"Error loading logging configuration from {path}: {e}. Using basic configuration.")
    else:
        logging.basicConfig(level=default_level)
        logging.warning(f"Logging configuration file not found at {path}. Using basic configuration.")


if __name__ == '__main__':
    # Example Usage:
    # 1. Create a `configs/logging.yaml` file (see example below).
    # 2. Run this script: `python src/utils/logging_config.py`
    # 3. Check the console for log messages.

    # Example `configs/logging.yaml` file:
    # ---
    # version: 1
    # formatters:
    #   simple:
    #     format: '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    # handlers:
    #   console:
    #     class: logging.StreamHandler
    #     level: DEBUG
    #     formatter: simple
    #     stream: ext://sys.stdout
    # root:
    #   level: INFO
    #   handlers: [console]
    # disable_existing_loggers: False

    # Set up logging (using default settings)
    setup_logging()

    # Get a logger
    logger = logging.getLogger(__name__)

    # Log some messages
    logger.debug("This is a debug message.")
    logger.info("This is an info message.")
    logger.warning("This is a warning message.")
    logger.error("This is an error message.")
    logger.critical("This is a critical message.")