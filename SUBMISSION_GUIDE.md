# Submission Guide

## Create Your Strategy

Create a single Python file with your strategy:

```python
# my_strategy.py

STRATEGY_NAME = "Your Corp Name"  # Optional — defaults to filename

def price_asteroid(features: dict, capital: float, round_info: dict) -> float:
    """
    Args:
        features: dict of ~95 values describing the asteroid (mostly float,
                  some categorical strings like spectral_class, belt_region, probe_type)
        capital: your current liquid capital (what you can bid with right now)
        round_info: dict with keys:
            - round_number: current round (1-indexed)
            - total_rounds: total rounds in this sector
            - sector_name: name of the current sector
            - economic_cycle_phase: "bust", "normal", or "boom"
            - asteroids_this_round: number of asteroids this round
            - risk_free_rate: per-round interest rate on liquid capital
            - extraction_delay: rounds until extraction revenue arrives
            - pending_revenue: your total expected revenue from in-progress extractions
            - num_pending_extractions: number of your extractions still in progress

    Returns:
        Your bid amount as a float. Return 0 to pass on this asteroid.
    """
    return 0.0
```

## Test Your Strategy

Use the training data (`data/training.csv`) to develop and validate your model. The training data includes `true_value` for each asteroid — this column will not be available during competition.

You can test your `price_asteroid` function by calling it with rows from the training data:

```python
import pandas as pd

df = pd.read_csv("data/training.csv")

# Convert a row to the features dict your function will receive
row = df.iloc[0]
features = row.drop("true_value").to_dict()
features.pop("asteroid_id", None)

# Simulate a call
bid = price_asteroid(features, capital=10000.0, round_info={
    "round_number": 1,
    "total_rounds": 50,
    "sector_name": "Outer Rim",
    "economic_cycle_phase": "bust",
    "asteroids_this_round": 10,
    "risk_free_rate": 0.002,
    "extraction_delay": 3,
    "pending_revenue": 0.0,
    "num_pending_extractions": 0,
})
print(f"Bid: {bid:.2f}, True value: {row['true_value']:.2f}")
```

## Submit

Submit your strategy file to the organizer. Details will be provided separately.

## Rules

1. **One file per team.** Your entire strategy must be in a single `.py` file.
2. **No network access.** Strategies run in a sandbox. No HTTP calls, no sockets.
3. **2-second timeout.** Your function must return within 2 seconds per asteroid.
4. **No filesystem access.** Don't read/write files during competition.
5. **Standard library + numpy/pandas allowed.** Other imports may not be available in the competition environment.

## What You Have

- **Training data**: `data/training.csv` with ~95 features + true values for 10,000 asteroids
- **Feature reference**: `DATA_DICTIONARY.md` with descriptions of every feature
- **Example strategy**: `strategies/example_strategy.py` — a simple heuristic bidder

## What You Don't Have

- The true value function (that's what you're trying to estimate)
- Other teams' strategies
- Advance knowledge of which specific asteroids will appear in competition
