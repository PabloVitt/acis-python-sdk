"""
ACIS Trading Python SDK

AI-powered stock portfolio generation.

Usage:
    from acis_trading import ACISClient

    client = ACISClient(api_key="your-api-key")
    portfolio = client.generate_portfolio(strategy="value", max_positions=20)
"""

from .client import ACISClient
from .exceptions import (
    ACISError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError,
)

__version__ = "1.0.0"
__all__ = [
    "ACISClient",
    "ACISError",
    "AuthenticationError",
    "RateLimitError",
    "ValidationError",
    "APIError",
]
