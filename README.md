# ARES: Autonomous Research & Experimentation System

## Project Description

ARES (Autonomous Research & Experimentation System) is an AI scientist designed to autonomously analyze complex scientific problems, generate and test hypotheses, iterate on solutions, and retrieve knowledge from open research sources like ArXiv and PubMed. ARES utilizes the Gemini API for content generation and possesses Chain of Thought (CoT) reasoning, multi-agent collaboration (Theorist AI, Data Scientist AI, Experiment AI, Critic AI), and self-improvement capabilities.

## Features

-   **Autonomous Research:** Analyzes complex scientific problems and proposes innovative solutions.
-   **Hypothesis Generation & Testing:** Generates and tests hypotheses using the Gemini API.
-   **Multi-Agent Collaboration:** Employs a team of AI agents (Theorist, Data Scientist, Experiment, Critic) for collaborative problem-solving.
-   **Chain of Thought (CoT) Reasoning:** Utilizes CoT reasoning to improve the quality of generated content.
-   **Knowledge Retrieval:** Retrieves relevant research papers from ArXiv and PubMed.
-   **Self-Improvement:** Continuously learns and improves its reasoning and experimentation capabilities.
-   **Ethical AI Use:** Designed to ensure ethical AI use in research and experimentation.

## Project Structure

```
Ares/
├── src/
│   ├── agents/
│   │   ├── theorist_agent.py
│   │   ├── data_scientist_agent.py
│   │   ├── experiment_agent.py
│   │   └── critic_agent.py
│   ├── knowledge_retrieval/
│   │   ├── arxiv_retriever.py
│   │   └── pubmed_retriever.py
│   ├── experimentation/
│   │   ├── simulation_engine.py
│   │   └── experiment_runner.py
│   ├── utils/
│   │   ├── gemini_api.py
│   │   └── logging_config.py
│   └── main.py
├── test/
│   ├── agents/
│   │   ├── test_theorist_agent.py
│   │   ├── test_data_scientist_agent.py
│   │   ├── test_experiment_agent.py
│   │   └── test_critic_agent.py
├── configs/
│   ├── config.yaml
│   └── logging.yaml
├── data/
│   └── pubmed_result.xml  (Example PubMed XML data)
├── logs/
├── README.md
├── requirements.txt
└── setup.py
```

## Setup Instructions

1.  **Create a virtual environment:**

    ```bash
    python -m venv venv
    ```
2.  **Activate the virtual environment:**

    -   On Linux/macOS:

        ```bash
        source venv/bin/activate
        ```
    -   On Windows:

        ```bash
        venv\Scripts\activate
        ```
3.  **Install dependencies:**

    ```bash
    pip install -r requirements.txt
    ```
4.  **Configure API keys:**

    -   Create a `configs/config.yaml` file and add your Gemini API key:

        ```yaml
        gemini_api_key: "YOUR_GEMINI_API_KEY"
        ```

## Usage

1.  Run the main application:

    ```bash
    python src/main.py
    ```

2.  Check the logs in the `logs/` directory for output and errors.

## Configuration

-   `configs/config.yaml`: Contains API keys, model names, and other settings.
-   `configs/logging.yaml`: Configures the logging behavior of the application.

## Dependencies

-   `google-generative-ai`: For interacting with the Gemini API.
-   `arxiv`: For retrieving research papers from ArXiv.
-   `pubmed_parser`: For parsing PubMed XML data.
-   `PyYAML`: For reading YAML configuration files.
-   `requests`: For making HTTP requests.
-   `pytest`: For running unit tests.
-   `python-dotenv`: For loading environment variables from a .env file.

## Contributing

Contributions are welcome! Please submit pull requests with detailed descriptions of your changes.

## License

[MIT](LICENSE) (Replace with your desired license)