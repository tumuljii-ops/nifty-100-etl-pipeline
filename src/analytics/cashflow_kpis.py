"""
cashflow_kpis.py

Cash Flow KPI Engine
"""


def free_cash_flow(operating_activity, investing_activity):
    """
    Free Cash Flow (FCF)

    FCF = Operating Cash Flow + Investing Cash Flow

    Investing activity is usually negative,
    so adding it effectively subtracts CapEx.
    """

    return round(operating_activity + investing_activity, 2)


def cfo_quality_score(cfo, pat):
    """
    CFO / PAT Quality

    >1.0  -> High Quality
    0.5-1 -> Moderate
    <0.5  -> Accrual Risk
    """

    if pat == 0:
        return None

    ratio = cfo / pat

    if ratio > 1:
        return "High Quality"

    elif ratio >= 0.5:
        return "Moderate"

    return "Accrual Risk"


def capex_intensity(investing_activity, sales):
    """
    CapEx Intensity

    abs(CFI)/Sales ×100
    """

    if sales == 0:
        return None, None

    value = abs(investing_activity) / sales * 100

    if value < 3:
        label = "Asset Light"

    elif value <= 8:
        label = "Moderate"

    else:
        label = "Capital Intensive"

    return round(value, 2), label


def fcf_conversion_rate(fcf, operating_profit):
    """
    FCF Conversion

    FCF / Operating Profit ×100
    """

    if operating_profit == 0:
        return None

    return round((fcf / operating_profit) * 100, 2)


def capital_allocation_pattern(cfo, cfi, cff, cfo_pat_ratio=None):
    """
    Capital Allocation Classifier
    """

    sign = (
        "+" if cfo >= 0 else "-",
        "+" if cfi >= 0 else "-",
        "+" if cff >= 0 else "-"
    )

    if sign == ("+", "-", "-"):

        if cfo_pat_ratio is not None and cfo_pat_ratio > 1.2:
            return "Shareholder Returns"

        return "Reinvestor"

    if sign == ("+", "+", "-"):
        return "Liquidating Assets"

    if sign == ("-", "+", "+"):
        return "Distress Signal"

    if sign == ("-", "-", "+"):
        return "Growth Funded by Debt"

    if sign == ("+", "+", "+"):
        return "Cash Accumulator"

    if sign == ("-", "-", "-"):
        return "Pre-Revenue"

    if sign == ("+", "-", "+"):
        return "Mixed"

    return "Unknown"