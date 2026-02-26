# Submission Guide

## Function Signature

Create a single Python file with your strategy:

```python
# my_strategy.py

STRATEGY_NAME = "Your Corp Name"  # Optional — defaults to filename

def price_asteroids(asteroids: list[dict], capital: float, round_info: dict) -> list[float]:
    """
    Called once per round with the full batch of asteroids.

    Args:
        asteroids: list of feature dicts (~95 values each, mostly float,
                   some categorical strings like spectral_class, belt_region, probe_type).
        capital: your current liquid capital (what you can bid with right now)
        round_info: dict with keys:
            - round_number: current round (1-indexed)
            - total_rounds: total rounds in this sector
            - sector_name: name of the current sector
            - economic_cycle_phase: "bust", "normal", or "boom"
            - asteroids_this_round: number of asteroids this round
            - risk_free_rate: per-round interest rate on liquid capital
            - num_active_competitors: number of non-bankrupt competitors
            - pending_revenue: your total expected revenue from in-progress extractions
            - num_pending_extractions: number of your extractions still in progress
            - previous_round: list of per-asteroid results from last round (None for round 1)
                Each entry: {winning_bid, was_sold, was_catastrophe, you_won}
            - market_history: cumulative market stats (None for round 1)
                Keys: rounds_completed, cumulative_asteroids_offered,
                      cumulative_asteroids_sold, cumulative_catastrophes,
                      avg_winning_bid_last5, your_total_wins, your_total_spending

    Returns:
        List of bid amounts (same length as asteroids). Return 0 to pass on an asteroid.
        If total bids exceed capital, all bids are scaled down proportionally.
    """
    return [0.0] * len(asteroids)
```

## Portfolio Bidding

You see all asteroids in a round at once and submit bids on the entire batch simultaneously. This means you can:
- Compare asteroids against each other and bid on the most attractive ones
- Allocate your capital budget across the batch
- Consider how many asteroids you want to win in a single round

If the sum of your non-zero bids exceeds your available capital, all bids are scaled down proportionally to fit within your budget.

## Market Intelligence

Starting from round 2, `round_info` includes:

- **`previous_round`**: A list with one entry per asteroid from last round. Each entry tells you the winning bid (or `None` if unsold), whether a catastrophe occurred, and whether you won it.

- **`market_history`**: Cumulative stats including total asteroids sold, catastrophes observed, recent average winning bids, and your own win/spending totals.

## Test Your Strategy

Use the training data (`data/training.csv`) to develop and validate your model. The training data includes target variables not available during competition: `mineral_value`, `extraction_yield`, `extraction_delay`, and `recovered_value`.

```python
import pandas as pd

df = pd.read_csv("data/training.csv")

# Build a batch of asteroid feature dicts (drop target columns)
target_cols = ["mineral_value", "extraction_yield", "extraction_delay", "recovered_value"]
batch = []
for _, row in df.head(10).iterrows():
    features = row.drop(target_cols).to_dict()
    features.pop("asteroid_id", None)
    batch.append(features)

# Simulate a round
bids = price_asteroids(batch, capital=10000.0, round_info={
    "round_number": 1,
    "total_rounds": 50,
    "sector_name": "Outer Rim",
    "economic_cycle_phase": "bust",
    "asteroids_this_round": 10,
    "risk_free_rate": 0.002,
    "num_active_competitors": 5,
    "pending_revenue": 0.0,
    "num_pending_extractions": 0,
    "previous_round": None,
    "market_history": None,
})

for i, bid in enumerate(bids):
    recovered = df.iloc[i]["recovered_value"]
    print(f"Asteroid {i}: bid={bid:.2f}, recovered_value={recovered:.2f}")
```

## Rules

1. **One file per team.** Your entire strategy must be in a single `.py` file.
2. **No network access.** Strategies run in a sandbox. No HTTP calls, no sockets.
3. **2-second timeout.** Your function must return within 2 seconds per round (all asteroids in the batch).
4. **No filesystem access.** Don't read/write files during competition.
5. **Standard library + numpy/pandas allowed.** Other imports may not be available in the competition environment.

## What You Have

- **Training data**: `data/training.csv` with ~95 features + target values for 10,000 asteroids
- **Feature reference**: `DATA_DICTIONARY.md` with descriptions of every feature
- **Example strategy**: `strategies/example_strategy.py` — a simple heuristic bidder

## What You Don't Have

- The mineral value, extraction yield, or extraction delay during competition (you must estimate these from the ~95 measurement features)
- Other teams' strategies
- Advance knowledge of which specific asteroids will appear in competition
