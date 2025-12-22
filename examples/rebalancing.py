"""
ACIS Trading SDK - Rebalancing Example

This example shows how to get AI-powered rebalancing suggestions
for an existing portfolio.
"""

from acis_trading import ACISClient, RateLimitError

API_KEY = "acis_live_your_key_here"


def main():
    client = ACISClient(api_key=API_KEY)

    # Example: Your current portfolio holdings
    # In production, you'd pull this from your brokerage API
    current_holdings = [
        {"ticker": "AAPL", "weight": 0.15, "shares": 100},
        {"ticker": "MSFT", "weight": 0.12, "shares": 50},
        {"ticker": "GOOGL", "weight": 0.10, "shares": 25},
        {"ticker": "AMZN", "weight": 0.08, "shares": 15},
        {"ticker": "NVDA", "weight": 0.20, "shares": 40},  # Overweight!
        {"ticker": "JPM", "weight": 0.05, "shares": 30},
        {"ticker": "JNJ", "weight": 0.05, "shares": 25},
        {"ticker": "V", "weight": 0.05, "shares": 20},
        {"ticker": "PG", "weight": 0.05, "shares": 30},
        {"ticker": "UNH", "weight": 0.05, "shares": 10},
        # Cash: 10%
    ]

    print("Current Portfolio:")
    print("-" * 40)
    for pos in current_holdings:
        print(f"  {pos['ticker']:<6} {pos['weight']:>6.1%}  ({pos['shares']} shares)")

    print("\nGetting AI rebalancing suggestions...")
    print("(Comparing to optimal Value strategy weights)\n")

    try:
        suggestions = client.get_rebalance_suggestions(
            current_positions=current_holdings,
            strategy="value",
            rebalance_threshold=0.02  # 2% threshold
        )

        # Group by action
        buys = [s for s in suggestions["suggestions"] if s["action"] == "buy"]
        sells = [s for s in suggestions["suggestions"] if s["action"] == "sell"]
        holds = [s for s in suggestions["suggestions"] if s["action"] == "hold"]

        if sells:
            print("SELL Recommendations:")
            for s in sells:
                print(f"  {s['ticker']}: {s['current_weight']:.1%} -> {s['target_weight']:.1%}")
                if s.get("reason"):
                    print(f"    Reason: {s['reason']}")

        if buys:
            print("\nBUY Recommendations:")
            for s in buys:
                print(f"  {s['ticker']}: {s['current_weight']:.1%} -> {s['target_weight']:.1%}")
                if s.get("shares_to_trade"):
                    print(f"    Shares to buy: {s['shares_to_trade']}")

        if holds:
            print(f"\nHOLD ({len(holds)} positions): ", end="")
            print(", ".join(s["ticker"] for s in holds))

        print(f"\nSummary: {len(sells)} sells, {len(buys)} buys, {len(holds)} holds")

    except RateLimitError as e:
        print(f"Rate limit exceeded. Try again after {e.reset_at}")


if __name__ == "__main__":
    main()
