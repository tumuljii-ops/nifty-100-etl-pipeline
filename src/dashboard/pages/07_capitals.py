import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("💰 Capital Allocation")

conn = sqlite3.connect("db/nifty100.db")

df = pd.read_sql(
    """
    SELECT
    company_id,
    free_cash_flow_cr,
    debt_to_equity,
    composite_quality_score
    FROM financial_ratios
    """,
    conn
)

conn.close()

def classify(row):

    if row["free_cash_flow_cr"] > 0 and row["debt_to_equity"] < 1:
        return "Strong"

    if row["free_cash_flow_cr"] > 0:
        return "Cash Generator"

    if row["debt_to_equity"] > 2:
        return "Highly Leveraged"

    return "Average"

df["category"] = df.apply(
    classify,
    axis=1
)

fig = px.treemap(
    df,
    path=["category","company_id"],
    values="composite_quality_score"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

st.dataframe(df)