import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("🏠 Dashboard")

conn = sqlite3.connect("db/nifty100.db")

ratios = pd.read_sql(
    "SELECT * FROM financial_ratios",
    conn
)

sectors = pd.read_sql(
    "SELECT * FROM sectors",
    conn
)

conn.close()

# -----------------------------
# Convert numeric columns
# -----------------------------

numeric = [
    "return_on_equity_pct",
    "pe_ratio",
    "debt_to_equity",
    "revenue_cagr_5yr"
]

for col in numeric:
    if col in ratios.columns:
        ratios[col] = pd.to_numeric(
            ratios[col],
            errors="coerce"
        )

# -----------------------------
# KPI Cards
# -----------------------------

c1, c2, c3 = st.columns(3)

with c1:

    st.metric(
        "Average ROE",
        round(
            ratios["return_on_equity_pct"].mean(),
            2
        )
    )

with c2:

    if "pe_ratio" in ratios.columns:

        st.metric(
            "Median PE",
            round(
                ratios["pe_ratio"].median(),
                2
            )
        )

with c3:

    st.metric(
        "Companies",
        sectors["company_id"].nunique()
    )

c4, c5, c6 = st.columns(3)

with c4:

    st.metric(
        "Median Debt/Equity",
        round(
            ratios["debt_to_equity"].median(),
            2
        )
    )

with c5:

    st.metric(
        "Median Revenue CAGR",
        round(
            ratios["revenue_cagr_5yr"].median(),
            2
        )
    )

with c6:

    debt_free = (
        ratios["debt_to_equity"] == 0
    ).sum()

    st.metric(
        "Debt Free Companies",
        debt_free
    )

st.divider()

# -----------------------------
# Donut Chart
# -----------------------------

st.subheader("Sector Distribution")

sector_count = (
    sectors
    .groupby("broad_sector")
    .size()
    .reset_index(name="count")
)

fig = px.pie(
    sector_count,
    names="broad_sector",
    values="count",
    hole=0.45
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -----------------------------
# Top Companies
# -----------------------------

st.subheader("Top Composite Quality Companies")

if "composite_quality_score" in ratios.columns:

    top = (
        ratios[
            [
                "company_id",
                "composite_quality_score"
            ]
        ]
        .sort_values(
            "composite_quality_score",
            ascending=False
        )
        .drop_duplicates("company_id")
        .head(5)
    )

    st.dataframe(
        top,
        use_container_width=True
    )