import asyncio
import logging
from typing import Any, Dict

from ..core.config_loader import ConfigLoader
from ..core.event_bus import event_bus
from .api_client import APIClient
from .websocket_manager import WebsocketManager

logger = logging.getLogger(__name__)

class BrokerConnector:
    def __init__(self, config: ConfigLoader):
        self.config = config
        self.api_client = APIClient(config)
        self.websocket_manager = WebsocketManager(config)

    async def start(self):
        logger.info("Starting Broker Connector...")
        # Authentication and other setup can be done here
        # For example, getting an access token
        # self.api_client.authenticate()
        
        # Start the websocket connection
        await self.websocket_manager.connect()
        self.listen_task = asyncio.create_task(self.websocket_manager.listen())
        logger.info("Broker Connector started.")

    async def stop(self):
        logger.info("Stopping Broker Connector...")
        await self.websocket_manager.close()
        logger.info("Broker Connector stopped.")

    def get_api_client(self) -> APIClient:
        return self.api_client
