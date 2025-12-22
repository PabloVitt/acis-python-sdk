"""
ACIS Trading SDK - Quick Start Example

This example shows basic usage of the ACIS Trading API.
"""

from acis_trading import ACISClient

# Replace with your actual API key
API_KEY = "acis_live_your_key_here"


def main():
    # Initialize the client
    client = ACISClient(api_key=API_KEY)

    # Check API health
    health = client.health_check()
    print(f"API Status: {health['status']}")
    print(f"API Version: {health['version']}")
    print()

    # Generate a value portfolio
    print("Generating Value Portfolio...")
    portfolio = client.generate_portfolio(
        strategy="value",
        max_positions=20,
        risk_tolerance="moderate"
    )

    print(f"\nGenerated {len(portfolio['positions'])} positions:\n")
    print(f"{'Ticker':<8} {'Weight':>8} {'Sector':<20} {'ML Score':>10}")
    print("-" * 50)

    for pos in portfolio["positions"][:10]:  # Show top 10
        print(
            f"{pos['ticker']:<8} "
            f"{pos['weight']:>7.1%} "
            f"{pos.get('sector', 'N/A'):<20} "
            f"{pos.get('ml_score', 0):>10.3f}"
        )

    # Check usage
    print("\n" + "=" * 50)
    usage = client.get_usage()
    print(f"API Usage: {usage['current_usage']}/{usage['rate_limit']} requests today")
    print(f"Remaining: {usage['remaining']} requests")


if __name__ == "__main__":
    main()
