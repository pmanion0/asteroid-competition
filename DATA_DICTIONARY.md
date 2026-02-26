# Data Dictionary

Feature reference for the Asteroid Mining Bidding Simulation training dataset. Each row represents one asteroid. The `true_value` column (provided in training data only) represents the realized extraction value in thousands of credits after all operations concluded.

Market conditions and data collection methods may differ between the training dataset and live competition sectors.

---

## Geological / Physical Properties

Measured by remote sensing and, where available, surface probe data.

| Feature | Description |
|---------|-------------|
| `mass` | Estimated mass in kilotonnes. |
| `density` | Bulk density in g/cm3. Ranges from porous rubble piles (~1.5) to solid metal bodies (~8.0). |
| `porosity` | Fraction of volume that is void space. High porosity can indicate rubble pile structure. |
| `spectral_class` | Tholen taxonomy classification (categorical: `C-type`, `S-type`, `M-type`, `X-type`). Each class reflects a different parent body differentiation history: C-types are primitive carbonaceous bodies, S-types are silicate-rich from partially differentiated parents, M-types are metallic fragments of differentiated cores, and X-types have ambiguous spectra. |
| `mineral_signature_iron` | Spectroscopic concentration estimate for iron (Fe), scaled 0-1. |
| `mineral_signature_nickel` | Spectroscopic concentration estimate for nickel (Ni), scaled 0-1. |
| `mineral_signature_cobalt` | Spectroscopic concentration estimate for cobalt (Co), scaled 0-1. |
| `mineral_signature_platinum` | Spectroscopic concentration estimate for platinum group metals (PGM), scaled 0-1. |
| `mineral_signature_rare_earth` | Spectroscopic concentration estimate for rare earth elements (REE), scaled 0-1. |
| `albedo` | Surface reflectivity measured via photometry. Related to surface composition and weathering. |
| `rotation_period` | Sidereal rotation period in hours. Fast rotators may complicate surface operations. |
| `surface_roughness` | Terrain roughness index (0=smooth, 1=extremely rough). Affects landing and drill placement. |
| `magnetic_field_strength` | Measured magnetic field intensity in arbitrary units. Most asteroids have negligible fields. |
| `thermal_inertia` | Thermal inertia in SI units. Indicates surface heat response characteristics. Extreme values in either direction can affect mining equipment performance. |
| `shape_elongation` | Ratio of longest to shortest axis (1.0=spherical, 3.0+=highly elongated). Highly elongated bodies may indicate weak internal structure. |
| `regolith_depth` | Estimated depth of surface regolith layer in meters. Deep regolith can complicate surface anchoring. |
| `water_ice_fraction` | Detected fraction of water ice (0-1). Many asteroids have zero water ice. Water ice preservation depends on heliocentric distance and surface exposure. |
| `volatile_content` | Fraction of volatile compounds detected. Includes ices and trapped gases. |
| `structural_integrity` | Engineering assessment of structural soundness (0=critically fractured, 1=solid monolith). Low-integrity bodies carry elevated operational risk. |
| `estimated_volume` | Derived: mass / density. |
| `surface_gravity` | Derived surface gravitational acceleration. |
| `escape_velocity` | Derived escape velocity from the surface. |
| `composition_heterogeneity` | Compositional variability across the body (0=uniform, 1=highly mixed). |
| `subsurface_anomaly_score` | Radar-derived score indicating subsurface structural anomalies. |
| `crystalline_fraction` | Fraction of mineral content in crystalline vs amorphous form. |

---

## Orbital / Location Properties

Derived from ephemeris data and belt surveys.

