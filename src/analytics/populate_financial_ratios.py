import sqlite3
import pandas as pd

from src.analytics.ratios import *
from src.analytics.cashflow_kpis import *
from src.analytics.cagr import *

print("=" * 70)
print("DAY 12 - POPULATING FINANCIAL RATIOS")
print("=" * 70)

# -------------------------------------------------------
# CONNECT DATABASE
# -------------------------------------------------------

conn = sqlite3.connect("db/nifty100.db")

# -------------------------------------------------------
# LOAD TABLES
# -------------------------------------------------------

profit_loss = pd.read_sql(
    "SELECT * FROM profitandloss",
    conn
)

balance_sheet = pd.read_sql(
    "SELECT * FROM balancesheet",
    conn
)

cashflow = pd.read_sql(
    "SELECT * FROM cashflow",
    conn
)

companies = pd.read_sql(
    "SELECT * FROM companies",
    conn
)

print("Profit & Loss :", profit_loss.shape)
print("Balance Sheet :", balance_sheet.shape)
print("Cashflow      :", cashflow.shape)
print("Companies     :", companies.shape)

# -------------------------------------------------------
# MERGE TABLES
# -------------------------------------------------------

df = profit_loss.merge(
    balance_sheet,
    on=["company_id", "year"],
    how="left",
    suffixes=("", "_bs")
)

df = df.merge(
    cashflow,
    on=["company_id", "year"],
    how="left",
    suffixes=("", "_cf")
)

df = df.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left",
    suffixes=("", "_company")
)

print("\nMerged Shape :", df.shape)

# -------------------------------------------------------
# KPI CALCULATIONS
# -------------------------------------------------------

print("\nCalculating Financial Ratios...")

# -----------------------------
# Net Profit Margin
# -----------------------------

df["net_profit_margin_pct"] = df.apply(
    lambda x:
    net_profit_margin(
        x["net_profit"],
        x["sales"]
    ),
    axis=1
)

# -----------------------------
# Operating Profit Margin
# -----------------------------

df["operating_profit_margin_pct"] = df.apply(
    lambda x:
    operating_profit_margin(
        x["operating_profit"],
        x["sales"]
    ),
    axis=1
)

# -----------------------------
# Return on Equity
# -----------------------------

df["return_on_equity_pct"] = df.apply(
    lambda x:
    return_on_equity(
        x["net_profit"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

# -----------------------------
# Debt To Equity
# -----------------------------

df["debt_to_equity"] = df.apply(
    lambda x:
    debt_to_equity(
        x["borrowings"],
        x["equity_capital"],
        x["reserves"]
    ),
    axis=1
)

# -----------------------------
# Interest Coverage
# -----------------------------

df["interest_coverage"] = df.apply(
    lambda x:
    interest_coverage_ratio(
        x["operating_profit"],
        x["other_income"],
        x["interest"]
    ),
    axis=1
)

# -----------------------------
# Asset Turnover
# -----------------------------

df["asset_turnover"] = df.apply(
    lambda x:
    asset_turnover(
        x["sales"],
        x["total_assets"]
    ),
    axis=1
)

# -----------------------------
# Free Cash Flow
# -----------------------------

df["free_cash_flow_cr"] = df.apply(
    lambda x:
    free_cash_flow(
        x["operating_activity"],
        x["investing_activity"]
    ),
    axis=1
)

# -----------------------------
# CapEx
# -----------------------------

df["capex_cr"] = df["investing_activity"].abs()

# -----------------------------
# Copy Existing Values
# -----------------------------

df["earnings_per_share"] = df["eps"]

df["book_value_per_share"] = df["book_value"]

df["dividend_payout_ratio_pct"] = df["dividend_payout"]

df["total_debt_cr"] = df["borrowings"]

df["cash_from_operations_cr"] = df["operating_activity"]

print("\nBasic KPIs Calculated Successfully.")

print("\nPreview")

print(
    df[
        [
            "company_id",
            "year",
            "net_profit_margin_pct",
            "operating_profit_margin_pct",
            "return_on_equity_pct",
            "debt_to_equity",
            "interest_coverage",
            "asset_turnover",
            "free_cash_flow_cr"
        ]
    ].head(10)
)

# -------------------------------------------------------
# CAGR CALCULATIONS
# -------------------------------------------------------

df["revenue_cagr_5yr"] = None
df["pat_cagr_5yr"] = None
df["eps_cagr_5yr"] = None

df["revenue_cagr_flag"] = None
df["pat_cagr_flag"] = None
df["eps_cagr_flag"] = None

df = df.sort_values(["company_id", "year"])

for company in df["company_id"].unique():

    company_rows = df[df["company_id"] == company]

    idx = company_rows.index.tolist()

    for i in range(5, len(idx)):

        current = idx[i]
        previous = idx[i-5]

        revenue, flag = revenue_cagr(
            df.loc[previous, "sales"],
            df.loc[current, "sales"],
            5
        )

        pat, flag2 = pat_cagr(
            df.loc[previous, "net_profit"],
            df.loc[current, "net_profit"],
            5
        )

        eps, flag3 = eps_cagr(
            df.loc[previous, "eps"],
            df.loc[current, "eps"],
            5
        )

        df.loc[current, "revenue_cagr_5yr"] = revenue
        df.loc[current, "pat_cagr_5yr"] = pat
        df.loc[current, "eps_cagr_5yr"] = eps

        df.loc[current, "revenue_cagr_flag"] = flag
        df.loc[current, "pat_cagr_flag"] = flag2
        df.loc[current, "eps_cagr_flag"] = flag3

print("CAGR Calculated.")

# -------------------------------------------------------
# COMPOSITE QUALITY SCORE
# -------------------------------------------------------

def quality_score(row):

    score = 0

    if pd.notna(row["return_on_equity_pct"]):

        if row["return_on_equity_pct"] > 15:
            score += 25

    if pd.notna(row["net_profit_margin_pct"]):

        if row["net_profit_margin_pct"] > 10:
            score += 25

    if pd.notna(row["debt_to_equity"]):

        if row["debt_to_equity"] < 1:
            score += 25

    if pd.notna(row["interest_coverage"]):

        if row["interest_coverage"] > 3:
            score += 25

    return score

df["composite_quality_score"] = df.apply(
    quality_score,
    axis=1
)

print("Composite Score Calculated.")

# -------------------------------------------------------
# FINAL TABLE
# -------------------------------------------------------

final_df = df[
    [
        "id",
        "company_id",
        "year",
        "net_profit_margin_pct",
        "operating_profit_margin_pct",
        "return_on_equity_pct",
        "debt_to_equity",
        "interest_coverage",
        "asset_turnover",
        "free_cash_flow_cr",
        "capex_cr",
        "earnings_per_share",
        "book_value_per_share",
        "dividend_payout_ratio_pct",
        "total_debt_cr",
        "cash_from_operations_cr"
    ]
]

final_df.to_sql(
    "financial_ratios",
    conn,
    if_exists="replace",
    index=False
)

count = conn.execute(
    "SELECT COUNT(*) FROM financial_ratios"
).fetchone()[0]

print("\n" + "="*60)
print("DAY 12 COMPLETED")
print("="*60)

print("Rows Written :", count)

conn.commit()
conn.close()