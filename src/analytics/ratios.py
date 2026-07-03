"""
ratios.py

Financial Ratio Engine

Contains profitability, leverage and efficiency ratio functions
used throughout the NIFTY100 ETL pipeline.
"""


def net_profit_margin(net_profit, sales):
    """
    Net Profit Margin (%)

    Formula:
    (Net Profit / Sales) * 100

    Returns:
        float : Percentage
        None  : if sales <= 0
    """

    if sales is None or sales <= 0:
        return None

    return round((net_profit / sales) * 100, 2)


def operating_profit_margin(operating_profit, sales):
    """
    Operating Profit Margin (%)

    Formula:
    (Operating Profit / Sales) * 100

    Returns:
        float
        None if sales <= 0
    """

    if sales is None or sales <= 0:
        return None

    return round((operating_profit / sales) * 100, 2)


def check_opm_difference(computed_opm, source_opm):
    """
    Cross-check computed OPM with source OPM.

    Returns:
        True  -> Difference > 1%
        False -> Difference <= 1%
        None  -> Missing values
    """

    if computed_opm is None or source_opm is None:
        return None

    difference = abs(computed_opm - source_opm)

    return difference > 1


def return_on_equity(net_profit, equity_capital, reserves):
    """
    Return on Equity (ROE)

    Formula:
    Net Profit / (Equity + Reserves)

    Edge Cases:
    denominator <= 0 -> None
    """

    denominator = equity_capital + reserves

    if denominator <= 0:
        return None

    return round((net_profit / denominator) * 100, 2)


def return_on_capital_employed(
    ebit,
    equity_capital,
    reserves,
    borrowings
):
    """
    Return on Capital Employed (ROCE)

    Formula:
    EBIT /
    (Equity + Reserves + Borrowings)

    Edge Case:
    denominator <=0
    """

    denominator = (
        equity_capital +
        reserves +
        borrowings
    )

    if denominator <= 0:
        return None

    return round((ebit / denominator) * 100, 2)


def return_on_assets(net_profit, total_assets):
    """
    Return on Assets (ROA)

    Formula:
    Net Profit / Total Assets

    Edge Case:
    total_assets <=0
    """

    if total_assets <= 0:
        return None

    return round((net_profit / total_assets) * 100, 2)


# ----------------------------------------------------------------------
# Day 09
# ----------------------------------------------------------------------

def debt_to_equity(borrowings, equity_capital, reserves):

    if borrowings == 0:
        return 0

    denominator = equity_capital + reserves

    if denominator <= 0:
        return None

    return round(borrowings / denominator, 2)


def high_leverage_flag(debt_equity, broad_sector):

    if debt_equity is None:
        return False

    if broad_sector == "Financials":
        return False

    return debt_equity > 5


def interest_coverage_ratio(
    operating_profit,
    other_income,
    interest
):

    if interest == 0:
        return None

    return round(
        (operating_profit + other_income) / interest,
        2
    )


def interest_coverage_label(icr):

    if icr is None:
        return "Debt Free"

    return ""


def interest_coverage_warning(icr):

    if icr is None:
        return False

    return icr < 1.5


def net_debt(
    borrowings,
    investments
):

    return round(
        borrowings - investments,
        2
    )


def asset_turnover(
    sales,
    total_assets
):

    if total_assets <= 0:
        return None

    return round(
        sales / total_assets,
        2
    )

