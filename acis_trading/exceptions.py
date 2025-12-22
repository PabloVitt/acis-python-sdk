"""
ACIS Trading SDK Exceptions
"""


class ACISError(Exception):
    """Base exception for ACIS SDK errors."""

    def __init__(self, message: str, status_code: int = None, response: dict = None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)


class AuthenticationError(ACISError):
    """Raised when API key is invalid or missing."""

    pass


class RateLimitError(ACISError):
    """Raised when API rate limit is exceeded."""

    def __init__(self, message: str, reset_at: str = None, **kwargs):
        self.reset_at = reset_at
        super().__init__(message, **kwargs)


class ValidationError(ACISError):
    """Raised when request parameters are invalid."""

    pass


class APIError(ACISError):
    """Raised when API returns an error response."""

    pass
