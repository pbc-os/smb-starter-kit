# Forecasting Methodology — Deep Dive

This document explains every parameter in `parameters.json`, what it controls, and how to think about tuning it. The model is a **blended weighted average** with per-entity overrides, holiday multipliers, and week-of-month adjustments. It's deliberately simple — a few dozen tunable knobs, no ML training, no GPUs, runs on Python standard library.

## The Core Equation

For any week `t` and entity `e`, the forecast is:

```
forecast(t, e) = (
    recent_weight   * recent_avg(t, e)
  + seasonal_weight * seasonal_avg(t, e)
  + yoy_weight      * yoy_adjusted(t, e)
)
* week_of_month_adjustment(t, e)
* holiday_multiplier(t, e)
```

Where:

- **`recent_avg(t, e)`** — The average (or exponentially-weighted average) of the last N weeks of revenue for entity `e`, with optional outlier trimming.
- **`seasonal_avg(t, e)`** — The average revenue for entity `e` in the same calendar month across all historical years.
- **`yoy_adjusted(t, e)`** — The seasonal average scaled by the year-over-year growth rate for entity `e`.
- **`week_of_month_adjustment(t, e)`** — A ±% adjustment based on which week of the month `t` falls in.
- **`holiday_multiplier(t, e)`** — A multiplicative adjustment for known holiday weeks.

If an entity has no YoY data (less than ~18 months of history), the model falls back to a `blending_no_yoy` weighting scheme that ignores the YoY term.

## Why Blended?

Each component captures a different signal:

- **Recent** captures current-state volume. If your business ramped up last month, recent-avg knows. Seasonal doesn't.
- **Seasonal** captures calendar effects. If every January is slow for you, seasonal knows. Recent-avg of the preceding December doesn't.
- **YoY growth** captures the long-run trend. If you grew 40% year-over-year, that's baked in.

No single component gets it right. The blend is what makes it robust. And because the right blend is business-specific, the weights are parameters — you tune them with autoresearch.

---

## Parameters Reference

### `blending` (required)

Weights for the three-component blend when YoY data is available.

```json
"blending": {
  "recent_weight":   0.82,
  "seasonal_weight": 0.16,
  "yoy_weight":      0.02
}
```

| Field | Default | Range | Notes |
|---|---|---|---|
| `recent_weight` | 0.82 | 0.0–1.0 | Weight on the recent 4-week (or N-week) average |
| `seasonal_weight` | 0.16 | 0.0–1.0 | Weight on the same-month historical average |
| `yoy_weight` | 0.02 | 0.0–1.0 | Weight on the YoY-growth-adjusted seasonal value |

