"""Shared helpers for the revenue-forecaster model.

Stdlib-only (no numpy/pandas) so the skill runs on any Python 3.9+ install.
"""

from __future__ import annotations

import statistics


def exponential_weighted_avg(values, decay):
    """Exponentially weighted average.

    Args:
        values: List of numbers, ordered chronologically (oldest first).
        decay: Decay factor in (0, 1]. 1.0 = equal weights. 0.95 = oldest
            entry gets ~5% less weight per step.

    Returns:
        Weighted average, or 0 if values is empty.
    """
    if not values:
        return 0.0
    n = len(values)
    weights = [decay ** i for i in range(n - 1, -1, -1)]
    total_weight = sum(weights)
    return sum(v * w for v, w in zip(values, weights)) / total_weight


def get_week_of_month(d):
    """Return 1-4 for which week of the month the date falls in.

    Weeks are defined by day of month: 1-7 = week 1, 8-14 = week 2,
    15-21 = week 3, 22+ = week 4. This is deliberately simple and
    doesn't correspond to ISO weeks.
    """
    return min((d.day - 1) // 7 + 1, 4)


def trim_outliers(data, threshold_pct):
    """Cap outlier revenue at threshold_pct * rolling median.

    The rolling median is computed over the last 12 weeks (or all weeks
    if fewer than 12 exist). Any week whose revenue exceeds
    `threshold_pct * rolling_median` is capped to that cap.

    Args:
        data: List of (week_date, revenue) tuples, sorted chronologically.
        threshold_pct: Multiplier of the rolling median used as the cap
            (e.g., 1.30 means cap at 130% of median).

    Returns:
        New list of (week_date, revenue) tuples with outliers capped.
    """
    if len(data) < 8:
        return list(data)
    window = [d for _, d in data[-12:]]
    rolling_median = statistics.median(window)
    cap = rolling_median * threshold_pct
    return [(w, min(d, cap)) for w, d in data]


def get_seasonal_avg(data_before, month, min_weeks):
    """Average revenue for a given month, with adjacent-month fallback.

    If fewer than `min_weeks` of data exist for the target month, fall
    back to adjacent months (prior month, next month, then ±2 months).
    If nothing matches, fall back to the overall recent average.

    Args:
        data_before: List of (week_date, revenue) tuples.
        month: Target calendar month (1-12).
        min_weeks: Minimum samples needed before falling back.

    Returns:
        (average, sample_count) tuple.
    """
    month_data = [d for w, d in data_before if w.month == month]
    if len(month_data) >= min_weeks:
        return statistics.mean(month_data), len(month_data)

    for offset in (-1, 1, -2, 2):
        adj_month = ((month - 1 + offset) % 12) + 1
        adj_data = [d for w, d in data_before if w.month == adj_month]
        if len(adj_data) >= min_weeks:
            return statistics.mean(adj_data), len(adj_data)

    if month_data:
        return statistics.mean(month_data), len(month_data)

    # Final fallback: average of the most recent 12 weeks
    tail = [d for _, d in data_before[-12:]]
    return (statistics.mean(tail), 0) if tail else (0.0, 0)


def rolling_stddev(values):
    """Standard deviation with a safe fallback for short series."""
    if len(values) < 2:
        return 0.0
    return statistics.stdev(values)
