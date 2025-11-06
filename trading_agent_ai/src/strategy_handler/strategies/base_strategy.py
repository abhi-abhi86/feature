from abc import ABC, abstractmethod
from typing import Optional

from ...core.event_types import MarketEvent, NewsEvent, VisionEvent

class BaseStrategy(ABC):
    @abstractmethod
    def calculate_signal(
        self, 
        market_data: MarketEvent, 
        news_data: Optional[NewsEvent], 
        vision_data: Optional[VisionEvent]
    ) -> str:
        """
        Calculates a trading signal based on the input data.
        Returns 'BUY', 'SELL', or 'HOLD'.
        """
        pass
