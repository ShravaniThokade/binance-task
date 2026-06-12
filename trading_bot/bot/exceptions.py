class TradingBotError(Exception):
    """Base exception for trading bot errors."""


class ValidationError(TradingBotError):
    """Raised when user input fails validation."""


class APIError(TradingBotError):
    """Raised when the Binance API returns an error."""

    def __init__(self, message: str, code: int | None = None):
        super().__init__(message)
        self.code = code


class NetworkError(TradingBotError):
    """Raised when a network or connectivity failure occurs."""
