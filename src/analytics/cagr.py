"""
cagr.py

Generic CAGR Engine
"""

from math import pow


def calculate_cagr(start_value, end_value, years):
    """
    CAGR Formula

    ((End / Start)^(1/Years) - 1) * 100

    Returns:
        (value, flag)
    """

    if years <= 0:
        return None, "INVALID_YEARS"

    if start_value == 0:
        return None, "ZERO_BASE"

    if start_value > 0 and end_value > 0:

        cagr = (
            pow(end_value / start_value, 1 / years) - 1
        ) * 100

        return round(cagr, 2), "NORMAL"

    if start_value > 0 and end_value < 0:
        return None, "DECLINE_TO_LOSS"

    if start_value < 0 and end_value > 0:
        return None, "TURNAROUND"

    if start_value < 0 and end_value < 0:
        return None, "BOTH_NEGATIVE"

    return None, "UNKNOWN"


def revenue_cagr(start_revenue, end_revenue, years):
    return calculate_cagr(
        start_revenue,
        end_revenue,
        years
    )


def pat_cagr(start_pat, end_pat, years):
    return calculate_cagr(
        start_pat,
        end_pat,
        years
    )


def eps_cagr(start_eps, end_eps, years):
    return calculate_cagr(
        start_eps,
        end_eps,
        years
    )


def insufficient_data(years_available, required_years):
    """
    Returns True if there isn't enough history.
    """

    return years_available < required_years