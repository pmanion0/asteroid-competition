"""Baseline heuristic bidder — reasonable but simple.

Uses a weighted combination of mineral signatures and prices with
conservative discounting. Should perform respectably but not dominate.
"""

STRATEGY_NAME = "Steady Eddie"


def price_asteroid(features: dict, capital: float, round_info: dict) -> float:
    """Conservative heuristic strategy."""
    # Skip if low confidence — data is unreliable
    confidence = features.get("survey_confidence", 0.5)
    if confidence < 0.35:
        return 0.0

    # Skip if low structural integrity — catastrophe risk
    integrity = features.get("structural_integrity", 0.8)
    if integrity < 0.3:
        return 0.0

    # Spectral class bonus (handle string categorical)
    spectral = features.get("spectral_class", "S-type")
    spectral_mult = {"C-type": 0.8, "S-type": 1.0, "M-type": 1.2, "X-type": 1.0}.get(
        str(spectral), 1.0
    )

    # Estimate mineral value (diminishing returns like the real model)
    mineral_value = 0.0
    mineral_pairs = [
        ("mineral_signature_iron", "mineral_price_iron"),
        ("mineral_signature_nickel", "mineral_price_nickel"),
        ("mineral_signature_cobalt", "mineral_price_cobalt"),
        ("mineral_signature_platinum", "mineral_price_platinum"),
        ("mineral_signature_rare_earth", "mineral_price_rare_earth"),
    ]
    for sig_key, price_key in mineral_pairs:
        sig = features.get(sig_key, 0.0)
        price = features.get(price_key, 0.0)
        mineral_value += (sig ** 0.7) * price * 0.3

    mineral_value *= spectral_mult

    # Water bonus — only near routes
    water = features.get("water_ice_fraction", 0.0)
    water_price = features.get("mineral_price_water", 100.0)
    delta_v = features.get("delta_v", 10.0)
    if delta_v < 5.0:
        mineral_value += water * water_price * 1.5

    # Mass scaling (sublinear)
    mass = features.get("mass", 100.0)
    mass_factor = mass ** 0.35 / 8.0

    # Accessibility discount (rough sigmoid approximation)
    accessibility = features.get("accessibility_score", 0.5)
    access_mult = max(0.1, min(1.0, accessibility * 1.5 - 0.2))

    # Extraction difficulty penalty
    difficulty = features.get("extraction_difficulty", 0.5)
    diff_mult = 1.0 - 0.3 * difficulty

    estimated_value = mineral_value * mass_factor * access_mult * diff_mult

    # Discount for winner's curse — bid well below estimated value
    bid = estimated_value * 0.55

    # Liquidity management: keep enough liquid capital as a buffer
    # Account for pending extractions tying up cash flow
    pending = round_info.get("pending_revenue", 0.0)
    num_pending = round_info.get("num_pending_extractions", 0)
    rounds_left = round_info.get("total_rounds", 50) - round_info.get("round_number", 1)

    # Be more conservative when lots of capital is locked up
    if num_pending > 3:
        bid *= 0.8
    # Be more aggressive near end when pending revenue will settle
    if rounds_left < 5 and pending > capital * 0.5:
        bid *= 1.2

    # Don't bid more than 10% of capital
    max_bid = capital * 0.10
    bid = min(bid, max_bid)

    # Skip if too small to be worth the catastrophe risk
    if bid < 20:
        return 0.0

    return bid
