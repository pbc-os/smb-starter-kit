"""Core forecasting model for revenue-forecaster.

Pure-python, stdlib-only. See ../references/methodology.md for the math
and parameter documentation.
"""

from __future__ import annotations

import statistics
from datetime import date

from utils import (
    exponential_weighted_avg,
    get_seasonal_avg,
    get_week_of_month,
    trim_outliers,
)


# ---------------------------------------------------------------------------
# Parameter merging
# ---------------------------------------------------------------------------

def get_entity_params(params, entity_name):
    """Merge per-entity overrides into global parameters.

    The merge is field-by-field: if the entity overrides a specific
    sub-field of a section (e.g., `holidays.christmas_mult`), the other
    fields in that section keep the global default.

    Args:
        params: Full parameters dict (as loaded from parameters.json).
        entity_name: Entity identifier matching a key in params["per_entity"].

    Returns:
        Merged parameters dict for this entity.
    """
    overrides = params.get("per_entity", {}).get(entity_name, {})
    merged = {k: v for k, v in params.items() if not k.startswith("_")}

    for section_key, override_val in overrides.items():
        if section_key.startswith("_"):
            continue
        if isinstance(override_val, dict) and section_key in merged and isinstance(merged[section_key], dict):
            merged[section_key] = {**merged[section_key], **override_val}
        else:
            merged[section_key] = override_val
    return merged


def filter_data(data, params, entity_name):
    """Exclude weeks before data_start_date or below min_weekly_revenue.

    Args:
        data: List of (week_date, revenue) tuples, sorted chronologically.
        params: Full parameters dict (not entity-merged).
        entity_name: Entity identifier.

    Returns:
        Filtered list of (week_date, revenue) tuples.
    """
    entity_filters = (
        params.get("per_entity", {})
        .get(entity_name, {})
        .get("data_filters", {})
    )
    global_filters = params.get("data_filters", {}).get("global", {})

    start_date_str = entity_filters.get("data_start_date") or global_filters.get("data_start_date")
    min_rev = entity_filters.get("min_weekly_revenue", global_filters.get("min_weekly_revenue", 0))

    result = data
    if start_date_str:
        start = date.fromisoformat(start_date_str)
        result = [(w, r) for w, r in result if w >= start]
    if min_rev and min_rev > 0:
        result = [(w, r) for w, r in result if r >= min_rev]
    return result


# ---------------------------------------------------------------------------
# Holiday detection
# ---------------------------------------------------------------------------

# ISO-week-based holiday mapping (US holidays that fall on fixed ISO weeks)
ISO_WEEK_HOLIDAYS = {
    47: ("pre_thanksgiving_mult",  "pre-Thanksgiving"),
    48: ("thanksgiving_mult",      "Thanksgiving"),
    49: ("post_thanksgiving_mult", "post-Thanksgiving"),
    50: ("pre_christmas_2wk_mult", "2wk pre-Christmas"),
    51: ("pre_christmas_mult",     "pre-Christmas"),
    52: ("christmas_mult",         "Christmas"),
    1:  ("new_years_mult",         "New Years"),
    2:  ("post_newyears_mult",     "post-New Years"),
    3:  ("early_jan_mult",         "early January"),
    4:  ("mlk_week_mult",          "MLK week"),
    5:  ("late_jan_mult",          "late January"),
}


def get_holiday_multiplier(target_week, params, entity_name):
    """Determine if target_week is a holiday week for this entity.

    Args:
        target_week: date object for the Monday of the target week.
        params: Full parameters dict (not entity-merged).
        entity_name: Entity identifier.

    Returns:
        (multiplier, holiday_name) tuple. (1.0, None) if not a holiday.
    """
    merged = get_entity_params(params, entity_name)
    holidays = merged.get("holidays", {})
    if not holidays.get("enabled", False):
        return 1.0, None

    iso_week = target_week.isocalendar()[1]

    # Calendar-based (variable-date) holidays
    if target_week.month == 4 and get_week_of_month(target_week) == 2:
        if "easter_passover_mult" in holidays:
            return holidays["easter_passover_mult"], "Easter/Passover"
    if target_week.month == 5 and target_week.day >= 25:
        if "memorial_day_mult" in holidays:
            return holidays["memorial_day_mult"], "Memorial Day"
    if target_week.month == 7 and target_week.day <= 7:
        if "july_4th_mult" in holidays:
            return holidays["july_4th_mult"], "July 4th"
    if target_week.month == 9 and target_week.day <= 7:
        if "labor_day_mult" in holidays:
            return holidays["labor_day_mult"], "Labor Day"

    # ISO-week-based holidays
    entry = ISO_WEEK_HOLIDAYS.get(iso_week)
    if entry:
        key, name = entry
        if key in holidays:
            return holidays[key], name

    return 1.0, None


# ---------------------------------------------------------------------------
# YoY growth rate
# ---------------------------------------------------------------------------

