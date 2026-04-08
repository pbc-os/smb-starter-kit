#!/usr/bin/env python3
"""CLI entry point for the revenue-forecaster skill.

Usage:
    python3 forecast.py --data history.csv [--params parameters.json] [--mode MODE]

Modes:
    weekly         Current-week forecast per entity (default)
    thirteen-week  13-week rolling projection per entity
    daily          Current week distributed across days using DOW multipliers
    stress         Apply a configurable shock to the weekly forecast

Examples:
    # Default weekly forecast
    python3 forecast.py --data history.csv

    # 13-week projection with recurring obligations
    python3 forecast.py --data history.csv --mode thirteen-week \\
        --obligations recurring.json

    # Daily breakdown
    python3 forecast.py --data history.csv --mode daily

    # Stress test: 30% drop for 3 weeks
    python3 forecast.py --data history.csv --mode stress --shock -0.30 --shock-weeks 3

Output is JSON on stdout.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

# Ensure we can import sibling modules regardless of where this script is run from
sys.path.insert(0, str(Path(__file__).parent))

from model import forecast_week, get_entity_params, filter_data  # noqa: E402
from utils import rolling_stddev  # noqa: E402


DEFAULT_PARAMS_PATH = Path(__file__).parent.parent / "templates" / "parameters.json"


# ---------------------------------------------------------------------------
# Data loading
# ---------------------------------------------------------------------------

def load_history(path):
    """Load a 3-column CSV into a dict of entity → [(week_date, revenue), ...].

    Skips rows with missing fields, non-date week_start, or non-numeric revenue.
    Sorts each entity's weeks chronologically.
    """
    by_entity = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or set(reader.fieldnames) < {"week_start", "entity", "revenue"}:
            sys.exit(
                f"Error: {path} must have header columns: week_start, entity, revenue "
                f"(got: {reader.fieldnames})"
            )
        for row_num, row in enumerate(reader, start=2):
            try:
                w = date.fromisoformat(row["week_start"].strip())
                r = float(row["revenue"].strip())
            except (ValueError, AttributeError):
                print(
                    f"Warning: skipping row {row_num} (bad data): {row}",
                    file=sys.stderr,
                )
                continue
            entity = row["entity"].strip()
            if not entity:
                continue
            by_entity.setdefault(entity, []).append((w, r))

    for entity in by_entity:
        by_entity[entity].sort(key=lambda x: x[0])
    return by_entity


def load_params(path):
    """Load parameters JSON. Falls back to the bundled starter if None."""
    p = Path(path) if path else DEFAULT_PARAMS_PATH
    with open(p) as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# Mode: weekly
# ---------------------------------------------------------------------------

def mode_weekly(data_by_entity, params, as_of):
    """Forecast the current week per entity."""
    monday = as_of - timedelta(days=as_of.weekday())
    results = {}
    for entity, data in data_by_entity.items():
        filtered = filter_data(data, params, entity)
        data_before = [(w, r) for w, r in filtered if w < monday]
        if not data_before:
            results[entity] = {"error": "no historical data before target week"}
            continue

        fc = forecast_week(data_before, monday, params, entity)
        point = fc["point_estimate"]

        # Confidence range from historical stddev
        var_n = get_entity_params(params, entity)["lookback"]["variability_weeks"]
        var_vals = [r for _, r in data_before[-var_n:]]
        stddev = rolling_stddev(var_vals)
        fc["confidence_range"] = {
            "low":  round(max(point - stddev, 0), 2),
            "high": round(point + stddev, 2),
        }
        fc["variability"] = {
            "stddev":          round(stddev, 2),
            "n_weeks_sampled": len(var_vals),
        }
        results[entity] = fc

    return {
        "mode":          "weekly",
        "forecast_date": as_of.isoformat(),
        "forecast_week": monday.isoformat(),
        "entities":      results,
    }


# ---------------------------------------------------------------------------
# Mode: thirteen-week
# ---------------------------------------------------------------------------

def mode_thirteen_week(data_by_entity, params, as_of, obligations_path=None):
    """Project 13 weeks forward per entity.

    Optionally incorporates recurring_obligations.json, a simple file with:
        { "entity": "Main Street", "weekly_obligation": 18000 }
    applied to each week. Net = forecast - obligations.
    """
    monday = as_of - timedelta(days=as_of.weekday())
    obligations = {}
    if obligations_path and os.path.exists(obligations_path):
        with open(obligations_path) as f:
            obligations_cfg = json.load(f)
        for row in obligations_cfg.get("entities", []):
            obligations[row["entity"]] = float(row.get("weekly_obligation", 0))

    results = {}
    for entity, data in data_by_entity.items():
        filtered = filter_data(data, params, entity)
        data_before = [(w, r) for w, r in filtered if w < monday]
        if not data_before:
            results[entity] = {"error": "no historical data before target week"}
            continue

        weekly_obligation = obligations.get(entity, 0.0)
        weeks_out = []
        rolling_history = list(data_before)

        for i in range(13):
            target = monday + timedelta(weeks=i)
            fc = forecast_week(rolling_history, target, params, entity)
            point = fc["point_estimate"]
            weeks_out.append({
                "week_start":        target.isoformat(),
                "forecast_revenue":  point,
                "weekly_obligation": round(weekly_obligation, 2),
                "net":               round(point - weekly_obligation, 2),
                "holiday":           fc["components"].get("holiday_name"),
            })
            # Use the forecast as the "history" for the next iteration
            rolling_history.append((target, point))

        totals = {
            "total_forecast_revenue":  round(sum(w["forecast_revenue"] for w in weeks_out), 2),
            "total_obligations":       round(sum(w["weekly_obligation"] for w in weeks_out), 2),
            "total_net":               round(sum(w["net"] for w in weeks_out), 2),
            "min_net_week":            min(weeks_out, key=lambda w: w["net"]),
        }
        results[entity] = {"weeks": weeks_out, "totals": totals}

    return {
        "mode":          "thirteen-week",
        "forecast_date": as_of.isoformat(),
        "start_week":    monday.isoformat(),
        "entities":      results,
    }


# ---------------------------------------------------------------------------
# Mode: daily
# ---------------------------------------------------------------------------

def compute_dow_multipliers(data_by_entity, as_of, lookback_weeks=13):
    """Compute day-of-week multipliers from recent history.

    Requires daily-granularity data (one row per day, not per week).
    If the input is weekly, returns equal multipliers (1.0 / 7).
    This function is here as a stub — the public version assumes weekly
    input and distributes evenly across 7 days. To use real DOW patterns,
    feed a daily CSV and extend this function.

    Returns:
        Dict of entity → {dow_index (0=Mon..6=Sun): multiplier}
    """
    return {
        entity: {i: 1.0 / 7.0 for i in range(7)}
        for entity in data_by_entity
    }


def mode_daily(data_by_entity, params, as_of):
    """Distribute the weekly forecast across days using DOW multipliers."""
    monday = as_of - timedelta(days=as_of.weekday())
    weekly = mode_weekly(data_by_entity, params, as_of)
    dow_mults = compute_dow_multipliers(data_by_entity, as_of)

    results = {}
    for entity, wk in weekly["entities"].items():
        if "error" in wk:
            results[entity] = wk
            continue
        point = wk["point_estimate"]
        mults = dow_mults.get(entity, {i: 1.0 / 7.0 for i in range(7)})
        days = []
        for dow in range(7):
            day = monday + timedelta(days=dow)
            days.append({
                "date":             day.isoformat(),
                "day_of_week":      day.strftime("%A"),
                "multiplier":       round(mults[dow], 4),
                "forecast_revenue": round(point * mults[dow], 2),
            })
        results[entity] = {
            "weekly_point_estimate": point,
            "days":                  days,
            "note":                  (
                "Using equal 1/7 distribution. For real day-of-week patterns, "
                "extend compute_dow_multipliers() to read daily-granularity data."
            ),
        }

    return {
        "mode":          "daily",
        "forecast_date": as_of.isoformat(),
        "forecast_week": monday.isoformat(),
        "entities":      results,
    }


# ---------------------------------------------------------------------------
# Mode: stress
# ---------------------------------------------------------------------------

def mode_stress(data_by_entity, params, as_of, shock, shock_weeks):
    """Apply a shock (e.g., -0.30 for 30% drop) for N weeks on top of weekly forecast."""
    monday = as_of - timedelta(days=as_of.weekday())
    results = {}
    for entity, data in data_by_entity.items():
        filtered = filter_data(data, params, entity)
        data_before = [(w, r) for w, r in filtered if w < monday]
        if not data_before:
            results[entity] = {"error": "no historical data before target week"}
            continue

        weeks_out = []
        rolling_history = list(data_before)
        for i in range(max(shock_weeks, 4)):
            target = monday + timedelta(weeks=i)
            fc = forecast_week(rolling_history, target, params, entity)
            baseline = fc["point_estimate"]
            shocked = baseline * (1 + shock) if i < shock_weeks else baseline
            weeks_out.append({
                "week_start":         target.isoformat(),
                "baseline_forecast":  baseline,
                "shocked_forecast":   round(shocked, 2),
                "shock_applied":      shock if i < shock_weeks else 0.0,
            })
            rolling_history.append((target, baseline))
        results[entity] = {
            "weeks":      weeks_out,
            "shock":      shock,
            "shock_weeks": shock_weeks,
        }

    return {
        "mode":          "stress",
        "forecast_date": as_of.isoformat(),
        "start_week":    monday.isoformat(),
        "entities":      results,
    }


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Revenue forecaster — blended trend + seasonal + YoY with holiday and WoM adjustments.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("--data", required=True, help="Path to historical CSV (week_start,entity,revenue)")
    parser.add_argument("--params", default=None, help="Path to parameters.json (defaults to bundled starter)")
    parser.add_argument(
        "--mode",
        choices=["weekly", "thirteen-week", "daily", "stress"],
        default="weekly",
        help="Forecast mode (default: weekly)",
    )
    parser.add_argument("--as-of", default=None, help="ISO date to treat as today (default: actual today)")
    parser.add_argument("--obligations", default=None, help="Path to recurring obligations JSON (thirteen-week mode)")
    parser.add_argument("--shock", type=float, default=-0.20, help="Stress-test shock (default: -0.20)")
    parser.add_argument("--shock-weeks", type=int, default=3, help="Stress-test duration in weeks (default: 3)")

    args = parser.parse_args()

    as_of = date.fromisoformat(args.as_of) if args.as_of else date.today()
    data_by_entity = load_history(args.data)
    params = load_params(args.params)

    if not data_by_entity:
        sys.exit(f"Error: no usable data in {args.data}")

    if args.mode == "weekly":
        out = mode_weekly(data_by_entity, params, as_of)
    elif args.mode == "thirteen-week":
        out = mode_thirteen_week(data_by_entity, params, as_of, args.obligations)
    elif args.mode == "daily":
        out = mode_daily(data_by_entity, params, as_of)
    else:  # stress
        out = mode_stress(data_by_entity, params, as_of, args.shock, args.shock_weeks)

    json.dump(out, sys.stdout, indent=2)
    sys.stdout.write("\n")


if __name__ == "__main__":
    main()
