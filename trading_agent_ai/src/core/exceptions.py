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
