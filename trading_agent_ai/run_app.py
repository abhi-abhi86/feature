#!/usr/bin/env python3
"""
Main runner script for the Trading Agent AI application.
This script handles the proper module imports and runs the application.
"""

import os
import sys
import asyncio
import qasync
from PyQt6.QtWidgets import QApplication

# Add the project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

from src.core.config_loader import ConfigLoader
from src.core.logger import setup_logging
from src.core.database import Database
from src.core.event_bus import event_bus
from src.data_handler.broker_connector import BrokerConnector
from src.news_handler.rss_fetcher import RSSFetcher
from src.strategy_handler.main_fuser import MainFuser
from src.portfolio_manager.portfolio import Portfolio
from src.portfolio_manager.risk_manager import RiskManager
from src.portfolio_manager.pnl_tracker import PnLTracker
from src.execution_handler.broker_executor import BrokerExecutor
from src.ui.main_overlay import MainOverlay
from src.ui.ui_manager import UIManager
from src.core.event_types import MarketEvent, NewsEvent, VisionEvent, SignalEvent, OrderRequestEvent, FillEvent

async def main():
    """Main application entry point."""
    # Initialize configuration and logging
    config = ConfigLoader()
    logging_config_path = os.path.join(project_root, 'config', 'logging.ini')
    setup_logging(logging_config_path)
    
    # Initialize database
    db = Database(config)
    db.initialize()
    
    # Initialize core components
    broker_connector = BrokerConnector(config)
    rss_fetcher = RSSFetcher(config)
    main_fuser = MainFuser()
    portfolio = Portfolio()
    risk_manager = RiskManager(portfolio)
    pnl_tracker = PnLTracker(portfolio)
    broker_executor = BrokerExecutor(config)
    
    # Initialize UI components
    main_overlay = MainOverlay()
    ui_manager = UIManager(main_overlay)
    
    # Event dispatcher
    async def event_dispatcher():
        try:
            while True:
                event = await asyncio.wait_for(event_bus.get(), timeout=1.0)
                
                if isinstance(event, MarketEvent):
                    await main_fuser.handle_market_event(event)
                    # Portfolio doesn't handle market events directly in this implementation
                    await pnl_tracker.on_market_data(event)
                    ui_manager.update_market_data(event)
                    
                elif isinstance(event, NewsEvent):
                    await main_fuser.handle_news_event(event)
                    
                elif isinstance(event, VisionEvent):
                    await main_fuser.handle_vision_event(event)
                    
                elif isinstance(event, SignalEvent):
                    # Check with risk manager
                    await risk_manager.on_signal(event)
                    ui_manager.add_signal(event)
                    
                elif isinstance(event, OrderRequestEvent):
                    await broker_executor.execute_order(event)
                    
                elif isinstance(event, FillEvent):
                    portfolio.on_fill(event)
                    # PnLTracker doesn't have update_fill method
                    ui_manager.update_portfolio(portfolio.get_positions())
                    
        except asyncio.TimeoutError:
            # Normal timeout, continue
            pass
        except Exception as e:
            print(f"Error in event dispatcher: {e}")
    
    # Start all components
    try:
        print("Starting Trading Agent AI...")
        
        # Start background services
        await broker_connector.start()
        rss_fetcher.start()
        
        # Update UI with connection status
        ui_manager.update_broker_status(broker_connector.is_connected())
        ui_manager.update_news_status(True)
        
        # Start UI event listener
        _ui_task = asyncio.create_task(ui_manager.listen_for_ui_events())
        
        # Start event dispatcher  
        _dispatcher_task = asyncio.create_task(event_dispatcher())  # Keep reference for GC
        
        # Show UI
        main_overlay.show()
        
        print("Trading Agent AI started successfully!")
        print("Demo mode is enabled - using mock market data")
        print("Close the UI window or press Ctrl+C to stop the application")
        
        # Show UI
        main_overlay.show()
        
        # Wait for the application to exit
        print("Application running. Close the window to exit.")
        
        # Set up clean exit handling
        import signal
        def signal_handler(signum, frame):
            print("\nReceived signal, shutting down...")
            app.quit()
        
        signal.signal(signal.SIGINT, signal_handler)
        
        # Keep running until the application quits
        try:
            while True:
                await asyncio.sleep(1)
        except asyncio.CancelledError:
            print("Main task cancelled")
            raise
            
    except KeyboardInterrupt:
        print("\nShutting down Trading Agent AI...")
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Cleanup
        print("Cleaning up...")
        await broker_connector.stop()
        rss_fetcher.stop()
        db.close()
        print("Cleanup completed")

if __name__ == "__main__":
    # Create PyQt application
    app = QApplication(sys.argv)
    
    # Set up async event loop
    loop = qasync.QEventLoop(app)
    asyncio.set_event_loop(loop)
    
    # Create a task for the main application
    main_task = asyncio.ensure_future(main())
    
    try:
        # Run the application
        loop.run_forever()
    except KeyboardInterrupt:
        print("\nReceived interrupt signal...")
    finally:
        # Cancel the main task if it's still running
        if not main_task.done():
            main_task.cancel()
        
        # Close the event loop
        loop.close()