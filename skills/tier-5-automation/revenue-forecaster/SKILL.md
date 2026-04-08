---
name: revenue-forecaster
version: 1.0.0
tier: automation
description: "Weekly revenue / sales forecasting for small businesses with multiple locations or product lines. Blends recent trend + seasonal baseline + YoY growth with per-entity holiday multipliers and week-of-month adjustments. Ships autoresearch-compatible eval and parameters so you can tune it on your own historical data."
requires:
  bins: ["python3"]
  skills: []
---

# Revenue Forecaster

**Predict next week's revenue. Project 13 weeks of cash. Stress-test scenarios. Tune it yourself with autoresearch.**

Most SMB forecasting is either a gut number or a wild spreadsheet. This skill gives your agent a real parametric forecast model that handles the things that actually matter for small businesses:

- **Multiple locations or product lines** with independent per-entity parameters (each location has its own holiday patterns, growth rate, and week-of-month quirks)
- **Holiday multipliers** (Thanksgiving, Christmas, New Year's, MLK, July 4th, etc.)
- **Week-of-month patterns** (some businesses spike on pay weeks; some dip early in the month)
- **Outlier trimming** so one anomalous holiday doesn't inflate the recent average
- **Exponential decay** on recent weeks for businesses with fast-changing volume
- **YoY growth blending** when you have enough history
- **Graceful fallback** when you don't — the same model runs with or without YoY data
- **Autoresearch integration** — the skill ships with a fixed eval script and a parameters file so you can [autoresearch](../autoresearch/) your way to lower MAPE on your own data

## Triggers

- "forecast revenue", "predict sales", "how much will we make"
- "weekly forecast", "this week's forecast"
- "13 week forecast", "13-week cash projection", "cash runway"
- "daily forecast", "how much on Friday"
- "stress test", "what if sales drop"
- "tune the forecast", "improve forecast accuracy"

## Prerequisites

- **Historical revenue data** in weekly buckets per entity. Minimum usable: 8 weeks. Good: 6+ months. Great: 1+ year (unlocks YoY blending).
- **Python 3.9+** with the standard library — no pandas/numpy required.
- **A way to feed the data** to the scripts. The built-in adapter reads CSV; see [`references/data-adapters.md`](references/data-adapters.md) for Google Sheets, BigQuery, and Square API patterns.

## Quick Start

1. **Bring your data** — Export a CSV with three columns:

    ```csv
    week_start,entity,revenue
    2025-10-06,Main Street,48350.00
    2025-10-06,Downtown,32110.00
    2025-10-13,Main Street,51200.00
    ...
    ```

    `week_start` must be the Monday of the week (ISO week start). `entity` is your location, shop, product line, or any other unit you want forecasted independently. `revenue` is that week's total.

2. **Copy the starter parameters** — `cp templates/parameters.json config/parameters.json` and edit it if you already know things about your business (e.g., Shop A has a Christmas spike of 2×).

3. **Run a forecast:**

    ```bash
    python3 scripts/forecast.py --data data/history.csv --params config/parameters.json
    ```

    Output is JSON to stdout with one entry per entity: point estimate, confidence range, component breakdown, and the methodology note so you can explain the number.

4. **Pair with autoresearch** (optional but recommended) — The scripts ship with `scripts/eval.py`, which is a backtesting evaluator that the [autoresearch skill](../autoresearch/) can drive to tune your parameters. The parameters that ship with this skill are sensible defaults, *not* optimized to your business — autoresearch is how you close that gap.

## Workflow

### Phase 1: Get Your Data In

The scripts expect a single CSV with one row per entity per week. The built-in reader in `scripts/forecast.py` handles CSV by default. For other sources:

- **Google Sheets** — Use the `google-sheets` skill to pull a range, pipe it as CSV into `forecast.py`.
- **BigQuery** — Use `bq query --format csv` and redirect into the script.
- **Square POS** — Use the Square Connect API (`GET /v2/payouts`) to dump weekly payout history to a CSV.
- **Custom** — Any data source that can produce rows of `(week_start, entity, revenue)` works.

See [`references/data-adapters.md`](references/data-adapters.md) for copy-pasteable patterns for each of the above.

### Phase 2: Pick a Forecast Mode

The same `forecast.py` entry point supports multiple modes via `--mode`:

| Mode | What it produces | When to use |
|---|---|---|
| `weekly` (default) | Point estimate + range + component breakdown for the current week, per entity | Weekly cash planning, AP run inputs |
| `thirteen-week` | Rolling 13-week cash projection with optional recurring obligations | Runway questions, big expense planning, approaching seasonal dips |
| `daily` | Weekly forecast distributed across days using day-of-week multipliers from recent history | Daily cash flow, "will deposits cover Friday payroll?" |
| `stress` | Applies a configurable shock (e.g., `-30% for 3 weeks`) on top of the weekly forecast | "What if sales drop?", summer slump prep, vendor payment planning |

Examples:

```bash
# Weekly forecast (default)
python3 scripts/forecast.py --data data/history.csv

# 13-week rolling projection, including recurring obligations
python3 scripts/forecast.py --data data/history.csv --mode thirteen-week \
  --obligations config/recurring_obligations.json

# Daily breakdown for the current week
python3 scripts/forecast.py --data data/history.csv --mode daily

# Stress test: 30% drop for 3 weeks starting now
python3 scripts/forecast.py --data data/history.csv --mode stress \
  --shock -0.30 --shock-weeks 3
```

### Phase 3: Tune It With Autoresearch

The defaults in `templates/parameters.json` are reasonable starting points — they are *not* tuned to your business. The whole point of shipping this with an eval script is so you can find the right parameters for *your* data.

1. **Scaffold an autoresearch session** — follow the [autoresearch skill](../autoresearch/) workflow. Point it at:
    - `research.md` → copy `templates/research.md` as your research file; edit the domain-knowledge section with what you know about your business (e.g., "Labor Day is dead for us", "Dec 24 is our biggest day").
    - `eval script` → `scripts/eval.py` (already read-only-safe — it never modifies parameters)
    - `parameters file` → `config/parameters.json`
    - `experiments/` → a new directory the agent creates
    - `archive.json`, `coverage.json` → the agent creates these on first run

2. **Run the loop.** The autoresearch skill handles the three-agent pipeline (researcher, critic, meta-reviewer). Start with 10–20 experiments.

3. **Watch the meta-reviewer.** The first big wins usually come from structural changes the researcher wouldn't find on its own: adding a holiday multiplier you didn't know existed, enabling week-of-month adjustments, tightening the outlier threshold. The meta-reviewer is the mechanism that surfaces these.

See [`references/methodology.md`](references/methodology.md) for a deep dive on each parameter and what it controls.

## Config Schema (parameters.json)

The parameters file has two sections: global defaults and per-entity overrides. Every field in the global section can be overridden per entity.

```jsonc
{
  "blending": {
    "recent_weight": 0.82,
    "seasonal_weight": 0.16,
    "yoy_weight":    0.02
  },
  "blending_no_yoy": {
    "recent_weight":   1.00,
    "seasonal_weight": 0.00
  },

  "lookback": {
    "recent_weeks":       4,
    "variability_weeks":  12,
    "seasonal_min_weeks": 3
  },

  "exponential_weighting": {
    "decay_factor": 1.0
  },

  "outlier_handling": {
    "trim_holiday_weeks":   true,
    "holiday_threshold_pct": 1.30
  },

  "week_of_month": {
    "enabled":     false,
    "week_1_adj":  0.0,
    "week_2_adj":  0.0,
    "week_3_adj":  0.0,
    "week_4_adj":  0.0
  },

  "holidays": {
    "enabled":             true,
    "thanksgiving_mult":   1.0,
    "christmas_mult":      1.0,
    "new_years_mult":      1.0,
    "mlk_week_mult":       1.0,
    "early_jan_mult":      1.0,
    "late_jan_mult":       1.0,
    "memorial_day_mult":   1.0,
    "july_4th_mult":       1.0,
    "labor_day_mult":      1.0,
    "easter_passover_mult": 1.0
  },

  "growth_adjustment": {
    "n_months_avg": 6
  },

  "data_filters": {
    "global": {
      "min_weekly_revenue": 0,
      "data_start_date":    null
    }
  },

  "per_entity": {
    "Main Street": {
      "holidays": {
        "christmas_mult":   2.05,
        "thanksgiving_mult": 1.94
      },
      "week_of_month": {
        "enabled":    true,
        "week_3_adj": 0.075
      }
    },
    "Downtown": {
      "exponential_weighting": { "decay_factor": 0.95 },
      "data_filters": {
        "data_start_date": "2024-09-02"
      }
    }
  }
}
```

The full schema with field-by-field documentation is in [`references/methodology.md`](references/methodology.md). The starter file at `templates/parameters.json` has all the knobs at neutral defaults so the model will run out of the box — autoresearch is what moves them away from neutral.

## Output Format

`forecast.py --mode weekly` emits JSON like this (one entry per entity):

```json
{
  "forecast_date": "2026-04-07",
  "forecast_week": "2026-04-06",
  "entities": {
    "Main Street": {
      "point_estimate": 48350.00,
      "confidence_range": { "low": 45200.00, "high": 51500.00 },
      "components": {
        "recent_4wk_avg":     48100.00,
        "seasonal_avg":       46800.00,
        "yoy_growth_rate":    0.042,
        "yoy_adjusted":       48765.60,
        "week_of_month":      1,
        "week_of_month_adj": -0.05
      },
      "methodology": {
        "weights": "82% recent + 16% seasonal + 2% YoY (6mo growth: 4.2%) | week 1 adj: -5.0%",
        "model_version": "1.0.0"
      }
    }
  }
}
```

The structure is deliberately verbose — the `components` and `methodology` blocks are so the agent can *explain* the forecast, not just report it. When the business owner asks "why is this number low?", the answer should be "week 1 of the month typically runs 5% under the 4-week average at Main Street," not "the model says so."

## Integration With Other Skills

- **`autoresearch`** — Tune parameters on your own historical data. This is the intended pairing.
- **`morning-briefing`** — Include this week's forecast in the daily digest.
- **`google-sheets`** — Read historical data from a sheet, pipe into `forecast.py`.
- **`google-ads`** — Compare forecasted revenue to ad spend for a rough CAC/ROAS view.
- **`semantic-layer-audit`** — Document which data source you're feeding to the forecaster and why.

## Tips

- **Start with default parameters.** They'll produce a forecast that's usually within 10–20% of actuals. Autoresearch is what gets you under 5%.
- **Enable YoY only when you have 18+ months of data.** With less history, a YoY term pulls from a tiny sample and adds variance without improving accuracy.
- **Per-entity overrides compound.** A global 1.0× Christmas multiplier with a per-entity 2.05× override means that entity gets 2.05×. The per-entity value wins.
- **Holiday multipliers should be learned, not guessed.** Your guess is usually within ±20%; autoresearch can usually get within ±2%.
- **The eval script is sacred.** Don't edit `scripts/eval.py` during an autoresearch session — that's the thing keeping the researcher honest. If the eval is wrong, fix it once and then freeze it again.
- **Retune quarterly.** Your business changes. Parameters should change with it. A 15-minute autoresearch session every quarter is usually enough to keep MAPE stable.

## Credits

The forecasting methodology in this skill — blended recent/seasonal/YoY with per-entity holiday multipliers and week-of-month adjustments — was developed at [Prospect Butcher Co](https://prospectbutcher.co) (a two-shop butcher in New York City) and tuned from 22% MAPE down to under 2% through roughly 90 autoresearch experiments across four model versions. The generalizations in this public version (pluggable data adapters, entity-agnostic naming, parameter files decoupled from any specific POS) are a cleanup of that work into something any SMB can point at its own data.

If you extend this skill with a new data adapter, a new forecast mode, or a genuinely new parameter that moves accuracy on real data, PRs welcome.

---

*Forecasting is the bridge between "what happened" and "what should we do next." Make the bridge a little less wobbly.*
