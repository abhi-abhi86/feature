import logging
from ..core.event_bus import event_bus
from ..core.event_types import MarketEvent, PnLUpdateEvent
from .portfolio import Portfolio
from datetime import datetime

logger = logging.getLogger(__name__)

class PnLTracker:
    def __init__(self, portfolio: Portfolio):
        self.portfolio = portfolio
        self.last_known_prices = {}
        self.realized_pnl = 0.0

    async def on_market_data(self, event: MarketEvent):
        """
        Updates last known prices and calculates unrealized P&L.
        """
        self.last_known_prices[event.ticker] = event.price
        await self._calculate_unrealized_pnl()

    async def _calculate_unrealized_pnl(self):
        unrealized_pnl = 0.0
        portfolio_value = self.portfolio.get_cash()
        
        for ticker, quantity in self.portfolio.get_positions().items():
            current_price = self.last_known_prices.get(ticker)
            if current_price:
                # This is a simplification. A real P&L calculation needs
                # the average cost of the position.
                # For now, we just calculate the market value of holdings.
                market_value = current_price * quantity
                portfolio_value += market_value
                # A proper unrealized P&L would be:
                # (current_price - average_buy_price) * quantity
        
        # For the MVP, we'll just emit the total portfolio value.
        pnl_event = PnLUpdateEvent(
            timestamp=datetime.now(),
            pnl=0, # Placeholder for real P&L
            portfolio_value=portfolio_value
        )
        await event_bus.put(pnl_event)