| Feature | Description |
|---------|-------------|
| `semi_major_axis` | Orbital semi-major axis in AU. |
| `eccentricity` | Orbital eccentricity. Most belt asteroids have near-circular orbits. |
| `inclination` | Orbital inclination in degrees relative to the ecliptic. |
| `delta_v` | Required velocity change (km/s) to reach the asteroid from the nearest transfer point. Reflects fuel expenditure for transport. |
| `belt_region` | Categorical belt position (`inner`, `main`, `outer`). |
| `cluster_id` | Geological cluster assignment. Asteroids in the same cluster share a common formation history. |
| `orbital_period` | Orbital period in years (derived from semi-major axis). |
| `perihelion_distance` | Closest approach to the Sun in AU. |
| `aphelion_distance` | Farthest distance from the Sun in AU. |
| `transfer_window_frequency` | How often optimal transfer windows occur (higher=more frequent). |
| `nearest_station_distance` | Distance to the nearest logistics station in AU. |
| `piracy_proximity_index` | Proximity to known piracy corridors. Higher values indicate greater security cost. |
| `communication_delay` | One-way light-time communication delay in minutes. |
| `orbital_stability_score` | Long-term orbital stability assessment (0=unstable, 1=highly stable). |
| `conjunction_frequency` | Rate of close approaches with other bodies (scaled). |

---

## Survey / Exploration Data

Compiled from prospecting missions. Survey methodology and timing vary.

| Feature | Description |
|---------|-------------|
| `survey_confidence` | Overall confidence rating of the survey data (0-1). Low values indicate the survey team had limited confidence in the measurements collected. |
| `probe_type` | Survey probe deployed (categorical: `passive`, `active_flyby`, `landing`, `drill_core`). Higher-grade probes generally yield more reliable data. |
| `surveyor_reputation` | Reputation score of the surveying firm (0-1). |
| `num_surveys` | Number of independent survey missions conducted. |
| `conflicting_results` | Binary flag (0 or 1). Set to 1 if independent surveys produced contradictory findings. |
| `extraction_difficulty` | Engineering assessment of extraction difficulty (0=trivial, 1=extremely difficult). |
| `accessibility_score` | How accessible deposits are to current drilling technology (0=inaccessible, 1=fully accessible). |
| `survey_age_years` | Time since the most recent survey in years. |
| `data_completeness` | Fraction of standard survey measurements successfully collected (0-1). Complete data enables better operational planning. |
| `spectral_resolution` | Resolution quality of the spectroscopic instruments used (0-1). |
| `ground_truth_samples` | Number of physical samples returned for laboratory analysis. |
| `estimated_extraction_cost` | Surveyor's estimate of total extraction cost in thousands of credits. |
| `drilling_feasibility` | Engineering assessment of drilling viability (0=infeasible, 1=ideal). |
| `equipment_compatibility` | Compatibility score with standard mining equipment (0-1). Low compatibility can significantly impact operational recovery rates. |
| `estimated_yield_tonnes` | Surveyor's estimate of extractable material in tonnes. |
| `survey_anomaly_flag` | Binary flag. Set to 1 if the survey team flagged unusual readings. |
| `previous_claim_history` | Number of times this asteroid has been previously claimed and abandoned. |
| `legal_encumbrance_score` | Degree of legal complications (0=clear, higher=more encumbered). |
| `environmental_hazard_rating` | Environmental risk assessment (0=benign, 1=severe). |
| `insurance_risk_class` | Insurance underwriter risk classification (integer, 1=lowest risk, 5=highest risk). |
| `extraction_delay` | Estimated extraction timeline in rounds. Varies by asteroid characteristics — difficulty, belt region, accessibility, and mass all affect how long operations take. |
| `extraction_yield` | Estimated operational recovery factor (0-1+). Represents what fraction of the mineral value is expected to be actually recovered during extraction. Depends on operational conditions — equipment fit, survey quality, surface environment, and gravity. Values above 1.0 indicate better-than-expected recovery. |

---

## Market / Economic Conditions

Snapshot of market conditions at the time of auction. Prices reflect current spot rates.

