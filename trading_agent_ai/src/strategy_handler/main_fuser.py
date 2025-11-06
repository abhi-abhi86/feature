import asyncio
import logging
from datetime import datetime

from ..core.event_bus import event_bus
from ..core.event_types import MarketEvent, NewsEvent, VisionEvent
from .strategies.multi_fusion import MultiFusionStrategy
from .signal_generator import SignalGenerator

logger = logging.getLogger(__name__)

class MainFuser:
    def __init__(self):
        self.strategy = MultiFusionStrategy()
        self.signal_generator = SignalGenerator()
        self.market_state = {}
        self.news_state = {}
        self.vision_state = {}

    def start(self):
        logger.info("Starting Main Fuser...")
        self.listen_task = asyncio.create_task(self._listen_for_events())
        logger.info("Main Fuser started.")

    async def _listen_for_events(self):
        while True:
            event = await event_bus.get()
            if isinstance(event, MarketEvent):
                self.market_state[event.ticker] = event
            elif isinstance(event, NewsEvent):
                # Simple logic: assume news affects all tickers for now
                self.news_state['latest'] = event
            elif isinstance(event, VisionEvent):
                self.vision_state[event.ticker] = event
            
            # After any new event, try to generate a signal
            await self._process_signals()
            event_bus.task_done()

    async def _process_signals(self):
        # This is a simplified logic. A real system would have a more
        # sophisticated way to decide which tickers to process.
        all_tickers = set(self.market_state.keys()) | set(self.vision_state.keys())
        
        for ticker in all_tickers:
            market_data = self.market_state.get(ticker)
            news_data = self.news_state.get('latest')
            vision_data = self.vision_state.get(ticker)

            # We need at least market data to proceed
            if not market_data:
                continue

            signal = self.strategy.calculate_signal(market_data, news_data, vision_data)
            
            if signal and signal != 'HOLD':
                await self.signal_generator.generate_signal(
                    ticker=ticker,
                    signal=signal,
                    market_data=market_data,
                    news_data=news_data,
                    vision_data=vision_data
                )