def get_yoy_growth(data_before, target_month, target_year, n_months=6):
    """Compute YoY growth rate over the last n_months months.

    Args:
        data_before: List of (week_date, revenue) tuples for one entity.
        target_month: Target calendar month (1-12).
        target_year: Target calendar year.
        n_months: Number of months back to average the growth calculation over.

    Returns:
        Average YoY growth rate as a float (e.g., 0.05 for 5%).
        Returns 0.0 if no valid prior-year comparison exists.
    """
    growth_rates = []
    for offset in range(n_months):
        m = target_month - 1 - offset
        y = target_year
        while m < 1:
            m += 12
            y -= 1
        prior_year = y - 1

        current = [d for w, d in data_before if w.month == m and w.year == y]
        prior = [d for w, d in data_before if w.month == m and w.year == prior_year]

        if current and prior:
            c_sum = sum(current)
            p_sum = sum(prior)
            if p_sum > 0:
                growth_rates.append((c_sum - p_sum) / p_sum)
    return statistics.mean(growth_rates) if growth_rates else 0.0


# ---------------------------------------------------------------------------
# Main forecast function
# ---------------------------------------------------------------------------

def forecast_week(data_before, target_week, params, entity_name):
    """Produce a single-week forecast for one entity.

    Args:
        data_before: List of (week_date, revenue) tuples, all weeks strictly
            before target_week for this entity.
        target_week: date object for the Monday of the week to forecast.
        params: Full parameters dict (not entity-merged).
        entity_name: Entity identifier.

    Returns:
        Dict with forecast value and component breakdown.
    """
    if not data_before:
        return {
            "point_estimate": 0.0,
            "components": {"error": "no historical data"},
        }

    p = get_entity_params(params, entity_name)
    recent_n = p["lookback"]["recent_weeks"]
    min_seasonal = p["lookback"]["seasonal_min_weeks"]

    # Optional outlier trimming
    working = list(data_before)
    oh = p.get("outlier_handling", {})
    if oh.get("trim_holiday_weeks", False):
        threshold = oh.get("holiday_threshold_pct", 1.30)
        working = trim_outliers(working, threshold)

    # Component 1: recent average (with optional exponential decay)
    recent_vals = [d for _, d in working[-recent_n:]]
    if not recent_vals:
        return {"point_estimate": 0.0, "components": {"error": "no recent data"}}

    decay = p.get("exponential_weighting", {}).get("decay_factor", 1.0)
    if decay < 1.0:
        recent_avg = exponential_weighted_avg(recent_vals, decay)
    else:
        recent_avg = statistics.mean(recent_vals)

    # Component 2: seasonal average (same month historical)
    seasonal_avg, seasonal_n = get_seasonal_avg(
        working, target_week.month, min_seasonal
    )

    # Component 3: YoY growth-adjusted seasonal
    yoy_months = p.get("growth_adjustment", {}).get("n_months_avg", 6)
    growth_rate = get_yoy_growth(
        data_before, target_week.month, target_week.year, n_months=yoy_months
    )

    if growth_rate == 0.0:
        blend = p.get("blending_no_yoy", {"recent_weight": 1.0, "seasonal_weight": 0.0})
        point = (
            recent_avg * blend.get("recent_weight", 1.0)
            + seasonal_avg * blend.get("seasonal_weight", 0.0)
        )
        weight_note = (
            f"{int(blend.get('recent_weight', 1.0) * 100)}% recent "
            f"+ {int(blend.get('seasonal_weight', 0.0) * 100)}% seasonal "
            f"(no YoY data)"
        )
        yoy_adjusted = recent_avg
    else:
        blend = p.get("blending", {"recent_weight": 0.82, "seasonal_weight": 0.16, "yoy_weight": 0.02})
        yoy_adjusted = seasonal_avg * (1 + growth_rate)
        point = (
            recent_avg * blend.get("recent_weight", 0.82)
            + seasonal_avg * blend.get("seasonal_weight", 0.16)
            + yoy_adjusted * blend.get("yoy_weight", 0.02)
        )
        weight_note = (
            f"{int(blend.get('recent_weight', 0.82) * 100)}% recent + "
            f"{int(blend.get('seasonal_weight', 0.16) * 100)}% seasonal + "
            f"{int(blend.get('yoy_weight', 0.02) * 100)}% YoY "
            f"({yoy_months}mo growth: {growth_rate:+.1%})"
        )

    # Week-of-month adjustment
    wom_config = p.get("week_of_month", {})
    wom = get_week_of_month(target_week)
    wom_adj = 0.0
    if wom_config.get("enabled", False):
        wom_adj = wom_config.get(f"week_{wom}_adj", 0.0)
        if wom_adj != 0:
            point *= 1 + wom_adj
            weight_note += f" | week {wom} adj: {wom_adj:+.1%}"

    # Holiday adjustment
    holiday_mult, holiday_name = get_holiday_multiplier(target_week, params, entity_name)
    if holiday_mult != 1.0:
        point *= holiday_mult
        weight_note += f" | {holiday_name} x{holiday_mult:.3f}"

    return {
        "point_estimate": round(point, 2),
        "components": {
            "recent_avg":         round(recent_avg, 2),
            "recent_n":           len(recent_vals),
            "seasonal_avg":       round(seasonal_avg, 2),
            "seasonal_n":         seasonal_n,
            "yoy_growth_rate":    round(growth_rate, 4),
            "yoy_adjusted":       round(yoy_adjusted, 2),
            "week_of_month":      wom,
            "week_of_month_adj":  wom_adj,
            "holiday_multiplier": holiday_mult,
            "holiday_name":       holiday_name,
            "decay_factor":       decay,
        },
        "methodology": {
            "weights":       weight_note,
            "model_version": "1.0.0",
        },
    }