| Feature | Description |
|---------|-------------|
| `mineral_price_iron` | Current spot price for iron per unit. |
| `mineral_price_nickel` | Current spot price for nickel per unit. |
| `mineral_price_cobalt` | Current spot price for cobalt per unit. |
| `mineral_price_platinum` | Current spot price for platinum group metals per unit. |
| `mineral_price_rare_earth` | Current spot price for rare earth elements per unit. |
| `mineral_price_water` | Current spot price for water ice per unit. |
| `fuel_cost_per_unit` | Current fuel cost for transport vessels. |
| `insurance_rate` | Current insurance premium rate for mining operations. |
| `tax_rate` | Applicable extraction tax rate for this claim's jurisdiction. |
| `economic_cycle_indicator` | Macro-economic cycle position. Values below 1.0 indicate contraction; above 1.0 indicates expansion. |
| `market_volatility_index` | Current market volatility measure. Higher values indicate more uncertain price environments. |
| `demand_backlog_months` | Months of unfilled demand orders in the minerals market. |
| `shipping_congestion_factor` | Shipping lane congestion level (0=clear, 1=severely congested). |
| `refinery_capacity_utilization` | Fraction of system-wide refinery capacity in use. |
| `spot_vs_contract_spread` | Spread between spot and long-term contract prices. |
| `credit_availability_index` | Availability of financing (0=tight, 1=abundant). |
| `competitor_activity_level` | Estimated activity level of other mining operations in the region. |
| `regulatory_burden_score` | Regulatory overhead for operations in this jurisdiction. |
| `supply_chain_disruption_risk` | Assessed risk of supply chain disruptions. |
| `technology_readiness_level` | Technology readiness level of available equipment (scale 5-9). |

---

## Sector / Environmental Conditions

Local space environment near the asteroid.

| Feature | Description |
|---------|-------------|
| `radiation_level` | Ambient radiation level in the asteroid's vicinity. Affects crew safety and equipment longevity. |
| `micrometeorite_density` | Local micrometeorite flux density. |
| `solar_flux` | Solar energy flux at the asteroid's location (relative to Earth=1.0). |
| `infrastructure_proximity` | Proximity to existing mining infrastructure and logistics hubs (0=remote, 1=well-connected). |
| `navigation_complexity` | Complexity of navigation in the local orbital environment. |
| `rescue_response_time_hours` | Estimated emergency response time from nearest rescue facility. |
| `local_jurisdiction_stability` | Political stability of the governing jurisdiction (0=unstable, 1=stable). |
| `worker_availability_index` | Availability of qualified mining crews in the region. |
| `power_grid_access` | Access to orbital power grid infrastructure. |
| `debris_field_density` | Density of debris in the local orbital environment. |

---

## Third-Party Estimates

External valuations and indices from commercial and public sources. These are provided as-is and reflect the methodology and assumptions of their respective providers.

| Feature | Description |
|---------|-------------|
| `ai_valuation_estimate` | Automated valuation from the ValuCorp v2.3 pricing model, trained on historical auction data. Released 2246; not yet validated over a full market cycle. |
| `media_hype_score` | Composite media attention index from mining industry newswires (0-10+). Reflects public and media interest in the claim. |
| `analyst_consensus_estimate` | Median valuation from a panel of 8 independent mining analysts. |
| `lucky_number` | Numerological favorability score (0-10) derived from orbital resonance patterns, per the Ceres Institute for Astroprospecting (2246). |
| `social_sentiment_score` | Aggregated sentiment from mining industry social feeds. Normalized to zero mean. |

---

## Target Variables

| Feature | Description |
|---------|-------------|
| `mineral_value` | *Training data only.* The total mineral content value of the asteroid — what's in the rock before extraction operations. This is the theoretical ceiling. Not available during competition. |
| `recovered_value` | *Training data only.* The actual revenue received after extraction: `mineral_value × extraction_yield`. This is what the winner takes home (before subtracting their bid). Negative values indicate a net loss. Not available during competition. |

---

## Notes

- Not all features are equally informative. Part of the challenge is determining which measurements carry signal.
- Market conditions in the training data reflect one economic period. Competition sectors may differ.
- Some features are derived from or correlated with others.
- Asteroid valuation involves interacting factors. Simple univariate relationships may not capture the full picture.
