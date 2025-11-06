# Development Environment Setup

This guide provides instructions on how to set up the local development environment for the AI-Powered Trading Agent.

## 1. Prerequisites

- **Python:** You will need Python 3.10 or newer. You can download it from [python.org](https://python.org).
- **Git:** Ensure Git is installed on your system. You can download it from [git-scm.com](https://git-scm.com).
- **Tesseract OCR:** The vision module depends on Tesseract for OCR. 
  - **macOS:** `brew install tesseract`
  - **Ubuntu:** `sudo apt-get install tesseract-ocr`
  - **Windows:** Download from the official Tesseract repository.

## 2. Clone the Repository

Clone the project repository to your local machine:

```bash
git clone <repository-url>
cd trading_agent_ai
```

## 3. Create a Virtual Environment

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
python -m venv venv
```

Activate the virtual environment:

- **macOS/Linux:**
  ```bash
  source venv/bin/activate
  ```
- **Windows:**
  ```bash
  .\venv\Scripts\activate
  ```

## 4. Install Dependencies

Install all the required Python packages using the `requirements.txt` file:

```bash
pip install -r requirements.txt
```

## 5. Configure API Keys

Your broker API keys and other secrets are managed through an environment file.

1.  Navigate to the `config/` directory.
2.  Create a new file named `broker_api_keys.env`.
3.  Add your keys to this file in the following format:

    ```env
    BROKER_API_KEY="YOUR_API_KEY"
    BROKER_API_SECRET="YOUR_API_SECRET"
    # Add any other required tokens or keys
    ```

    **Note:** This file is listed in `.gitignore` and will not be committed to the repository.

## 6. (Optional) Phase 2: Local LLM Setup

For the "Chart-GPT" feature, you will need to run a local Large Language Model.

1.  **Install Ollama:** Follow the instructions on [ollama.ai](https://ollama.ai) to install the Ollama server on your desktop.

2.  **Download a Model:** Pull a model that you want to use. We recommend a small, fast model for development.

    ```bash
    ollama pull phi3
    ```

## 7. Run the Application

Once the setup is complete, you can run the main application using the provided script:

```bash
sh scripts/run_app.sh
```
