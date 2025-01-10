# Capstone Project - AI-Driven LLM Agent for Data WorkFlow

## Description
This project implements an AI-powered chatbot for vehicle data workflow. It enables users to query vehicle-related information, fetches data from relevant websites and displays it in user-friendly formats.

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

## Contributors
Anjali Garg - Anjaligarg1010@gmail.com
Basil John Milton Muthuraj - bjmm1296@gmail.com
Karishma Kamble - kkarishma2809@gmail.com
Mohan Areti - Mohan.areti7@gmail.com
Yun Wu Hailey - yo861128@gmail.com

