# ASTEROID AUCTION CHALLENGE

<img src="asteroid-auction-challenge.png" alt="Asteroid Auction Challenge" width="760" />


## Year 2247. The Belt is Open.

Six years ago, the Titan Crash wiped out half the Belt's active mining operations overnight. Commodity prices collapsed. Credit markets froze. Dozens of corporations went bankrupt as extraction revenues dried up and debt obligations came due. The survivors were the ones who had kept cash reserves, diversified across geological clusters, and hadn't overcommitted capital to long-duration extraction operations they couldn't afford to wait on.

The Terran Mining Consortium responded by deregulating drilling rights. For the first time in decades, independent mining corporations can bid directly for extraction permits — no more exclusive Consortium contracts. The Belt is open to anyone with capital and the nerve to deploy it.

Your corporation has secured a seat at the auction table. Over the coming weeks, hundreds of asteroids will be offered across three sectors of the Belt, each operating under different economic conditions. You'll bid against rival corporations in sealed-bid auctions, paying upfront for extraction rights and waiting for operations to deliver returns — if they deliver at all.

The Belt's geological diversity is staggering. Carbonaceous rubble piles sit alongside solid metallic bodies. Some asteroids are rich in iron and nickel; others harbor platinum group metals or water ice deposits that supply the Belt's fuel infrastructure. The relationship between what you can measure remotely and what you actually extract is complex — mineral concentrations, physical structure, accessibility, location, and market conditions all interact in ways that simple models tend to miss.

The prospecting industry has grown alongside deregulation. Survey firms range from elite operations deploying drill-core sampling probes to budget outfits running passive spectral scans from orbit. Quality varies. The 2245 Pyrite Rush — where corporations bid aggressively on claims that turned out to be geologically worthless — is a cautionary tale about the cost of trusting bad data. Meanwhile, a wave of commercial data providers now offers automated valuations, analyst reports, sentiment indices, and other products of varying provenance. Some have genuine track records; others launched last year and haven't been tested through a full market cycle.

The Belt is also unforgiving. Void rocks — hollow shells that look promising on remote scans — are an expensive lesson in due diligence. Structural collapses during drilling can destroy an entire operation. Worst of all, toxic outgassing events can contaminate an entire geological cluster. The Sigma-7 disaster of 2244 destroyed three active mining operations in a single cluster when one drill hit a volatile pocket.

Capital management is survival. After the Titan Crash, the Consortium imposed phased extraction timelines — you pay for drilling rights immediately, but revenue from extraction operations takes time to arrive. During that window, your capital is locked. Win too many claims too fast and you'll find yourself cash-poor and unable to act when the real opportunities appear — or unable to absorb the inevitable losses. Liquid capital earns a modest return, so there's always a baseline to beat.

---

## How It Works

