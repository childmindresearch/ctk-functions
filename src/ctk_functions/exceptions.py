"""Custom exceptions for the CTK functions package."""

from ctk_functions import config

logger = config.get_logger()


class LoggingError(Exception):
    """Exception that logs the error message."""

    def __init__(self, message: str) -> None:
        """Logs the exception message to the logger.

        Args:
            message: The exception message.
        """
        logger.error(message)
        super().__init__(message)


class TransformerError(LoggingError):
    """Exception for transformer errors."""


class RedcapError(LoggingError):
    """Exception for REDCap errors."""
