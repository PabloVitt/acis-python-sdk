"""
ACIS Trading API Client

A Python client for the ACIS Trading API - AI-powered stock portfolio
generation and rebalancing.
"""

import requests
from typing import List, Dict, Optional, Literal
from dataclasses import dataclass

from .exceptions import (
    ACISError,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError,
)


@dataclass
class Position:
    """Represents a portfolio position."""

    ticker: str
    weight: float
    shares: Optional[float] = None
    price: Optional[float] = None
    sector: Optional[str] = None
    ml_score: Optional[float] = None

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "weight": self.weight,
            "shares": self.shares,
            "price": self.price,
            "sector": self.sector,
            "ml_score": self.ml_score,
        }


@dataclass
class RebalanceSuggestion:
    """Represents a rebalancing suggestion."""

    ticker: str
    action: str  # 'buy', 'sell', 'hold'
    current_weight: float
    target_weight: float
    weight_change: float
    shares_to_trade: Optional[int] = None
    reason: Optional[str] = None


class ACISClient:
    """
    ACIS Trading API Client.

    Provides access to AI-powered portfolio generation and rebalancing.

    Args:
        api_key: Your ACIS API key (get one at https://acis-trading.com/api-keys)
        base_url: API base URL (defaults to production)
        timeout: Request timeout in seconds (default: 30)

    Example:
        >>> client = ACISClient(api_key="acis_live_xxx")
        >>> portfolio = client.generate_portfolio(strategy="value")
        >>> for position in portfolio["positions"]:
        ...     print(f"{position['ticker']}: {position['weight']:.1%}")
    """

    DEFAULT_BASE_URL = "https://acis-trading.com/api/v1"

    def __init__(
        self,
        api_key: str,
        base_url: str = None,
        timeout: int = 30,
    ):
        if not api_key:
            raise AuthenticationError("API key is required")

        self.api_key = api_key
        self.base_url = (base_url or self.DEFAULT_BASE_URL).rstrip("/")
        self.timeout = timeout
        self._session = requests.Session()
        self._session.headers.update(
            {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
                "User-Agent": "acis-python-sdk/1.0.0",
            }
        )

    def _request(
        self,
        method: str,
        endpoint: str,
        params: dict = None,
        json: dict = None,
    ) -> dict:
        """Make an API request."""
        url = f"{self.base_url}{endpoint}"

        try:
            response = self._session.request(
                method=method,
                url=url,
                params=params,
                json=json,
                timeout=self.timeout,
            )
        except requests.exceptions.Timeout:
            raise APIError("Request timed out", status_code=408)
        except requests.exceptions.ConnectionError:
            raise APIError("Connection failed", status_code=503)

        return self._handle_response(response)

    def _handle_response(self, response: requests.Response) -> dict:
        """Handle API response and raise appropriate exceptions."""
        try:
            data = response.json()
        except ValueError:
            data = {"detail": response.text}

        if response.status_code == 200:
            return data

        if response.status_code == 401:
            raise AuthenticationError(
                data.get("detail", "Invalid API key"),
                status_code=401,
                response=data,
            )

        if response.status_code == 429:
            raise RateLimitError(
                data.get("detail", "Rate limit exceeded"),
                status_code=429,
                reset_at=data.get("reset_at"),
                response=data,
            )

        if response.status_code == 422:
            raise ValidationError(
                data.get("detail", "Validation error"),
                status_code=422,
                response=data,
            )

        raise APIError(
            data.get("detail", f"API error: {response.status_code}"),
            status_code=response.status_code,
            response=data,
        )

    # =========================================================================
    # Portfolio Generation
    # =========================================================================

    def generate_portfolio(
        self,
        strategy: Literal[
            "value",
            "growth",
            "dividend",
            "adaptive",
            "value_largecap",
            "value_smallcap",
            "growth_largecap",
            "growth_smallcap",
        ],
        max_positions: int = 20,
        risk_tolerance: Literal["conservative", "moderate", "aggressive"] = "moderate",
        investment_amount: float = None,
    ) -> dict:
        """
        Generate an AI-optimized portfolio.

        Uses LightGBM machine learning models trained on fundamental and
        technical factors to select optimal securities.

        Args:
            strategy: Investment strategy to use
                - "value": Undervalued stocks with strong fundamentals
                - "growth": High-growth companies
                - "dividend": Income-focused dividend stocks
                - "adaptive": Dynamic market-regime aware
                - "value_largecap": Large-cap value stocks
                - "value_smallcap": Small/mid-cap value stocks
                - "growth_largecap": Large-cap growth stocks
                - "growth_smallcap": Small/mid-cap growth stocks
            max_positions: Maximum number of positions (5-50)
            risk_tolerance: Risk profile (conservative, moderate, aggressive)
            investment_amount: Optional investment amount for share calculation

        Returns:
            dict: Portfolio with positions, weights, and metadata

        Example:
            >>> portfolio = client.generate_portfolio(
            ...     strategy="value",
            ...     max_positions=25,
            ...     risk_tolerance="moderate"
            ... )
            >>> print(f"Generated {len(portfolio['positions'])} positions")
        """
        payload = {
            "strategy": strategy,
            "max_positions": max_positions,
            "risk_tolerance": risk_tolerance,
        }

        if investment_amount:
            payload["investment_amount"] = investment_amount

        return self._request("POST", "/portfolios/generate", json=payload)

    def get_rebalance_suggestions(
        self,
        current_positions: List[Dict[str, float]],
        strategy: Literal[
            "value",
            "growth",
            "dividend",
            "adaptive",
            "value_largecap",
            "value_smallcap",
            "growth_largecap",
            "growth_smallcap",
        ],
        market_cap: Literal["large", "small"] = "large",
        rebalance_threshold: float = 0.02,
    ) -> dict:
        """
        Get AI-powered rebalancing suggestions for an existing portfolio.

        Compares current positions to optimal target weights and provides
        specific buy/sell/hold recommendations.

        Args:
            current_positions: List of current positions, each with:
                - ticker (str): Stock symbol
                - weight (float): Current portfolio weight (0-1)
                - shares (int, optional): Number of shares held
            strategy: Target strategy to rebalance toward
            market_cap: Market cap focus ("large" or "small")
            rebalance_threshold: Minimum weight difference to trigger rebalance

        Returns:
            dict: Rebalancing suggestions with actions and reasoning

        Example:
            >>> positions = [
            ...     {"ticker": "AAPL", "weight": 0.15, "shares": 100},
            ...     {"ticker": "MSFT", "weight": 0.12, "shares": 50},
            ...     {"ticker": "GOOGL", "weight": 0.10, "shares": 25},
            ... ]
            >>> suggestions = client.get_rebalance_suggestions(
            ...     current_positions=positions,
            ...     strategy="value",
            ...     rebalance_threshold=0.03
            ... )
            >>> for s in suggestions["suggestions"]:
            ...     print(f"{s['action'].upper()} {s['ticker']}")
        """
        payload = {
            "current_positions": current_positions,
            "strategy": strategy,
            "market_cap": market_cap,
            "rebalance_threshold": rebalance_threshold,
        }

        return self._request("POST", "/portfolios/rebalance", json=payload)

    # =========================================================================
    # Account & Usage
    # =========================================================================

    def get_usage(self) -> dict:
        """
        Get current API usage statistics.

        Returns:
            dict: Usage stats including:
                - current_usage: Requests made today
                - rate_limit: Daily request limit for your tier
                - remaining: Requests remaining today
                - reset_at: When the limit resets

        Example:
            >>> usage = client.get_usage()
            >>> print(f"Used {usage['current_usage']}/{usage['rate_limit']} requests")
        """
        return self._request("GET", "/usage")

    def health_check(self) -> dict:
        """
        Check API health and availability.

        Returns:
            dict: API status and version information

        Example:
            >>> health = client.health_check()
            >>> print(f"API Status: {health['status']}")
        """
        return self._request("GET", "/health")

    def get_risk_levels(self) -> list:
        """
        Get available risk level configurations.

        Returns:
            list: Available risk profiles with parameters

        Example:
            >>> levels = client.get_risk_levels()
            >>> for level in levels:
            ...     print(f"{level['name']}: {level['description']}")
        """
        return self._request("GET", "/risk-levels")

    # =========================================================================
    # User Portfolio Management
    # =========================================================================

    def get_my_portfolios(self) -> list:
        """
        Get all portfolios associated with your account.

        Returns:
            list: Your subscribed portfolios with current positions

        Example:
            >>> portfolios = client.get_my_portfolios()
            >>> for p in portfolios:
            ...     print(f"{p['strategy']}: {p['position_count']} positions")
        """
        return self._request("GET", "/user/portfolios")

    def get_portfolio(self, strategy: str) -> dict:
        """
        Get detailed portfolio for a specific strategy.

        Args:
            strategy: Strategy identifier (e.g., "value_strategy")

        Returns:
            dict: Full portfolio details including positions and performance
        """
        return self._request("GET", f"/user/portfolios/{strategy}")

    def get_portfolio_history(
        self,
        strategy: str,
        days: int = 30,
    ) -> list:
        """
        Get historical performance data for a portfolio.

        Args:
            strategy: Strategy identifier
            days: Number of days of history (1-365)

        Returns:
            list: Daily portfolio values and returns
        """
        return self._request(
            "GET",
            f"/user/portfolios/{strategy}/history",
            params={"days": days},
        )

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def get_value_portfolio(self, max_positions: int = 20) -> dict:
        """Generate a value-focused portfolio."""
        return self.generate_portfolio(strategy="value", max_positions=max_positions)

    def get_growth_portfolio(self, max_positions: int = 20) -> dict:
        """Generate a growth-focused portfolio."""
        return self.generate_portfolio(strategy="growth", max_positions=max_positions)

    def get_dividend_portfolio(self, max_positions: int = 20) -> dict:
        """Generate a dividend-focused portfolio."""
        return self.generate_portfolio(strategy="dividend", max_positions=max_positions)

    def get_adaptive_portfolio(self, max_positions: int = 20) -> dict:
        """Generate a market-adaptive portfolio."""
        return self.generate_portfolio(strategy="adaptive", max_positions=max_positions)
