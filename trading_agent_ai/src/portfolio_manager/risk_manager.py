import logging
from ..core.event_bus import event_bus
from ..core.event_types import SignalEvent, OrderRequestEvent
from .portfolio import Portfolio

logger = logging.getLogger(__name__)

class RiskManager:
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio
        self.max_order_size_pct = 0.1  # Max 10% of portfolio in a single trade
        self.max_position_size_pct = 0.2 # Max 20% of portfolio in a single asset

    async def on_signal(self, event: SignalEvent):
        """
        Checks a signal against risk rules before creating an order request.
        """
        if self._is_signal_valid(event):
            order_quantity = self._calculate_order_quantity(event)
            if order_quantity > 0:
                order_request = OrderRequestEvent(
                    timestamp=event.timestamp,
                    ticker=event.ticker,
                    action=event.signal,
                    quantity=order_quantity
                )
                await event_bus.put(order_request)
                logger.info(f"Risk Manager approved signal. Generated Order Request: {order_request}")
            else:
                logger.warning(f"Signal for {event.ticker} blocked by Risk Manager (quantity is zero).")

    def _is_signal_valid(self, event: SignalEvent) -> bool:
        # Basic validation
        if event.signal not in ['BUY', 'SELL']:
            logger.warning(f"Invalid signal action: {event.signal}")
            return False
        
        # Add more complex rules here, e.g., check for unusual price, etc.
        return True

    def _calculate_order_quantity(self, event: SignalEvent) -> float:
        # This is a very simple quantity calculation.
        # A real system would be much more sophisticated.
        
        if event.signal == 'BUY':
            cash_to_spend = self.portfolio.get_cash() * self.max_order_size_pct
            # We need price info to calculate quantity. For now, we'll need to get it.
            # This highlights a dependency: RiskManager needs price data.
            # For MVP, let's assume a fixed quantity for now.
            # In a real system, you'd get the latest price from the market_state.
            return 10 # Placeholder
        
        elif event.signal == 'SELL':
            current_position = self.portfolio.get_positions().get(event.ticker, 0)
            return current_position # Sell the whole position
            
        return 0
