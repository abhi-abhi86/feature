import asyncio
import logging
from datetime import datetime

from ..core.event_bus import event_bus
from ..core.event_types import FillEvent
from ..data_handler.api_client import APIClient

logger = logging.getLogger(__name__)

class OrderManager:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client

    async def track_order(self, order_id: str):
        """
        Tracks the lifecycle of an order by polling its status.
        """
        logger.info(f"Tracking order {order_id}...")
        asyncio.create_task(self._poll_order_status(order_id))

    async def _poll_order_status(self, order_id: str):
        while True:
            try:
                status_response = self.api_client.get_order_status(order_id)
                
                if status_response and status_response.get('status') == 'FILLED':
                    logger.info(f"Order {order_id} is FILLED.")
                    fill_event = FillEvent(
                        timestamp=datetime.now(),
                        order_id=order_id,
                        ticker=status_response['ticker'],
                        action=status_response['action'],
                        quantity=status_response['quantity'],
                        price=status_response['fill_price']
                    )
                    await event_bus.put(fill_event)
                    break # Stop polling once filled
                elif status_response and status_response.get('status') in ['REJECTED', 'CANCELLED']:
                    logger.warning(f"Order {order_id} was {status_response.get('status')}.")
                    break
                else:
                    logger.debug(f"Order {order_id} status is {status_response.get('status')}.")

            except Exception as e:
                logger.error(f"Error polling order status for {order_id}: {e}")
                break # Stop polling on error

            await asyncio.sleep(5) # Poll every 5 seconds
