# Research Instructions — Revenue Forecaster

This file is the `research.md` template for an [autoresearch](../../autoresearch/) session optimizing the revenue-forecaster skill. Copy it to your project root, fill in the bracketed sections with what you know about your business, and run the autoresearch loop.

## Objective

**What we're optimizing:** Weekly revenue forecast for `[your business name]`.
**Primary metric:** MAPE (Mean Absolute Percentage Error) — lower is better.
**Current baseline:** `[run eval.py once with the starter parameters to establish this]`.
**Target:** `[set a realistic stretch target, e.g., "< 5% MAPE on the last 16 weeks"]`

## How to Evaluate

Run the eval script. **Do NOT modify the eval script** under any circumstances.

```bash
python3 scripts/eval.py --data data/history.csv --params config/parameters.json
# For holdout validation (critic only):
python3 scripts/eval.py --data data/history.csv --params config/parameters.json --holdout
```

The eval script outputs:

- **Primary metric:** Aggregate MAPE across all entities and all validation windows
- **Per-entity breakdown:** So the critic can check for regressions
- **Per-window breakdown:** last 8 weeks, weeks 9–16, last 16 weeks, monthly aggregates

## Business Context (fill this in)

```
Business type:        [e.g., "specialty coffee roaster with 2 locations"]
Revenue source:       [e.g., "Square + Shopify, deposits land daily"]
Entities:             [list them, e.g., "Main Street, Downtown"]
Years of history:     [e.g., "Main Street: 8 months, Downtown: 18 months"]

Known patterns:
- [e.g., "Christmas week is 2x normal for Main Street"]
- [e.g., "Downtown has a mid-month spike on the 15th"]
- [e.g., "Summer (Jun-Aug) drops ~40% at both locations"]
- [e.g., "New location ramped up for 3 months before stabilizing"]

Holidays that matter:
- [e.g., "Thanksgiving, Christmas, New Year's: major"]
- [e.g., "Memorial Day, July 4th, Labor Day: minor at best"]
- [e.g., "Mother's Day, Father's Day: no effect"]

Things we've already tried that DIDN'T work:
- [e.g., "Tried a single global holiday multiplier — didn't match per-shop patterns"]
- [e.g., "Tried 8-week recent window — added noise without improving accuracy"]
```

## Available Parameters

See `config/parameters.json` for the full list and `skills/tier-5-automation/revenue-forecaster/references/methodology.md` for a deep-dive on what each parameter controls.

**Priority order for exploration** (biggest typical wins first):

1. **Holiday multipliers.** Set realistic `christmas_mult`, `thanksgiving_mult`, etc. per entity. This is almost always the #1 win.
2. **Outlier trimming.** Verify `outlier_handling.trim_holiday_weeks = true`.
3. **Per-entity blending weights.** Different entities often need different weights.
4. **Week-of-month adjustments.** Enable and tune if the per-entity error breakdown shows systematic within-month patterns.
5. **Exponential decay on recent average.** Try `decay_factor: 0.95` for fast-changing entities.
6. **Blending weight fine-tuning.** Last, not first — the above usually move the metric more.

## Critic Gates

Default gates (configurable — edit as needed):

- **Gate 1 — Holdout validation.** Did MAPE improve on the holdout window (last 4 weeks)?
- **Gate 2 — No-entity-regression.** No individual entity got more than 2× worse than the overall improvement.
- **Gate 3 — Stability.** Improvement is larger than 0.1% MAPE (the noise floor for this eval).
- **Gate 4 — Directional sanity.** Holiday multipliers stay in `[0.3, 3.0]`. Blending weights stay non-negative and sum to ≤1.05.

## Data Sources

- **Historical revenue:** `data/history.csv` (columns: `week_start`, `entity`, `revenue`)
- **Holidays:** Encoded in the model — no external data needed
- **Validation splits:** Eval script supports `--holdout` for holdout-only evaluation

## Rules

1. Change ONE parameter per experiment
2. NEVER modify the eval script
3. Always revert failed experiments before trying the next one
4. Target the biggest error first (check per-entity breakdown after each run)
5. Log every experiment in `experiments/`
6. Stop after 15 experiments or when the last 3 all fail → trigger meta-review
7. **Coverage before depth** — don't tune blending 20 times when holiday multipliers have 0 experiments

## Session Settings

- **Max experiments per session:** 15
- **Meta-review interval:** Every 10 experiments (or after 3 consecutive failures)
- **Archive max entries:** 5 (diverse top configs)
- **Convergence threshold:** Stop if last 5 experiments all fail
- **Branch strategy:** Create a git branch per session (e.g., `autoresearch/forecast-YYYY-MM-DD`)

## Learned Insights

*(This section is auto-populated by the meta-reviewer agent. Leave it empty initially — the meta-reviewer will append findings here as the session progresses.)*
