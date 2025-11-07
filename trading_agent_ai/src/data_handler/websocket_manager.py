import asyncio
import websockets
import json
import logging
import random
from datetime import datetime

from ..core.config_loader import ConfigLoader
from ..core.event_bus import event_bus
from ..core.event_types import MarketEvent

logger = logging.getLogger(__name__)

class WebsocketManager:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.websocket_url = self.config.get("Broker", "websocket_url")
        self.websocket = None
        self.mock_mode = False

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.websocket_url)
            logger.info(f"Connected to WebSocket at {self.websocket_url}")
            # You might need to send an authentication message here
            # depending on the broker's API
        except Exception as e:
            logger.warning(f"Failed to connect to WebSocket: {e}")
            logger.info("Switching to mock mode for testing/development")
            self.mock_mode = True
            # Don't raise exception, continue in mock mode

    async def listen(self):
        if self.mock_mode:
            await self._mock_listen()
            return
            
        if not self.websocket:
            logger.error("WebSocket is not connected and not in mock mode.")
            return

        try:
            while True:
                message = await self.websocket.recv()
                data = json.loads(message)
                # Process the data and create a MarketEvent
                # This part is highly dependent on the broker's data format
                # Example for a hypothetical format:
                if data.get('type') == 'tick':
                    market_event = MarketEvent(
                        timestamp=datetime.now(),
                        ticker=data['ticker'],
                        price=data['price'],
                        volume=data['volume']
                    )
                    await event_bus.put(market_event)
                    logger.debug(f"Published MarketEvent: {market_event}")
        except websockets.exceptions.ConnectionClosed:
            logger.warning("WebSocket connection closed.")
        except Exception as e:
            logger.error(f"An error occurred in WebSocket listener: {e}")

    async def _mock_listen(self):
        """Generate mock market data for testing purposes."""
        logger.info("Starting mock market data generation")
        tickers = ["NIFTY", "BANKNIFTY", "RELIANCE", "TCS", "INFY"]
        
        while True:
            try:
                # Generate mock market data
                ticker = random.choice(tickers)
                base_price = {"NIFTY": 18000, "BANKNIFTY": 42000, "RELIANCE": 2500, "TCS": 3500, "INFY": 1500}
                price_change = random.uniform(-50, 50)
                price = base_price.get(ticker, 1000) + price_change
                volume = random.randint(1000, 10000)
                
                market_event = MarketEvent(
                    timestamp=datetime.now(),
                    ticker=ticker,
                    price=round(price, 2),
                    volume=volume
                )
                
                await event_bus.put(market_event)
                logger.debug(f"Published Mock MarketEvent: {market_event}")
                
                # Wait 5 seconds between mock data points
                await asyncio.sleep(5)
                
            except Exception as e:
                logger.error(f"Error in mock data generation: {e}")
                await asyncio.sleep(1)

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            logger.info("WebSocket connection closed.")
        elif self.mock_mode:
            logger.info("Mock mode stopped.")
