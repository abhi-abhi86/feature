from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class MarketEvent:
    ticker: str
    price: float
    volume: int
    timestamp: float
    additional_data: Optional[Dict[str, Any]] = None


@dataclass
class NewsEvent:
    headline: str
    source: str
    timestamp: float
    sentiment_score: float
    url: Optional[str] = None


@dataclass
class VisionEvent:
    ticker: str
    pattern: str
    confidence: float
    timestamp: float
    bounding_box: Optional[Dict[str, Any]] = None


@dataclass
class SignalEvent:
    ticker: str
    action: str  # 'BUY' or 'SELL'
    price: float
    confidence: float
    explanation: str
    timestamp: float


@dataclass
class OrderRequestEvent:
    ticker: str
    action: str
    quantity: int
    price: float
    timestamp: float


@dataclass
class FillEvent:
    order_id: str
    ticker: str
    action: str
    quantity: int
    price: float
    timestamp: float


@dataclass
class PnLUpdateEvent:
    ticker: str
    pnl: float
    timestamp: float


@dataclass
class ChatRequestEvent:
    message: str
    timestamp: float


@dataclass
class AlertEvent:
    message: str
    level: str  # 'INFO', 'WARNING', 'ERROR'
    timestamp: float
