import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("🏭 Sector Analysis")

conn = sqlite3.connect("db/nifty100.db")

sector = pd.read_sql(
    """
    SELECT *
    FROM sectors
    """,
    conn
)

ratio = pd.read_sql(
    """
    SELECT
    company_id,
    sales,
    return_on_equity_pct,
    market_cap_crore
    FROM financial_ratios
    """,
    conn
)

conn.close()

df = sector.merge(
    ratio,
    on="company_id"
)

selected = st.selectbox(
    "Sector",
    sorted(df["broad_sector"].dropna().unique())
)

plot = df[
    df["broad_sector"] == selected
]

fig = px.scatter(
    plot,
    x="sales",
    y="return_on_equity_pct",
    size="market_cap_crore",
    color="sub_sector",
    hover_name="company_id"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(plot)