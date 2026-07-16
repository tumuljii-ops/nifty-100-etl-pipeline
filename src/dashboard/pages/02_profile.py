import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px

st.title("🏢 Company Profile")

conn = sqlite3.connect("db/nifty100.db")

companies = pd.read_sql(
    "SELECT id, company_name FROM companies",
    conn
)

ticker = st.selectbox(
    "Select Company",
    companies["id"]
)

ratios = pd.read_sql(
    """
    SELECT *
    FROM financial_ratios
    WHERE company_id=?
    """,
    conn,
    params=[ticker]
)

pl = pd.read_sql(
    """
    SELECT year,sales,net_profit
    FROM profitandloss
    WHERE company_id=?
    """,
    conn,
    params=[ticker]
)

company = pd.read_sql(
    """
    SELECT *
    FROM companies
    WHERE id=?
    """,
    conn,
    params=[ticker]
)

conn.close()

if company.empty:

    st.error("Ticker not found.")

    st.stop()

company = company.iloc[0]

st.header(company["company_name"])

c1, c2, c3 = st.columns(3)

latest = ratios.iloc[-1]

c1.metric(
    "ROE",
    latest["return_on_equity_pct"]
)

c2.metric(
    "ROCE",
    latest["roce_percentage"]
)

c3.metric(
    "Net Profit Margin",
    latest["net_profit_margin_pct"]
)

c4, c5, c6 = st.columns(3)

c4.metric(
    "Debt/Equity",
    latest["debt_to_equity"]
)

c5.metric(
    "Revenue CAGR",
    latest["revenue_cagr_5yr"]
)

c6.metric(
    "Free Cash Flow",
    latest["free_cash_flow_cr"]
)

st.divider()

fig = px.bar(
    pl,
    x="year",
    y=[
        "sales",
        "net_profit"
    ],
    barmode="group",
    title="Revenue & Net Profit"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

if len(ratios) > 1:

    fig2 = px.line(
        ratios,
        x="year",
        y=[
            "return_on_equity_pct",
            "roce_percentage"
        ],
        markers=True
    )

    st.plotly_chart(
        fig2,
        use_container_width=True
    )

st.success("✔ Strong analytics available")

st.error("✖ Demo placeholder for Cons")