### The Auction
Each round, a batch of asteroids is offered for sale via **first-price sealed-bid auction**:
- All bidders submit bids simultaneously (no one sees others' bids)
- Highest bid wins and pays their bid amount
- Profit = recovered value - your bid (recovered value = mineral value x extraction yield)
- Bid 0 (or return 0) to pass on an asteroid

### Your Job
Each round, you see **all asteroids at once** and submit bids on the entire batch. You implement **one function**:

```python
def price_asteroids(asteroids: list[dict], capital: float, round_info: dict) -> list[float]:
    """
    asteroids:   list of feature dicts (~95 values each), one per asteroid offered this round
    capital:     your current liquid capital (what you can bid with right now)
    round_info:  round metadata (see below)
    returns:     list of bids (same length as asteroids). 0 to pass on an asteroid.
    """
```

**Portfolio constraint**: If the sum of your bids exceeds your capital, all bids are scaled down proportionally. You must allocate your budget across the full batch.

The `round_info` dict contains:
| Key | Description |
|-----|-------------|
| `round_number` | Current round (1-indexed) |
| `total_rounds` | Total rounds in this sector |
| `sector_name` | Name of the current sector |
| `economic_cycle_phase` | `"bust"`, `"normal"`, or `"boom"` |
| `asteroids_this_round` | Number of asteroids offered this round |
| `risk_free_rate` | Per-round interest rate on liquid capital |
| `num_active_competitors` | Number of non-bankrupt competitors |
| `pending_revenue` | Total revenue you expect from in-progress extractions |
| `num_pending_extractions` | Number of extractions still in progress |
| `previous_round` | List of per-asteroid results from last round (see below), or `None` for round 1 |
| `market_history` | Cumulative market stats (see below), or `None` for round 1 |

**Previous round results** (`previous_round`): A list with one entry per asteroid from the previous round:
| Key | Description |
|-----|-------------|
| `winning_bid` | The winning bid amount, or `None` if unsold |
| `was_sold` | Whether the asteroid was sold |
| `was_catastrophe` | Whether a catastrophe occurred |
| `you_won` | Whether you won this asteroid |

**Market history** (`market_history`):
| Key | Description |
|-----|-------------|
| `rounds_completed` | Number of rounds completed so far |
| `cumulative_asteroids_offered` | Total asteroids offered across all rounds |
| `cumulative_asteroids_sold` | Total asteroids sold |
| `cumulative_catastrophes` | Total catastrophes observed |
| `avg_winning_bid_last5` | Average winning bid over last 5 rounds |
| `your_total_wins` | Your cumulative wins |
| `your_total_spending` | Your cumulative spending |

### The Features (~95 total)
Each asteroid comes with a rich feature set covering geological properties, orbital mechanics, survey data, market conditions, environmental factors, and third-party estimates. Most features are numeric; a few are categorical strings. See `DATA_DICTIONARY.md` for the full reference.

### Catastrophic Events
A fraction of asteroids will trigger catastrophic events when mined. The rate is feature-driven — asteroids with low structural integrity, low density, high porosity, or high volatile content are significantly more dangerous:
- **Void Rock**: Hollow shell. You lose your bid plus a cleanup penalty.
- **Structural Collapse**: Drilling destabilizes the body. Bid lost plus penalty.
- **Toxic Outgassing**: Releases toxic gases that damage all operations in the same geological cluster — yours and others'.

Winning multiple asteroids in the same cluster increases both the probability of catastrophe and your exposure to cascade events.

### Extraction Operations
- **Extraction yield**: Not all mineral value is recovered during operations. Operational conditions — equipment compatibility, survey data quality, surface environment — all affect recovery rates. Your revenue from an asteroid is `mineral_value × extraction_yield`. The training data includes `extraction_yield` for each asteroid so you can learn what drives it.
- **Extraction delay**: When you win, your bid is paid immediately. Revenue arrives after a variable delay that depends on the asteroid's characteristics (difficulty, location, accessibility, size). The training data includes `extraction_delay` for each asteroid.
- **Interest**: Liquid capital earns a per-round return (given in `round_info`).
- **Bankruptcy**: If your capital hits zero, you're eliminated. No coming back.

### Tournament Structure

The competition runs across three sectors with elimination:

| Sector | Rounds | Asteroids/Round | Capital | Market | Advance |
|--------|--------|-----------------|---------|--------|---------|
| **Outer Rim** | 50 | 10 | $10,000 | Bust | Top 50% |
| **Inner Belt** | 50 | 10 | $8,000 | Normal | Top 40% |
| **Core Belt** | 100 | 10 | $6,000 | Boom | Final rank |

Each sector resets capital. Economic conditions change between sectors.

---

## Getting Started

### What You Have
- `data/training.csv` — 10,000 asteroids with ~95 features and target values
- `DATA_DICTIONARY.md` — description of every feature
- `strategies/example_strategy.py` — a simple baseline bidder to study

### Build Your Model
Load the training data and explore. The training data includes target variables not available during competition: `mineral_value` (what's in the rock), `extraction_yield` (recovery fraction), `extraction_delay` (rounds until revenue), and `recovered_value` (what the winner actually receives: `mineral_value × extraction_yield`). Your goal is to estimate what asteroids are worth and how long extraction will take, then bid profitably.

```python
import pandas as pd

df = pd.read_csv("data/training.csv")
print(df.shape)          # (10000, 97)
print(df.describe())     # summary statistics
```

### Write Your Strategy
Create a Python file with your bidding function:

```python
STRATEGY_NAME = "My Corp"

def price_asteroids(asteroids: list[dict], capital: float, round_info: dict) -> list[float]:
    # See all asteroids at once — allocate your capital across the batch
    bids = []
    for features in asteroids:
        # Your bidding logic here
        bids.append(0.0)  # 0 to pass
    return bids
```

See `SUBMISSION_GUIDE.md` for detailed submission instructions, rules, and constraints.

---

## Dependencies

Players can use any Python packages in their strategy files. We recommend:
- `numpy`, `pandas` for data analysis
- `scikit-learn` for modeling

These are listed in `pyproject.toml`. Install with `uv sync` or `pip install -e .`
