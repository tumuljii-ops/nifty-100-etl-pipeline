from src.analytics.cashflow_kpis import *


def test_fcf():

    assert free_cash_flow(
        1000,
        -300
    ) == 700


def test_cfo_quality_high():

    assert cfo_quality_score(
        100,
        80
    ) == "High Quality"


def test_cfo_quality_moderate():

    assert cfo_quality_score(
        80,
        100
    ) == "Moderate"


def test_cfo_quality_risk():

    assert cfo_quality_score(
        30,
        100
    ) == "Accrual Risk"


def test_capex():

    value, label = capex_intensity(
        -200,
        5000
    )

    assert label == "Moderate"


def test_fcf_conversion():

    assert fcf_conversion_rate(
        500,
        1000
    ) == 50


def test_pattern():

    assert capital_allocation_pattern(
        100,
        -200,
        -50
    ) == "Reinvestor"


def test_growth_debt():

    assert capital_allocation_pattern(
        -100,
        -50,
        200
    ) == "Growth Funded by Debt"