import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("📈 Trend Analysis")

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql(
    "SELECT DISTINCT company_id FROM financial_ratios ORDER BY company_id",
    conn
)

ticker = st.selectbox(
    "Company",
    companies["company_id"]
)

df = pd.read_sql(
    """
    SELECT year,
           sales,
           net_profit,
           return_on_equity_pct,
           operating_profit_margin_pct
    FROM financial_ratios
    WHERE company_id=?
    """,
    conn,
    params=[ticker]
)

conn.close()

metric = st.multiselect(
    "Select Metrics",
    [
        "sales",
        "net_profit",
        "return_on_equity_pct",
        "operating_profit_margin_pct"
    ],
    default=["sales"]
)

if metric:

    fig = px.line(
        df,
        x="year",
        y=metric,
        markers=True,
        title=ticker
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

st.dataframe(df)