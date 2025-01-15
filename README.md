# Capstone Project - LLM-Powered AI Agent for Automated Data WorkFlow

## Description
This project implements an AI-powered chatbot designed to streamline the vehicle evaluation workflow for post-accident assessments. The chatbot serves as a valuable tool for vehicle evaluators by fetching essential data from multiple online sources and presenting it in a user-friendly format. Instead of manually searching through various websites, evaluators can now obtain accurate and relevant information in seconds, saving significant time and effort. The agent utilizes web scraping techniques to fetch real-time data and employs Large Language Models (LLMs) via APIs to dynamically interpret and respond to specific user queries. By tailoring its responses based on user inputs, the chatbot ensures personalized and context-specific answers, making it the go-to assistant for vehicle evaluation processes. This project was developed as a capstone for the Analytics Strategy and Practice course at UIC, highlighting its practical impact in solving real-world challenges.

## Prerequisites
- Python 3.x (recommended: 3.9 or above)
- Conda package manager
- Microsoft Edge browser
- Streamlit (installed via the `environment.yml`)

## Setup
1. Create and activate the Conda environment: 
conda env create -f environment.yml conda activate capstone

2. The `config.json` file provided in the project directory already contains the required API key. No additional setup is needed for API configuration.

## Running the Project
Run the chatbot using Streamlit:
streamlit run ccc_ai_agent.py

The command above assumes you are in the correct directory. If you are not, provide the relative or absolute path to `ccc_ai_agent.py`.
e.g.: streamlit run /path/to/ccc_project/ccc_ai_agent.py

This will open the Streamlit app in your default web browser.

## Testing Selenium (Optional)
To verify that Selenium and the WebDriver are configured correctly, run the test script: 
python selenium_test.py

This will open a browser, navigate to Google, and print the page title in the console.

## Troubleshooting
1. **Streamlit Issues**:
   - Ensure you are running the command from the activated `capstone` environment.
   - If Streamlit is not recognized, check the environment setup and re-install it:
     ```
     conda install streamlit
     ```

2. **Selenium Issues**:
   - Ensure Microsoft Edge is installed and updated.
   - If WebDriver fails, download the correct version of the Edge WebDriver from the official Microsoft website.

## Project Files
- `ccc_ai_agent.py`: Main script for running the AI agent application via Streamlit.
- `config.json`: Contains the API key (already pre-configured).
- `environment.yml`: Conda environment file with project dependencies.
- `requirements.txt`: Lists Python dependencies for pip installations (if needed).
- `README.md`: Documentation for project setup and usage.
- `selenium_test.py`: Script to test Selenium WebDriver functionality.
- `ccc_logo.png`: Logo of CCC used in the project interface.
- `uic_logo.png`: Logo of UIC used in the project interface.
- `.gitignore.txt`: Specifies files to ignore during version control (e.g., `config.json`).


