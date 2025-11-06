class TradingAgentError(Exception):
    """Base exception for the trading agent application."""
    pass


class BrokerConnectionError(TradingAgentError):
    """Raised when unable to connect to the broker API."""
    pass


class InsufficientFundsError(TradingAgentError):
    """Raised when there are insufficient funds for a trade."""
    pass


class InvalidSignalError(TradingAgentError):
    """Raised when a signal is invalid or malformed."""
    pass


class RateLimitExceededError(TradingAgentError):
    """Raised when API rate limits are exceeded."""
    pass


class AuthenticationError(TradingAgentError):
    """Raised when authentication with broker fails."""
    pass


class DataFetchError(TradingAgentError):
    """Raised when unable to fetch data from external sources."""
    pass


class ModelLoadError(TradingAgentError):
    """Raised when unable to load a trained model."""
    pass


# News Handler Exceptions
class NewsFetchError(TradingAgentError):
    """Raised when unable to fetch news from RSS feeds."""
    pass


class FeedManagerError(TradingAgentError):
    """Raised when feed manager encounters an error."""
    pass


# Vision Module Exceptions
class VisionProcessingError(TradingAgentError):
    """Raised when vision processing fails."""
    pass


class OCRError(TradingAgentError):
    """Raised when OCR extraction fails."""
    pass


class CaptureError(TradingAgentError):
    """Raised when screen capture fails."""
    pass


# Generative AI Exceptions
class AIResponseError(TradingAgentError):
    """Raised when AI response is invalid or fails."""
    pass


class PromptBuildError(TradingAgentError):
    """Raised when prompt building fails."""
    pass


# Execution Handler Exceptions
class OrderExecutionError(TradingAgentError):
    """Raised when order execution fails."""
    pass


class ComplianceError(TradingAgentError):
    """Raised when compliance checks fail."""
    pass


# Strategy Handler Exceptions
class StrategyFusionError(TradingAgentError):
    """Raised when strategy fusion fails."""
    pass


class SignalGenerationError(TradingAgentError):
    """Raised when signal generation fails."""
    pass


# Portfolio Manager Exceptions
class PortfolioError(TradingAgentError):
    """Raised when portfolio operations fail."""
    pass


class RiskManagementError(TradingAgentError):
    """Raised when risk management checks fail."""
    pass


# UI Exceptions
class UIError(TradingAgentError):
    """Raised when UI operations fail."""
    pass


# Database Exceptions
class DatabaseConnectionError(TradingAgentError):
    """Raised when database connection fails."""
    pass


# Backtester/ML Exceptions
class BacktestError(TradingAgentError):
    """Raised when backtesting fails."""
    pass


class TrainingError(TradingAgentError):
    """Raised when model training fails."""
    pass
