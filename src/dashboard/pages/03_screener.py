import streamlit as st
import sqlite3
import pandas as pd

st.title("🔍 Stock Screener")

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

conn.close()

df = df.merge(
    companies,
    left_on="company_id",
    right_on="id",
    how="left"
)

# -----------------------------
# Convert Numeric Columns
# -----------------------------

numeric = [
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "revenue_cagr_5yr",
    "pat_cagr_5yr",
    "operating_profit_margin_pct",
    "interest_coverage",
    "pe_ratio",
    "pb_ratio",
    "dividend_yield_pct"
]

for col in numeric:

    if col in df.columns:

        df[col] = pd.to_numeric(
            df[col],
            errors="coerce"
        )

# -----------------------------
# Sidebar Filters
# -----------------------------

st.sidebar.header("Filters")

roe = st.sidebar.slider(
    "Minimum ROE",
    -50,
    100,
    15
)

de = st.sidebar.slider(
    "Maximum Debt/Equity",
    0.0,
    5.0,
    1.0
)

fcf = st.sidebar.number_input(
    "Minimum Free Cash Flow",
    value=0.0
)

# -----------------------------
# Apply Filters
# -----------------------------

filtered = df.copy()

filtered = filtered[
    filtered["return_on_equity_pct"] >= roe
]

filtered = filtered[
    filtered["debt_to_equity"] <= de
]

filtered = filtered[
    filtered["free_cash_flow_cr"] >= fcf
]

st.subheader(
    f"{len(filtered)} Companies Matched"
)

show = [
    "company_id",
    "company_name",
    "return_on_equity_pct",
    "debt_to_equity",
    "free_cash_flow_cr",
    "composite_quality_score"
]

show = [c for c in show if c in filtered.columns]

st.dataframe(
    filtered[show],
    use_container_width=True
)

csv = filtered.to_csv(index=False)

st.download_button(
    "⬇ Download CSV",
    csv,
    "screener.csv",
    "text/csv"
)