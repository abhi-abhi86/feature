import logging
from ..core.event_bus import event_bus
from ..core.event_types import OrderRequestEvent
from ..data_handler.api_client import APIClient
from .order_manager import OrderManager
from .sebi_compliance import SEBICompliance

logger = logging.getLogger(__name__)

class BrokerExecutor:
    def __init__(self, api_client: APIClient):
        self.api_client = api_client
        self.order_manager = OrderManager(api_client)
        self.compliance = SEBICompliance()

    async def on_order_request(self, event: OrderRequestEvent):
        """
        Handles an order request, checks compliance, and places the order.
        """
        if self.compliance.check_rate_limit():
            try:
                order_details = {
                    "ticker": event.ticker,
                    "action": event.action,
                    "quantity": event.quantity,
                    "order_type": event.order_type
                    # Add other broker-specific parameters
                }
                
                # In a real scenario, you would get a fresh auth token here
                # self.compliance.get_auth_token()

                response = self.api_client.place_order(order_details)
                
                if response and response.get('order_id'):
                    order_id = response['order_id']
                    logger.info(f"Order placed successfully. Order ID: {order_id}")
                    await self.order_manager.track_order(order_id)
                else:
                    logger.error(f"Failed to place order. Response: {response}")

            except Exception as e:
                logger.error(f"An error occurred while placing order: {e}")
        else:
            logger.warning("Order placement skipped due to rate limiting.")
