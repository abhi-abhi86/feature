import logging
from datetime import datetime
from typing import Optional

from ..core.event_bus import event_bus
from ..core.event_types import SignalEvent, MarketEvent, NewsEvent, VisionEvent

logger = logging.getLogger(__name__)

class SignalGenerator:
    async def generate_signal(
        self,
        ticker: str,
        signal: str,
        market_data: MarketEvent,
        news_data: Optional[NewsEvent],
        vision_data: Optional[VisionEvent]
    ):
        """
        Creates a SignalEvent and puts it on the event bus.
        """
        confidence = self._calculate_confidence(news_data, vision_data)
        reason = self._build_reason_string(signal, market_data, news_data, vision_data)

        signal_event = SignalEvent(
            timestamp=datetime.now(),
            ticker=ticker,
            signal=signal,
            confidence=confidence,
            reason=reason
        )

        await event_bus.put(signal_event)
        logger.info(f"Generated Signal: {signal_event}")

    def _calculate_confidence(
        self,
        news_data: Optional[NewsEvent],
        vision_data: Optional[VisionEvent]
    ) -> float:
        # Simple confidence calculation based on available data sources
        # This can be made more sophisticated
        sources = 0
        if news_data:
            sources += 1
        if vision_data:
            sources += 1
        
        # Placeholder for predictive model
        # sources += 1 

        return sources / 3.0 # Assuming 3 potential sources

    def _build_reason_string(
        self,
        signal: str,
        market_data: MarketEvent,
        news_data: Optional[NewsEvent],
        vision_data: Optional[VisionEvent]
    ) -> str:
        """
        Builds the simple template explanation for the signal.
        """
        pattern_name = vision_data.pattern if vision_data else "N/A"
        sentiment_score = f"{news_data.sentiment:.2f}" if news_data else "N/A"

        return (f"Signal: {signal} {market_data.ticker}, "
                f"Reason: Image model ({pattern_name}), "
                f"News ({sentiment_score})")
