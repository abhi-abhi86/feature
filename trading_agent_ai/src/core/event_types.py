from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict

@dataclass
class MarketEvent:
    timestamp: datetime
    ticker: str
    price: float
    volume: int

@dataclass
class NewsEvent:
    timestamp: datetime
    headline: str
    source: str
    sentiment: float

@dataclass
class VisionEvent:
    timestamp: datetime
    ticker: str
    pattern: str
    confidence: float

@dataclass
class SignalEvent:
    timestamp: datetime
    ticker: str
    signal: str  # 'BUY', 'SELL', 'HOLD'
    confidence: float
    reason: str

@dataclass
class OrderRequestEvent:
    timestamp: datetime
    ticker: str
    action: str  # 'BUY', 'SELL'
    quantity: float
    order_type: str = 'MARKET'

@dataclass
class FillEvent:
    timestamp: datetime
    ticker: str
    action: str
    quantity: float
    price: float
    order_id: str

@dataclass
class PnLUpdateEvent:
    timestamp: datetime
    pnl: float
    portfolio_value: float

@dataclass
class ChatRequestEvent:
    timestamp: datetime
    text: str

@dataclass
class AppLogEvent:
    timestamp: datetime
    level: str
    message: str
