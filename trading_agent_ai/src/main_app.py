import asyncio
import sys
import qasync
from PyQt6.QtWidgets import QApplication

from .core.config_loader import ConfigLoader
from .core.logger import setup_logging
from .core.database import Database
from .core.event_bus import event_bus
from .data_handler.broker_connector import BrokerConnector
from .news_handler.rss_fetcher import RSSFetcher
from .strategy_handler.main_fuser import MainFuser
from .portfolio_manager.portfolio import Portfolio
from .portfolio_manager.risk_manager import RiskManager
from .portfolio_manager.pnl_tracker import PnLTracker
from .execution_handler.broker_executor import BrokerExecutor
from .ui.main_overlay import MainOverlay
from .ui.ui_manager import UIManager
from .core.event_types import MarketEvent, NewsEvent, VisionEvent, SignalEvent, OrderRequestEvent, FillEvent

async def main():
    # 1. Initialization
    config = ConfigLoader()
    setup_logging()
    db = Database(config.get("Paths", "database_path"))
    
    # 2. Module Setup
    broker_connector = BrokerConnector(config)
    news_fetcher = RSSFetcher(config)
    strategy_fuser = MainFuser()
    
    portfolio = Portfolio()
    risk_manager = RiskManager(portfolio)
    pnl_tracker = PnLTracker(portfolio)
    
    broker_executor = BrokerExecutor(broker_connector.get_api_client())

    # 3. Start Core Services
    await broker_connector.start()
    news_fetcher.start()
    strategy_fuser.start()
    portfolio.start()

    # 4. Event Loop for dispatching events
    async def event_dispatcher():
        while True:
            event = await event_bus.get()
            if isinstance(event, (MarketEvent, NewsEvent, VisionEvent)):
                await strategy_fuser._process_signals()
            elif isinstance(event, SignalEvent):
                await risk_manager.on_signal(event)
            elif isinstance(event, OrderRequestEvent):
                await broker_executor.on_order_request(event)
            elif isinstance(event, FillEvent):
                portfolio.on_fill(event)
            elif isinstance(event, MarketEvent):
                await pnl_tracker.on_market_data(event)
            event_bus.task_done()

    # Start the dispatcher
    dispatcher_task = asyncio.create_task(event_dispatcher())

    # 5. UI Setup
    app = QApplication.instance() or QApplication(sys.argv)
    
    overlay = MainOverlay()
    ui_manager = UIManager(overlay)
    
    # Start the UI event listener
    ui_listener_task = asyncio.create_task(ui_manager.listen_for_ui_events())
    
    overlay.show()
    
    # The qasync event loop will run both Qt and asyncio events.
    await asyncio.gather(dispatcher_task, ui_listener_task)


if __name__ == "__main__":
    try:
        app = QApplication(sys.argv)
        loop = qasync.QEventLoop(app)
        asyncio.set_event_loop(loop)
        
        with loop:
            loop.run_until_complete(main())
            
    except KeyboardInterrupt:
        print("Application shutting down.")
