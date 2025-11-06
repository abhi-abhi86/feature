# AI-Powered Trading Agent (Zero-Budget MVP)

This project is a desktop-first, AI-powered trading agent designed for the Indian market. It leverages a multi-modal AI approach, fusing signals from computer vision, predictive modeling, and real-time news sentiment analysis. The entire application is built on a "zero-budget" philosophy, using a 100% free and open-source technology stack.

## Key Features

- **Multi-Modal AI Strategy**: The core "Alpha Engine" fuses signals from three distinct sources for high-confidence trade suggestions:
    1.  **Image-Based Signals**: A YOLOv8 model trained to recognize chart patterns (e.g., Bullish Flags, Head & Shoulders) directly from screen captures.
    2.  **Predictive Signals**: A hybrid LSTM-Transformer model to forecast price direction from historical data.
    3.  **News Sentiment Signals**: Real-time "current affairs" analysis by fetching headlines from public RSS feeds and scoring them locally with the VADER sentiment analysis engine.
- **Zero-Budget Architecture**: Runs entirely on your local machine with no cloud costs.
    - **Data**: Connects to broker-provided APIs for market data and uses free public RSS feeds for news.
    - **Database**: Uses a local SQLite database (`app_data.db`) for all live data storage (trades, signals, etc.).
    - **Generative AI**: (Phase 2) Integrates with local LLMs like Llama 3 via Ollama for a "Chart-GPT" feature, providing free, context-aware explanations of trading signals.
- **Desktop-First UI**: A transparent, always-on-top UI overlay built with PyQt6 that displays critical information without obscuring your main trading platform.
- **Event-Driven Architecture**: A monolithic but modular design where components (Data, News, Strategy, Portfolio, Execution) run in a single application and communicate asynchronously via an in-memory event bus (`asyncio.Queue`).
- **Compliance by Design**: The execution handler is built with the SEBI framework in mind, incorporating logic for rate-limiting and 2FA token management.
- **Offline Tooling**: Includes a complete `ml_pipeline` for processing data and training your own models, and a `backtester` (using VectorBT) to test strategies before deployment.

## System Architecture (Monolithic Desktop App)

The application runs as a single process, with modules communicating via an internal event bus.

1.  **Data Handler**: Connects to the broker's WebSocket for real-time price data and its REST API for historical data and account information.
2.  **News Handler**: Fetches headlines from RSS feeds using `feedparser` and passes them to the sentiment analyzer.
3.  **Strategy Handler (Alpha Engine)**: The brain of the operation. It listens for market, news, and vision events and uses the `MultiFusionStrategy` to generate a trading signal ('BUY', 'SELL', 'HOLD').
4.  **Portfolio & Risk Manager**: Tracks current positions, cash, and P&L. The `RiskManager` acts as a gatekeeper, validating signals against pre-defined risk rules (e.g., max order size) before allowing a trade.
5.  **Execution Handler**: The only module authorized to place trades. It listens for approved order requests and sends them to the broker API, while managing order lifecycle and compliance.
6.  **UI (Overlay)**: The PyQt frontend, which listens for events (like P&L updates) and displays them.

## Technology Stack

- **Core Language**: Python (3.10+)
- **Core & EDA**: `asyncio`, `asyncio.Queue`
- **Data Handling & Storage**: `pandas`, `numpy`, `sqlite3`, `pyarrow`, `feedparser`
- **Vision Module**: `mss`, `opencv-python`, `pytesseract`, `ultralytics` (for YOLOv8)
- **Analytics & ML**: `torch`, `transformers`, `ta-lib`, `scikit-learn`, `vaderSentiment`
- **Backtesting**: `vectorbt`, `pyfolio`
- **UI**: `PyQt6`, `pyqtgraph`, `qasync`
- **MLOps**: `mlflow` (for local experiment tracking)
- **Generative AI (Phase 2)**: `ollama`

## Setup and Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/abhi-abhi86/feature.git
    cd feature/trading_agent_ai
    ```

2.  **Prerequisites**
    - This project uses `TA-Lib`. You must install the underlying C library before installing the Python wrapper. Follow the instructions for your OS [here](https://github.com/mrjbq7/ta-lib).

3.  **Create a Virtual Environment**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
    ```

4.  **Install Dependencies**
    ```bash
    pip install -r requirements.txt
    ```

5.  **Configure API Keys**
    - Create a file named `broker_api_keys.env` inside the `config/` directory.
    - Add your broker's API key, secret, and any other required tokens in this format:
      ```
      API_KEY=your_api_key
      API_SECRET=your_api_secret
      ```
    - This file is gitignored for security.

6.  **Add Trained Models**
    - Place your trained YOLOv8 model (e.g., `best.pt`) in `models/vision/`.
    - Place your trained prediction model (e.g., `lstm_transformer.pt`) in `models/prediction/`.

## Usage

To run the application, execute the main entry point:

```bash
python src/main_app.py
```

## Project Roadmap

### Phase 1: The Core "Image-Based" App (MVP)
- [x] Build the 5-module monolithic desktop app.
- [x] Integrate broker API for data and execution.
- [x] Integrate `feedparser` for RSS news and `VADER` for sentiment.
- [x] Train and integrate the YOLOv8 vision model.
- [x] Build the `Strategy Handler` to fuse signals from vision, prediction, and sentiment.
- [x] Build the PyQt overlay UI.
- [x] Implement simple, template-based explanations for signals.

### Phase 2: Add "Local-AI" Chat (The "Chart-GPT" Feature)
- [ ] Set up a local LLM runner like Ollama.
- [ ] Integrate the Ollama Python client into `generative_ai/llm_client.py`.
- [ ] Build the `chat_widget.py` for the UI.
- [ ] Build the `prompt_builder.py` to send rich, context-aware prompts to the local LLM for trade explanations.

### Phase 3: The "Push to Cloud" (Future Upgrade)
- [ ] Refactor the application into `src/client` and `src/server` components.
- [ ] Replace the local LLM with a cloud-based one (e.g., Gemini API).
- [ ] Migrate the SQLite database to a cloud database (e.g., Cloud Firestore).
- [ ] Deploy the server component to a cloud virtual machine.
