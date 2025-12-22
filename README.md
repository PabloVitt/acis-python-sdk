# ACIS Trading Python SDK

[![PyPI version](https://badge.fury.io/py/acis-trading.svg)](https://badge.fury.io/py/acis-trading)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the [ACIS Trading API](https://acis-trading.com) - AI-powered stock portfolio generation.

## Features

- **AI Portfolio Generation** - Generate optimized portfolios using LightGBM machine learning models
- **8 Investment Strategies** - Value, Growth, Dividend, Adaptive, plus Large/Small Cap variants
- **Walk-Forward Validated** - Models validated with proper time-series methodology (no lookahead bias)

## Installation

```bash
pip install acis-trading
```

## Quick Start

```python
from acis_trading import ACISClient

# Initialize client with your API key
client = ACISClient(api_key="acis_live_your_key_here")

# Generate a value-focused portfolio
portfolio = client.generate_portfolio(
    strategy="value",
    max_positions=20,
    risk_tolerance="moderate"
)

# Print the positions
for position in portfolio["positions"]:
    print(f"{position['ticker']}: {position['weight']:.1%} (ML Score: {position['ml_score']:.2f})")
```

## Available Strategies

All 8 strategies are available with API Pro ($149/mo):

| Strategy | Description |
|----------|-------------|
| `dividend` | Income-focused dividend stocks |
| `adaptive` | Dynamic market-regime aware |
| `value` | Undervalued stocks with strong fundamentals |
| `growth` | High-growth companies |
| `value_largecap` | Large-cap value stocks |
| `growth_largecap` | Large-cap growth stocks |
| `value_smallcap` | Small/mid-cap value stocks |
| `growth_smallcap` | Small/mid-cap growth stocks |

## API Reference

### Generate Portfolio

```python
portfolio = client.generate_portfolio(
    strategy="value",           # Required: strategy name
    max_positions=20,           # Optional: 5-50 positions (default: 20)
    risk_tolerance="moderate",  # Optional: conservative, moderate, aggressive
    investment_amount=100000    # Optional: for share calculation
)
```

**Response:**
```python
{
    "positions": [
        {
            "ticker": "AAPL",
            "weight": 0.05,
            "shares": 33,
            "price": 150.25,
            "sector": "Technology",
            "ml_score": 0.82
        },
        # ... more positions
    ],
    "metadata": {
        "strategy": "value",
        "generated_at": "2025-01-15T10:30:00Z",
        "model_version": "v2.1"
    }
}
```

### Check Usage

```python
usage = client.get_usage()

print(f"Requests today: {usage['current_usage']}/{usage['rate_limit']}")
print(f"Remaining: {usage['remaining']}")
print(f"Resets at: {usage['reset_at']}")
```

### Convenience Methods

```python
# Quick portfolio generation
value_portfolio = client.get_value_portfolio()
growth_portfolio = client.get_growth_portfolio()
dividend_portfolio = client.get_dividend_portfolio()
adaptive_portfolio = client.get_adaptive_portfolio()
```

## Error Handling

```python
from acis_trading import (
    ACISClient,
    AuthenticationError,
    RateLimitError,
    ValidationError,
    APIError
)

client = ACISClient(api_key="your_key")

try:
    portfolio = client.generate_portfolio(strategy="value")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError as e:
    print(f"Rate limit exceeded. Resets at: {e.reset_at}")
except ValidationError as e:
    print(f"Invalid parameters: {e.message}")
except APIError as e:
    print(f"API error ({e.status_code}): {e.message}")
```

## Examples

### Build a Multi-Strategy Portfolio

```python
from acis_trading import ACISClient

client = ACISClient(api_key="your_key")

# Generate portfolios for each strategy
strategies = ["value", "growth", "dividend"]
all_positions = {}

for strategy in strategies:
    portfolio = client.generate_portfolio(
        strategy=strategy,
        max_positions=10
    )

    for pos in portfolio["positions"]:
        ticker = pos["ticker"]
        if ticker not in all_positions:
            all_positions[ticker] = {"strategies": [], "total_weight": 0}
        all_positions[ticker]["strategies"].append(strategy)
        all_positions[ticker]["total_weight"] += pos["weight"] / len(strategies)

# Find stocks appearing in multiple strategies
consensus_picks = {
    ticker: data for ticker, data in all_positions.items()
    if len(data["strategies"]) >= 2
}

print("Consensus picks (in 2+ strategies):")
for ticker, data in sorted(consensus_picks.items(), key=lambda x: -x[1]["total_weight"]):
    print(f"  {ticker}: {data['strategies']} - {data['total_weight']:.1%}")
```

### Export to CSV

```python
import csv
from acis_trading import ACISClient

client = ACISClient(api_key="your_key")
portfolio = client.generate_portfolio(strategy="value", max_positions=25)

with open("portfolio.csv", "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["ticker", "weight", "shares", "sector", "ml_score"])
    writer.writeheader()
    writer.writerows(portfolio["positions"])

print("Portfolio exported to portfolio.csv")
```

## Rate Limits

**API Pro Plan:** $149/month
- 50,000 API calls/month
- 10,000 daily rate limit
- All 8 AI strategies
- 30-day free trial

## Getting an API Key

1. Sign up at [acis-trading.com/signup](https://acis-trading.com/signup?plan=api_pro)
2. Go to [API Keys](https://acis-trading.com/api-keys) in your dashboard
3. Create a new API key

SDK access requires the API Pro plan. Start with a 30-day free trial.

## Support

- **Documentation:** [acis-trading.com/api-docs](https://acis-trading.com/api-docs)
- **Issues:** [GitHub Issues](https://github.com/acis-trading/acis-python-sdk/issues)
- **Email:** support@acis-trading.com

## License

MIT License - see [LICENSE](LICENSE) for details.

---

Built with LightGBM and walk-forward validation. No lookahead bias. Real ML, not marketing.
