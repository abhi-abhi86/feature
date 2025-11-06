import asyncio
import websockets
import json
import logging
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

    async def connect(self):
        try:
            self.websocket = await websockets.connect(self.websocket_url)
            logger.info(f"Connected to WebSocket at {self.websocket_url}")
            # You might need to send an authentication message here
            # depending on the broker's API
        except Exception as e:
            logger.error(f"Failed to connect to WebSocket: {e}")
            raise

    async def listen(self):
        if not self.websocket:
            logger.error("WebSocket is not connected.")
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

    async def close(self):
        if self.websocket:
            await self.websocket.close()
            logger.info("WebSocket connection closed.")
