from src.analytics.ratios import *

def test_net_profit_margin():
    assert net_profit_margin(200, 1000) == 20.00

def test_net_profit_margin_zero_sales():
    assert net_profit_margin(200, 0) is None

def test_operating_profit_margin():
    assert operating_profit_margin(300, 1000) == 30.00

def test_opm_difference():
    assert check_opm_difference(25, 23) == True

def test_roe():
    assert return_on_equity(100, 200, 300) == 20.00

def test_negative_equity():
    assert return_on_equity(100, -200, 100) is None

def test_roce():
    assert return_on_capital_employed(150, 200, 300, 500) == 15.00

def test_roa():
    assert return_on_assets(100, 500) == 20.00

def test_debt_to_equity():
    assert debt_to_equity(100, 200, 300) == 0.20

def test_debt_free():
    assert debt_to_equity(0, 200, 300) == 0

def test_high_leverage():
    assert high_leverage_flag(6, "Industrials") == True

def test_interest_coverage():
    assert interest_coverage_ratio(100, 20, 10) == 12.00

def test_interest_zero():
    assert interest_coverage_ratio(100, 20, 0) is None

def test_icr_label():
    assert interest_coverage_label(None) == "Debt Free"

def test_net_debt():
    assert net_debt(1000, 300) == 700

def test_asset_turnover():
    assert asset_turnover(1000, 500) == 2.00