**Weights should sum to 1.0** (the model doesn't enforce it, but unequal sums distort the forecast).

**Why these defaults?** The 4-week recent average already captures current volume levels. Seasonal provides a small anchor, and a tiny YoY weight gives a growth uplift without the volatility of a larger weight. These defaults came from a real-world tuning session — expect to adjust them for your business.

### `blending_no_yoy` (required)

Used automatically when an entity has no prior-year data to compute YoY growth.

```json
"blending_no_yoy": {
  "recent_weight":   1.00,
  "seasonal_weight": 0.00
}
```

| Field | Default | Notes |
|---|---|---|
| `recent_weight` | 1.00 | Weight on recent average |
| `seasonal_weight` | 0.00 | Weight on seasonal baseline |

For a new business (< 12 months of history), `recent: 1.0, seasonal: 0.0` often wins — the seasonal baseline is too noisy or missing.

### `lookback` (required)

How many weeks to look back for each component.

```json
"lookback": {
  "recent_weeks":       4,
  "variability_weeks":  12,
  "seasonal_min_weeks": 3
}
```

| Field | Default | Range | Notes |
|---|---|---|---|
| `recent_weeks` | 4 | 2–12 | Number of recent weeks used for the "recent" component |
| `variability_weeks` | 12 | 8–26 | Number of weeks used to compute the stddev for the confidence range |
| `seasonal_min_weeks` | 3 | 1–10 | Minimum sample size in the target month before falling back to adjacent months |

**Tuning note:** A longer `recent_weeks` smooths out noise but reacts slower to real changes. Most SMBs converge at 4 weeks.

### `exponential_weighting`

```json
"exponential_weighting": {
  "decay_factor": 1.0
}
```

| Field | Default | Range | Notes |
|---|---|---|---|
| `decay_factor` | 1.0 | 0.5–1.0 | 1.0 = equal weights across recent weeks; 0.95 = ~5% less weight on the oldest week in the window |

Use decay < 1.0 when recent volume is changing fast (a new location ramping up, a product going viral, a seasonal swing starting). Use decay = 1.0 for stable businesses.

### `outlier_handling`

```json
"outlier_handling": {
  "trim_holiday_weeks":   true,
  "holiday_threshold_pct": 1.30
}
```

| Field | Default | Notes |
|---|---|---|
| `trim_holiday_weeks` | true | When true, caps any week's revenue at `threshold_pct * rolling_median` before it enters the recent average |
| `holiday_threshold_pct` | 1.30 | Multiplier of the 12-week rolling median used as the cap |

**Why this matters:** If Thanksgiving week was 2× normal, and that week lands in the 4-week recent window, the recent average is 25% inflated for a month afterward — causing over-forecasting of all four weeks after the holiday. Outlier trimming prevents this. The holiday multiplier (below) is what puts the actual 2× spike back into the forecast on the right week.

### `week_of_month`

```json
"week_of_month": {
  "enabled":    false,
  "week_1_adj": 0.0,
  "week_2_adj": 0.0,
  "week_3_adj": 0.0,
  "week_4_adj": 0.0
}
```

| Field | Default | Notes |
|---|---|---|
| `enabled` | false | Turn the feature on globally or per-entity |
| `week_N_adj` | 0.0 | Multiplicative adjustment: `point *= (1 + week_N_adj)` |

**Why this exists:** Many SMBs have systematic within-month patterns. Service businesses often see spikes on pay weeks (weeks containing the 1st and 15th). Restaurants see dips on rent weeks. A 5–10% WoM effect is surprisingly common and is one of the biggest single wins in real tuning sessions.

**Tuning:** Start disabled. Once autoresearch has squeezed blending weights, enable and try `week_3_adj: 0.05` if your business spikes mid-month, or `week_1_adj: -0.05` if it dips early-month.

### `holidays`

```json
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
}
```

Holiday multipliers are **multiplicative** — `1.0` means "no effect", `2.0` means "double", `0.5` means "half". The defaults are all `1.0` so the model doesn't inflate or deflate anything until you tune them.

**How the model detects holidays:** By ISO week number (Thanksgiving = week 48, Christmas = week 52, etc.) and by calendar date (Easter/Passover is approximated as the 2nd week of April; Memorial Day as the last week of May; July 4th as the first week of July; Labor Day as the first week of September).

**Which holidays matter?** This is business-specific. A butcher shop cares about Thanksgiving and Christmas (people buy huge cuts). A bar cares about New Year's Eve, St. Patrick's Day, and the Super Bowl. A flower shop cares about Mother's Day and Valentine's Day. Enable the holidays that matter for your business and set the others to `1.0`.

**Pre- and post-holiday effects:** You can extend the model with additional keys like `pre_christmas_mult`, `pre_christmas_2wk_mult`, `post_thanksgiving_mult`, `post_newyears_mult` if your business has a recognizable lead-up or hangover pattern. The starter `templates/parameters.json` includes these as neutral `1.0` values.

### `growth_adjustment`

```json
"growth_adjustment": {
  "n_months_avg": 6
}
```

| Field | Default | Notes |
|---|---|---|
| `n_months_avg` | 6 | Number of recent months used to compute the YoY growth rate |

A longer `n_months_avg` smooths out noise in the growth calculation; a shorter one is more reactive. 6 is a good compromise for stable businesses; use 3 for fast-changing ones and 12 for very stable ones.

### `data_filters`

```json
"data_filters": {
  "global": {
    "min_weekly_revenue": 0,
    "data_start_date":    null
  }
}
```

| Field | Default | Notes |
|---|---|---|
| `min_weekly_revenue` | 0 | Exclude weeks where revenue was below this number (e.g., closed weeks, opening ramp) |
| `data_start_date` | null | ISO date string; exclude all weeks before this date |

**Why this matters:** If an entity had a 3-month opening ramp where weekly revenue was under $5k, those weeks will distort the seasonal and YoY calculations. Set `min_weekly_revenue` or `data_start_date` to exclude them.

---

## `per_entity` Overrides

Every field in the global config can be overridden per entity:

```json
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
  }
}
```

The merge rule is "per-entity wins field-by-field", not "per-entity replaces the whole section". So the example above keeps the global defaults for every holiday except `christmas_mult` and `thanksgiving_mult`.

**When to use per-entity overrides:**

- Two locations with different customer demographics and different holiday profiles
- Two product lines where one has strong seasonality and the other doesn't
- A location that just opened and needs its own `data_filters.data_start_date`
- An entity with a recognizable within-month pattern the others don't have

**When not to use per-entity overrides:**

- You only have one entity. Just set the globals.
- You have less than 6 months of data per entity. The per-entity tuning will fit to noise.

---

## Common Model Wins (in order of typical impact)

Based on real tuning sessions, the biggest accuracy improvements usually come from, in order:

1. **Holiday multipliers.** Setting a realistic Christmas/Thanksgiving multiplier on a butcher/restaurant/flower shop can drop holiday-week MAPE from 30%+ to under 2%.
2. **Outlier trimming.** Without it, a single holiday week inflates the recent average for a month afterward.
3. **Per-entity overrides.** Two locations rarely have the same profile. Forcing one set of parameters on both is almost always worse than independent tuning.
4. **Week-of-month adjustments.** Often worth 1–3% MAPE once blending is saturated.
5. **Exponential decay on recent.** Worth 0.5–1% MAPE for fast-changing volume; near-zero for stable businesses.
6. **Blending weight tuning.** Usually worth 0.5–1.5% MAPE, but diminishing returns — don't spend 20 experiments here if the above haven't been tried.
7. **YoY growth n_months.** Last-mile tuning, usually worth 0.1–0.3% MAPE.

Use this ordering when planning an autoresearch session: check the big wins first.
