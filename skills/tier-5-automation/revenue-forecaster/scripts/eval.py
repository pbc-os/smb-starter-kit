#!/usr/bin/env python3
"""Backtesting eval for revenue-forecaster. Autoresearch-compatible.

Usage:
    python3 eval.py --data history.csv --params parameters.json
    python3 eval.py --data history.csv --params parameters.json --holdout
    python3 eval.py --data history.csv --params parameters.json --window 16
    python3 eval.py --data history.csv --params parameters.json --json

This script walks historical data backward in time and asks the model to
predict each week given only the data before it. It reports aggregate
MAPE and a per-entity / per-window breakdown so a critic agent can
validate improvements.

The `--holdout` flag evaluates ONLY on the most recent 4 weeks — the
"sealed envelope" split. The researcher agent in autoresearch should
never run with `--holdout`; only the critic does.

This script is INTENDED TO BE READ-ONLY under autoresearch. Do not
modify it mid-session. If you discover a bug, fix it once and then
freeze it again.
"""

from __future__ import annotations

import argparse
import json
import statistics
import sys
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from model import forecast_week, filter_data  # noqa: E402


DEFAULT_WINDOWS = {
    "last_8":    8,
    "weeks_9_16": (9, 16),
    "last_16":  16,
}

HOLDOUT_WEEKS = 4  # "sealed envelope" — only the critic sees this


def load_history(path):
    """Same CSV loader as forecast.py — duplicated here to keep eval standalone."""
    import csv
    by_entity = {}
    with open(path, newline="") as f:
        reader = csv.DictReader(f)
        if not reader.fieldnames or set(reader.fieldnames) < {"week_start", "entity", "revenue"}:
            sys.exit(
                f"Error: {path} must have columns: week_start, entity, revenue "
                f"(got: {reader.fieldnames})"
            )
        for row in reader:
            try:
                w = date.fromisoformat(row["week_start"].strip())
                r = float(row["revenue"].strip())
            except (ValueError, AttributeError):
                continue
            entity = row["entity"].strip()
            if not entity:
                continue
            by_entity.setdefault(entity, []).append((w, r))
    for entity in by_entity:
        by_entity[entity].sort(key=lambda x: x[0])
    return by_entity


def load_params(path):
    with open(path) as f:
        return json.load(f)


def mape(actuals, predictions):
    """Mean Absolute Percentage Error. Returns None if no valid pairs."""
    pairs = [
        (a, p) for a, p in zip(actuals, predictions)
        if a is not None and p is not None and a > 0
    ]
    if not pairs:
        return None
    errors = [abs(a - p) / a for a, p in pairs]
    return 100.0 * statistics.mean(errors)


def backtest_entity(data, params, entity_name, windows, holdout_only=False):
    """Walk backward through time, predicting each week from only prior data.

    Returns a dict mapping window name → list of (actual, predicted) pairs.
    """
    filtered = filter_data(data, params, entity_name)
    if len(filtered) < 12:
        return {}  # not enough history to backtest

    # Determine the validation frontier
    all_weeks = [w for w, _ in filtered]
    last_week = max(all_weeks)

    results = {name: [] for name in windows}

    for idx, (target_week, actual) in enumerate(filtered):
        weeks_back = (last_week - target_week).days // 7
        if weeks_back < 0:
            continue

        # Holdout = last 4 weeks only (sealed envelope)
        in_holdout = weeks_back < HOLDOUT_WEEKS

        if holdout_only and not in_holdout:
            continue
        if not holdout_only and in_holdout:
            # Researcher mode: skip the holdout so it can't peek
            continue

        data_before = filtered[:idx]
        if len(data_before) < 4:
            continue

        fc = forecast_week(data_before, target_week, params, entity_name)
        pred = fc["point_estimate"]

        for name, spec in windows.items():
            if isinstance(spec, tuple):
                lo, hi = spec
                if lo <= weeks_back + 1 <= hi:
                    results[name].append((actual, pred))
            else:
                if weeks_back < spec:
                    results[name].append((actual, pred))

    return results


def main():
    parser = argparse.ArgumentParser(description="Backtesting eval for revenue-forecaster.")
    parser.add_argument("--data", required=True, help="Historical CSV (week_start,entity,revenue)")
    parser.add_argument("--params", required=True, help="Parameters JSON")
    parser.add_argument(
        "--holdout",
        action="store_true",
        help="Evaluate only on the most recent 4 weeks (the sealed envelope)",
    )
    parser.add_argument(
        "--window",
        type=int,
        default=None,
        help="Override to eval on the last N weeks only (default: multi-window)",
    )
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of human-readable")

    args = parser.parse_args()
    data_by_entity = load_history(args.data)
    params = load_params(args.params)

    if args.window:
        windows = {f"last_{args.window}": args.window}
    else:
        windows = DEFAULT_WINDOWS

    report = {
        "mode":    "holdout" if args.holdout else "train",
        "windows": {},
        "per_entity": {},
        "primary_mape": None,
    }

    all_pairs = {name: [] for name in windows}

    for entity, data in data_by_entity.items():
        entity_results = backtest_entity(
            data, params, entity, windows, holdout_only=args.holdout
        )
        report["per_entity"][entity] = {}
        for name, pairs in entity_results.items():
            if not pairs:
                continue
            actuals = [a for a, _ in pairs]
            preds = [p for _, p in pairs]
            entity_mape = mape(actuals, preds)
            report["per_entity"][entity][name] = {
                "mape": round(entity_mape, 3) if entity_mape is not None else None,
                "n_weeks": len(pairs),
            }
            all_pairs[name].extend(pairs)

    for name, pairs in all_pairs.items():
        if not pairs:
            continue
        actuals = [a for a, _ in pairs]
        preds = [p for _, p in pairs]
        m = mape(actuals, preds)
        report["windows"][name] = {
            "mape":    round(m, 3) if m is not None else None,
            "n_weeks": len(pairs),
        }

    # Primary metric = average MAPE across populated windows
    populated = [w["mape"] for w in report["windows"].values() if w["mape"] is not None]
    if populated:
        report["primary_mape"] = round(statistics.mean(populated), 3)

    if args.json:
        json.dump(report, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print_human_readable(report, args.holdout)

    # Exit cleanly
    sys.exit(0)


def print_human_readable(report, holdout):
    print(f"Revenue Forecaster Eval — {'HOLDOUT' if holdout else 'TRAIN'}")
    print("=" * 60)
    print()
    print(f"Primary MAPE (avg across windows): {report['primary_mape']}%")
    print()
    print("Per-window:")
    for name, data in report["windows"].items():
        print(f"  {name:15s}  {data['mape']:>7}%  ({data['n_weeks']} weeks)")
    print()
    print("Per-entity:")
    for entity, windows in report["per_entity"].items():
        print(f"  {entity}:")
        for name, data in windows.items():
            print(f"    {name:15s}  {data['mape']:>7}%  ({data['n_weeks']} weeks)")


if __name__ == "__main__":
    main()
