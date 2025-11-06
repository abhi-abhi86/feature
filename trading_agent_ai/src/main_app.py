import asyncio
import sys
from pathlib import Path
from PyQt6.QtWidgets import QApplication

# Add the project root to the Python path to allow for absolute imports
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

# Core components
from src.core.config_loader import ConfigLoader
from src.core.logger import setup_logging
from src.core.event_bus import EventBus
from src.core.database import DatabaseManager

# Main application modules
from src.data_handler.broker_connector import BrokerConnector
from src.news_handler.rss_fetcher import RSSFetcher
from src.strategy_handler.main_fuser import MainFuser
from src.portfolio_manager.portfolio import Portfolio
from src.execution_handler.broker_executor import BrokerExecutor

# UI components
from src.ui.main_overlay import MainOverlay
from src.ui.ui_manager import UIManager

# --- Global Exception Hook ---
def handle_exception(exc_type, exc_value, exc_traceback):
    """Log any uncaught exceptions."""
    if issubclass(exc_type, KeyboardInterrupt):
        sys.__excepthook__(exc_type, exc_value, exc_traceback)
        return
    log.critical("Uncaught exception:", exc_info=(exc_type, exc_value, exc_traceback))

sys.excepthook = handle_exception

# --- Main Application Class ---
class TradingAgentApp:
    """The main application class that orchestrates all components."""
    def __init__(self):
        # Initial setup
        self.config = ConfigLoader()
        self.log = setup_logging(self.config.get('Logging', 'log_config_path'))
        self.log.info("--- Starting Trading Agent AI ---")

        # Core components
        self.event_bus = EventBus()
        self.db_manager = DatabaseManager(self.config.get('Database', 'db_path'))

        # Initialize main modules
        self.log.info("Initializing application modules...")
        self.broker_connector = BrokerConnector(self.config, self.event_bus)
        self.rss_fetcher = RSSFetcher(self.config, self.event_bus)
        self.strategy_fuser = MainFuser(self.config, self.event_bus)
        self.portfolio = Portfolio(self.config, self.event_bus, self.db_manager)
        self.broker_executor = BrokerExecutor(self.config, self.event_bus)
        
        # Initialize UI
        self.log.info("Initializing UI...")
        self.qt_app = QApplication(sys.argv)
        self.ui_manager = UIManager(self.event_bus)
        self.main_overlay = MainOverlay(self.ui_manager)
        self.ui_manager.set_main_window(self.main_overlay) # Give manager a reference to the window

    async def run(self):
        """Starts all asynchronous tasks and the UI event loop."""
        self.log.info("Starting application event loop...")
        
        # Create a list of all async tasks to run
        tasks = [
            self.broker_connector.run(),
            self.rss_fetcher.run(),
            self.strategy_fuser.run(),
            self.portfolio.run(),
            self.broker_executor.run(),
            self.ui_manager.run() # The UI manager also runs in the async loop
        ]

        # Show the UI
        self.main_overlay.show()

        # Run all tasks concurrently
        await asyncio.gather(*tasks)

    def start(self):
        """Public method to start the application."""
        try:
            asyncio.run(self.run())
        except KeyboardInterrupt:
            self.log.info("Application shutting down gracefully.")
        finally:
            self.qt_app.quit()

if __name__ == "__main__":
    # To avoid issues with PyQt and asyncio, we use this structure.
    # The QApplication must be created before the asyncio loop starts.
    app = TradingAgentApp()
    app.start()
