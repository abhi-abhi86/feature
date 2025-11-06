# TODO: AI-Powered Trading Agent (Zero-Budget MVP) Implementation

## Phase 1: Core Infrastructure (Foundation) - In Progress
- [ ] `src/core/config_loader.py`: Implement ConfigLoader class to read main_config.ini, logging.ini, prompts.json using configparser and json.
- [ ] `src/core/logger.py`: Implement setup_logging() function to configure logging from logging.ini.
- [ ] `src/core/event_bus.py`: Define global asyncio.Queue as event_bus.
- [ ] `src/core/event_types.py`: Define dataclasses for all events (MarketEvent, NewsEvent, VisionEvent, SignalEvent, etc.).
- [ ] `src/core/exceptions.py`: Define custom exception classes (e.g., BrokerConnectionError).
- [ ] `src/core/database.py`: Implement Database class for SQLite connection, with methods like save_trade(), get_trade_history().
- [ ] `src/core/sentiment.py`: Implement SentimentAnalyzer class using vaderSentiment for get_sentiment(text).
- [ ] `config/main_config.ini`: Populate with sample sections [Broker], [API], [General].
- [ ] `config/logging.ini`: Populate with basic logging config.
- [ ] `config/prompts.json`: Populate with sample prompts for Phase 2.
- [ ] `requirements.txt`: List all dependencies (e.g., pyqt6, ultralytics, vaderSentiment, feedparser, etc.).

## Phase 2: Data and News Handlers
- [ ] `src/data_handler/broker_connector.py`: Implement BrokerConnector class to initialize WebSocket and API client.
- [ ] `src/data_handler/websocket_manager.py`: Implement WebsocketManager to listen for market data and emit MarketEvent.
- [ ] `src/data_handler/api_client.py`: Implement APIClient for REST calls (historical data, account info).
- [ ] `src/news_handler/rss_fetcher.py`: Implement RSSFetcher to fetch news and emit NewsEvent.
- [ ] `src/news_handler/feed_manager.py`: Implement FeedManager to load RSS URLs from config.

## Phase 3: Strategy and Portfolio Handlers
- [ ] `src/strategy_handler/main_fuser.py`: Implement MainFuser to listen for events and fuse signals.
- [ ] `src/strategy_handler/strategies/base_strategy.py`: Define BaseStrategy abstract class.
- [ ] `src/strategy_handler/strategies/multi_fusion.py`: Implement MultiFusionStrategy with fusion logic (YOLO + Prediction + Sentiment).
- [ ] `src/strategy_handler/signal_generator.py`: Implement SignalGenerator to create SignalEvent.
- [ ] `src/portfolio_manager/portfolio.py`: Implement Portfolio class to track positions.
- [ ] `src/portfolio_manager/risk_manager.py`: Implement RiskManager to validate signals.
- [ ] `src/portfolio_manager/pnl_tracker.py`: Implement PnLTracker to calculate P&L and emit updates.

## Phase 4: Execution Handler and Vision
- [ ] `src/execution_handler/broker_executor.py`: Implement BrokerExecutor to place orders.
- [ ] `src/execution_handler/order_manager.py`: Implement OrderManager to track order lifecycle.
- [ ] `src/execution_handler/sebi_compliance.py`: Implement SEBICompliance for rate limiting and auth.
- [ ] `src/vision/capture.py`: Implement screen capture using mss.
- [ ] `src/vision/ocr.py`: Implement OCR using pytesseract.
- [ ] `src/vision/perception.py`: Implement VisionModule for YOLO inference and VisionEvent emission.

## Phase 5: UI and Main App
- [ ] `src/ui/main_overlay.py`: Implement MainOverlay as transparent PyQt window.
- [ ] `src/ui/ui_manager.py`: Implement UIManager to connect event_bus to UI widgets.
- [ ] `src/ui/widgets/chat_widget.py`: Implement ChatWidget for Phase 2 chat.
- [ ] `src/ui/widgets/plot_widget.py`: Implement PlotWidget for P&L chart using pyqtgraph.
- [ ] `src/ui/widgets/alert_widget.py`: Implement AlertWidget for toasts/pop-ups.
- [ ] `src/ui/widgets/config_widget.py`: Implement ConfigWidget for settings.
- [ ] `src/ui/widgets/status_widget.py`: Implement StatusWidget for connection status.
- [ ] `src/main_app.py`: Implement main entry point to initialize modules, event_bus, DB, UI, and start asyncio loop.

## Phase 6: Generative AI (Phase 2)
- [ ] `src/generative_ai/llm_client.py`: Implement LLMClient wrapper for Ollama.
- [ ] `src/generative_ai/prompt_builder.py`: Implement prompt building functions.

## Phase 7: ML Pipeline and Backtester (Offline Scripts)
- [ ] `ml_pipeline/data_processor.py`: Implement data cleaning script.
- [ ] `ml_pipeline/feature_engineering.py`: Implement feature addition using TA-Lib.
- [ ] `ml_pipeline/train_vision.py`: Implement YOLO training script.
- [ ] `ml_pipeline/train_prediction.py`: Implement LSTM-Transformer training.
- [ ] `backtester/engine.py`: Implement BacktestEngine using vectorbt.
- [ ] `backtester/strategies.py`: Implement vectorized strategies.
- [ ] `backtester/reporting.py`: Implement reporting with pyfolio.

## Phase 8: Tests and Tools
- [ ] Implement test files in tests/ with unit tests for key modules.
- [ ] Implement tools/ scripts (data_collector.py, db_inspector.py, etc.).

## Followup Steps
- [ ] Install dependencies via pip install -r requirements.txt.
- [ ] Run app locally to test after each phase.
- [ ] Ensure data in data/ and train models to models/.
- [ ] Test with mock broker API initially.
- [ ] Document setup in docs/.
